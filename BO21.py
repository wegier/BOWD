import sys
from PyQt4 import QtGui, QtCore;
from PyQt4.QtCore import QTimer;
from enum import Enum;
import problemfile;
import genetic;
import findways;
from time import sleep;



class FieldType:
    normal = 0;
    obstacle = -1;
    materialS = 1;
    materialD = 2;
    material = 3;#This is required as we have one bursh for material soruce and dest
    path = 4;
# - Points associated with material are represended in gridArray by two succesive numbers - loading point is odd, unloading is even 
# - ex. (1, 2), (3, 4)....




#=========================================================================================
# MaterialType - associated with every square that is not an obstacle or normal cell     #
#                                                                                        #
#                                                                                        #   
# - numberOfMaterials - static variable incremented every time new instance gets created #
# - loadingPoint - X, Y of material source in mainWindow.grid.gridArray[][]              #
# - unloadingPoint - as above                                                            #
#=========================================================================================

class MaterialType:
    #static variable
    numberOfMaterials = 0;

    def __init__(self, source = 0, dest = 0):
        self.number = MaterialType.numberOfMaterials;
        MaterialType.numberOfMaterials += 1;

        self.loadingPoint = source;
        self.unloadingPoint = dest;
         


#=========================================================================================
# ClickableSquare - basic element of CheckerBoard                                        #
#                                                                                        #
#                                                                                        #   
# - x,y  - cordinates on ChecherBoard relative to top lef corner                         # 
# - size - length of square border
# - textbox - displays number of current material (if cell is loading/unloading point)
# - attr - used for storing data about cell type
#=========================================================================================
class ClickableSquare(QtGui.QLabel):
    
    clicked = QtCore.pyqtSignal(int,int)
    
    def __init__(self, _x, _y, _size, _colour = 'white', _number ="", _attr = FieldType.normal):
         
        super(ClickableSquare, self).__init__()
        self.x = _x
        self.y = _y
        self.size = _size
        self.colour = _colour
        self.number = _number
        self.attr = _attr;
        #texbox properites - layout is useld for centering
        self.resize(_size, _size);
        self.setMinimumHeight(_size);
        self.setMinimumWidth(_size);
        self.pixmap = QtGui.QPixmap(_size, _size)
        
        self.textbox = QtGui.QLabel(self);
        self.textbox.setFont(QtGui.QFont("Arial", int(_size/2)-1) );
        self.textbox.resize(_size, _size);
        self.textbox.setMinimumHeight(_size);
        self.textbox.setMinimumWidth(_size);
        self.textbox.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtGui.QHBoxLayout();
        layout.setMargin(0);
        layout.addWidget(self.textbox);

        self.setLayout(layout);
        self.update();
        
#==================================================    

        
    def mousePressEvent(self, event):
        self.clicked.emit(self.x,self.y)
                
#==================================================

    def getXY(self):
        return [self.x, self.y];
#==================================================    


    def setAsNormal(self):
        self.colour = 'white'
        self.number = "";
        self.attr = FieldType.normal;
        self.update();
                
#==================================================    

    def setAsObstacle(self):
        self.colour = 'black'
        self.number = "";
        self.attr = FieldType.obstacle;
        self.update();
                
#==================================================    

    def setAsMaterialSource(self,number):
        self.colour = 'yellow'
        self.number = number;
        self.attr = FieldType.materialS;
        self.update();
                
#==================================================    

    def setAsMaterialDest(self,number):
        self.colour = 'orange'
        self.number = number;
        self.attr = FieldType.materialD;
        self.update();
                
#==================================================    
        
    def isNormal(self):
        if self.attr == FieldType.normal:
            return True;
        else:
            return False;
                
#==================================================    
        
    def isObstacle(self):
        if self.attr == FieldType.obstacle:
            return True;
        else:
            return False;
                
#==================================================    

    def isMaterialSource(self):
        if self.attr == FieldType.materialS:
            return True;
        else:
            return False;
                
#==================================================    

    def isMaterialDest(self):
        if self.attr == FieldType.materialD:
            return True;
        else:
            return False;
                
#==================================================    

    def isMaterial(self):
        return (self.isMaterialSource() or self.isMaterialDest());

          
#==================================================          
    def update(self):
        self.textbox.setText(self.number)
        self.pixmap.fill(QtGui.QColor(self.colour))
        self.setPixmap(self.pixmap)
        self.repaint();
#==================================================
#==================================================       

class Circle(QtGui.QLabel):
        
    def __init__(self, _x, _y, _radius, _text, _parent):
         
        super(Circle, self).__init__(_parent)
        self.x = _x
        self.y = _y
        self.radius = _radius
        self.size = 2*_radius
        self.text = _text
              
        self.resize(self.size, self.size);
        self.setMinimumHeight(self.size);
        self.setMinimumWidth(self.size);
    
        
        self.textbox = QtGui.QLabel(_text,self);
        self.textbox.setFont(QtGui.QFont("Arial", int(self.radius/1.5)));
        self.textbox.resize(self.size, self.size);
        self.textbox.setMinimumHeight(self.size);
        self.textbox.setMinimumWidth(self.size);
        self.textbox.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtGui.QHBoxLayout();
        self.layout.setMargin(0);
        self.layout.addWidget(self.textbox);

        self.setLayout(self.layout);
        self.update();
 
    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self);
        qp.setBrush(QtCore.Qt.green)
        pen = QtGui.QPen(QtCore.Qt.green,0, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawEllipse(0,0,self.size, self.size)
        qp.end()

        
        
        

#=========================================================================================
# CheckerBoard - contains CilckableSquares and lines, stores data about cells            #
#                                                                                        #
#                                                                                        #   
# -gridX, gridY - relative positon of top letf corner to Window top lef corner
# -thickness - thickness of a border line in px
# -squares - stores every clickablle square, enables access to square by coordinates    
# -gridArray - holds number representing cell type !!!!!                                 #
#=========================================================================================
        
class CheckerBoard(QtGui.QWidget):

        
    def __init__(self,n,m, sq, th, initSourceCells, initDestCells , initObstacleCells , initBoard ):
        super(CheckerBoard, self).__init__()

        #Bursh - connected with checkboxes, determines what should be done when cell is clicked
        self.brush = FieldType.normal;
        self.width = m;
        self.height = n;
        #Relative positon of grid top left corner
        self.gridX = 50;
        self.gridY = 50;
        #Dimension of single square
        self.sqSize = sq;
        #Grid thickness
        self.thickness = th;
        #Setting dimensions
        self.resize(self.height*(self.thickness+self.sqSize), self.width*(self.thickness+self.sqSize));
        #Minimum dimensions as above, prevents squeezing by layout in main window
        self.setMinimumHeight(self.height*(self.thickness+self.sqSize)+self.gridX);
        self.setMinimumWidth(self.width*(self.thickness+self.sqSize)+self.gridY);
        #List of drawed paths
        self.paths = [];
        #List of drawed circles - for animation
        self.circles = [];
        #Data array
        if initBoard == []:
            self.gridVal = [[0 for(x) in range(m)] for y in range(n)];
        else:
            self.gridVal = initBoard
        #Data array
        self.squares = [[0 for(x) in range(m)] for y in range(n)];
        #
        self.sourceCells = [];
        self.destCells = [];
        self.obstacleCells = [];
        #Creating clickable rectangles
        self.createRect(initSourceCells,initDestCells,initObstacleCells);
               
#==================================================    
    def setBrush(self, _checkedBox):
        if _checkedBox.text() == "Normalny":
            self.brush = FieldType.normal;
        elif _checkedBox.text() == "Przeszkoda":
            self.brush = FieldType.obstacle;
        elif _checkedBox.text() == "Surowiec":
            self.brush = FieldType.material;
  
#==================================================    
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        
#==================================================    
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, self.thickness, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        #Lines
        for i in range(self.height + 1):
            qp.drawLine(self.gridX, self.gridY+i*self.sqSize,    self.gridX+self.sqSize*self.width,   self.gridY+i*self.sqSize)
        for i in range(self.width + 1) :
            qp.drawLine(self.gridX+i*self.sqSize, self.gridY,   self.gridX+i*self.sqSize,   self.gridX+self.sqSize*self.height)
        
#==================================================    
    def createRect(self, initSourceCells, initDestCells, initObstacleCells):
        originX = self.gridX + self.thickness/2;
        originY = self.gridY + self.thickness/2;
        border = self.sqSize - self.thickness;
        for i in range(self.height):
            for j in range(self.width) :
                square = ClickableSquare(i,j,border, 'white')
                square.clicked.connect(self.handleSquareClicked)
                square.setParent(self)
                square.move(originX + border*j +self.thickness*j,  originY + border*i +self.thickness*i)
                self.squares[i][j] = square;

        #Applying initial conditions - this block is ommited when plain grid is created
        for i in range(len(initSourceCells)):
            x = initSourceCells[i][0];
            y = initSourceCells[i][1];
            self.squares[x][y].setAsMaterialSource(str(i+1));
            self.sourceCells.append(self.squares[x][y]);
        for i in range(len(initDestCells)):
            x = initDestCells[i][0];
            y = initDestCells[i][1];
            self.squares[x][y].setAsMaterialDest(str(i+1));
            self.destCells.append(self.squares[x][y]);
        for i in range(len(initObstacleCells)):
            x = initObstacleCells[i][0];
            y = initObstacleCells[i][1];
            self.squares[x][y].setAsObstacle();
            self.obstacleCells.append(self.squares[x][y]);
        
#==================================================
            
    def addCircle(self, i, j,_text, i_offset = 0, j_offset = 0):
        originX = self.gridX + self.thickness/2;
        originY = self.gridY + self.thickness/2;
        border = self.sqSize - self.thickness;
        circle = Circle(i ,j, self.sqSize/2-self.thickness/2, _text, self)
        circle.move(originX + border*j +self.thickness*j + i_offset,  originY + border*i +self.thickness*i + j_offset)
        self.circles.append(circle);
        circle.show();

#==================================================
            
    def delCircles(self):
        while(len(self.circles)):
            toDel = self.circles.pop();
            toDel.hide();
            toDel.textbox.deleteLater();
            toDel.deleteLater();
        self.show();
            
#==================================================    
       
    def createPath(self, pathPoints, colour):
        newPath = [];

        thickness = self.thickness * 4;

        originX = self.gridX + thickness/2;
        originY = self.gridY + thickness/2;
        border = self.sqSize - thickness;
        for i in range(len(pathPoints)-1):
            x = pathPoints[i][0];
            y = pathPoints[i][1]
            square = ClickableSquare(x,y, border, colour, "" ,FieldType.path)
            square.clicked.connect(self.handleSquareClicked)
            square.setParent(self)
            square.move(originX + border*y +thickness*y,  originY + border*x +thickness*x)
            newPath.append(square);
        self.paths.append(newPath);
        self.parentWidget().parentWidget().pathList.addPath(newPath);
        self.show();

        
#==================================================
        
    def showPath(self, path):
         for i in range(len(path)):
            path[i].show();

        
#==================================================    
            
    def hidePath(self, path):
         for i in range(len(path)):
            path[i].hide();

        
#==================================================


    def handleSquareClicked(self, x, y):

        #Global interface

        clicked = self.squares[x][y];
        XY = self.squares[x][y].getXY();
          
        if self.brush == FieldType.normal and  clicked.isObstacle():
                clicked.setAsNormal();
                self.obstacleCells.remove(clicked);
                self.gridVal[x][y] = FieldType.normal;
                problemfile.board = self.gridVal; ### Could be done better...
                problemfile.forbidden.remove(XY);

        elif self.brush == FieldType.obstacle  and  clicked.isNormal():
                clicked.setAsObstacle();
                self.obstacleCells.append(clicked);
                self.gridVal[x][y] = FieldType.obstacle;
                problemfile.board = self.gridVal; 
                problemfile.forbidden.append(XY);

        elif self.brush == FieldType.material and clicked.isNormal():
            if len(self.sourceCells) == len(self.destCells): #This means that last time we added dest (or started from 0), so source must be added
                self.sourceCells.append(clicked);
                problemfile.collectpts.append(XY);
                clicked.setAsMaterialSource(str(len(self.sourceCells)))
            elif len(self.sourceCells) > len(self.destCells):#This means that last time we added source, so dest must be added
                self.destCells.append(clicked);
                problemfile.providepts.append(XY);
                clicked.setAsMaterialDest(str(len(self.destCells)))
           # self.gridVal[x][y] = len(self.sourceCells) + len(self.destCells) #Points associated with material are represended in gridArray by two succesive numbers - loading point is odd, unloading is eve
    
        elif self.brush == FieldType.normal and  clicked.isMaterial(): #Deleting existing materials is allowed only in the same order as elements were added 
            if len(self.sourceCells) == len(self.destCells) and clicked == self.destCells[len(self.destCells)-1]:#if last added was destination point 
                self.destCells.pop();
                problemfile.providepts.pop();
                clicked.setAsNormal();
                self.gridVal[x][y] = FieldType.normal;
            elif len(self.sourceCells) > len(self.destCells) and clicked == self.sourceCells[len(self.sourceCells)-1]:#if last added was source point :
                self.sourceCells.pop();
                problemfile.collectpts.pop();
                clicked.setAsNormal();
                self.gridVal[x][y] = FieldType.normal;
                
        clicked.update();

#==================================================

        
#==================================================
#==================================================    
class PathList(QtGui.QListWidget):
    def __init__(self, parent):
        super(PathList, self).__init__(parent)
    def addPath(self, newPath):
        newItem = QtGui.QListWidgetItem('Scieżka (%d)' % (self.count()+1), self);
        self.addItem(newItem);

        
#==================================================
#==================================================    
        
class ShowPathButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(ShowPathButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        window.grid.showPath(window.grid.paths[window.pathList.currentRow()]);

        
#==================================================
#==================================================
        
class HidePathButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(HidePathButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        window.grid.hidePath(window.grid.paths[window.pathList.currentRow()]);

        
#==================================================            
#==================================================    

class SaveButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(SaveButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget().parentWidget();
        filePath = QtGui.QFileDialog.getSaveFileName(window, 'Zapisz Plik');
        problemfile.write_problem_file(filePath);    

        
#==================================================            
#==================================================    

class LoadButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(LoadButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        
        window = self.parentWidget().parentWidget().parentWidget();
        filePath = QtGui.QFileDialog.getOpenFileName(window, 'Otwórz Plik');
        problemfile.read_problem_file(filePath);
        window.widthEdit.backspace();
        window.widthEdit.backspace();
        window.widthEdit.insert(str(problemfile.m));
        
        window.heightEdit.backspace();
        window.heightEdit.backspace();
        window.heightEdit.insert(str(problemfile.n));
        
        window.makeGrid(problemfile.n, problemfile.m, problemfile.collectpts, problemfile.providepts,problemfile.forbidden, problemfile.board);

        
#==================================================    
#==================================================
        
class MakeGridButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(MakeGridButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        window.makeGrid(int(window.heightEdit.text()),int(window.widthEdit.text()),  [],[],[],[]);

#==================================================    
#==================================================
        
class StartAlgorithmButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(StartAlgorithmButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        print("START");
      
        p = ParamEdit.parameters[0];
        k = len(problemfile.collectpts); 
        board = problemfile.board; 
        collectpts = problemfile.collectpts;
        providepts = problemfile.providepts;
        T = ParamEdit.parameters[1];
        pops = ParamEdit.parameters[2];
        num_it = ParamEdit.parameters[3];
        ##r = ParamEdit.parameters[4];
        r =4;
        sel_size = ParamEdit.parameters[5];
        elit = ParamEdit.parameters[6];
        tourn_size = ParamEdit.parameters[7];
        mut = ParamEdit.parameters[8];
        x = ParamEdit.parameters[9];
        mut_size = ParamEdit.parameters[10];

        genetic.run_gen_algorithm(p, k, board, collectpts, providepts, T, pops, num_it, r, sel_size, elit, x, mut, tourn_size, mut_size, window.nameEdit.text());
        print("KONIEC");
		




#==================================================    
#==================================================
        
class ParamEdit(QtGui.QWidget):
    parameters = [];
    numberOfInstances = 0; 
    def __init__(self, text,parent):
        super(ParamEdit,self).__init__(parent);

        self.id = ParamEdit.numberOfInstances;
        ParamEdit.numberOfInstances = ParamEdit.numberOfInstances+1;
        ParamEdit.parameters.append(0);
        self.label = QtGui.QLabel(text,self);
        self.lineEdit = QtGui.QLineEdit(self);
        self.layout = QtGui.QVBoxLayout(self);
        self.layout.addWidget(self.label);
        self.layout.addWidget(self.lineEdit);
        
        self.lineEdit.textChanged.connect(self.handleChange);
        
    def handleChange(self):
        data = self.lineEdit.text();
        if len(data) > 0 :
            ParamEdit.parameters[self.id] = int(self.lineEdit.text());
        else:
            ParamEdit.parameters[self.id] = 0;

#==================================================    
#==================================================

		
class AnimateButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(AnimateButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        #czas czekania na ruch w milisekundach
        self.sleep_time = 250; 
        
        genetic.get_best_chrom();
        if findways.time < 0:
            return;            	
        self.paths = genetic.best_paths;
        self.j = 0;
		
        QTimer.singleShot(self.sleep_time, self.move);

    def move(self):
        if self.j == findways.time + 1:
            return;
        j = self.j;	
        mainWindow.grid.delCircles();		
        for i in range(genetic.p):
            if(len(self.paths[i]) > 0):		
                mainWindow.grid.addCircle(self.paths[i][j][0], self.paths[i][j][1],str(i + 1),0,0);
        self.j = self.j + 1;
        QTimer.singleShot(self.sleep_time, self.move);
			
    
        
#==================================================
                
#==================================================    
        
        

class Window(QtGui.QMainWindow):


    def __init__(self,n,m, sq = 25, th = 2):

        super(Window, self).__init__()

        
        self.grid = CheckerBoard(10,10,20,2,[],[],[],[]); #tu musi coś być                
        #main layout
        self.layout = QtGui.QGridLayout();
        self.layout.addWidget(self.grid, 0,0);
        self.cw = QtGui.QWidget(self);
        self.cw.setLayout(self.layout);
        self.setCentralWidget(self.cw);

        #window central colum 
        self.cLayout = QtGui.QBoxLayout(2,self.cw); # 2 - top to bottom
        #creating board
        self.makeButton = MakeGridButton("Utwórz Planszę", self.cw);
        self.cLayout.addWidget(self.makeButton);
        self.heightEdit = QtGui.QLineEdit(self.cw);
        self.heightEdit.setInputMask("D9");
        self.heightEdit.insert("10");
        self.widthEdit = QtGui.QLineEdit(self.cw);
        self.widthEdit.setInputMask("D9");
        self.widthEdit.insert("10");
        self.sizeLayout = QtGui.QHBoxLayout(self.cw);
        self.sizeLayout.addWidget(self.heightEdit);
        self.sizeLayout.addWidget(self.widthEdit);
        self.cLayout.addLayout(self.sizeLayout);

        

        #Brushes
        self.brushesLayout = QtGui.QBoxLayout(2,self.cw);
        self.checkBoxGroup = QtGui.QButtonGroup(self.cw);
        self.brushesFrame = QtGui.QGroupBox(self.cw)    
        self.normalCell = QtGui.QCheckBox("Normalny", self.cw);
        self.normalCell.setChecked(1); #default brush
        self.obstacleCell = QtGui.QCheckBox("Przeszkoda",self.cw);
        self.materialCell = QtGui.QCheckBox("Surowiec",self.cw);

        self.checkBoxGroup.addButton(self.normalCell);
        self.checkBoxGroup.addButton(self.obstacleCell);
        self.checkBoxGroup.addButton(self.materialCell);
        self.checkBoxGroup.buttonClicked.connect(self.grid.setBrush); #to i tak jest robione przez przycisk, ale jest tam wywoływana też funkcja disconnect, więc jest potrzebne (pewnie się da bardziej elegancko)

        
        self.brushesLayout.addWidget(self.normalCell);
        self.brushesLayout.addWidget(self.obstacleCell);
        self.brushesLayout.addWidget(self.materialCell);
        self.brushesFrame.setLayout(self.brushesLayout);
        self.brushesFrame.setTitle("Pędzel");
        self.cLayout.addWidget(self.brushesFrame);

        #Path list
        self.pathList = PathList(self.cw);
        self.cLayout.addWidget(self.pathList);
        #path List controll buttons
        self.showButton = ShowPathButton("Pokaz", self.cw);
        self.hideButton = HidePathButton("Ukryj", self.cw);

        self.cLayout.addWidget(self.showButton);
        self.cLayout.addWidget(self.hideButton);

        #Stretch
        self.cLayout.addStretch();

        #control buttons
        #control buttons frame
        self.controlButLayout = QtGui.QBoxLayout(2, self.cw);
        self.controlButFrame = QtGui.QGroupBox(self.cw);
        self.controlButFrame.setTitle("Obsługa Plików");
        #loadButton
        self.loadButton = LoadButton("Wczytaj", self.cw);
        self.controlButLayout.addWidget(self.loadButton);
        #Save button
        self.saveButton = SaveButton("Zapisz", self.cw);
        self.controlButLayout.addWidget(self.saveButton);
        self.controlButFrame.setLayout(self.controlButLayout);
        self.cLayout.addWidget(self.controlButFrame);
        #Result name
        self.nameLabel = QtGui.QLabel("Nazwa Pliku Wynikowego");
        self.nameEdit = QtGui.QLineEdit("wyniki",self.cw);        
        self.cLayout.addWidget(self.nameLabel);
        self.cLayout.addWidget(self.nameEdit);


        #Margins in toolbar
        self.cLayout.setContentsMargins(20,50,50,40);


        #right colum - algorithm parameters
        self.rLayout = QtGui.QVBoxLayout(self.cw);

        self.paramLayout = QtGui.QVBoxLayout(self.cw);
        self.paramFrame = QtGui.QGroupBox(self.cw)    

        self.lPlatfromParam = ParamEdit("Liczba platform",self.cw);
        self.paramLayout.addWidget(self.lPlatfromParam);
        self.czasTrParam = ParamEdit("Czas trwania cyklu",self.cw);
        self.paramLayout.addWidget(self.czasTrParam);
        self.rozPopParam = ParamEdit("Rozmiar populacji",self.cw);
        self.paramLayout.addWidget(self.rozPopParam);
        self.lItParam = ParamEdit("Liczba iteracji",self.cw);
        self.paramLayout.addWidget(self.lItParam);
        self.lRParam = ParamEdit("Liczba r",self.cw);
        self.paramLayout.addWidget(self.lRParam);
        self.lRParam.hide(); ##DISABLED
        self.rozPopPoSelParam = ParamEdit("Rozmiar populacji po selekcji",self.cw);
        self.paramLayout.addWidget(self.rozPopPoSelParam);
        self.lOsElitParam = ParamEdit("Liczba osobników elitarnych",self.cw);
        self.paramLayout.addWidget(self.lOsElitParam);
        self.rTurnParam = ParamEdit("Rozmiar turnieju",self.cw);
        self.paramLayout.addWidget(self.rTurnParam);
        self.lOsZMut = ParamEdit("Liczba osobników z mutacji",self.cw);
        self.paramLayout.addWidget(self.lOsZMut);
        self.lOsZKrzyz = ParamEdit("Liczba osobników z krzyżowania",self.cw);
        self.paramLayout.addWidget(self.lOsZKrzyz);
        self.lGenDoMut = ParamEdit("Liczba genów do mutacji",self.cw);
        self.paramLayout.addWidget(self.lGenDoMut);
        
        self.paramFrame.setLayout(self.paramLayout);
        self.paramFrame.setTitle("Parametry Algorytmu Genetycznego");
        self.rLayout.addWidget(self.paramFrame);

        self.startAlgorithmButton = StartAlgorithmButton("Start", self.cw);
        self.rLayout.addWidget(self.startAlgorithmButton);
        self.animateButton = AnimateButton("Animuj", self.cw);
        self.rLayout.addWidget(self.animateButton);

        self.rLayout.setContentsMargins(20,50,50,40);

        #Sublayouts added to main layout

        self.layout.addLayout(self.cLayout, 0,1);
        self.layout.addLayout(self.rLayout, 0,2);
         
        self.show();

    def makeGrid(self, _m, _n, initSourceCells, initDestCells, initObstacleCells, initBoard):

        window = self;

        window.checkBoxGroup.buttonClicked.disconnect(window.grid.setBrush);
        window.layout.removeWidget(window.grid);

        #Deleting old grid
        
        window.grid.deleteLater();

        #Updating Global interface

        problemfile.m = _m;
        problemfile.n = _n;

        problemfile.forbidden = initObstacleCells;
        problemfile.providepts = initDestCells;
        problemfile.collectpts = initSourceCells;
        problemfile.board = initBoard; 

        #Creating new grid and setting parameters
                
        window.grid = CheckerBoard(problemfile.m,problemfile.n,20,2, problemfile.collectpts, problemfile.providepts, problemfile.forbidden, problemfile.board);
        window.grid.setParent(window.cw)
        window.checkBoxGroup.buttonClicked.connect(window.grid.setBrush);
        window.checkBoxGroup.buttonClicked.emit(window.checkBoxGroup.checkedButton());
        window.layout.addWidget(window.grid, 0,0);
        window.layout.setRowMinimumHeight(0,window.grid.height);
        
        window.grid.show();

        
    
           
##########################################################################################################
app = QtGui.QApplication(sys.argv)
mainWindow = Window(30,20,30,2) #liczba komórek na wysokość, na szerokość, wielkość kwadratu, grubosć linii (musi byc wielkorotnością 2)
#mainWindow.grid.addCircle(5,7,"1",5,5);# - Dwa ostatnie argumenty - offset - opcjonalne
#mainWindow.grid.delCircles();

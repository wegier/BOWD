import sys
from PyQt4 import QtGui, QtCore;
from enum import Enum;

#RYSOWANIE  - 3, listy
#przerobić tak, żeby w siatce były zakodowane tylko przeszkody
#SEELEKCJA W GENETYCZNYM
#liczba populacji, co z nią robimy

#Interface:
# - mainWindow.grid.gridArray[X][Y] - stores data representing cell type 
# - Definition of cell types
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


        
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.x,self.y)

    def setAsNormal(self):
        self.colour = 'white'
        self.number = "";
        self.attr = FieldType.normal;
        self.update();

    def setAsObstacle(self):
        self.colour = 'black'
        self.number = "";
        self.attr = FieldType.obstacle;
        self.update();

    def setAsMaterialSource(self,number):
        self.colour = 'yellow'
        self.number = number;
        self.attr = FieldType.materialS;
        self.update();

    def setAsMaterialDest(self,number):
        self.colour = 'orange'
        self.number = number;
        self.attr = FieldType.materialD;
        self.update();
        
    def isNormal(self):
        if self.attr == FieldType.normal:
            return True;
        else:
            return False;
        
    def isObstacle(self):
        if self.attr == FieldType.obstacle:
            return True;
        else:
            return False;

    def isMaterialSource(self):
        if self.attr == FieldType.materialS:
            return True;
        else:
            return False;

    def isMaterialDest(self):
        if self.attr == FieldType.materialD:
            return True;
        else:
            return False;

    def isMaterial(self):
        return (self.isMaterialSource() or self.isMaterialDest());

        
    def update(self):
        self.textbox.setText(self.number)
        self.pixmap.fill(QtGui.QColor(self.colour))
        self.setPixmap(self.pixmap)
        self.repaint();

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

        
    def __init__(self,n,m, sq, th):
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
        #Data array
        self.gridVal = [[0 for(x) in range(m)] for y in range(n)]
        #Data array
        self.squares = [[0 for(x) in range(m)] for y in range(n)]
        #
        self.sourceCells = [];
        self.destCells = [];
        self.obstacleCells = [];
        #Clickable Rectangles
        self.createRect();

    def setBrush(self, _checkedBox):

        if _checkedBox.text() == "Normalny":
            self.brush = FieldType.normal;
        elif _checkedBox.text() == "Przeszkoda":
            self.brush = FieldType.obstacle;
        elif _checkedBox.text() == "Surowiec":
            self.brush = FieldType.material;
        
        print(self.brush);


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, self.thickness, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        #Lines
        for i in range(self.height + 1):
            qp.drawLine(self.gridX, self.gridY+i*self.sqSize,    self.gridX+self.sqSize*self.width,   self.gridY+i*self.sqSize)
        for i in range(self.width + 1) :
            qp.drawLine(self.gridX+i*self.sqSize, self.gridY,   self.gridX+i*self.sqSize,   self.gridX+self.sqSize*self.height)

    def createRect(self):
        #
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
        
    def showPath(self, path):
         for i in range(len(path)):
            path[i].show();
            
    def hidePath(self, path):
         for i in range(len(path)):
            path[i].hide();

# def applyGrid(self, gridToApply):
 #       
 #       for i in range(self.height):
  #          for j in range(self.width):
                
        
    def handleSquareClicked(self, x, y):
        if self.brush == FieldType.normal and  not self.squares[x][y].isNormal() and  not self.squares[x][y].isMaterial():
                self.squares[x][y].setAsNormal();
                self.gridVal[x][y] = FieldType.normal;
                self.obstacleCells.remove(self.squares[x][y]);
        elif self.brush == FieldType.obstacle  and  not self.squares[x][y].isObstacle() and not self.squares[x][y].isMaterial():
                self.squares[x][y].setAsObstacle();
                self.gridVal[x][y] = FieldType.obstacle;
                self.obstacleCells.append(self.squares[x][y]);
        elif self.brush == FieldType.material and not self.squares[x][y].isMaterial():
            if len(self.sourceCells) == len(self.destCells): #This means that last time we added dest (or started from 0), so source must be added
                self.sourceCells.append(self.squares[x][y]);
                self.squares[x][y].setAsMaterialSource(str(len(self.sourceCells)))
            elif len(self.sourceCells) > len(self.destCells):#This means that last time we added source, so source must be added
                self.destCells.append(self.squares[x][y]);
                self.squares[x][y].setAsMaterialDest(str(len(self.destCells)))
            self.gridVal[x][y] = len(self.sourceCells) + len(self.destCells) #Points associated with material are represended in gridArray by two succesive numbers - loading point is odd, unloading is even 
        elif self.brush == FieldType.normal and  self.squares[x][y].isMaterial(): #Deleting existing materials is allowed only in the same order as elements were added 
            if len(self.sourceCells) == len(self.destCells) and self.squares[x][y] == self.destCells[len(self.destCells)-1]:#if last added was destination point 
                self.destCells.pop();
                self.squares[x][y].setAsNormal();
                self.gridVal[x][y] = FieldType.normal;
            elif len(self.sourceCells) > len(self.destCells) and self.squares[x][y] == self.sourceCells[len(self.sourceCells)-1]:#if last added was source point :
                self.sourceCells.pop();
                self.squares[x][y].setAsNormal();
                self.gridVal[x][y] = FieldType.normal;
        self.squares[x][y].update();
        

class PathList(QtGui.QListWidget):
    def __init__(self, parent):
        super(PathList, self).__init__(parent)
    def addPath(self, newPath):
        newItem = QtGui.QListWidgetItem('Scieżka (%d)' % (self.count()+1), self);
        self.addItem(newItem);
        
class ShowPathButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(ShowPathButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        window.grid.showPath(window.grid.paths[window.pathList.currentRow()]);

class HidePathButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(HidePathButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        window = self.parentWidget().parentWidget();
        window.grid.hidePath(window.grid.paths[window.pathList.currentRow()]);

class SaveButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(SaveButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
        #TU IDZIE DZIAŁANEI PRZYCISKU ZAPISYWANIA
        print("ZAAAAPIS");
	    #na razie test findpaths
        #chrom = chromosome.randChrom(2,2);
        chrom = [[1, 0],[0, 1]];
        srccells = [[c.x, c.y] for c in mainWindow.grid.sourceCells];
        destcells = [[c.x, c.y] for c in mainWindow.grid.destCells];
        print(chrom);
        res = findways.find_paths(2, 2, mainWindow.grid.gridVal, srccells, destcells, chrom, 50);
        paths = findways.paths;
        for pth in paths:
            print(pth);	
            mainWindow.grid.createPath(pth, 'red');
        print("wynik");
        print(res);

class LoadButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(LoadButton, self).__init__(text, parent);
        self.clicked.connect(self.handleClicked);
    def handleClicked(self):
       #TU IDZIE DZIAŁANEI PRZYCISKU WCZYTYWANIA
        print("WCZYYTTAJ");
        

class Window(QtGui.QMainWindow):


    def __init__(self,n,m, sq = 25, th = 2):
        super(Window, self).__init__()
        
        #Checkerboard widget 
        self.grid = CheckerBoard(n,m,sq,th)
        self.grid.setParent(self)
       
        #layout
        self.layout = QtGui.QGridLayout();
        self.layout.addWidget(self.grid, 0,0);
        self.cw = QtGui.QWidget(self);
        self.cw.setLayout(self.layout);
        self.setCentralWidget(self.cw);

        #window rightside
        self.rLayout = QtGui.QBoxLayout(2,self.cw); # 2 - top to bottom
        #Brushes
        self.brushesLayout = QtGui.QBoxLayout(2,self.cw);
        self.checkBoxGroup = QtGui.QButtonGroup(self.cw);
        self.brushesFrame = QtGui.QGroupBox(self.cw)    
        self.normalCell = QtGui.QCheckBox("Normalny", self.cw);
        self.obstacleCell = QtGui.QCheckBox("Przeszkoda",self.cw);
        self.materialCell = QtGui.QCheckBox("Surowiec",self.cw);

        self.checkBoxGroup.addButton(self.normalCell);
        self.checkBoxGroup.addButton(self.obstacleCell);
        self.checkBoxGroup.addButton(self.materialCell);
        
        self.checkBoxGroup.buttonClicked.connect(self.grid.setBrush);
        self.brushesLayout.addWidget(self.normalCell);
        self.brushesLayout.addWidget(self.obstacleCell);
        self.brushesLayout.addWidget(self.materialCell);
        self.brushesFrame.setLayout(self.brushesLayout);
        self.brushesFrame.setTitle("Pędzel");
        self.rLayout.addWidget(self.brushesFrame);

        #Path list
        self.pathList = PathList(self.cw);
        self.rLayout.addWidget(self.pathList);
        #path List controll buttons
        self.showButton = ShowPathButton("Pokaz", self.cw);
        self.hideButton = HidePathButton("Ukryj", self.cw);
        self.rLayout.addWidget(self.showButton);
        self.rLayout.addWidget(self.hideButton);

        #Stretch
        self.rLayout.addStretch();

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
        self.rLayout.addWidget(self.controlButFrame);
        #Margins in toolbar
        self.rLayout.setContentsMargins(20,50,50,40);


        self.layout.addLayout(self.rLayout, 0,1);
        self.layout.setRowMinimumHeight(0,self.grid.height);

    
        #Size of window is determined by number of cells
        #self.setGeometry(50, 50, m*(sq+2*th)+200, n*(sq+2*th));
        self.show()
        
    
           
##########################################################################################################
import chromosome;
import findways;

app = QtGui.QApplication(sys.argv)

mainWindow = Window(5,5,30,2) #liczba komórek na wysokość, na szerokość, wielkość kwadratu, grubosć linii (musi byc wielkorotnością 2)

#mainWindow.grid.createPath([[0,0],[1,1],[2,1], [2,2]], 'red'); # lista punktów (x,y) a potem kolor
#mainWindow.grid.createPath([[5,5],[5,4],[5,3], [5,2]], 'blue');
#mainWindow.grid.createPath([[6,3],[6,4],[6,5], [6,6]], 'pink');
#mainWindow.grid.gridArray[][]; - przechowuje plansze 0 oznaczają puste pola, -1 przeszkody, dwie kolejene liczby dodatnie kolejno punkt odbioru i dostawy (1 2) (3 4) itd 
#sys.exit(app.exec_())
#srccells = [[c.x, c.y] for c in mainWindow.grid.sourceCells];
#destcells = [[c.x, c.y] for c in mainWindow.grid.destCells];

#chrom = chromosome.randChrom(3,3);
#print(chrom);

#paths = findways.find_paths(3, 4, mainWindow.grid.gridArray, srccells, destcells, chrom, 30);
#for pth in paths:
#	mainWindow.grid.createPath(pth, 'red');





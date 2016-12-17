n = 0;
m = 0;
p = 0;
#liczba surowcow
k = 0;
forbidden = [];
collectpts = [];
providepts = [];
need = [];

#plansza z wpisanymi polami zabronionymi
board = [];

#wczytywanie pliku z ustawieniem
def read_problem_file(filename):
        
	global n;
	global m;
	global p;
	global forbidden;
	global collectpts;
	global providepts;
	global need;
	global k;
	global board;
	f = open(filename, 'r');
	s = f.read();
	l = s.split("|");
	#wymiary planszy:
	n = int(l[0]);
	m = int(l[1]);
	#liczba platform
	p = int(l[2]);
	#pola zabronione
	forb = l[3].split(";");
	
	forbidden = [];
	for point in forb:
		h = point.split("-");
		forbidden.append([int(h[0]), int(h[1])]);
	
	del forb;
	
	#punkty poboru surowcow
	coll = l[4].split(";");
	collectpts = [];
	for point in coll:
		h = point.split("-");
		collectpts.append([int(h[0]), int(h[1])]);
	
	del coll;
	k = len(collectpts);
	
	#punkty dostarczania surowcow
	prov = l[5].split(";");
	providepts = [];
	for point in prov:
		h = point.split("-");
		providepts.append([int(h[0]), int(h[1])]);
	
	del prov;
	
	#nd = l[6].split(";");
	#need = [];
	#for mat in nd:
#		need.append(float(mat));
	#del nd;
	
	#utworz tablice, po ktorej poruszac beda sie platformy 
	#i w odpowiednich miejscach wpisz jedynki
	board = [[0 for x in range(m)] for y in range(n)];
	for point in forbidden:
		board[point[0]][point[1]] = 1;
	f.close
		
#zapis ustawienia do pliku
def write_problem_file(filename):
        
	global n;
	global m;
	global p;
	global forbidden;
	global collectpts;
	global providepts;
	global need;
	global k;
	global board;
	
	s = str(m) + "|" + str(n) + "|" + str(p) + "|";
	
	ls = [str(point[0]) + "-" + str(point[1]) for point in forbidden];
	s = s + ";".join(ls) + "|";
	
	ls = [str(point[0]) + "-" + str(point[1]) for point in collectpts];
	s = s + ";".join(ls) + "|";
	
	ls = [str(point[0]) + "-" + str(point[1]) for point in providepts];
	s = s + ";".join(ls) + "|";
	
	#ls = [str(mat) for mat in need];
	#s = s + ";".join(ls);
	
	f = open(filename, 'w');
	f.write(s);
	f.close();
	

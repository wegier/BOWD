import queue;

#wyliczone sciezki dla kazdej z platform
paths = [[]];

#czas wykonywania zadania dla platformy, dla ktorej zajmuje to najdluzej.
time = -1;

#kopia zmiennej board do uzytku lokalnego
board_internal = [];

#liczba platform, dla ktorych zostaly juz policzone sciezki
numpl = 0;

#Znajdz najkrotsze mozliwie sciezki, ktorymi maja przejsc platformy 
#w celu dostarczenia surowcow z ich punktu poboru do punktu docelowego przy
#ustalonym przyporzadkowaniu platform do surowcow i ich kolejnosci rozwozenia

#p -liczba platform

#k - liczba surowcow

#board - plansza zawierajaca 0 w punktach dozwolonych, 1 - w zabronionych

#collectpts - punkty poboru surowcow

#providepts - punkty docelowe dla surowcow


#chrom - "chromosom" - czyli macierz zawierajaca przyporzadkowanie platform do
#surowcow i ich kolejnosc rozwozenia - patrz opis algorytmu genetycznego

#T - maksymalna liczba krokow, jaka wykonac moga platformy


#funkcja wpisuje sciezki do tablicy paths i liczbe ruchow platformy, ktorej
#wykonywanie zadania zajmuje najdluzej (lub -1 jesli zadanie jest niewykonalne
#w czasie mniejszym lub równym T),
# natomiast zwraca czas wykonywania ruchow przez platformy lub p * (T+1), 
# jeżeli nie jest możliwe wykonanie zadania w czasie (liczbie ruchow) mniejszej
#lub równej T

def find_paths(p, k, board, collectpts, providepts, chrom, T):
	global paths;
	global time;
	global board_internal;
	global numpl;
	
	board_internal = board;
	paths = [];
	numpl = 0;
	#wartosc funkcji celu.
	res = 0;
	#Dla kazdej platformy znajdz najkrotsza sciezke prowadzaco przez wszystkie
	#zadane punkty
	for i in range(p):
		print("HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
		#Dlugosc przebytej drogi - 0
		G = 0;
		#pierwszy z kolei surowiec dla danej platformy
		l = 1;
		paths.append([]);
		if(not l in chrom[i]):
			#brak surowcow dla danej platformy - pusta sciezka
			continue;
		#poczatkowe polozenie 
		j = chrom[i].index(l);
		curpos = collectpts[j];
		begpos = curpos;
		#dolacz punkt poczatkowy do trasy.
		paths[i].append(begpos);
		while l in chrom[i]:
			#aktualnie obslugiwany surowiec
			j = chrom[i].index(l);
			#Przejdz do punktu odbioru surowca
			smallpth = find_way(board, curpos, collectpts[j], G);
			#jesli nie znaleziono drogi
			if(smallpth == [[-1, -1]]):
				time = -1;
				return p*(T+1);
			#dolacz te trase do calosci trasy platformy
			paths[i] += smallpth;
			if(len(paths[i]) > 0):
				G = len(paths[i]) -1;
			curpos = collectpts[j];
			
			#jesli dlugosc trasy przekracza maksymalna dopuszczalna dlugosc
			#zakoncz wykonywanie funkcji
			if len(paths[i]) > T:
				time = -1;
				return p*(T+1);
			
			#Przejdz do punktu docelowego dla surowca
			
			smallpth = find_way(board, curpos, providepts[j], G);
			if(smallpth == [[-1, -1]]):
				time = -1;
				return p*(T+1);
			#dolacz te trase do calosci trasy platformy
			paths[i] += smallpth;
			
			if(len(paths[i]) > 0):
				G = len(paths[i]) -1;
			
			curpos = providepts[j];
			
			#jesli dlugosc trasy przekracza maksymalna dopuszczalna dlugosc
			#zakoncz wykonywanie funkcji
			if len(paths[i]) > T:
				time = -1;
				return p*(T+1);			
			
			#kolejny surowiec do obsluzenia
			l += 1;
		#Wroc do pola poczatkowego
		
		smallpth = find_way(board, curpos, begpos, G);
		if(smallpth == [[-1, -1]]):
			time = -1;
			return p*(T+1);
		if len(paths[i]) > T:
				time = -1;
				return p*(T+1);
		#dolacz te trase do calosci trasy platformy
		paths[i] += smallpth;
		
		if(len(paths[i]) > 0):
			G = len(paths[i]) -1;	
			
		if(len(paths[i]) - 1 > time):
			time = len(paths[i]) - 1;
		numpl = numpl + 1;
		#korzystajac z faktu, ze platformy przed dotarciem do punktu koncowego
		#nie moga sie zatrzymywac, wartosc funkcji celu: 
		res += len(paths[i]);
	#Dlugosc poszczegolnych sciezek
	
	#Do zakonczenia cyklu (czas T) platformy maja czekac w miejscu
	#O ile sciezka dla danej platformy nie jest pusta - wtedy rowniez lista
	#jest pusta
	
	for i in range(p):
		#pusta sciezka dla danej platformy
		if(len(paths[i]) == 0):
			continue;
		lastel = paths[i][len(paths[i]) - 1];
		while(len(paths[i]) < T):
			paths[i].append(lastel);
		
	return res;

		
#Zwraca najkrotsza dozwolona sciezke (kolejne punkty) na planszy board
#prowadzaca z punktu poczatkowego begpt do koncowego endpt - z wylaczeniem
#punktu poczatkowego. Pierwszy element sciezki bedzie [-1, -1], jesli taka
#droga nie bedzie istniec
#Algorytm na podstawie http://iair.mchtr.pw.edu.pl/~bputz/aisd_cpp/lekcja7/segment4/main.htm
#Gg dlugosc juz przebytej drogi na poczatku
def find_way(board, begpt, endpt, Gg):
	#poczatek pokrywa sie z koncem
	if begpt == endpt:
		return [];
	#Zastosowany algorytm A*
	#Lista wezlow zamknietych
	CL = [];
	#lista ojcow wezlow zamknietych
	CL_fath = [];
	#lista wezlow otwartych 
	OL = [];
	#lista ojcow wezlow otwartych
	OL_fath = [];
	#lista wartosci funkcji heurystycznych dla wezlow otwartych
	OL_Fs = [];
	#lista dlugosci sciezek do danych pol w OL
	OL_Gs = [];
	
	#obliczanie funkcji heurystycznej
	G = Gg;
	
	H = abs(endpt[0] - begpt[0]) + abs(endpt[1] - begpt[1]);
	F = G + H;
	OL.append(begpt);
	OL_fath.append([-1,-1]);
	OL_Fs.append(F);
	OL_Gs.append(G);
	
	cur = begpt;
	curf = [-1, -1];
	
	while len(OL) > 0:
		#indeks elementu OL o najmniejszej wartosci F - stare, dla A-star
		#m_index = OL_Fs.index(min(OL_Fs));
		
		#zmiana na bardziej floodfill - jesli A-star by zupelnie
		#nie dzialal:
		m_index = OL_Gs.index(min(OL_Gs));
		
		#element OL o najmniejszej wartosci  G (dawniej F)
		#cur = OL[m_index];
		#ojciec tego elementu
		curf = OL_fath[m_index];
		
		#dlugosc sciezki dojsca do tego wezla
		curG = OL_Gs[m_index];
		
		#usun aktualny element z listy OL
		del OL[m_index];
		del OL_fath[m_index];
		del OL_Fs[m_index];
		del OL_Gs[m_index];
		
		#umiesc pole i jego rodzica na liscie odpowiednio wezlow zamknietych
		#i ich ojcow 
		
		CL.append(cur);
		CL_fath.append(curf);
		#sprawdz czy to wezel docelowy
		if(cur == endpt):
			return go_back(begpt, endpt, curf, CL, CL_fath);
		#znajdz sasiadow
		neighs = getNeighbours(cur, curG + 1);
		#Dla kazdego dostepnego sasiada:
		for nei in neighs:
			#jesli sasiad jest wierzcholkiem zamknietym - nic nie rob
			if nei in CL:
				continue;
			
			#szacowana odleglosc do wezla koncowego
			H = abs(endpt[0] - nei[0]) + abs(endpt[1] - nei[1]);
			#sasiad nie znajduje sie na OL
			if not (nei in OL):
				#Oblicz funckje heurystyczna dla sasiada oraz dlugosc
				#sciezki od poczatku do niego.
				G = curG + 1;
				F = G + H;
				#Wstaw nowy punkt do tablicy OL
				OL.append(nei);
				OL_fath.append(cur);
				OL_Fs.append(F);
				OL_Gs.append(G);
				continue;
			#sasiad znajduje sie w OL
			ind = OL.index(nei);
			G = curG + 1;
			#zmien rodzica sasiada, jesli nowa droga do wierzcholka krotsza
			if G < OL_Gs[ind]:
				OL_fath[ind] = cur;
				OL_Gs[ind] = G;
				OL_Fs = G + H;
			
	#nie znaleziono drogi
	return [[-1, -1]];
	

#Tylko do uzytku wewnterznego funkcji find_way - zwraca liste krokow od poczatku
#do konca na podstawie wierzcholka koncowego i listy wierzcholkow i ich rodzicow
#Zwracana jest lista bez wierzcholka poczatkowego

def go_back(begpt, endpt, endfath, pts, fathers):
	#print("pola");
	#print(pts);
	#print("ojcowie");
	#print(fathers);
	#print("koncowe");
	#print(endpt);
	#print("poczatkowea");
	#print(begpt);
	lifo = queue.LifoQueue();
	curpt = endpt;
	curf = endfath;
	#utworz stos na podstawie rodzicow
	while(curpt != begpt):
		lifo.put(curpt);
		i = pts.index(curf);
		curpt = curf;
		curf = fathers[i];
	
	#odtworz droge
	path = [];
	while not lifo.empty():
		el = lifo.get();
		path.append(el);
	return path;

#otrzymuje sasiadow danego pola (z uwzglednieniem pol zabronionych)
#point - aktualne pole
#G - odleglosc od poczatku do aktualnego pola 
def getNeighbours(point, G):
	n = len(board_internal);
	m = len(board_internal[1]);
	
	neighs = [];
	
	#Pola zabronione przy tym G 
	#przez to, ze znajduja sie tu wczesniejsze platformy	
	#lub przez to, ze przechodzac w ten sposob nastapilo by zdezenie
	#(gdy platformy sie zamieniaja miejscami)
	occupied = [];
	for i in range(numpl):
		if(G < len(paths[i])):
			occupied.append(paths[i][G]);
			# zamiana miejscami niedopuszczalna.
			#if(point == paths[i][G]):
				#occupied.append(paths[i][G-1]);
		else:
			occupied.append(paths[i][len(paths[i]) - 1])
		
	#Sprawdz, czy sasiednie pole nie wychodzi poza granice planszy
	#jak rowniez czy nie jest zabronione przez to jak wyglada plansza lub
	#przez obecnosc w nastepnym ruchu na tym polu innej platformy
	if point[0] > 0:
		if(not (board_internal[point[0] - 1][point[1]] == -1)):
			if not ([point[0] - 1, point[1]] in occupied):
				neighs.append([point[0] - 1, point[1]]);
	if point[0] < n - 1:
		if(not (board_internal[point[0] + 1][point[1]] == -1)):
			if not ([point[0] + 1, point[1]] in occupied):
				neighs.append([point[0] + 1, point[1]]);	
	
	if point[1] > 0:
		if(not (board_internal[point[0]][point[1] - 1] == -1)):
			if not ([point[0], point[1] - 1] in occupied):
				neighs.append([point[0], point[1] - 1]);
	if point[1] < n - 1:
		if(not (board_internal[point[0]][point[1] + 1] == -1)):
			if not ([point[0],point[1] + 1] in occupied):
				neighs.append([point[0], point[1] + 1]);
	print("G");
	print(G);
	print(point);
	print("Sasiedzi:");
	print(neighs);
	print("Juz zajete");
	print(occupied);
	return neighs;
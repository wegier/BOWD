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
			smallpth = find_way(board, curpos, collectpts[j], G, T);
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
			
			smallpth = find_way(board, curpos, providepts[j], G, T);
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
		
		smallpth = find_way(board, curpos, begpos, G, T);
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
def find_way(board, begpt, endpt, Gg, T):
	#poczatek pokrywa sie z koncem
	if begpt == endpt:
		return [];
	#Zastosowany algorytm FloodFill
	#Lista wezlow zamknietych
	CL = [];
	#lista indeksow ojcow wezlow zamknietych
	CL_fath = [];
	#lista wezlow otwartych 
	OL = [];
	#lista ojcow wezlow otwartych
	OL_fath = [];
	#lista dlugosci sciezek do danych pol w OL
	OL_Gs = [];
	
	#Odleglosc od poczatku
	G = Gg;
	
	OL.append(begpt);
	OL_fath.append(-1);
	OL_Gs.append(G);
	
	cur = begpt;
	curf = -1;
	
	while len(OL) > 0 and G < T:
		#indeks elementu OL o najmniejszej wartosci G
		m_index = OL_Gs.index(min(OL_Gs));
		
		#element OL o najmniejszej wartosci  G 
		cur = OL[m_index];
		#ojciec tego elementu
		curf = OL_fath[m_index];
		
		#dlugosc sciezki dojsca do tego wezla
		curG = OL_Gs[m_index];
		
		#usun aktualny element z listy OL
		del OL[m_index];
		del OL_fath[m_index];
		del OL_Gs[m_index];
		
		#umiesc pole i jego rodzica na liscie odpowiednio wezlow zamknietych
		#i ich ojcow 
		curind = len(CL);
		CL.append(cur);
		CL_fath.append(curf);
		#sprawdz czy to wezel docelowy
		if(cur == endpt):
			return go_back(begpt, endpt, curf, CL, CL_fath);
		#znajdz sasiadow
		neighs = getNeighbours(cur, curG + 1);
		G = curG + 1;
		#Dla kazdego dostepnego sasiada:
		for nei in neighs:
			#jesli dany sasiad znajduje sie na OL i do tego jego 
			#odleglosc od poczatku zapisana jest na liscie OL - nie
			#dodawaj go jeszcze raz do listy
			if(nei in OL):
				indices = [i for i, p in enumerate(OL) if p == nei];
				no_add = 0;
				for i in indices:
					if(OL_Gs[i] == G):
						no_add == 1;
						break;
				if(no_add == 1):
					continue;
				#W przeciwnym wypadku dodaj ten punkt z nowa wartoscia
				#G do tablicy OL
			OL.append(nei);
			OL_fath.append(curind);
			OL_Gs.append(G);
			
			
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
	while(curf != -1):
		lifo.put(curpt);
		curpt = pts[curf];
		curf = fathers[curf];
	
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
			if(point == paths[i][G]):
				occupied.append(paths[i][G-1]);
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
	#print("G");
	#print(G);
	#print(point);
	#print("Sasiedzi:");
	#print(neighs);
	#print("Juz zajete");
	#print(occupied);
	return neighs;
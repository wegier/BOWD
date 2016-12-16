import findways;
import chromosome;

#plik do algorytmu genetycznego

#Populacja zapisana za pomoca chromosomow
chroms = [];
addaptation = [];
pop_size = 0;
p = 0;
k = 0;
board = [];
collectpts = [];
providepts = [];
T = 0;


#pops - rozmiar populacji
#num_it - liczba iteracji
#r - patrz funkcja addapt_scaling()
#sel_size, elit - patrz funkcja selection()
#x, mut - patrz funkcja new_population()
#pozostale zmienne - oznaczenia takie same jak stosowane w innych miejscach
#z dodana litera l
def run_gen_algorithm(pl, kl, boardl, collectptsl, provideptsl, Tl, pops,
	num_it, r, sel_size, elit, x, mut, tourn_size):
	global p;
	global k;
	global pop_size;
	global board;
	global collectpts;
	global providepts;
	global T;
	
	p = pl;
	k = kl;
	board = [];
	collectpts = [];
	providepts = [];
	T = 0;
	board = [];

	pop_size = pops;
	rand_population();
	
	for i in range(num_it):
		random.seed(time.time());
		addapt_scaling(r);
		selection(sel_size, elit, tourn_size);
		new_population(x, mut);

#Losuje populacje liczaca 
def rand_population():
	global chroms;
	global addaptation;
	chroms = [];
	addaptation = [];
	
	for i in range(pop_size):
		chroms.append(randChrom(p, k));


#Po wykonaniu ponizszej funkcji w liscie addaptation zapisane jest przystosowanie
#osobnika odpowiadajacych danemu indeksowi w liscie 

#zastosowano skalowanie liniowe 
#parametr r to maksymalna wartosc przeskalowanego przystosowania 
#przy zalozeniu, ze srednie przystosowanie jest rowne 1

def addapt_scaling(r):
	#policz nieprzeskalowane przystosowanie kazdego z osobnikow (najmniejsze
	#bedzie najlepsze)
	addaptation = [];
	for chr in chroms:
		addaptation.append(find_paths(p, k, board, collectpts, providepts, chr, T));
	#Srednia przystosowania
	av = float(sum(addaptation)) / float(len(addaptation));
	#najlepsze przystosowanie
	best = float(min(addaptation));
	a = (r - 1)/(best - av);
	b = (best - (r*av))/(best - av);
	#dokonaj przeskalowania dla kazdego elementu addaptation
	addaptation[:] = [(a*x + b) for x in addaptation]; 
	
#selekcja osobnikow - chroms - populacja zapisana za pomoca chromosomow
#(wybrane osobniki zostana wykorzystane do krzyzowania i mutacji)
#sel_size - liczba osobnikow powstajaca w wyniku selekcji
#elit - liczba osobnikow o najlepszej ocenie przystosowania
#ktora na pewno przezyje podczas selekcji (k<=n, gdy
#nie jest stosowana strategia elitarna k = 0)
#Na razie zastosowano selekcje turniejowa, moze to zostac w przyszlosci
#zmienione
# tourn_size - liczba osobnikow uczestniczaca w turnieju.
def selection(sel_size, elit, tourn_size):
	global chroms;
	#Tymczasowa zmienna do zapisywania populacji po selekcji
	selected = [];
	#Wyszukaj elit najlepszych osobnikow
	for i in range(elit):
		ind = addaptation.index(max(addaptation));
		selected.append(chroms[ind]);
		del chroms[ind];
		del addaptation[ind];
		#addaptation[ind] = -addaptation[ind]; - przy zastosowaniu ruletki mogloby 
		#tak byc
	#osobniki pozostajace do selekcji
	sel_size = sel_size - elit;
	#zmien wartosci zmienione wczesniej na ujemne znowu na dodatnie
	#for(i in range(len(addaptation))): 
	#	if(addaptation[i] < 0):
	#		addaptation[i] = -addaptation[i];
	
	#wyselekcjonuj osobniki na podstawie turniejow Liczba turniejow
	#dobrana jest w taki sposob, aby po rozgraniu wszystkich zostala
	#wystarczajaco duza liczba osobnikow do wypelnienia listy selected
	num_tourns = int((len(chroms) - sel_size)/(tourn_size - 1));
	for i in range(num_tourns): 
		#wybierz osobnikow do turnieju
		tourn = random.sample(range(len(chroms)), tourn_size);
		#osobniki do turnieju:
		competitors = [chroms[j] for j in tourn];
		#ich ocena przystosowania:
		comp_addapt = [addaptation[j] for j in tourn];
		#wybierz najlepszego z osobnikow z turnieju
		best = comp_addapt.index(max(comp_addapt));
		#dodaj go do wyselkcjonowanych osobnikow
		selected.append(competitors[best]);
		#usun osobniki wystepujace w turnieju z listy
		chroms = [chr for chr, i in enumerate(chroms) if j not in tourn];
		addaptation = [chr for chr, i in enumerate(addaptation) if j not in tourn];
	#z pozostajacych osobnikow wybierz tylu najlepszych, zeby wypelnili
	#pozostajaca czesc listy selected
	sel_size = sel_size - num_tourns;
	for i in range(sel_size):
		ind = addaptation.index(max(addaptation));
		selected.append(chroms[ind]);
		del chroms[ind];
		del addaptation[ind];
	
#po selekcji tworzy nowa populacje z osobnikow pozostalych po selekcji,
#osobnikow powstalych w wyniku krzyzowania i osobnikow powstalych 
#w wyniku mutacji
#x - liczba osobnikow powstalych z krzyzowania
#mut - liczba osobnikow powstalych w wyniku mutacji
def new_population(x, mut):
	pass;

	
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
	num_it, r, sel_size, elit, x, mut):
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
	
	for(i in range(num_it)):
		addapt_scaling(r);
		selection(sel_size, elit);
		new_population(x, mut):

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
	#policz nieprzeskalowane przystosowanie kazdego z osobnikow
	addaptation = [];
	for(chr in chroms):
		addaptation.append(find_paths(p, k, board, collectpts, providepts, chr, T));
	#Srednia przystosowania
	av = float(sum(addaptation)) / float(len(addaptation));
	#najlepsze przystosowanie
	best = float(max(addaptation));
	a = (r - 1)/(best - av);
	b = (best - (r*av))/(best - av);
	#dokonaj przeskalowania dla kazdego elementu adaptation
	addaptation[:] = [(a*x + b) for x in addaptation]; 
	
#selekcja osobnikow - chroms - populacja zapisana za pomoca chromosomow
#(wybrane osobniki zostana wykorzystane do krzyzowania i mutacji)
#sel_size - liczba osobnikow powstajaca w wyniku selekcji
#elit - liczba osobnikow o najlepszej ocenie przystosowania
#ktora na pewno przezyje podczas selekcji (k<=n, gdy
#nie jest stosowana strategia elitarna k = 0)
#w tym projekcie zastosowano selekcje turniejowa.
def selection(sel_size, elit):
	global chroms;
	pass;

#po selekcji tworzy nowa populacje z osobnikow pozostalych po selekcji,
#osobnikow powstalych w wyniku krzyzowania i osobnikow powstalych 
#w wyniku mutacji
#x - liczba osobnikow powstalych z krzyzowania
#mut - liczba osobnikow powstalych w wyniku mutacji
def new_population(x, mut):
	pass;

	
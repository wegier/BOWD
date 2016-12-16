import findways;
import chromosome;

#plik do algorytmu genetycznego

#Populacja zapisana za pomoca chromosomow
chroms = [];
addaptation = [];
pop_size = 0;
p = 0;
k = 0;


#Losuje populacje liczaca pops osobnikow
#pl- liczba platform, kl - liczba surowcow
def rand_population(pops, pl, kl):
	global p;
	global k;
	global pop_size;
	global chroms;
	global addaptation;
	chroms = [];
	addaptation = [];
	pop_size = pops;
	p = pl;
	k = kl;
	for i in range(pop_size):
		chroms.append(randChrom(p, k));
	pass;


#Po wykonaniu ponizszej funkcji w liscie addaptation zapisane jest przystosowanie
#osobnika odpowiadajacych danemu indeksowi w liscie 

#zastosowano skalowanie liniowe
#parametr k to maksymalna wartosc przeskalowanego przystosowania 
#przy zalozeniu, ze srednie przystosowanie jest rowne 1

def addapt_scaling(k):
	#policz nieprzeskalowane przystosowanie kazdego z osobnikow
	pass;

#selekcja osobnikow - chroms - populacja zapisana za pomoca chromosomow
#(wybrane osobniki zostana wykorzystane do krzyzowania i mutacji)
# n - liczba osobnikow powstajaca w wyniku
#k - liczba osobnikow o najlepszej ocenie przystosowania
#ktora na pewno przezyje podczas selekcji (k<=n, gdy
#nie jest stosowana strategia elitarna k = 0)
#w tym projekcie zastosowano selekcje turniejowa.
def selection(n, k):
	global chroms;
	pass;

#po selekcji tworzy nowa populacje z osobnikow pozostalych po selekcji,
#osobnikow powstalych w wyniku krzyzowania i osobnikow powstalych 
#w wyniku mutacji
#x - liczba osobnikow powstalych z krzyzowania
#m - liczba osobnikow powstalych w wyniku mutacji
def new_population():
	pass;

	
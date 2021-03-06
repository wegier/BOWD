import findways;
import chromosome;
import time;
import random;

#plik do algorytmu genetycznego

#Populacja zapisana za pomoca chromosomow
chroms = [];
#zmienna do zapisywania populacji po selekcji
selected = [];
#ocena przystosowania poszczegolnych osobnikow
addaptation = [];
pop_size = 0;
p = 0;
k = 0;
board = [];
collectpts = [];
providepts = [];
T = 0;

#najlepszy chromosom w przedostatniej populacji
best_chrom = [];
#jego wartosc przystosowania
best_chrom_addapt = 0;
#Sciezki platform dla tego (najlepszego) chromosomu
best_paths = [];
#Zapobiega kilkukrotnemu liczeniu drogi dla znanego juz chromosomu
#Lista juz znanych chromosomow
known_chroms = [];
#lista ich przystosowan
known_addapt = [];

#pops - rozmiar populacji
#num_it - liczba iteracji
#r - patrz funkcja addapt_scaling()
#sel_size, elit - patrz funkcja selection()
#x, mut - patrz funkcja new_population()
#pozostale zmienne - oznaczenia takie same jak stosowane w innych miejscach
#z dodana litera l
def run_gen_algorithm(pl, kl, boardl, collectptsl, provideptsl, Tl, pops,
	num_it, r, sel_size, elit, x, mut, tourn_size, mut_size, filename):
	global p;
	global k;
	global pop_size;
	global board;
	global collectpts;
	global providepts;
	global T;
	global known_chroms;
	global known_addapt;
	
	
	p = pl;
	k = kl;
	board = boardl;
	collectpts = collectptsl;
	providepts = provideptsl;
	T = Tl;

	known_chroms = [];
	known_addapt = [];
	
	f = open(filename, 'w');
	pop_size = pops;
	#random.seed(time.time());
	#Na potrzeby testow wartosc stala.
	random.seed(7);
	rand_population();
	for i in range(num_it):
		addapt_scaling(r);
		selection(sel_size, elit, tourn_size);
		new_population(x, mut, mut_size);
		print(best_chrom_addapt);
		f.write(str(i+1) + ";" + str(best_chrom_addapt) + "\n");
	f.close();

#Losuje populacje 
def rand_population():
	global chroms;
	global addaptation;
	chroms = [];
	addaptation = [];
	
	for i in range(pop_size):
		chroms.append(chromosome.randChrom(p, k));


#Po wykonaniu ponizszej funkcji w liscie addaptation zapisane jest przystosowanie
#osobnika odpowiadajacych danemu indeksowi w liscie 

#zastosowano skalowanie liniowe 
#parametr r to maksymalna wartosc przeskalowanego przystosowania 
#przy zalozeniu, ze srednie przystosowanie jest rowne 1

def addapt_scaling(r):
	global addaptation;
	global best_chrom;
	global best_chrom_addapt;
	global known_chroms;
	global known_addapt;
	#policz nieprzeskalowane przystosowanie kazdego z osobnikow (najmniejsze
	#bedzie najlepsze)
	addaptation = [];
	for i in range(len(chroms)):
		if(chroms[i] in known_chroms):
			addaptation.append(known_addapt[known_chroms.index(chroms[i])]);
		else:
			ad = findways.find_paths(p, k, board, collectpts, providepts, chroms[i], T);
			known_chroms.append(chroms[i]);
			known_addapt.append(ad);
			addaptation.append(ad);
	#Srednia przystosowania
	av = float(sum(addaptation)) / float(len(addaptation));
	#najlepsze przystosowanie
	best = min(addaptation);
	
	best_chrom_addapt =  float(best);
	best_chrom = chroms[addaptation.index(best)];
	best = float(best);
	if(best != av):
		a = (r - 1)/(best - av);
		b = (best - (r*av))/(best - av);
	else:
		a = 1/av;
		b = 0;
	#dokonaj przeskalowania dla kazdego elementu addaptation
	addaptation = [(a*x + b) for x in addaptation]; 
	
	
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
	global selected;
	global addaptation;
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
	#		addaptation[i] = -addaptation[i];\
	
	#wyselekcjonuj osobniki na podstawie turniejow Liczba turniejow
	#dobrana jest w taki sposob, aby po rozgraniu wszystkich zostala
	#wystarczajaco duza liczba osobnikow do wypelnienia listy selected
	num_tourns = min(int((len(chroms) - sel_size)/(tourn_size - 1)) , sel_size);
	
	for i in range(num_tourns): 
		#wybierz osobnikow do turnieju
		tourn = random.sample(range(len(chroms)), tourn_size);
		#osobniki do turnieju:
		competitors = [chroms[j] for j in tourn];
		#ich ocena przyst1osowania:
		comp_addapt = [addaptation[j] for j in tourn];
		#wybierz najlepszego z osobnikow z turnieju
		best = comp_addapt.index(max(comp_addapt));
		#dodaj go do wyselkcjonowanych osobnikow
		selected.append(competitors[best]);
		#usun osobniki wystepujace w turnieju z listy
		chroms = [chr for j, chr in enumerate(chroms) if j not in tourn];
		addaptation = [a for j, a in enumerate(addaptation) if j not in tourn];
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
def new_population(x, mut, mut_size):
	global chroms;
	global selected;
	#osobniki z selekcji 
	chroms = selected;	
	mutchr = random.sample(selected, mut);
	#mutuj i dodawaj osobniki do listy chroms
	for chr in mutchr:
		chroms.append(chromosome.mutate(chr, p, k, mut_size));
	
	#dobieramy pary do krzyzowania - zakladamy, ze populacja nie jest
	#monogamiczna - i dodajemy potomka otrzymanego w wyniku krzyzowania
	#do populacji
	for i in range(x):
		parents = random.sample(selected, 2);
		chroms.append(chromosome.crossV2(parents[0], parents[1], p, k));
	

#wylicza jaki chromosom ma najlepsza wartosc funkcji celu w danej populacji
#i ja zwraca
def get_best_chrom():
	global addaptation;
	global best_chrom;
	global best_chrom_addapt;
	global best_paths;
	#policz nieprzeskalowane przystosowanie kazdego z osobnikow (najmniejsze
	#bedzie najlepsze)
	addaptation = [];
	for chr in chroms:
		addaptation.append(findways.find_paths(p, k, board, collectpts, providepts, chr, T));

	#najlepsze przystosowanie
	best = min(addaptation);
	best_chrom_addapt = best;
	best_chrom = chroms[addaptation.index(best)];
	findways.find_paths(p, k, board, collectpts, providepts, best_chrom, T)
	best_paths = findways.paths;

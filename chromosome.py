import random;
import time;

#wazne, aby nieuzywane pola w macierzy byly wypelnione zerami!
#p - liczba platform
#k - liczba surowcow
#Mutuj chromosom
def mutate(chrom, p, k):
	#ponizsze niedopuszczalne
	if(p == 0 or k == 0):
		return;
	#zainicjalizuj generator liczb pseudolosowych
	random.seed(time.time());
	#wybierz liczbe surowcow, dla ktorej zastapi zmiana platform
	#maks. k/2, czyli polowa liczby wszystkich surowcow, chyba ze
	#liczba surowcow to 1
	num_changes = 1;
	if(k > 1):
		num_changes = random.randrange(1, int(k/2)+1);
	
	
	#wybierz losowo surowce do zmiany platform
	to_change = random.sample(range(k), num_changes);

	for mat in to_change:
		#wybierz losowo nowa platforme dla surowca
		new_plat = random.randrange(p);
		#jako ktora byla obslugiwana ta platforma (jedyna niezerowa
		#liczba w kolumnie)
		seq = max([el[mat] for el in chrom]);
		#stara platforma tego surowca
		old_plat = [el[mat] for el in chrom].index(seq);
		#zmiana przyporzadkowania surowca do platformy
		chrom[old_plat][mat] = 0;
		chrom[new_plat][mat] = seq;
	return assureUniqueness(chrom, p, k);
	
#krzyzowanie
def cross(chrom1, chrom2, p, k):
	#ponizsze niedopuszczalne
	if(p == 0 or k == 0):
		return;
	#zainicjalizuj generator liczb pseudolosowych
	random.seed(time.time());
	#wybierz liczbe surowcow, ktorej przyporzadkowanie do platform
	#zostanie wziete z pierwszego chromosomu.
	num_chrom1 = random.randrange(1, k+1);
	#wybierz ktore to surowce
	from_chrom1 = random.sample(range(k), num_chrom1);
	
	chrom = [[] for i in range(p)];
	#dla kazdego surowca przyporzadkuj go do odpowiedniej platformy zgodnie
	#z informacja w chromosomie
	for i in range(k):
		if i in from_chrom1:
			for j in range(p):
				chrom[j].append(chrom1[j][i]);
		else:
			for j in range(p):
				chrom[j].append(chrom2[j][i]);
	return assureUniqueness(chrom, p, k);

#Ta wersja prawdopodobnie lepsza - ustala zachowuje kolejnosc w chromosomach
#i dodatkowo te surowce, ktore byly obok siebie (o ile nadal sa przyporzadkowane)
#do tej samej platformy sa nadal obok siebie
def crossV2(chrom1, chrom2, p, k):
	#ponizsze niedopuszczalne
	if(p == 0 or k == 0):
		return;
	#zainicjalizuj generator liczb pseudolosowych
	random.seed(time.time());
	#wybierz liczbe surowcow, ktorej przyporzadkowanie do platform
	#zostanie wziete z pierwszego chromosomu.
	num_chrom1 = random.randrange(1, k+1);
	#wybierz ktore to surowce
	from_chrom1 = random.sample(range(k), num_chrom1);
	
	chrom = [[] for i in range(p)];
	
	#do kazdej platformy przyporzadkuj, surowce z ktorego chromosomu
	#beda obslugiwane jako pierwsze
	which_first = [random.randrange(1, 2) for i in range(p)];
	
	for i in range(k):
		if i in from_chrom1:
			for j in range(p):
				if(which_first[j] == 1):
					chrom[j].append(chrom1[j][i]);
				else:
					if(chrom1[j][i] != 0):
						chrom[j].append(chrom1[j][i] + k);
					else:
						chrom[j].append(0);
					
		else:
			for j in range(p):
				if(which_first[j] == 2):
					chrom[j].append(chrom2[j][i]);
				else:
					if(chrom2[j][i] != 0):
						chrom[j].append(chrom2[j][i] + k);
					else:
						chrom[j].append(0);
						

	#Wprawdzie na pewno liczby oznaczajace kolejnosc dla kazdej z platform
	#sa rozne, ale funkcja ta zapewnia, ze sa od 1 do liczby surowcow dla danej
	#platformy
	return assureUniqueness(chrom, p, k);

#Losuj chromosom
def randChrom(p, k):
	random.seed(time.time());
	#utworz macierz wypelniona zerami
	chrom = [[0 for j in range(k)] for i in range(p)];
	#Dla kazdego surowca wybierz losowo platforme
	for i in range(k):
		j = random.randrange(0, p);
		chrom[j][i] = 1;
	#losuje kolejnosc surowcow
	chrom = assureUniqueness(chrom, p, k);
	return chrom;
	
	
#Zapewnij, ze w chromosomie dla danej platformy ani jeden surowiec
#nie jest obslugiwany jednoczesnie
def assureUniqueness(chrom, p, k):
	#bedzie to potrzebne pozniej
	#wykonaj ponizsze czynnosci dla kazdej platformy
	for i in range(p):
		#do zerowych elementow dodaj 3*liczbe surowcow + 1
		for j in range(k):
			if(chrom[i][j] == 0):
				chrom[i][j] = (3*k) + 1;
		#Liczba, jaka zostanie przyporzadkowana nastepnej w kolejnosci
		#platformie
		seq = 1;
		#wartosc najmniejszego elementu (pierwszego obslugiwanego surowca):
		first = min(chrom[i]);
		
		#dopoki nie dokonano przeksztalcenia na wszystkich niezerowych elementach

		while first < (3*k) + 1:
			#wybierz wszystkie elementy o najmniejszej wartosci
			
			indices = [ind for ind, x in enumerate(chrom[i]) if x == first];
			
			#poprzestawiaj kolejnosc tych elementow
			random.shuffle(indices);
			#przyporzadkuj kolejne dostepne liczby surowcom reprezentowanym
			#przez indices (na razie + k + 1)
			for ind in indices:
				chrom[i][ind] = (3*k) + 1 + seq;
				seq += 1;
			first = min(chrom[i]);
		
		#Dla danej platformy sa juz rozne liczby od 1 do liczby
		#surowcow przyporzadkowanej tej platformie, jednak z dodana
		#liczba k+1 - odejmij ta liczbe od kazdego elementu
		chrom[i] = [(el- (3*k) - 1) for el in chrom[i]];
	return chrom;
import sys
import os
from copy import deepcopy

#TODO: 
# -How to generate events: Keep a list of Autobuz and iterate over it to find out if there is an event at the next station each of the Autobuz arrives at
# -List should be sorted from low to high by time it takes Autobuz to go between stations
# -Iterate again only over events
# -For each Autobuz that has an event at the next station, generate one Succesor (when Om changes state)
# -Each NEXT event assumes Om did not change state at the previous event (so when I print it out I can print "asteapta...")
# -WHEN checking to see if there is an Event, check if Om has been passed by Autobuz already (and thus cannot board, so no event is triggered)
# -For this ^^^, Autobuz must have field of list of (Om, destination) that is reset every time he returns to that destination and that Om is no longer there

# -NodParcurgere MUST have field of list of Autobuz, so that when I want to genereazaSuccesori for it I can iterate over the RIGHT list
# -Graph should have field of list of Autobuz so that I can iterate over it when generating successors
# -Om must have field of stare (so I know what to print for other Om's when at every event only one changes stare)
# -Autobuz must have field of Om (automatically generates event if there s a person inside and it gets to the next station)
# -Adapt Graph and Node
# -Remember to handle people who have remaining_destinations == []
#Figure out euristica
# -Figure out timeout
# -rewrite comments to be of appropriate format
# -write doc
   
class Autobuz:
    def __init__(self, id, price, break_duration, trip_duration, destinations):
        self.id = id
        self.price = price
        self.break_duration = break_duration
        self.trip_duration = trip_duration
        self.destinations = destinations
        self.current_loc = len(destinations)-1 #index for list destinations
        self.direction_forward = False #initially leaves from end of route
        self.om = None #add Om when one boards
    
    def __str__(self):
        return (f"id={self.id}\n"
                f"price={self.price}\n"
                f"break_duration={self.break_duration}\n"
                f"trip_duration={self.trip_duration}\n"
                f"om={self.om}\n")
    
    def getNextDest(self):
        if self.direction_forward:
            if len(self.destinations)-1 == current_loc: #if Autobuz reaches rightmost destination, it also takes a break and changes directions
                current_loc = current_loc #remove later
                direction_forward = False #Autobuz changes direction
                return destinations[current_loc], (break_time + trip_time) #return destination reached and elapsed time
  
            else:
                self.current_loc += 1
                return destinations[current_loc], trip_duration
        
        else:
            if 0 == current_loc: #if Autobuz reaches leftmost destination, it also takes a break and changes directions
                current_loc = current_loc #remove later
                direction_forward = True
                return destinations[current_loc],  (break_time + trip_duration)
            
            else:
                self.current_loc -= 1
                return destinations[current_loc], trip_duration

class Om:
    def __init__(self, name, money, destinations):
        self.name = name
        self.money = money
        self.destinations = destinations
        self.remaining_dest = destinations[1:]
        self.current_loc = 0
        self.state = "waiting" #can be "waiting" or "in_bus"
        self.autobuz = None #Autobuz id

    def isDone(self):
        if self.remaining_dest == []:
            return True
        return False

    def __str__(self):
        return (f"name={self.name}\n"
                f"money={self.money}\n"
                f"current_loc={self.remaining_dest[0]}\n"
                f"first_dest={self.destinations[0]}\n"
                f"state={self.state}\n"
                f"autobuz={self.autobuz}\n")

class NodInfo:
    def __init__(self, oameni, time):
        self.oameni = oameni
        self.time = time

    def __str__(self):
        str_oameni = [str(o) for o in oameni]
        return (f"Time: {self.time}\n"
                f"Oameni:\n{str_oameni}\n")
    

class NodParcurgere:
    graf = None #static
    
    def __init__(self, id, info, parinte, cost, h, autobuze): #self, id, info, parinte, cost, h, autobuze
        self.id = id # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte #parintele din arborele de parcurgere
        self.g = cost #costul de la radacina la nodul curent
        self.h = h
        self.f = self.g + self.h
        self.autobuze = autobuze #required for genereazaSuccesori

    def __gt__(self, other):
        if(self.info > other.info):
            return True
        else:
            return False

    def __eq__(self, other):
        if(self.info == other.info):
            return True
        else:
            return False
    
    def __lt__(self, other):
        if(self.info<other.info):
            return True
        else:
            return False

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l
		
    def afisDrum(self):
        l = self.obtineDrum()
        print(("->").join(l))
        print("Cost: ", self.g)
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if(infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte
		
        return False
		
    def noSol(self):  #TODO: check if initially there are multiple people in the same place
        noSol = False #      check if timestamp is so high that no other Autobuz can reach NextDestination

        cost_min_bilet = 100000

        for a in self.autobuze:
            if a.price < cost_min_bilet:
                cost_min_bilet = a.price

        for o in self.info.oameni:
            if o.money < cost_min_bilet and o.current_loc != o.destinations[-1]: #if om is not done and has no money =[
                noSol = True
                break

        return noSol

    def __str__(self):
        sir = ""
        sir += str(self.info)+"("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += " g:{}".format(self.g)
        sir += " h:{}".format(self.h)
        sir += " f:{})".format(self.f)
        return sir

class Graph: #TODO 
    def __init__(self, time_end, nod_start):
        self.time_end = time_end
        self.start = nod_start
        self.nodCurent = nod_start

    def testeaza_scop(self, nodCurent): #TODO: be careful of the fact that either you ll have no people at the end
                                        #      or each of their "remaining_dest" MUST be empty. I see no other way to check
                                        #      against the fact that they must visit each destination in order.
        isScop = True
        for o in nodcurent.info.oameni:
            if o.remaining_dest != []:
                isScop = False
                break
        return isScop

    def nuAreSolutii(self, nod): 
        return nod.noSol()       

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori=[]
		
        return listaSuccesori

	# euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if testeaza_scop(infoNod):
            return 0
        if tip_euristica=="euristica banala":
            return 1
        else: #TODO
            h=0
            
            return h

    def __repr__(self):
        sir=""
        for (k,v) in self.__dict__.items() :
            sir+="{} = {}\n".format(k,v)
        return(sir)

def init():
    if len(sys.argv) != 5:
        print("Invalid number of arguments, exiting...")
        sys.exit(0) 
    else:
        try:
            dir_in = sys.argv[1]
            dir_out = sys.argv[2]
            nsol = int(sys.argv[3])
            timeout = sys.argv[4]
        except Exception as eroare:
            print("Provided arguments are of wrong type, exiting...")
            sys.exit(0)
    return dir_in, dir_out, nsol, timeout

def make_files(dir_in, dir_out):
    try:
        listaFisiere = os.listdir(f"{dir_in}")
    except Exception as eroare:
            print("Path to input file is invalid, exiting...")
            quit()
    if not os.path.exists(f"{dir_out}"):
        os.mkdir(f"{dir_out}")
    paths_out = []
    for numeFisier in listaFisiere:
        numeFisierOutput="output_"+numeFisier
        f=open(f"{dir_out}/"+numeFisierOutput,"w")
        paths_out.append(f"{dir_out}/"+numeFisierOutput)
        f.close()
    for i in range(len(listaFisiere)):
        listaFisiere[i] = dir_in + "/" + listaFisiere[i]
    return listaFisiere, paths_out

def get_dest(string):
    index1 = 0
    index2 = -1
    while string[index1] != "\"":
        index1 += 1
    while string[index2] != "\"":
        index2 -= 1
    return string[index1+1:index2]

def get_multiple_dest(list_of_str):
    new_list = []
    for x in list_of_str:
        new_list.append(get_dest(x))
    return new_list

def read_one(paths_in, paths_out, current_fis=0):
    f = open(f"{paths_out[current_fis]}", "r")
    if f.read() != "":
        print("Output is already written for this input!")
        return None
    f.close()
    f = open(f"{paths_in[current_fis]}", "r")
    
    line = f.readline()
    line_spaces = line.split(" ")
    line_dest = line.split(",")
    time_begin, time_end = line_spaces[0], line_spaces[1]

    autobuze = []

    line = f.readline()
    line_spaces = line.split(" ")
    line_dest = line.split(",")
    while line_spaces[0].isnumeric() and line_spaces[1][0].isnumeric():
        id = int(line_spaces[0])
        price = float(line_spaces[1][:-3])
        break_duration = int(line_spaces[2][:-3])
        trip_duration = int(line_spaces[3][:-3])
        path = [get_dest(line_dest[1])] + get_multiple_dest(line_dest[1:])
        autobuze.append( Autobuz(id, price, break_duration, trip_duration, path) )

        line = f.readline()
        line_spaces = line.split(" ")
        line_dest = line.split(",")
    
    nr_oameni = int(line_spaces[0])
    oameni = []

    for i in range(nr_oameni):
        line = f.readline()
        line_spaces = line.split(" ")
        line_dest = line.split(",")

        name = line_spaces[0]
        money = float(line_spaces[1][:-3])
        destinations = [get_dest(line_dest[0])] + get_multiple_dest(line_dest[1:])
        oameni.append( Om(name, money, destinations) )

    return time_begin, time_end, autobuze, oameni, nr_oameni

def a_star(gr, nrSolutiiCautate, tip_euristica):
	#in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
	c=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
	
	while len(c) > 0:
		nodCurent = c.pop(0)
		
		if gr.testeaza_scop(nodCurent):
			print("Solutie: ")
			nodCurent.afisDrum(afisCost=True, afisLung=True)
			print("\n----------------\n")
			input()
			nrSolutiiCautate -= 1
			if nrSolutiiCautate == 0:
				return
		lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)	
		for s in lSuccesori:
			i = 0
			gasit_loc = False
			for i in range(len(c)):
				#diferenta fata de UCS e ca ordonez dupa f
				if c[i].f >= s.f :
					gasit_loc = True
					break
			if gasit_loc:
				c.insert(i,s)
			else:
				c.append(s)

def timeToMinutes(timestamp):
    # print(f"timestamp is {timestamp} and type is {type(timestamp)}\n")
    if len(timestamp) == 5: #16:00
        return int(timestamp[:2])*60 + int(timestamp[3])*10 + int(timestamp[4])
    else: #len(timestamp) == 4 #8:00
        return int(timestamp[0])*60 + int(timestamp[3])*10 + int(timestamp[4])



def main():
    dir_in, dir_out, nrsol, timeout = init()
    paths_in, paths_out = make_files(dir_in, dir_out)
    for i in range(len(paths_in)):
        time_begin, time_end, autobuze, oameni, nr_oameni = read_one(paths_in, paths_out, i)
        
        time_begin = timeToMinutes(time_begin)
        time_end = timeToMinutes(time_end)
        print(f"\ntime_begin = {time_begin}, time_end = {time_end}, time_begin*2 == time_end = {time_begin*2 == time_end}\n")

        nod_start =  NodParcurgere(0, NodInfo(oameni, time_begin), None, 0, 0, autobuze)
        graf = Graph(time_end, nod_start) #TODO

        if graf.nuAreSolutii(nod_start):
            print("Starea de inceput nu permite solutii")
            sys.exit(0)
        



if __name__ == '__main__':
    main()
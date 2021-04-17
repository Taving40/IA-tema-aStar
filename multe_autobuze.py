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
        self.id = id #used in pairing of Om and Autobuz when Om has boarded
        self.price = price
        self.break_duration = break_duration #extra time Autobuz takes when it reaches end of route
        self.trip_duration = trip_duration #time Autobuz takes between 2 stations
        self.destinations = destinations #route Autobuz travels 
        self.current_loc = len(destinations)-1 #index for list destinations
        self.direction_forward = False #initially leaves from end of route (as in example_output)
        self.om = None #field of type Om to see if there is anyone currently in Autobuz
        self.metOm = [] #list of Om that autobuz has already passed by (used to check against so Om cannot board Autobuz after it has passed him by)
    
    def __str__(self):
        return (f"id={self.id} "
                f"price={self.price} "
                f"break_duration={self.break_duration} "
                f"trip_duration={self.trip_duration} "
                f"om={self.om} "
                f"current_loc={self.destinations[self.current_loc]}")
    
    def unmeetLoc(self, loc): #method to remove Om as having been met by Autobuz (if he changed locations since he was met he is again given the chance to board)
        to_remove = None
        for i in range(len(self.metOm)):
            if self.metOm[i][1] == loc:
                to_remove = self.metOm[i]
        if to_remove != None:
            self.metOm.remove(to_remove)
            print(f"\n{to_remove[0].name} was removed from banned list because bus reached {loc}\n")

    def hasMet(self, om): #method to see if Om was previously met by Autobuz (and thus should not be given a chance to board)
        wasMet = False
        for i in range(len(self.metOm)):
            if self.metOm[i][0].name == om.name:
                wasMet = True
                break
        return wasMet

    def updateOmLocation(self):
        if self.om != None:
            self.om.current_loc = self.destinations[self.current_loc]

    def getNextDest(self):
        if self.direction_forward:
            if len(self.destinations)-1 == self.current_loc: #if Autobuz reaches rightmost destination, it also takes a break and changes directions
                self.direction_forward = False #Autobuz changes direction
                self.updateOmLocation()
                return self.destinations[self.current_loc], (self.break_duration + self.trip_duration) #return destination reached and elapsed time
  
            else:
                self.current_loc += 1
                self.updateOmLocation()
                return self.destinations[self.current_loc], self.trip_duration
        
        else:
            if 0 == self.current_loc: #if Autobuz reaches leftmost destination, it also takes a break and changes directions
                self.direction_forward = True #Autobuz changes direction
                self.updateOmLocation()
                return self.destinations[self.current_loc],  (self.break_duration + self.trip_duration)
            
            else:
                self.current_loc -= 1
                self.updateOmLocation()
                return self.destinations[self.current_loc], self.trip_duration

class Om:
    def __init__(self, name, money, destinations):
        self.name = name
        self.money = money
        self.destinations = destinations
        self.remaining_dest = destinations[1:]
        self.current_loc = destinations[0] 
        self.state = "waiting" #can be "waiting" or "travelling"
        self.autobuz = None #Autobuz id

    def isDone(self):
        if self.remaining_dest == []:
            return True
        return False

    def hasVisitedNext(self):
        if len(self.remaining_dest):
            self.remaining_dest = []
        else:
            self.remaining_dest = self.remaining_dest[1:]

    def __str__(self):
        return (f"name={self.name} "
                f"money={self.money} "
                f"current_loc={self.current_loc} "
                f"first_dest={self.destinations[0]} "
                f"state={self.state} "
                f"autobuz={self.autobuz}")

class NodInfo:
    def __init__(self, oameni, autobuze, time):
        self.oameni = oameni
        self.time = time
        self.autobuze = autobuze #required for genereazaSuccesori

    def __str__(self):
        str_oameni = [str(o) for o in self.oameni]
        str_auto = [str(a) for a in self.autobuze]
        return (f"Time: {self.time}\n"
                f"Oameni:\n{str_oameni}\n"
                f"Autobuze:\n{str_auto}\n")
    
    def sort_auto(self):
        key = lambda buz1, buz2: buz1 if buz1.trip_duration <= buz2.trip_duration else buz2
        self.autobuze.sort(key=key)
    

class NodParcurgere:
    graf = None #static
    
    def __init__(self, info, parinte, cost, h=0): 
        self.info = info
        self.parinte = parinte #parintele din arborele de parcurgere
        self.g = cost #costul de la radacina la nodul curent
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [str(self.info)]
        nod = self
        while nod.parinte is not None:
            l.insert(0, str(nod.parinte.info))
            nod = nod.parinte
        return l
		
    def afisDrum(self):
        l = self.obtineDrum()
        print(("->").join(l))
        print("Cost: ", self.g)
        return len(l)

    def contineInDrum(self, NodNou):
        nodDrum = self
        while nodDrum is not None:
            if(NodNou.info == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte
		
        return False
		
    def noSol(self):  
        noSol = False 

        cost_min_bilet = 100000

        for a in self.info.autobuze:
            if a.price < cost_min_bilet:
                cost_min_bilet = a.price

        #check if there is Om that can no longer move and stil has remaining_dest
        for o in self.info.oameni:
            if o.money < cost_min_bilet and o.remaining_dest != []: #if om is not done and has no money =[
                noSol = True
                break
        
        #check if there are multiple people in the same place
        set_destinatii = set()

        for o in self.info.oameni:
            if o.current_loc in set_destinatii:
                noSol = True
                break
            else:
                set_destinatii.add(o.current_loc)

        return noSol

    def __str__(self):
        sir = ""
        sir += str(self.info)+"("
        #sir += "drum="
        #drum = self.obtineDrum()
        #sir += ("->").join(drum)
        sir += "g:{}".format(self.g)
        sir += " h:{}".format(self.h)
        sir += " f:{})".format(self.f)
        return sir

class Graph: #TODO 
    def __init__(self, time_end, nod_start):
        self.time_end = time_end
        self.start = nod_start
        self.nodCurent = nod_start

    def testeaza_scop(self, nodInfo): #TODO: be careful of the fact that either you ll have no people at the end
                                        #      or each of their "remaining_dest" MUST be empty. I see no other way to check
                                        #      against the fact that they must visit each destination in order.
        isScop = True
        for o in nodInfo.oameni:
            if o.remaining_dest != []:
                isScop = False
                break
        return isScop

    def nuAreSolutii(self, nod): 
        return nod.noSol()       

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"): #TODO: handle events for when buses first start and there s someone there already
        listaSuccesori=[]                                                       #     make sure that Om MUST unboard when Autobuz reaches first or last destination
                                                                                # "autobuzele dispar cand ajung in capat, generarea urmatorului fiind separata"
        if self.nuAreSolutii(nodCurent):
            return listaSuccesori

        tempNod = deepcopy(nodCurent) #might cause issues related to field "parinte"

        timpCurent = tempNod.info.time
        autobuzeCurent = tempNod.info.autobuze
        oameniCurent = tempNod.info.oameni

        print("-"*30 + "\nStarting state:\nAutobuze:")
        for a in nodCurent.info.autobuze:
            print(f"{a.id} is at {a.destinations[a.current_loc]} and has {a.om} inside")
        for o in nodCurent.info.oameni:
            print(f"{o.name} is at {o.current_loc} and is in {o.autobuz}")
        print("\n\n")

        while(timpCurent < self.time_end): #iterate over all possible events from current time until end time

            if self.nuAreSolutii(tempNod):
                print("\nOprit din generat pentru ca nu mai am solutii\n")
                break

            #iterate over autobuz
            for i in range(len(autobuzeCurent)):

                posEvent = autobuzeCurent[i].getNextDest() #possible event triggered when Autobuz reaches next station

                if autobuzeCurent[i].om != None:
                    print(f"Bus {autobuzeCurent[i].id} is now at {autobuzeCurent[i].destinations[autobuzeCurent[i].current_loc]} and has {autobuzeCurent[i].om.name} inside")
                else:
                    print(f"Bus {autobuzeCurent[i].id} is now at {autobuzeCurent[i].destinations[autobuzeCurent[i].current_loc]} and has no one inside")

                #decide if it actually is "event" (event = Om changes state and a succesor must be added to the list)
                temp_loc = posEvent[0]
                temp_est_time = posEvent[1]
                posOm = None #possible Om met in station, remains None if no Om in station

                timpCurent += temp_est_time #no matter whether Om changes states, we still consider the trip of the Autobuz to have taken place
                #(changing tempNod not nodCurent as parent node must stay the same)
                #timpCurent is now equal to when the current Autobuz has reached its next station

                #iterate over oameni not in Autobuz and check their locations
                for j in range(len(oameniCurent)):
                    if oameniCurent[j].autobuz == None and oameniCurent[j].current_loc == temp_loc:
                        posOm = j
                        break

                if posOm == None: #remove previously encountered Om that has since changed position
                    autobuzeCurent[i].unmeetLoc(temp_loc)
                    # print(f"removed {temp_loc} from bus {autobuzeCurent[i].id} (which has inside {autobuzeCurent[i].om}) banned list ")
                    
                #if there is an Om in station and Autobuz arrives but already has Om inside
                if posOm != None and oameniCurent[posOm] != None and autobuzeCurent[i].om != None: 
                    print(f"parent is: {nodCurent}\n\n, found {oameniCurent[posOm]}\n\n and {autobuzeCurent[i].om}\n\n\n\n\n\n")
                    
                    #register Om as having not gotten on this Autobuz, so that he cannot take it until he changes positions
                    autobuzeCurent[i].metOm.append((oameniCurent[posOm], temp_loc)) 
                    print(f"{oameniCurent[posOm].name} was added to banned list (case 1)")
                    continue 

                #if there is an Om at station and Autobuz is empty (generate successor where Om boards)
                elif posOm != None and oameniCurent[posOm] != None: 
                    
                    print(f"{oameniCurent[posOm].name} was met", end="")
                    if autobuzeCurent[i].hasMet(oameniCurent[posOm]): #if person chose not to board the first time, we ignore
                        print(f" and didnt board because he is banned")
                        continue
                    print(f" and boarded bus {autobuzeCurent[i].id}")

                    go_back_to = deepcopy(oameniCurent[posOm])

                    oameniCurent[posOm].autobuz = autobuzeCurent[i].id
                    oameniCurent[posOm].state = "travelling"
                    oameniCurent[posOm].money -= autobuzeCurent[i].price
                    autobuzeCurent[i].om = deepcopy(oameniCurent[posOm]) #deepcopy just to be sure

                    info = NodInfo(deepcopy(oameniCurent), deepcopy(autobuzeCurent), timpCurent) #lists provided to new NodInfo and new NodParcurgere are changed from tempNod not nodCurent (because nodCurent must NOT change)
                    nod_nou = NodParcurgere(info, nodCurent, autobuzeCurent[i].price + (timpCurent - nodCurent.info.time), self.calculeaza_h(info))
                    #cost is the price for boarding + (time after Autobuz reached new station - time of parent node)
                    if not nodCurent.contineInDrum(nod_nou):
                        listaSuccesori.append(nod_nou)
                    
                    #for future events, we consider that this Om did not board the Autobuz
                    autobuzeCurent[i].metOm.append((oameniCurent[posOm], temp_loc)) 
                    oameniCurent[posOm] = go_back_to
                    autobuzeCurent[i].om = None
                    print(f"{oameniCurent[posOm].name} was added to banned list (case 2)")
                    print(f"\n\nAm generat si adaugat in lista de succesori urmatorul nod: {listaSuccesori[-1].info}\n\n")

                #if station is empty and Autobuz has Om inside (generate successor where Om unboards)
                elif posOm == None and autobuzeCurent[i].om != None: 

                    #find om object in oameniCurent so that we change the actual Nod
                    temp_om = autobuzeCurent[i].om.name
                    for j in range(len(oameniCurent)):
                       if temp_om == oameniCurent[j].name:
                           temp_om = j
                           break 

                    go_back_to = deepcopy(oameniCurent[temp_om])

                    oameniCurent[temp_om].autobuz = None
                    oameniCurent[temp_om].state = "waiting"

                    #update the remaining destinations for Om if this station was first in his remaining destinations list
                    if oameniCurent[temp_om].remaining_dest != [] and oameniCurent[temp_om].remaining_dest[0] == temp_loc:
                        oameniCurent[temp_om].hasVisitedNext()

                    autobuzeCurent[i].om = None

                    info = NodInfo(deepcopy(oameniCurent), deepcopy(autobuzeCurent), timpCurent)
                    nod_nou = NodParcurgere(info, nodCurent, (timpCurent - nodCurent.info.time), self.calculeaza_h(info))

                    if not nodCurent.contineInDrum(nod_nou):
                        listaSuccesori.append(nod_nou)
                    
                    #for future events, we consider that this Om stayed in Autobuz 
                    oameniCurent[temp_om] = go_back_to
                    autobuzeCurent[i].om = oameniCurent[temp_om]
                    oameniCurent[temp_om].state = "travelling"

                
        return listaSuccesori


    # TODO: idei euristica
    # decided by the total cost needed for each Om to reach all of his destinations 
    # probably by adding up all the "ideal" costs (as if reaching destination only took one station)
    # next should estimate how many stations it would take and multiply by lowest or highest or average cost?
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if self.testeaza_scop(infoNod):
            return 0
        if tip_euristica == "euristica banala":
            return 1
        else: #TODO
            h=0
            
            return h

    def __repr__(self):
        sir=""
        for (k,v) in self.__dict__.items():
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
    time_begin, time_end = line_spaces[0].strip(), line_spaces[1].strip()

    autobuze = []

    line = f.readline()
    line_spaces = line.split(" ")
    line_dest = line.split(",")
    while line_spaces[0].isnumeric() and line_spaces[1][0].isnumeric():
        id = int(line_spaces[0])
        price = float(line_spaces[1][:-3])
        break_duration = int(line_spaces[2][:-3])
        trip_duration = int(line_spaces[3][:-3])
        path = [get_dest(line_dest[0])] + get_multiple_dest(line_dest[1:])
        autobuze.append( Autobuz(id, price, break_duration, trip_duration, path) )

        line = f.readline()
        line_spaces = line.split(" ")
        line_dest = line.split(",")
    
    nr_oameni = int(line_spaces[0])
    oameni = []

    for _ in range(nr_oameni):
        line = f.readline()
        line_spaces = line.split(" ")
        line_dest = line.split(",")

        name = line_spaces[0]
        money = float(line_spaces[1][:-3])
        destinations = [get_dest(line_dest[0])] + get_multiple_dest(line_dest[1:])
        oameni.append( Om(name, money, destinations) )

    return time_begin, time_end, autobuze, oameni, nr_oameni

def a_star(gr, nrSolutiiCautate, tip_euristica): #TODO: to remember when printing: if Om is "waiting" it means he has unboarded and if he is "travelling" it means he has boarded
    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(gr.start.info, None, 0, gr.calculeaza_h(gr.start.info))]

    while len(c) > 0:
        nodCurent = c.pop(0)
        
        if gr.testeaza_scop(nodCurent.info):
            print("Solutie: ")
            # nodCurent.afisDrum(afisCost=True, afisLung=True)
            nodCurent.afisDrum()
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        print(f"\nAm terminat de generat {len(lSuccesori)} succesori pt un nod\n")	
        for s in lSuccesori:
            i = 0
            print("-"*30 + "\n" + s.info.oameni[0].current_loc + "\n")
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
    if len(timestamp) == 5: 
        return int(timestamp[0])*600 + int(timestamp[1])*60 + int(timestamp[3])*10 + int(timestamp[4])
    return None

        



def main():
    dir_in, dir_out, nrsol, timeout = init()
    paths_in, paths_out = make_files(dir_in, dir_out)
    for i in [0]:#range(len(paths_in)):
        print("-"*20 + "pt input nr {}".format(i) + "-"*20)

        time_begin, time_end, autobuze, oameni, nr_oameni = read_one(paths_in, paths_out, i)

        time_begin = timeToMinutes(time_begin)
        time_end = timeToMinutes(time_end)
        # print(f"\ntime_begin = {time_begin}, time_end = {time_end}, time_begin*2 == time_end = {time_begin*2 == time_end}\n")

        info = NodInfo(oameni, autobuze, time_begin)
        nod_start =  NodParcurgere(info, None, 0, 0)
        graf = Graph(time_end, nod_start) #TODO: test genereazaSuccesori
        nod_start.graf = graf

        if graf.nuAreSolutii(nod_start):
            print("Starea de inceput nu permite solutii")
            sys.exit(0)

        # succesori_start = graf.genereazaSuccesori(nod_start)

        # for s in succesori_start:
        #     print(s)

        a_star(graf, 1, "euristica banala")

        



if __name__ == '__main__':
    main()
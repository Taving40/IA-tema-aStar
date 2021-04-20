import sys
import os
from copy import deepcopy

#TODO: 
# Figure out euristica
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
                #f"price={self.price} "
                #f"break_duration={self.break_duration} "
                #f"trip_duration={self.trip_duration} "
                f"current_loc={self.destinations[self.current_loc]} "
                f"direction_forward={self.direction_forward} "
                f"om={self.om} "
                )
    
    def goingToBreak(self): #method to check if Autobuz will take a break before it reaches the next destination (enters garage)
        if (
            (self.current_loc == 0 and not self.direction_forward) or
            (self.current_loc == len(self.destinations)-1 and self.direction_forward)
            ):
            return True
        return False


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

    def getCurrentDest(self, time_begin, time_actual, oameni=None): 
        time_decal = time_actual - time_begin
        #current_dest_index = time_decal % (len(self.destinations) * self.trip_duration + self.break_duration) formula for smarter way of calculating dest
        temp_copy = deepcopy(self)
        temp_copy.current_loc = len(temp_copy.destinations)-1
        temp_copy.direction_forward = False
        while time_decal >= 0:
            _, time = temp_copy.getNextDest()
            #TODO: add met people to metOm?
            time_decal -= time
        if temp_copy.direction_forward and temp_copy.current_loc == 0:
            return temp_copy.destinations[0], 0, temp_copy.direction_forward
        elif temp_copy.direction_forward and temp_copy.current_loc != 0:
            return temp_copy.destinations[temp_copy.current_loc-1], temp_copy.current_loc-1, temp_copy.direction_forward
        elif not temp_copy.direction_forward and temp_copy.current_loc == len(temp_copy.destinations)-1:
            return temp_copy.destinations[len(temp_copy.destinations)-1], len(temp_copy.destinations)-1, temp_copy.direction_forward
        elif not temp_copy.direction_forward and temp_copy.current_loc != len(temp_copy.destinations)-1:
            return temp_copy.destinations[temp_copy.current_loc+1], temp_copy.current_loc+1, temp_copy.direction_forward


class Om:
    def __init__(self, name, money, destinations):
        self.name = name
        self.money = money
        self.destinations = destinations
        self.remaining_dest = destinations[1:]
        self.current_loc = destinations[0] 
        self.state = "waiting" #can be "waiting" or "travelling"
        self.autobuz = None #Autobuz id
        self.last_action = None

    def isDone(self):
        if self.remaining_dest == []:
            return True
        return False

    def hasVisitedNext(self):
        if len(self.remaining_dest) == 1:
            self.remaining_dest = []
        else:
            self.remaining_dest = self.remaining_dest[1:]

    def __str__(self):
        return (f"name={self.name} "
                #f"money={self.money} "
                f"current_loc={self.current_loc} "
                #f"state={self.state} "
                f"autobuz={self.autobuz} ")
                #f"remainig={self.remaining_dest}")

class Event:
    def __init__(self, tip, autobuz, om, time):
        self.tip = tip
        self.autobuz = autobuz
        self.om = om
        self.time = time

    def __str__(self):
        return (f"---------------------------------------\n"
                f"Time: {self.time} \n"
                f"Tip: {self.tip} \n"
                f"Autobuz: {self.autobuz} \n"
                f"Om: {self.om} \n"
                f"---------------------------------------\n")

class NodInfo:
    def __init__(self, oameni, autobuze, time, event=None):
        self.oameni = oameni
        self.time = time
        self.autobuze = autobuze #required for genereazaSuccesori
        self.event = event

    def __str__(self):
        str_oameni = [str(o) for o in self.oameni]
        str_auto = [str(a) for a in self.autobuze]
        return (f"Time: {self.time}\n"
                f"Oameni:\n{str_oameni}\n"
                f"Autobuze:\n{str_auto}\n"
                f"Event:\n{self.event}\n")
    
    def sort_auto(self):
        key = lambda buz1, buz2: buz1 if buz1.trip_duration <= buz2.trip_duration else buz2
        self.autobuze.sort(key=key)
    

class NodParcurgere:

    def __init__(self, info, parinte, cost, h=0): 
        self.info = info
        self.parinte = parinte #parintele din arborele de parcurgere
        self.g = cost #costul de la radacina la nodul curent
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l
		
    def afisDrum(self):
        # TODO:
        # function to figure out timp_mers, timp_asteptat and traseu
        l = self.obtineDrum()
        # for i in range(len(l)):
        #     l[i] = str(l[i])
        # print(("\n\n------------------------------->\n\n").join(l))
        for i in range(1, len(l)):
            print(f"{i})\n{minutesToTime(l[i].time)}")
            for j in range(len(l[i].oameni)):
                if l[i].oameni[j].state != l[i-1].oameni[j].state:
                    if l[i-1].oameni[j].state == "waiting" and l[i].oameni[j].state == "travelling":
                        #function that returns timp_mers, timp_asteptat, traseu with paramater drum 
                        print(f"Omul {l[i].oameni[j].name} a urcat in statia {l[i].oameni[j].current_loc} in autobuzul {l[i].oameni[j].autobuz} pentru traseul ???. Buget: {l[i].oameni[j].money}lei. Timp mers: ???. Timp asteptare: ???.")
                    elif  l[i-1].oameni[j].state == "travelling" and l[i].oameni[j].state == "waiting":
                        #function that returns timp_mers, timp_asteptat, traseu with paramater drum 
                        print(f"Omul {l[i].oameni[j].name} a coborat in statia {l[i].oameni[j].current_loc} din autobuzul {l[i].oameni[j].autobuz}. Buget: {l[i].oameni[j].money}lei. Timp mers: ???. Timp asteptare: ???.")
                else:
                    if l[i].oameni[j].state == "travelling":
                        #function that returns timp_mers, timp_asteptat, traseu with paramater drum 
                        print(f"Omul {l[i].oameni[j].name} se deplasează cu autobuzul {l[i].oameni[j].autobuz} de la statia {l[i-1].oameni[j].current_loc} la statia {l[i].oameni[j].current_loc} pe traseul ???. Buget: {l[i].oameni[j].money}lei. Timp mers: ???. Timp asteptare: ???.")
                    elif l[i].oameni[j].state == "waiting":
                        print(f"Omul {l[i].oameni[j].name} așteaptă în stația {l[i].oameni[j].current_loc}. Buget: {l[i].oameni[j].money}lei. Timp mers: ???. Timp asteptare: ???.")
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

class Graph: 
    def __init__(self, time_end, nod_start):
        self.time_end = time_end
        self.start = nod_start
        self.nodCurent = nod_start

    def testeaza_scop(self, nodInfo): 
        isScop = True
        for o in nodInfo.oameni:
            if o.remaining_dest != []:
                isScop = False
                break
        return isScop

    def nuAreSolutii(self, nod): 
        return nod.noSol()       

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"): 
        listaSuccesori=[]                                                           
                                                                                
        if self.nuAreSolutii(nodCurent):
            return listaSuccesori

        tempNod = deepcopy(nodCurent)

        timpCurent = tempNod.info.time
        autobuzeCurent = tempNod.info.autobuze
        oameniCurent = tempNod.info.oameni
        lista_events = []
        
        while(timpCurent < self.time_end): #iterate over all possible events from current time until end time
            if self.nuAreSolutii(tempNod):
                print("\nOprit din generat pentru ca nu mai am solutii\n")
                break

            #iterate over autobuz
            for i in range(len(autobuzeCurent)):

                if timpCurent != nodCurent.info.time:
                    # print(f"Verific daca autobuzul {autobuzeCurent[i].id} ajunge la urmatoarea statie: {(timpCurent - nodCurent.info.time)} / {autobuzeCurent[i].trip_duration} = {((timpCurent - nodCurent.info.time) / autobuzeCurent[i].trip_duration)}")
                    if ((timpCurent - self.start.info.time) / autobuzeCurent[i].trip_duration).is_integer(): #if current time decal from beginning time divides evenly into trip_duration of Autobuz that means it has reached its next dest
                        # print("S-a verificat ca rezultatul e intreg")
                        posEvent = autobuzeCurent[i].getNextDest() #possible event triggered when Autobuz reaches next station
                    else:
                        continue

                    temp_loc = posEvent[0]
                else: #find events for initial location of Autobuze
                    temp_loc = autobuzeCurent[i].destinations[autobuzeCurent[i].current_loc]
                
                #iterate over oameni not in Autobuz and check their locations
                posOm = None #possible Om met in station, remains None if no Om in station
                for j in range(len(oameniCurent)):
                    if oameniCurent[j].autobuz == None and oameniCurent[j].current_loc == temp_loc:
                        posOm = j
                        break
                if posOm == None: #remove previously encountered Om that has since changed position
                    autobuzeCurent[i].unmeetLoc(temp_loc)
                    # print(f"removed {temp_loc} from bus {autobuzeCurent[i].id} (which has inside {autobuzeCurent[i].om}) banned list ")
                    
                #IF there is an Om in station and Autobuz arrives but already has Om inside
                if posOm != None and oameniCurent[posOm] != None and autobuzeCurent[i].om != None: 
                    if autobuzeCurent[i].goingToBreak():
                        # print(f"{ oameniCurent[posOm].name} was met before break and {autobuzeCurent[i].om.name} is inside bus, there are no more successors")
                        timpCurent = self.time_end+1
                        break
                    
                    #register Om as having not gotten on this Autobuz, so that he cannot take it until he changes positions
                    autobuzeCurent[i].metOm.append((oameniCurent[posOm], temp_loc)) 
                    # print(f"{oameniCurent[posOm].name} was added to banned list (case 1)")
                    continue 

                #IF there is an Om at station and Autobuz is empty (generate successor where Om boards)
                elif posOm != None and oameniCurent[posOm] != None: 
                    
                    #if Autobuz is going to take break  
                    if autobuzeCurent[i].goingToBreak():
                        # print(f"{oameniCurent[posOm].name} did not board because he was met at the last station")
                        continue

                    # print(f"{oameniCurent[posOm].name} was met", end="")
                    if autobuzeCurent[i].hasMet(oameniCurent[posOm]): #if person chose not to board the first time, we ignore
                        # print(f" and didnt board because he is banned")
                        continue
                    # print(f" and boarded bus {autobuzeCurent[i].id}")

                    go_back_to = deepcopy(oameniCurent[posOm])
                    oameniCurent[posOm].autobuz = autobuzeCurent[i].id
                    oameniCurent[posOm].state = "travelling"
                    oameniCurent[posOm].money -= autobuzeCurent[i].price
                    autobuzeCurent[i].om = deepcopy(oameniCurent[posOm]) 

                    new_event = Event("boarding", deepcopy(autobuzeCurent[i]), deepcopy(oameniCurent[posOm]), timpCurent)
                    lista_events.append(new_event)

                    # info = NodInfo(deepcopy(oameniCurent), deepcopy(autobuzeCurent), timpCurent) #lists provided to new NodInfo and new NodParcurgere are changed from tempNod not nodCurent (because nodCurent must NOT change)
                    # nod_nou = NodParcurgere(info, nodCurent, nodCurent.g + autobuzeCurent[i].price + (timpCurent - nodCurent.info.time), self.calculeaza_h(info))
                    
                    #for future events, we consider that this Om did not board the Autobuz
                    autobuzeCurent[i].metOm.append((oameniCurent[posOm], temp_loc)) 
                    oameniCurent[posOm] = go_back_to
                    autobuzeCurent[i].om = None
                    # print(f"{oameniCurent[posOm].name} was added to banned list (case 2)")
                    # print(f"\n\nAm generat si adaugat in lista de succesori urmatorul nod: {listaSuccesori[-1]}\n\n")

                #IF station is empty and Autobuz has Om inside (generate successor where Om unboards)
                elif posOm == None and autobuzeCurent[i].om != None: 
                    # print("\nAm intrat pe cazul in care am om in autobuz si nimeni in statie.\n")
                    # print(f"\nRn, {autobuzeCurent[i].om.name} is at {autobuzeCurent[i].om.current_loc}\n")

                    #find om object in oameniCurent so that we change the actual Nod
                    temp_om = autobuzeCurent[i].om.name
                    for j in range(len(oameniCurent)):
                       if temp_om == oameniCurent[j].name:
                           temp_om = j
                           break 

                    oameniCurent[temp_om].current_loc = autobuzeCurent[i].om.current_loc #update location of Om from oameni to same Om from inside Autobuz

                    # print(f"\n {oameniCurent[temp_om].name} is at {oameniCurent[temp_om].current_loc}")
                    go_back_to = deepcopy(oameniCurent[temp_om])
                    # print(f"\ngo_back_to este {go_back_to}\n")
                    oameniCurent[temp_om].autobuz = None
                    oameniCurent[temp_om].state = "waiting"

                    #update the remaining destinations for Om if this station was first in his remaining destinations list
                    if oameniCurent[temp_om].remaining_dest != [] and oameniCurent[temp_om].remaining_dest[0] == temp_loc:
                        oameniCurent[temp_om].hasVisitedNext()
                    autobuzeCurent[i].om = None

                    new_event = Event("unboarding", deepcopy(autobuzeCurent[i]), deepcopy(oameniCurent[temp_om]), timpCurent)
                    lista_events.append(new_event)

                    # info = NodInfo(deepcopy(oameniCurent), deepcopy(autobuzeCurent), timpCurent)
                    # nod_nou = NodParcurgere(info, nodCurent, nodCurent.g + (timpCurent - nodCurent.info.time), self.calculeaza_h(info))

                    #for future events, we consider that this Om stayed in Autobuz 
                    oameniCurent[temp_om] = go_back_to
                    autobuzeCurent[i].om = oameniCurent[temp_om]
                    oameniCurent[temp_om].state = "travelling"

                    # if not nodCurent.contineInDrum(nod_nou):
                    #     listaSuccesori.append(nod_nou)
                    #     print(f"\n\nAm generat si adaugat in lista de succesori urmatorul nod: {listaSuccesori[-1]}\n\n")

                    #if Autobuz is also going to break, forcefully terminate method (since there is no other action that could be taken)
                    if autobuzeCurent[i].goingToBreak():
                        # print(f"{autobuzeCurent[i].om.name} got off at last possible station, no further successors exist for this node")
                        timpCurent = self.time_end+1
                        break

            timpCurent += autobuzeCurent[0].trip_duration #incrementez timeline-ul in cel mai mare increment de timp relevant (shortest trip duration)

        for i in range(len(lista_events)):

            if (nodCurent.info.event != None and
                lista_events[i].tip == "unboarding" and 
                nodCurent.info.event.tip == "boarding" and
                nodCurent.info.event.om.name == lista_events[i].om.name and
                nodCurent.info.event.om.current_loc == lista_events[i].om.current_loc and 
                nodCurent.info.event.time == lista_events[i].time):
                continue #Om cannot unboard right after boarding

            if (nodCurent.info.event != None and
                lista_events[i].tip == "boarding" and 
                nodCurent.info.event.tip == "unboarding" and
                nodCurent.info.event.om.name == lista_events[i].om.name and
                nodCurent.info.event.om.current_loc == lista_events[i].om.current_loc and
                nodCurent.info.event.time == lista_events[i].time):
                continue #Om cannot board right after unboarding

            if (lista_events[i].om.last_action != None and
                lista_events[i].tip != lista_events[i].om.last_action[0] and
                lista_events[i].autobuz.id == lista_events[i].om.last_action[1] and
                lista_events[i].om.current_loc == lista_events[i].om.last_action[2] and
                lista_events[i].time == lista_events[i].om.last_action[3]):
                continue #same as above but works accross Graph "layers"

            #TODO: find way to prevent Om from doing these 2 actions^^^^ no matter the depth of node
            #currently Om unboards, new event happens and he boards again
            
            # print(lista_events[i])

            autobuze_new = deepcopy(nodCurent.info.autobuze)
            oameni_new = deepcopy(nodCurent.info.oameni)
            for j in range(len(autobuze_new)):
                if autobuze_new[j].id == lista_events[i].autobuz.id:
                    autobuze_new[j] = lista_events[i].autobuz
                else:
                    print(f"{autobuze_new[j].id} updated {autobuze_new[j].destinations[autobuze_new[j].current_loc]} to ", end="")
                    x, autobuze_new[j].current_loc, autobuze_new[j].direction_forward = autobuze_new[j].getCurrentDest(self.start.info.time, lista_events[i].time, oameni_new)
                    if autobuze_new[j].om != None:
                        autobuze_new[j].om.current_loc = autobuze_new[j].destinations[autobuze_new[j].current_loc]
                    print(x + f" given params: start_time={self.start.info.time}, actual_time={lista_events[i].time}")
            for j in range(len(oameni_new)):
                if oameni_new[j].name == lista_events[i].om.name:
                    oameni_new[j] = lista_events[i].om
                    oameni_new[j].last_action = [lista_events[i].tip, lista_events[i].autobuz.id, deepcopy(oameni_new[j].current_loc), lista_events[i].time]
                else:
                    for k in range(len(autobuze_new)):
                        if autobuze_new[k].om != None and autobuze_new[k].om.name == oameni_new[j].name:
                            oameni_new[j].current_loc = autobuze_new[k].om.current_loc

            

            info_new = NodInfo(oameni_new, autobuze_new, lista_events[i].time, deepcopy(lista_events[i]))
            cost_new = nodCurent.g
            if lista_events[i].tip == "boarding":
                cost_new += lista_events[i].autobuz.price 
            cost_new += lista_events[i].time - nodCurent.info.time 
            nod_new = NodParcurgere(info_new, nodCurent, cost_new, self.calculeaza_h(info_new))
            if not nodCurent.contineInDrum(nod_new):
                listaSuccesori.append(nod_new)
                print(f"\n\nAm generat si adaugat in lista de succesori urmatorul nod: {listaSuccesori[-1]}\n\n")
            else:
                print("Am generat un succesor care e deja in drumul parintelui")

        return listaSuccesori


    # TODO: idei euristica
    # decided by the total cost needed for each Om to reach all of his destinations 
    # probably by adding up all the "ideal" costs (as if reaching destination only took one station)
    # next should estimate how many stations it would take and multiply by lowest or highest or average cost?
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if self.testeaza_scop(infoNod):
                return 0
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
            print(nodCurent.info.oameni[0].remaining_dest)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        print(f"\n*********************************************\nGenerez succesori pt nodul \n{nodCurent.info}\n*********************************************\n")
        lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)	
        for s in lSuccesori:
            i = 0
            # print("-"*30 + "\n" + s.info.oameni[0].current_loc + "\n")
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

def minutesToTime(minutes):
    h10, h1, m10, m1 = 0, 0, 0, 0
    h10 = int(minutes/600)
    h1 = int(minutes%600 / 60)
    m10 = int((minutes - (h10*600 + h1*60)) / 10)
    m1 = int((minutes - (h10*600 + h1*60)) % 10)
    return f"{h10}{h1}:{m10}{m1}"



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
        graf = Graph(time_end, nod_start)

        if graf.nuAreSolutii(nod_start):
            print("Starea de inceput nu permite solutii")
            sys.exit(0)

        # succesori_start = graf.genereazaSuccesori(nod_start)

        # for s in succesori_start:
        #     print(s)

        a_star(graf, nrsol, "euristica banala")

        



if __name__ == '__main__':
    main()
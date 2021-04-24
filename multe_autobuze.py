import sys
import os
from copy import deepcopy
from func_timeout import func_timeout, FunctionTimedOut
from time import time
   
class Autobuz:
    """Models a bus that can move according to a route and retain information about the person currently on-board

    """

    def __init__(self, id, price, break_duration, trip_duration, destinations):
        """__init__ 

        Args:
            id (int): Number used as identifier for Autobuz object.
            price (int): Price Om must pay to board (the price of a ticket). 
            break_duration (int): Time in minutes to start moving again after looping once through all stations.
            trip_duration (int): Time in minutes to move between two adjacent stations.
            destinations (list of str): The route the object travels.
            current_loc (int): Index for list destinations.
            direction_forward (bool): True if Autobuz is currently moving from left to right in regards to destinations.
            om (Om): Om that is currently aboard object.
            metOm (list of Om): list of Om that autobuz has already passed by and didn't pick up.
        
        Note:
            metOm is used to check against so that Om cannot board Autobuz after it has passed him by.
            Initially object starts from last station, moving from right-most station to the left.

        """

        self.id = id 
        self.price = price
        self.break_duration = break_duration 
        self.trip_duration = trip_duration 
        self.destinations = destinations 
        self.current_loc = len(destinations)-1 
        self.direction_forward = False 
        self.om = None 
        self.metOm = [] 
    
    def getIndexLoc(self, location):
        """Provides ease of access.

        Args:
            location (str): One of the stations in destinations

        Returns:
            The index the station was found at in the list, None otherwise.

        """

        for i in range(len(self.destinations)):
            if self.destinations[i] == location:
                return i
        return None

    def __str__(self):
        return (f"id={self.id} "
                f"price={self.price} "
                f"break_duration={self.break_duration} "
                f"trip_duration={self.trip_duration} "
                f"current_loc={self.destinations[self.current_loc]} "
                f"direction_forward={self.direction_forward} "
                f"om={self.om} "
                )
    
    def goingToBreak(self): 
        """Checks if object will take a break before it reaches the next destination.

        Returns:
            True if Autobuz is at the last station and moving from right to left or at the first station and moving from left to right, False otherwise.

        """
        
        if (
            (self.current_loc == 0 and not self.direction_forward) or
            (self.current_loc == len(self.destinations)-1 and self.direction_forward)
            ):
            return True
        return False


    def unmeetLoc(self, loc): 
        """Removes all previously met people at the provided station.

        Args:
            loc (str): Station belonging to object's route

        """
        
        to_remove = None
        for i in range(len(self.metOm)):
            if self.metOm[i][1] == loc:
                to_remove = self.metOm[i]
        if to_remove != None:
            self.metOm.remove(to_remove)
            # print(f"\n{to_remove[0].name} was removed from banned list because bus reached {loc}\n")

    def hasMet(self, om):
        """Check if provided Om was previously met

        Args:
            om (Om): Om that is checked to see if he was met and did not board this Autobuz

        Returns:
            True if om was met, False otherwise

        """
        wasMet = False
        for i in range(len(self.metOm)):
            if self.metOm[i][0].name == om.name:
                wasMet = True
                break
        return wasMet

    def updateOmLocation(self):
        """Updates the location field of the Om currently travelling on this Autobuz

        """
        if self.om != None:
            self.om.current_loc = self.destinations[self.current_loc]

    def getNextDest(self):
        """Used to move this Autobuz to the next station in its route.

        Returns:
            A string with the name of the station it arrives at, the time it took to reach that station

        """

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
        """Calculates the position this Autobuz is meant to be at at time_actual

        Args:
           time_begin (int): Time in minutes that Autobuz starts moving
           time_actual (int): Time in minutes that Autobuz stops moving
           oameni (list of Om): A list of all people used to update the metOm field of object

        Returns:
            A string with the station name, the index the station is at in destinations, whether the object is moving forward or not, the updated field metOm

        """
        time_decal = time_actual - time_begin

        temp_oameni_loc = {}
        for o in oameni:
            temp_oameni_loc[o.current_loc] = o
        temp_copy = deepcopy(self)

        while time_decal >= 0:
            station, time = temp_copy.getNextDest()
            if time_decal - time > 0:
                temp_copy.unmeetLoc(station)
                if station in temp_oameni_loc.keys():
                    temp_copy.metOm.append((temp_oameni_loc[station], station))
            time_decal -= time
        if temp_copy.direction_forward and temp_copy.current_loc == 0:
            return (temp_copy.destinations[0], 
                    0,
                    not temp_copy.direction_forward, 
                    temp_copy.metOm)
        elif temp_copy.direction_forward and temp_copy.current_loc != 0:
            return (temp_copy.destinations[temp_copy.current_loc-1], 
                    temp_copy.current_loc-1, 
                    temp_copy.direction_forward, 
                    temp_copy.metOm)
        elif not temp_copy.direction_forward and temp_copy.current_loc == len(temp_copy.destinations)-1:
            return (temp_copy.destinations[len(temp_copy.destinations)-1],
                    len(temp_copy.destinations)-1,
                    not temp_copy.direction_forward,
                    temp_copy.metOm)
        elif not temp_copy.direction_forward and temp_copy.current_loc != len(temp_copy.destinations)-1:
            return (temp_copy.destinations[temp_copy.current_loc+1], 
                    temp_copy.current_loc+1, 
                    temp_copy.direction_forward, 
                    temp_copy.metOm)

class Om:
    """Models a person that cantravel by bus and wishes to arrive at a list of stations in a specific order

    """
    def __init__(self, name, money, destinations):
        """__init__

        Args:
          name (str): Name of the person.
          money (float): Current budget of the person.
          destinations (list of str): A list of the stations at which this person whises to arrive at (in order).
          remaining_dest (list of str): A list of the remaining stations at which this person wishes to arrive at (in order).
          current_loc (str): The current location of the person.
          state (str): Either "waiting" or "travelling".
          autobuz (int): Id of Autobuz that person is currently passanger of.
          last_action (Event): Describes the last action this person took (either boarded or unboarded a bus). 

        """
        self.name = name
        self.money = money
        self.destinations = destinations
        if len(destinations) > 1:
            self.remaining_dest = destinations[1:]
        else:
            self.remaining_dest = []
        self.current_loc = destinations[0] 
        self.state = "waiting" #can be "waiting" or "travelling"
        self.autobuz = None #Autobuz id
        self.last_action = None

    def hasVisitedNext(self):
        """Updates the remaining stations as having visited the next one on the list.

        """
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
    """Describes the changing of state of one Om

    """
    def __init__(self, tip, autobuz, om, time):
        """__init__

        Args:
          tip (str): Either "boarding" or "unboarding".
          autobuz (Autobuz): Autobuz that was involved in the changing of state of Om.
          om (Om): The Om that changed states.
          time (int): Time in minutes when even occured.
        """
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
    """Holds the information for a "state" of the problem. 
    
        Note:
            Field of NodParcurgere
    """
    def __init__(self, oameni, autobuze, time, event=None):
        """__init__

        Args:
           oameni (list of Om): List of all people that haven't finished visiting their desired locations.
           autobuze (list of Autobuze): List of all buses. Used in simulating movement between problem "states".
           time (int): Time in minutes of the current "state" of the problem.
           event (Event): The event that led to this "state" of the problem. 

        """
        self.oameni = oameni
        self.time = time
        self.autobuze = autobuze 
        self.event = event

    def __str__(self):
        str_oameni = [str(o) for o in self.oameni]
        str_auto = [str(a) for a in self.autobuze]
        return (f"Time: {self.time}\n"
                f"Oameni:\n{str_oameni}\n"
                f"Autobuze:\n{str_auto}\n"
                f"Event:\n{self.event}\n")
    
    def getOmIndex(self, name):
        """Provides ease of access

        Args:
           name (str): Name of Om.
        
        Returns:
            The index of Om with the provided name, otherwise None.

        """
        for i in range(len(self.oameni)):
            if self.oameni[i].name == name:
                return i
        return None

    def sort_auto(self):
        """Sorts field autobuze by trip_duration from least to greatest.

        """
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
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l
	
    def getInfoDrum(self, l):
        """Updates list oameni with the appropriate value for fields timp_asteptat, timp_mers and traseu

        Args:
           l (list of NodParcurgere): A chain that reached the end-state.
        
        Returns:
            The same list of Nodparcurgere with appropriate fields updated.

        """
        for i in range(0, len(l)):
            for j in range(len(l[i].info.oameni)):
                l[i].info.oameni[j].timp_asteptat = 0
                l[i].info.oameni[j].timp_mers = 0
                l[i].info.oameni[j].traseu = None
                
        for i in range(1, len(l)):
            for j in range(len(l[i].info.oameni)):
                index_prev = l[i-1].info.getOmIndex(l[i].info.oameni[j].name)
                if l[i].info.oameni[j].state != l[i-1].info.oameni[index_prev].state:
                    if l[i-1].info.oameni[index_prev].state == "waiting" and l[i].info.oameni[j].state == "travelling":
                        l[i].info.oameni[j].timp_asteptat = l[i-1].info.oameni[index_prev].timp_asteptat + l[i].info.time - l[i-1].info.time
                        l[i].info.oameni[j].timp_mers = l[i-1].info.oameni[index_prev].timp_mers
                    elif  l[i-1].info.oameni[index_prev].state == "travelling" and l[i].info.oameni[j].state == "waiting":
                        l[i].info.oameni[j].timp_mers = l[i-1].info.oameni[index_prev].timp_mers + l[i].info.time - l[i-1].info.time
                        l[i].info.oameni[j].timp_asteptat = l[i-1].info.oameni[index_prev].timp_asteptat
                else:
                    if l[i].info.oameni[j].state == "travelling":
                        l[i].info.oameni[j].timp_mers = l[i-1].info.oameni[index_prev].timp_mers + l[i].info.time - l[i-1].info.time
                        l[i].info.oameni[j].timp_asteptat = l[i-1].info.oameni[index_prev].timp_asteptat
                    elif l[i].info.oameni[j].state == "waiting":
                        l[i].info.oameni[j].timp_asteptat = l[i-1].info.oameni[index_prev].timp_asteptat + l[i].info.time - l[i-1].info.time
                        l[i].info.oameni[j].timp_mers = l[i-1].info.oameni[index_prev].timp_mers

        for i in range(1, len(l)):
            if l[i].info.event.tip == "boarding":
                temp_traseu = [l[i].info.event.om.current_loc]
                j = i
                while j < len(l) and (l[j].info.event.tip != "unboarding" or l[j].info.event.om.name != l[i].info.event.om.name):
                    j += 1
                if j >= len(l):
                    return None
                unboarding_loc = l[j].info.event.om.current_loc
                direction = l[i].info.event.autobuz.direction_forward
                index_boarding = l[i].info.event.autobuz.getIndexLoc(temp_traseu[0])
                index_unboarding = l[i].info.event.autobuz.getIndexLoc(unboarding_loc)
                if direction:
                    for x in range(index_boarding+1, index_unboarding+1):
                        temp_traseu.append(l[i].info.event.autobuz.destinations[x])
                else:
                    for x in range(index_boarding-1, index_unboarding-1, -1):
                        temp_traseu.append(l[i].info.event.autobuz.destinations[x])
                l[i].info.oameni[l[i].info.getOmIndex(l[i].info.event.om.name)].traseu = temp_traseu
                for x in range(i, j):
                    index = l[x].info.getOmIndex(l[i].info.event.om.name)
                    assert index != None
                    l[x].info.oameni[index].traseu = temp_traseu

        return l


    def afisDrum(self): 
        rez = ""
        l = self.obtineDrum()
        if len(l) == 1:
            rez += f"Starea initiala este si finala\n"
            return 1, rez + str(self)
        l = self.getInfoDrum(l)
        
        for i in range(1, len(l)):
            # print(f"{i})\n{minutesToTime(l[i].info.time)}")
            rez += f"{i})\n{minutesToTime(l[i].info.time)}\n"
            a_terminat = True
            for j in range(len(l[i].info.oameni)):
                if l[i].info.oameni[j].name == l[i].info.event.om.name:
                    a_terminat = False    
            if a_terminat:
                om = l[i-1].info.oameni[l[i-1].info.getOmIndex(l[i].info.event.om.name)]
                # print(f"Omul {om.name} a coborat in statia {om.traseu[-1]} din autobuzul {l[i].info.event.autobuz.id} si si-a terminat traseul. Buget: {om.money}lei. Timp mers: {om.timp_mers + l[i].info.time - l[i-1].info.time}. Timp asteptare: {om.timp_asteptat}.")
                rez += f"Omul {om.name} a coborat in statia {om.traseu[-1]} din autobuzul {l[i].info.event.autobuz.id} si si-a terminat traseul. Buget: {om.money}lei. Timp mers: {om.timp_mers + l[i].info.time - l[i-1].info.time}. Timp asteptare: {om.timp_asteptat}.\n"
            for j in range(len(l[i].info.oameni)):
                index_prev = l[i-1].info.getOmIndex(l[i].info.oameni[j].name)
                if l[i].info.oameni[j].state != l[i-1].info.oameni[index_prev].state:
                    if l[i-1].info.oameni[index_prev].state == "waiting" and l[i].info.oameni[j].state == "travelling":
                        traseu_str = "->".join(l[i].info.oameni[j].traseu)
                        # print(f"Omul {l[i].info.oameni[j].name} a urcat in statia {l[i].info.oameni[j].current_loc} in autobuzul {l[i].info.oameni[j].autobuz} pentru traseul {traseu_str}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.")
                        rez += f"Omul {l[i].info.oameni[j].name} a urcat in statia {l[i].info.oameni[j].current_loc} in autobuzul {l[i].info.oameni[j].autobuz} pentru traseul {traseu_str}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.\n"
                    elif  l[i-1].info.oameni[index_prev].state == "travelling" and l[i].info.oameni[j].state == "waiting":
                        # print(f"Omul {l[i].info.oameni[j].name} a coborat in statia {l[i].info.oameni[j].current_loc} din autobuzul {l[i].info.event.autobuz.id}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.")
                        rez += f"Omul {l[i].info.oameni[j].name} a coborat in statia {l[i].info.oameni[j].current_loc} din autobuzul {l[i].info.event.autobuz.id}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.\n"
                else:
                    if l[i].info.oameni[j].state == "travelling":
                        traseu_str = "->".join(l[i].info.oameni[j].traseu)
                        # print(f"Omul {l[i].info.oameni[j].name} se deplasează cu autobuzul {l[i].info.oameni[j].autobuz} de la statia {l[i-1].info.oameni[index_prev].current_loc} la statia {l[i].info.oameni[j].traseu[-1]} pe traseul {traseu_str}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.")
                        rez += f"Omul {l[i].info.oameni[j].name} se deplasează cu autobuzul {l[i].info.oameni[j].autobuz} de la statia {l[i-1].info.oameni[index_prev].current_loc} la statia {l[i].info.oameni[j].traseu[-1]} pe traseul {traseu_str}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.\n"
                    elif l[i].info.oameni[j].state == "waiting":
                        # print(f"Omul {l[i].info.oameni[j].name} așteaptă în stația {l[i].info.oameni[j].current_loc}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.")
                        rez += f"Omul {l[i].info.oameni[j].name} așteaptă în stația {l[i].info.oameni[j].current_loc}. Buget: {l[i].info.oameni[j].money}lei. Timp mers: {l[i].info.oameni[j].timp_mers}. Timp asteptare: {l[i].info.oameni[j].timp_asteptat}.\n"
            # print("Cost pana acum: ", l[i].g)
            rez += f"Cost pana acum {l[i].g}\n"
        return len(l), rez

    def contineInDrum(self, NodNou):
        nodDrum = self
        while nodDrum is not None:
            if(NodNou.info == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte
		
        return False
		
    def noSol(self):  
        """Checks if there are no further chains that could reach an end-state.
        
        Note:
            Checks if there is Om that can no longer move and stil has remaining stations unvisited.
            Checks if there are multiple people in the same place.


        Returns:
            True if there may be a future cahin to reach an end-state, False otherwise

        """
        noSol = False 

        cost_min_bilet = 100000

        for a in self.info.autobuze:
            if a.price < cost_min_bilet:
                cost_min_bilet = a.price

        for o in self.info.oameni:
            if o.money < cost_min_bilet and o.remaining_dest != []: 
                noSol = True
                break
        
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

    def testeaza_scop(self, nodInfo): 
        isScop = True
        if nodInfo.oameni == []:
            return isScop
        for o in nodInfo.oameni:
            if o.remaining_dest != []:
                isScop = False
                break
        return isScop

    def nuAreSolutii(self, nod): 
        return nod.noSol()       

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"): 
        listaSuccesori=[]                                                           
                                                                                
        if self.nuAreSolutii(nodCurent) or self.testeaza_scop(nodCurent.info):
            return listaSuccesori

        tempNod = deepcopy(nodCurent)

        timpCurent = tempNod.info.time
        autobuzeCurent = tempNod.info.autobuze
        oameniCurent = tempNod.info.oameni
        lista_events = []
        
        while(timpCurent < self.time_end): 
            if self.nuAreSolutii(tempNod):
                # print("\nOprit din generat pentru ca nu mai am solutii\n")
                break

            for i in range(len(autobuzeCurent)):

                if timpCurent != nodCurent.info.time:
                    if ((timpCurent - self.start.info.time) / autobuzeCurent[i].trip_duration).is_integer(): #if current time decal from beginning time divides evenly into trip_duration of Autobuz that means it has reached its next dest
                        posEvent = autobuzeCurent[i].getNextDest() #possible event triggered when Autobuz reaches next station
                    else:
                        continue

                    temp_loc = posEvent[0]
                else: 
                    temp_loc = autobuzeCurent[i].destinations[autobuzeCurent[i].current_loc]
                
                posOm = None 
                for j in range(len(oameniCurent)):
                    if oameniCurent[j].autobuz == None and oameniCurent[j].current_loc == temp_loc:
                        posOm = j
                        break
                if posOm == None: 
                    autobuzeCurent[i].unmeetLoc(temp_loc)
                
                # if posOm != None:
                    # print(f"La timpul {timpCurent}, ma uit daca am event pt autobuzul {autobuzeCurent[i].id}, cu omul {oameniCurent[posOm].name}")

                #IF there is an Om in station and Autobuz arrives but already has Om inside
                if posOm != None and oameniCurent[posOm] != None and autobuzeCurent[i].om != None: 
                    if autobuzeCurent[i].goingToBreak():
                        # print(f"{ oameniCurent[posOm].name} was met before break and {autobuzeCurent[i].om.name} is inside bus, there are no more successors")
                        timpCurent = self.time_end+1
                        break
                    
                    autobuzeCurent[i].metOm.append((oameniCurent[posOm], temp_loc)) 
                    continue 

                #IF there is an Om at station and Autobuz is empty (generate successor where Om boards)
                elif posOm != None and oameniCurent[posOm] != None: 
                    
                    
                    if autobuzeCurent[i].goingToBreak():
                        # print(f"{oameniCurent[posOm].name} did not board because he was met at the last station")
                        continue

                    # print(f"{oameniCurent[posOm].name} was met", end="")
                    if autobuzeCurent[i].hasMet(oameniCurent[posOm]): #if person chose not to board the first time, we ignore
                        # print(f" and didnt board")
                        continue
                    # print(f" and boarded bus {autobuzeCurent[i].id}")

                    go_back_to = deepcopy(oameniCurent[posOm])
                    oameniCurent[posOm].autobuz = autobuzeCurent[i].id
                    oameniCurent[posOm].state = "travelling"
                    oameniCurent[posOm].money -= autobuzeCurent[i].price
                    autobuzeCurent[i].om = deepcopy(oameniCurent[posOm]) 

                    new_event = Event("boarding", deepcopy(autobuzeCurent[i]), deepcopy(oameniCurent[posOm]), timpCurent)
                    lista_events.append(new_event)
                    # print(new_event)
                    
                    #for future events, we consider that this Om did not board the Autobuz
                    autobuzeCurent[i].metOm.append((oameniCurent[posOm], temp_loc)) 
                    oameniCurent[posOm] = go_back_to
                    autobuzeCurent[i].om = None

                #IF station is empty and Autobuz has Om inside (generate successor where Om unboards)
                elif posOm == None and autobuzeCurent[i].om != None: 

                    temp_om = autobuzeCurent[i].om.name
                    for j in range(len(oameniCurent)):
                       if temp_om == oameniCurent[j].name:
                           temp_om = j
                           break 

                    oameniCurent[temp_om].current_loc = autobuzeCurent[i].om.current_loc 

                    go_back_to = deepcopy(oameniCurent[temp_om])
                    oameniCurent[temp_om].autobuz = None
                    oameniCurent[temp_om].state = "waiting"


                    if oameniCurent[temp_om].remaining_dest != [] and oameniCurent[temp_om].remaining_dest[0] == temp_loc:
                        oameniCurent[temp_om].hasVisitedNext()
                    autobuzeCurent[i].om = None

                    new_event = Event("unboarding", deepcopy(autobuzeCurent[i]), deepcopy(oameniCurent[temp_om]), timpCurent)
                    lista_events.append(new_event)
                    # print(new_event)

                    #for future events, we consider that this Om stayed in Autobuz 
                    oameniCurent[temp_om] = go_back_to
                    autobuzeCurent[i].om = oameniCurent[temp_om]
                    oameniCurent[temp_om].state = "travelling"

                    #if Autobuz is also going to break, forcefully terminate method (since there is no other action that could be taken)
                    if autobuzeCurent[i].goingToBreak():
                        # print(f"{autobuzeCurent[i].om.name} got off at last possible station, no further successors exist for this node")
                        timpCurent = self.time_end+1
                        break

            timpCurent += autobuzeCurent[0].trip_duration 

        for i in range(len(lista_events)):
            #print(lista_events[i])

            if (lista_events[i].om.last_action != None and
                lista_events[i].tip != lista_events[i].om.last_action[0] and
                lista_events[i].autobuz.id == lista_events[i].om.last_action[1] and
                lista_events[i].om.current_loc == lista_events[i].om.last_action[2] and
                lista_events[i].time == lista_events[i].om.last_action[3]):
                continue #prevent Om from unboarding/boarding right after boarding/unboarding from the SAME Autobuz at the SAME timestamp

            autobuze_new = deepcopy(nodCurent.info.autobuze)
            oameni_new = deepcopy(nodCurent.info.oameni)
            for j in range(len(autobuze_new)):
                if autobuze_new[j].id == lista_events[i].autobuz.id:
                    autobuze_new[j] = lista_events[i].autobuz
                else:
                    (x, 
                    autobuze_new[j].current_loc, 
                    autobuze_new[j].direction_forward,
                    autobuze_new[j].metOm) = autobuze_new[j].getCurrentDest(nodCurent.info.time, lista_events[i].time, oameni_new) #self.start.info.time
                    if autobuze_new[j].om != None:
                        autobuze_new[j].om.current_loc = autobuze_new[j].destinations[autobuze_new[j].current_loc]

            for j in range(len(oameni_new)):
                if oameni_new[j].name == lista_events[i].om.name:
                    oameni_new[j] = lista_events[i].om
                    oameni_new[j].last_action = [lista_events[i].tip, lista_events[i].autobuz.id, deepcopy(oameni_new[j].current_loc), lista_events[i].time]
                else:
                    for k in range(len(autobuze_new)):
                        if autobuze_new[k].om != None and autobuze_new[k].om.name == oameni_new[j].name:
                            oameni_new[j].current_loc = autobuze_new[k].om.current_loc
            for o in oameni_new:
                if o.remaining_dest == []:
                    oameni_new.remove(o)
            

            info_new = NodInfo(oameni_new, autobuze_new, lista_events[i].time, deepcopy(lista_events[i]))
            cost_new = nodCurent.g
            if lista_events[i].tip == "boarding":
                cost_new += lista_events[i].autobuz.price 
            cost_new += lista_events[i].time - nodCurent.info.time 
            nod_new = NodParcurgere(info_new, nodCurent, cost_new, self.calculeaza_h(info_new))
            if not nodCurent.contineInDrum(nod_new):
                listaSuccesori.append(nod_new)
                # print(f"\n\nAm generat si adaugat in lista de succesori urmatorul nod: {listaSuccesori[-1]}\n\n")
            else:
                pass
                # print("Am generat un succesor care e deja in drumul parintelui")

        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if self.testeaza_scop(infoNod):
                return 0
            return 1
        elif tip_euristica == "euristica admisibila 1":
            h=0
            cost_min_bilet = 100000
            for a in infoNod.autobuze:
                if cost_min_bilet > a.price:
                    cost_min_bilet = a.price
            for o in infoNod.oameni:
                h += len(o.remaining_destinations)*cost_min_bilet
            return h
        elif tip_euristica == "euristica admisibila 2": 
            h=0
            max_destinations = 0
            for o in infoNod.oameni:   
                if len(o.remaining_dest) > max_destinations:
                    max_destinations = len(o.remaining_dest)
            shortest_trip_duration = self.time_end+1
            for a in infoNod.autobuze:
                if shortest_trip_duration > a.trip_duration:
                    shortest_trip_duration = a.trip_duration
            h = max_destinations*shortest_trip_duration
            return h
        elif tip_euristica == "euristica neadmisibila": 
            h=0
            cost_max_bilet = -1
            for a in infoNod.autobuze:
                if cost_max_bilet < a.price:
                    cost_max_bilet = a.price
            for o in infoNod.oameni:
                h += len(o.remaining_destinations)*cost_max_bilet
            return h

    def __repr__(self):
        sir=""
        for (k,v) in self.__dict__.items():
            sir+="{} = {}\n".format(k,v)
        return(sir)

def init():
    """Reads arguments provided through command-line

        Returns:
            Name of input directory, name of output directory, number of end-state chains to be printed, timeout

    """
    if len(sys.argv) != 5:
        print("Invalid number of arguments, exiting...")
        sys.exit(0) 
    else:
        try:
            dir_in = sys.argv[1]
            dir_out = sys.argv[2]
            nsol = int(sys.argv[3])
            timeout = int(sys.argv[4])
        except Exception as eroare:
            print("Provided arguments are of wrong type, exiting...")
            sys.exit(0)
    return dir_in, dir_out, nsol, timeout

def make_files(dir_in, dir_out):
    """Reads arguments provided through command-line

        Args:
            dir_in (str): Name of input directory
            dir_out (str): Name of output directory

        Returns:
            List of input files' paths, list of output files' paths

    """
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
    """Strips a string of quotation marks.

        Args:
            string (str): String to be stripped.

        Returns:
            The string without quotation marks.
    """
    if "\"" not in string:
        return string
    index1 = 0
    index2 = -1
    while string[index1] != "\"":
        index1 += 1
    while string[index2] != "\"":
        index2 -= 1
    return string[index1+1:index2]

def get_multiple_dest(list_of_str):
    """Maps get_dest to a list of strings.

        Args:
            list_of_str (list of str): List of strings to be stripped of quotation marks.
        Returns:
            List of strings stripped of quotation marks.

    """
    new_list = []
    for x in list_of_str:
        new_list.append(get_dest(x))
    return new_list

def read_one(paths_in, paths_out, current_fis=0):
    """Reads the input of one file from input directory.

        Args:
            paths_in (list of str): List of paths for input files.
            paths_out (list of str): List of paths for output files.
            current_fis (int): Index of input file to be read.
        
        Returns:
            String with beginning timestamp, string with end timestamp, list of Autobuz, list of Om
            
    """

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

    return time_begin, time_end, autobuze, oameni

def write_one(paths_out, solutii, current_fis, note=""):
    """Writes results of one algortihm using one euristic to one of the output files.

    Args:
        paths_out (list of str): List of paths for output files.
        solutii (list of str): List of results found.
        current_fis (int): Index of output file to be written to.
  
    """
    f = open(f"{paths_out[current_fis]}", "a")
    f.write(note)
    for s in solutii:
        f.write(s)

def timeToMinutes(timestamp):
    """Converts a string timestamp into an int number of minutes.

        Args:
            timestamp (str): Timestamp to be converted into minutes
        
        Returns:
            Number of minutes equivalent to the timestamp
            
    """
    if len(timestamp) == 5: 
        return int(timestamp[0])*600 + int(timestamp[1])*60 + int(timestamp[3])*10 + int(timestamp[4])
    return None

def minutesToTime(minutes):
    """Converts an int number of minutes into a string timestamp.

        Args:
            minutes (int): Number of minutes to be converted into timestamp.
        
        Returns:
            Timestamp equivalent of the number of minutes
            
    """
    h10, h1, m10, m1 = 0, 0, 0, 0
    h10 = int(minutes/600)
    h1 = int(minutes%600 / 60)
    m10 = int((minutes - (h10*600 + h1*60)) / 10)
    m1 = int((minutes - (h10*600 + h1*60)) % 10)
    return f"{h10}{h1}:{m10}{m1}"

def uniform_cost(gr, nrSolutiiCautate, tip_euristica):

    c=[NodParcurgere(gr.start.info, None, 0, gr.calculeaza_h(gr.start.info))]
    solutii = []
    max_noduri = 1
    total_noduri = 1
    initial_time = time()

    while len(c)>0:
        nodCurent=c.pop(0)
        
        if gr.testeaza_scop(nodCurent.info):
            sol = "Solutie: \n"
            x, y = nodCurent.afisDrum()
            sol += y + "\n"
            sol += f"Lungimea drumului este: {str(x-1)}\n"
            sol += f"Costul drumului este: {nodCurent.g}\n"
            sol += f"Numarul maxim de noduri in memorie: {max_noduri}\n"
            sol += f"Numarul total de noduri calculate este: {total_noduri}\n"
            sol += f"Solutia a fost gasita in {time()-initial_time}\n----------------\n"
            solutii.append(sol)
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return solutii
        lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)	
        total_noduri += len(lSuccesori)	
        if max_noduri < len(lSuccesori):
            max_noduri = len(lSuccesori)
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(c)):
                if c[i].g>s.g :
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)
    return solutii

def a_star(gr, nrSolutiiCautate, tip_euristica): 
    c=[NodParcurgere(gr.start.info, None, 0, gr.calculeaza_h(gr.start.info))]

    solutii = []
    max_noduri = 1
    total_noduri = 1
    initial_time = time()

    while len(c) > 0:
        nodCurent = c.pop(0)
        
        if gr.testeaza_scop(nodCurent.info):
            sol = "Solutie: \n"
            x, y = nodCurent.afisDrum()
            sol += y + "\n"
            sol += f"Lungimea drumului este: {str(x-1)}\n"
            sol += f"Costul drumului este: {nodCurent.g}\n"
            sol += f"Numarul maxim de noduri in memorie: {max_noduri}\n"
            sol += f"Numarul total de noduri calculate este: {total_noduri}\n"
            sol += f"Solutia a fost gasita in {time()-initial_time}\n----------------\n"
            solutii.append(sol)
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return solutii
        lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        total_noduri += len(lSuccesori)	
        if max_noduri < len(lSuccesori):
            max_noduri = len(lSuccesori)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f >= s.f :
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)
    return solutii

def a_star_optimizat(gr, tip_euristica):
    l_open=[NodParcurgere(gr.start.info, None, 0, gr.calculeaza_h(gr.start.info))]

    solutii = []
    max_noduri = 1
    total_noduri = 1
    initial_time = time()

    l_closed=[]
    while len(l_open)>0:
        nodCurent=l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent.info):
            sol = "Solutie: \n"
            x, y = nodCurent.afisDrum()
            sol += y + "\n"
            sol += f"Lungimea drumului este: {str(x-1)}\n"
            sol += f"Costul drumului este: {nodCurent.g}\n"
            sol += f"Numarul maxim de noduri in memorie: {max_noduri}\n"
            sol += f"Numarul total de noduri calculate este: {total_noduri}\n"
            sol += f"Solutia a fost gasita in {time()-initial_time}\n----------------\n"
            solutii.append(sol)
            return solutii
        lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)	
        total_noduri += len(lSuccesori)	
        if max_noduri < len(lSuccesori):
            max_noduri = len(lSuccesori)
        for s in lSuccesori:
            gasitC=False
            for nodC in l_open:
                if s.info==nodC.info:
                    gasitC=True
                    if s.f>=nodC.f:
                        lSuccesori.remove(s)
                    else:
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info==nodC.info:
                        if s.f>=nodC.f:
                            lSuccesori.remove(s)
                        else:
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(l_open)):
                if l_open[i].f>s.f or (l_open[i].f==s.f and l_open[i].g<=s.g) :
                    gasit_loc=True
                    break
            if gasit_loc:
                l_open.insert(i,s)
            else:
                l_open.append(s)
    return solutii

def ida_star(gr, nrSolutiiCautate, tip_euristica):

    nodStart=NodParcurgere(gr.start.info, None, 0, gr.calculeaza_h(gr.start.info)) #TODO: add tip_euristica as param here and everywhere else this is called
    solutii = []
    max_noduri = 1
    total_noduri = 1
    initial_time = time()
    limita=nodStart.f
    while True:
        nrSolutiiCautate, rez, solutii = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, tip_euristica, solutii, max_noduri, total_noduri, initial_time)
        if rez=="gata":
            break
        if rez==float('inf'):
            break
        limita=rez
    return solutii

def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica, solutii, max_noduri, total_noduri, initial_time):
    if nodCurent.f>limita:
        return nrSolutiiCautate, nodCurent.f, solutii
    if gr.testeaza_scop(nodCurent.info) and nodCurent.f==limita :
        sol = "Solutie: \n"
        x, y = nodCurent.afisDrum()
        sol += y + "\n"
        sol += f"Lungimea drumului este: {str(x-1)}\n"
        sol += f"Costul drumului este: {nodCurent.g}\n"
        sol += f"Numarul maxim de noduri in memorie: {max_noduri}\n"
        sol += f"Numarul total de noduri calculate este: {total_noduri}\n"
        sol += f"Solutia a fost gasita in {time()-initial_time}\n----------------\n"
        solutii.append(sol)
        nrSolutiiCautate-=1
        if nrSolutiiCautate==0:
            return 0, "gata", solutii
    lSuccesori=gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)	
    total_noduri += len(lSuccesori)	
    if max_noduri < len(lSuccesori):
        max_noduri = len(lSuccesori)
    minim=float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez, solutii = construieste_drum(gr, s, limita, nrSolutiiCautate, tip_euristica, solutii, max_noduri, total_noduri, initial_time)
        if rez=="gata":
            return 0, "gata", solutii
        if rez<minim:
            minim=rez
    return nrSolutiiCautate, minim, solutii

def main():
    dir_in, dir_out, nrsol, timeout = init()
    paths_in, paths_out = make_files(dir_in, dir_out)
    for i in range(len(paths_in)):
        # print("-"*20 + f"pt input nr {i+1}" + "-"*20)

        time_begin, time_end, autobuze, oameni = read_one(paths_in, paths_out, i)

        time_begin = timeToMinutes(time_begin)
        time_end = timeToMinutes(time_end)

        info = NodInfo(oameni, autobuze, time_begin)
        nod_start =  NodParcurgere(info, None, 0, 0)
        graf = Graph(time_end, nod_start)

        if graf.nuAreSolutii(nod_start):
            print("Starea de inceput nu permite solutii")
            sys.exit(0)

        list_algo = [uniform_cost, a_star, a_star_optimizat, ida_star]
        list_euristici = ["euristica banala", "euristica admisibila 1", "euristica admisibila 2", "euristica neadmisibila"]
        sep = "*"*37 + "\n\n\n"
        for algo in list_algo:
            if algo != a_star_optimizat:
                for eu in list_euristici:
                    try:
                        solutii = func_timeout(timeout, algo, args=(graf, nrsol, eu))
                        write_one(paths_out, solutii, i, f"Solutii pentru {algo.__name__}, cu {eu}\n" + sep)
                    except FunctionTimedOut:
                        write_one(paths_out, [], i, note=f"Algoritmul {algo.__name__}, cu {eu} a fost timed out\n" + sep)
            else:
                for eu in list_euristici:
                    try:
                        solutii = func_timeout(timeout, algo, args=(graf, eu))
                        write_one(paths_out, solutii, i, f"Solutie pentru {algo.__name__}, cu {eu}\n" + sep)
                    except FunctionTimedOut:
                        write_one(paths_out, [], i, note=f"Algoritmul {algo.__name__}, cu {eu} a fost timed out\n" + sep)

if __name__ == '__main__':
    main()
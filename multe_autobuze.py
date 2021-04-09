import sys
import os
from copy import deepcopy
   
class Autobuz:
    def __init__(self, id, price, break_duration, trip_duration, destinations):
        self.id = id
        self.price = price
        self.break_duration = break_duration
        self.trip_duration = trip_duration
        self.destinations = destinations
        self.current_loc = None
    
    def __str__(self):
        return (f"id={self.id}\n"
                f"price={self.price}\n"
                f"break_duration={self.break_duration}\n"
                f"trip_duration={self.trip_duration}\n"
                f"first_dest={self.destinations[0]}\n")
    
class Om:
    def __init__(self, name, money, destinations):
        self.name = name
        self.money = money
        self.destinations = destinations
        self.remaining_dest = destinations[1:]
        self.remaining_money = money
        self.current_loc = destinations[0]

    def __str__(self):
        return (f"name={self.name}\n"
                f"money={self.money}\n"
                f"current_loc={self.current_loc}\n"
                f"first_dest={self.destinations[0]}\n")

    def isDone(self):
        if self.remaining_dest == []:
            return True
        return False

class Nod:
    def __init__(self, autobuze, oameni, time):
        self.autobuze = autobuze
        self.oameni = oameni
        self.time = time

    def __str__(self):
        str_auto = [str(a) for a in autobuze]
        str_oameni = [str(o) for o in oameni]
        return (f"Time: {self.time}\n"
                f"Autobuze:\n{str_auto}\n"
                f"Oameni:\n{str_oameni}\n")
    
    def noSol(self): #TODO: decide if applicable to task
        return False

def init():
    if len(sys.argv) != 5:
        print("Invalid number of arguments, exiting...")
        quit() 
    else:
        try:
            dir_in = sys.argv[1]
            dir_out = sys.argv[2]
            nsol = int(sys.argv[3])
            timeout = sys.argv[4]
        except Exception as eroare:
            print("Provided arguments are of wrong type, exiting...")
            quit()
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


def noSol(nod): #TODO: decide if applicable to task
    pass
    



def main():
    dir_in, dir_out, nsol, timeout = init()
    paths_in, paths_out = make_files(dir_in, dir_out)
    for i in range(len(paths_in)):
        time_begin, time_end, autobuze, oameni, nr_oameni = read_one(paths_in, paths_out, i)
         
        if noSol(nod_start):
            print("Starea de inceput nu permite solutii")
            quit()
        



if __name__ == '__main__':
    main()
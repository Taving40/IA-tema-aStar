import sys
import os
   
def read():
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
    return listaFisiere, paths_out


def main():
    dir_in, dir_out, nsol, timeout = read()
    paths_in, paths_out = make_files(dir_in, dir_out)



if __name__ == '__main__':
    main()
# Tema 1 - cautare informata - Comparație între tehnicile de căutare



# Cerinta - Multe autobuze

## Context.

Avem un oraș în care circulă niște autobuze. Pentru fiecare autobuz cunoastem numărul traseul, prețul, intervalul de timp la care pleacă din garaj căte un nou autobuz pe traseu, timpul de deplasare între stații succesive (fiecare autobuz are o viteză proprie; drumul între două stații consecutive durează mereu la fel). De exemplu, autobuzul 100 pleacă la fiecare 15 minute și timpul de parcurgere a segmentului între oricare 2 stații consecutive este de 4 minute. Pe de altă parte, 200 pleacă la fiecare 12 minute și parcurge drumul între oricare 2 stații consecutive pe traseul său în 7 minute.

Autobuzele merg în 2 sensuri, deci lista de stații(traseul) va fi parcursă și în sens opus, autobuzele plecând din garajele din capete.

N oameni certați între ei care nu vor să se mai vadă niciodată, au toți de parcurs în ziua curentă un drum. Drumul unui om e dat ca listă de stații. Prima stație e cea din care începe drumul. Drumul omului se termină cu ultima locație pe care o are de vizitat după care omul dispare de pe hartă (nu îl mai luăm în considerare). Locațiile trebuie vizitate exact în ordinea din listă.O locație, pentru a fi considerată vizitată, trebuie să îndeplinească condițiile: să fie prima nevizitată din lista omului și omul obligatoriu să coboare din autobuz acolo. Dacă un om are în listă stațiile s1,s2,s3 și trece prin s3 și apoi prin s1, doar s1 se consideră vizitată, nu și s3. Va trebui să treacă prin stația s3 din nou: s3 se va considera vizitată doar daca ajunge în ea după ce a trecut prin s2.

Dacă un om a ajuns într-o stație și coboară din autobuz, poate urca imediat în alt autobuz, dacă următorul autobuz dorit a ajuns și el în același timp în stație. Urcările și coborârile se fac instant (deci nu iau timp).

Soluția va consta în a indica fiecărui om ce autobuze trebuie sa ia și până unde să se ducă cu ele astfel încât să treacă prin toate locațiile dorite și să nu se afle doi oameni în aceeași locație (stație sau autobuz) fiind certați. Pentru a rezolva asta e posibil să fie necesar să deplasăm un om cu o stație mai departe de destinație (iar apoi să se întoarcă în alt autobuz), dacă la destinație se află un alt om dintre cei N. Deci dacă un om a ajuns într-o stație dar nu coboară, nu îl afectează dacă în stația respectivă așteaptă un alt om. Omul, dacă trebuie să ia un autobuz X și așteaptă în stație, obligatoriu se va urca în autobuzul X atunci când autobuzul sosește (nu are voie să lase un autobuz cu numărul X să treacă și apoi să urce în următorul cu numărul X).

Fiecare om are o suma de bani și nu poate cumpăra mai multe bilete decât îi permite bugetul.

## Stări și conexiuni.
Nodurile-stări în graful problemei vor fi momentele de timp când un om își schimbă activitatea (așteaptă/merge cu autobuzul), mutările fiind, deci, aceste schimbări. 


## Costul

Costul va fi suma tuturor timpilor parcurși și a banilor consumați pentru toți cei N oameni (vom considera costul unei mutari ca suma celor două măsuri, deoarece vrem șî timpi cât mai mici dar și cât mai puțini bani consumați. Totuși trebuie să se memoreze separat pentru a fi indicate cu exactitate în afișarea drumului). Din momentul în care un om și-a terminat drumul, nu se mai adună nimic la cost pentru el.


## Fisierul de intrare

   Primul rând va fi ora la care toți oamenii sunt in prima stație din lista lor. Tot la această oră pleacă câte un autobuz din fiecare garaj (un garaj e un capăt de traseu, deci pleacă autobuze în ambele sensuri pe un traseu. Pe același rând va fi și ora la care trebuie să fi terminat toți oamenii traseul (nu avem voie să generăm stări după această oră).
    Următoarele rânduri conțin date pentru fiecare autobuz: numărul autobuzui, prețul biletului, intervalul de timp între două plecări din garaj, timpul între două stații consecutive, traseul indicat printr-un sir de forma statie_1,statie_2, ... statie_n.
    Un rand cu numărul de oameni, apoi fiecare om cu suma de bani pe care o are și traseul pe care îl dorește

## Fișier output.

În fișierul de output se vor afișa drumurile-soluție In cadrul afisarii soutiei, pentru fiecare nod din drum:

   se va arata fiecare moment de timp în care s-a schimbat ceva, începând cu ora de la care pornesc toate deplasările. Schimbările se referă doar la urcatul sau coborâtul din autobuz, nu și faptul că un om a trecut printr-o stație (în care nu a coborât). Momentul de timp este reprezentat prin ora.

   La fiecare pas se va afișa starea fiecarui om (care încă nu și-a terminat drumul) cu următoarele tipuri de mesaje:
        "Omul [nume-om] așteaptă în stația [nume-statie]" "Omul [nume-om] se deplasează cu autobuzul [numar-autobuz] de la statia [nume-statie] la statia [nume-statie] pe traseul [traseu]", unde zonele între parenteze drepte vor fi înlocuite cu informația cerută. Traseul este strict zona pe care o parcurge omul, și are forma "statie_1 -> statie_2 -> .... statie_n", iar stațiile între care se deplasează sunt cele între care se află acum, nu capetele traseului.
        Omul [nume-om] a coborât în stația [nume-stație] din autobuzul [nr]
        Omul [nume-om] a coborât în stația [nume-stație] din autobuzul [nr] și și-a terminat traseul
        Omul [nume-om] a urcat în stația [nume-stație] in autobuzul [nr] pentru traseul [traseu]
        După status se va afișa și bugetul, timpul total de mers cu autobuzul și timpul total de așteptare

   Important! mesajul cu terminarea traseului ar trebui să fie ultimul pentru fiecare om, și acel om nu va mai fi menționat în nodurile următoare.

   Observație: dacă un om coboară dintr-un autobuz, și urcă în același moment de timp în alt autobuz (e posibil când ambele autobuze au ajuns în stație în același timp), se vor afișa atât mesajul de coborâre cât și de urcare.
    Se va afișa și costul de până atunci: suma pentru toți oamenii a banilor consumați și a timpului petrecut p

import random as r

def c_film(film):
    return "_".join("_".join("_".join(film.split(' ')).split(":")).split('-'))

def liste_alea(liste, nbr):
    l = []
    for i in range(nbr):
        number = r.randint(0,len(liste)-1)
        while liste[number] in l:
            number = r.randint(0,len(liste))
        l.append(liste[number])
    return l


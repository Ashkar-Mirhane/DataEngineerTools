import ast
import random as r
import pandas as pd

def dataframe_to_list(df):
    df = df.dropna()
    df = df.drop(columns='Unnamed: 0')
    df_lst = df.values.tolist()
    for i in range(len(df_lst)):
        df_lst[i][8] = ast.literal_eval(df_lst[i][8])
        df_lst[i][4] = ast.literal_eval(df_lst[i][4])
        
        try:
            df_lst[i][2] = ast.literal_eval(df_lst[i][2])
        except:
            df_lst[i][2] = []
        df_lst[i][10] = ast.literal_eval(df_lst[i][10])
        df_lst[i][12] = ast.literal_eval(df_lst[i][12])
        df_lst[i].append("/static/poster/"+c_film(df_lst[i][0])+"_poster")
        
        if df_lst[i][11] == "Reviews":
            df_lst[i][11] = 0
        df_lst[i].append(round((df_lst[i][8]['note_moyenne']+float(".".join(df_lst[i][10][0].split(',')))+int(df_lst[i][11])/10)/3, 1))
        number_star = [list(range(int(df_lst[i][-1])))]
        if df_lst[i][-1] - int(df_lst[i][-1])>= 0.5:
            number_star.append(1)
            number_star.append(list(range(9-int(df_lst[i][-1]))))
        else:
            number_star.append(0)
            number_star.append(list(range(10-int(df_lst[i][-1]))))

        df_lst[i].append(number_star)
        df_lst[i].append(c_film(df_lst[i][0]))
        df_lst[i][7] = ast.literal_eval(df_lst[i][7])
        
    return df_lst



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


def recherche_annee(annee, data):
    l = []
    for i in range(len(data)):
        if data[i][6][-4:] == str(annee):
            l.append(data[i])
    return l

type_film = [{'_id': 'Drame', 'nombre de films': 432},
{'_id': 'Action', 'nombre de films': 242},
 {'_id': 'Comédie', 'nombre de films': 142},
 {'_id': 'Animation', 'nombre de films': 98},
 {'_id': 'Biopic', 'nombre de films': 92},
 {'_id': 'Comédie dramatique', 'nombre de films': 78},
 {'_id': 'Aventure', 'nombre de films': 60},
 {'_id': 'Policier', 'nombre de films': 52},
 {'_id': 'Thriller', 'nombre de films': 50},
 {'_id': 'Documentaire', 'nombre de films': 40},
 {'_id': 'Épouvante-Horreur', 'nombre de films': 38},
 {'_id': 'Science-fiction', 'nombre de films': 18},
 {'_id': 'Fantastique', 'nombre de films': 12},
 {'_id': 'Comédie musicale', 'nombre de films': 10},
 {'_id': 'Western', 'nombre de films': 8},
 {'_id': 'Historique', 'nombre de films': 6},
 {'_id': 'Romance', 'nombre de films': 6},
 {'_id': 'Comédie romantique', 'nombre de films': 4},
 {'_id': 'Gangster', 'nombre de films': 4},
 {'_id': 'Musique', 'nombre de films': 2},
 {'_id': 'Film noir', 'nombre de films': 2},
 {'_id': 'Expérimental', 'nombre de films': 2},
 {'_id': 'Arts martiaux', 'nombre de films': 2}]

def lst_type_film():
    l = []
    for elm in type_film:
        l.append(elm['_id'])
    return l

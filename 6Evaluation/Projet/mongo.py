import fonctions_utiles as f

import pymongo
from pymongo import MongoClient
import pandas as pd
client = MongoClient('localhost', 27017)
database = client['local']
collection = database['projet_DATA_ENGINEERING']

df_films = pd.read_csv('FILMS.csv')


#NETTOYAGE DATAFRAME
def nettoyage_dataframe(dataframe):
    dataframe = dataframe.drop('Unnamed: 0',1)
    dataframe = dataframe.fillna('"Non"')
    b = []
    for i in range(len(dataframe['theme_production'])):
            b.append(eval(dataframe['theme_production'][i]))

    dataframe = dataframe.drop('theme_production',1)
    dataframe.insert(2,'theme_production',b,True)
    b = []
    for i in range(len(dataframe['Realisateur'])):
        b.append(eval(dataframe['Realisateur'][i]))
    dataframe = dataframe.drop('Realisateur',1)
    dataframe.insert(4,'Realisateur',b,True)
    b = []
    for i in range(len(dataframe['acteurs_principaux'])):
        b.append(eval(dataframe['acteurs_principaux'][i]))
    dataframe = dataframe.drop('acteurs_principaux',1)
    dataframe.insert(7,'acteurs_principaux',b,True)
    b = []
    for i in range(len(dataframe['charts'])):
        b.append(eval(dataframe['charts'][i]))
    dataframe = dataframe.drop('charts',1)
    dataframe.insert(8,'charts',b,True)
    b = []
    for i in range(len(dataframe['charts_IMDB'])):
        b.append(eval(dataframe['charts_IMDB'][i]))
    dataframe = dataframe.drop('charts_IMDB',1)
    dataframe.insert(10,'charts_IMDB',b,True)
    b = []
    for i in range(len(dataframe['charts_IMDB'])):
        b.append(eval(dataframe['other_details'][i]))
    dataframe = dataframe.drop('other_details',1)
    dataframe.insert(12,'other_details',b,True)

    b = []
    for i in range(len(dataframe['theme_production'])):
        try:
            b.append(eval(dataframe['theme_production'][i]))
        except TypeError : 
            b.append(dataframe['theme_production'][i])
        except NameError : 
            b.append(dataframe['theme_production'][i])
    for i in range(len(b)):
        if b[i]!='Non':
            b[i] = b[i][0]
    dataframe = dataframe.drop('theme_production',1)
    dataframe.insert(2,'theme_production',b,True)
    b = []
    for i in range(len(dataframe['Realisateur'])):
        try:
            b.append(eval(dataframe['Realisateur'][i]))
        except TypeError : 
            b.append(dataframe['Realisateur'][i])
        except NameError : 
            b.append(dataframe['Realisateur'][i])
    for i in range(len(b)):
        if b[i]!='Non':
            b[i] = b[i][0]
    dataframe = dataframe.drop('Realisateur',1)
    dataframe.insert(4,'Realisateur',b,True)
    b = []
    for i in range(len(dataframe['other_details'])):
        try:
            b.append(eval(dataframe['other_details'][i]))
        except TypeError : 
            b.append(dataframe['other_details'][i])
        except NameError : 
            b.append(dataframe['other_details'][i])
    for i in range(len(b)):
        try:
            b[i]['budget'] = int(b[i]['budget'][1:].replace(',',''))
            b[i]['Cumulative_WW_Gross'] = int(b[i]['Cumulative_WW_Gross'][1:].replace(',',''))
        except ValueError : 
            pass
        except TypeError :
            pass
    dataframe = dataframe.drop('other_details',1)
    dataframe.insert(12,'other_details',b,True)

    dataframe.drop_duplicates(subset ="nom_film", keep = 'first', inplace=True)
    return dataframe

df_films = nettoyage_dataframe(df_films)

df_films['charts_METACRITIC'] = df_films['charts_METACRITIC'].apply(lambda x: 0 if x=='Reviews' else x )
df_films['nom_film_attache'] = df_films['nom_film'].apply(lambda x: f.c_film(x))
df_films['nom_fichier_image'] = df_films['nom_film'].apply(lambda x: "/static/poster/"+f.c_film(x)+"_poster")
df_films['note_moyenne'] = round((df_films['charts'].apply(lambda x: x['note_moyenne']) + df_films['charts_IMDB'].apply(lambda x: float(".".join(x[0].split(',')))) + df_films['charts_METACRITIC'].apply(lambda x: int(x)/10))/3,1)
df_films['etoiles'] = df_films['note_moyenne'].apply(lambda x: [list(range(int(x))), 1, list(range(9-int(x)))] if x - int(x)<=0.5 else [list(range(int(x))), 0, list(range(10-int(x)))])


collection.delete_many({})
DOCUMENTS = df_films.to_dict('records')
collection.insert_many(DOCUMENTS)
varProject = {"_id":0}

def liste_theme():
    l = collection.aggregate([
        {"$group" : {"_id": "$theme_production", "nombre de films" : {"$sum" : 1}}},
        {"$sort" : {"nombre de films": -1}}
        ])

    l = list(l)
    liste_theme = []
    for i in range(len(l)):
        if l[i]['_id'] == 'Non':
            liste_theme.append("Documentaire")
        else:
            liste_theme.append(l[i]['_id'])
    return liste_theme

def liste_realisateur():
    l= ['Alfonso Cuarón', 'Damien Chazelle', 'Pete Docter', 'Claude Barras', 'Lenny Abrahamson', 'Isao Takahata', 'Park Chan-wook', 'Bob Persichetti', 'George Miller', 'Quentin Tarantino']
    return l


def TOP_par_theme(theme):
    varProject = {"_id":0}
    dico ={
        "TOP_Drame" : collection.find({"theme_production":"Drame","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]).limit(50),
        "TOP_Action" : collection.find({"theme_production":"Action","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]).limit(50),
        "TOP_Comédie" : collection.find({"theme_production":"Comédie","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]).limit(50),
        "TOP_Animation" : collection.find({"theme_production":"Animation","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Biopic" : collection.find({"theme_production":"Biopic","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Comédie_dramatique" : collection.find({"theme_production":"Comédie dramatique","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Aventure" : collection.find({"theme_production":"Aventure","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Policier" : collection.find({"theme_production":"Policier","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Thriller" : collection.find({"theme_production":"Thriller","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Documentaire" : collection.find({"theme_production":"Non","charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Épouvante-Horreur" : collection.find({"theme_production":"Épouvante-Horreur","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Science_fiction" : collection.find({"theme_production":"Science-fiction","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Fantastique" : collection.find({"theme_production":"Fantastique","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Western" : collection.find({"theme_production":"Western","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Comédie_musicale" : collection.find({"theme_production":"Comédie musicale","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Romance" : collection.find({"theme_production":"Romance","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Historique" : collection.find({"theme_production":"Historique","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Comédie_romantique" : collection.find({"theme_production":"Comédie romantique","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Gangster" : collection.find({"theme_production":"Gangster","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Expérimental" : collection.find({"theme_production":"Expérimental","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Arts_martiaux" : collection.find({"theme_production":"Arts martiaux","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Musique" : collection.find({"theme_production":"Musique","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]),
        "TOP_Film_noir" : collection.find({"theme_production":"Film noir","charts.nombre_critiques":{"$gte":500}},varProject).sort([("charts.note_moyenne", -1)]) 
    }
    return list(dico['TOP_'+f.c_film(theme)])

def TOP_meilleurs_realisateurs():
    varProject = {"_id":0}
    l = []
    dico ={
        "Alfonso Cuarón" : collection.find({"Realisateur" : 'Alfonso Cuarón'},varProject),
        "Damien Chazelle" : collection.find({"Realisateur" : 'Damien Chazelle'},varProject),
        "Pete Docter" : collection.find({"Realisateur" : 'Pete Docter'},varProject),
        "Claude Barras" : collection.find({"Realisateur" : 'Claude Barras'},varProject),
        "Lenny Abrahamson" : collection.find({"Realisateur" : 'Lenny Abrahamson'},varProject),
        "Isao Takahata" : collection.find({"Realisateur" : 'Isao Takahata'},varProject),
        "Park Chan-wook" : collection.find({"Realisateur" : 'Park Chan-wook'},varProject),
        "Bob Persichetti" : collection.find({"Realisateur" : 'Bob Persichetti'},varProject),
        "George Miller" : collection.find({"Realisateur" : 'George Miller'},varProject),
        "Quentin Tarantino" : collection.find({"Realisateur" : 'Quentin Tarantino'},varProject)
    }

    for realisateur in liste_realisateur():
        l = l + list(dico[realisateur])
    return l



def TOP_Box_Office():
    Best_Box_Office = collection.find({"other_details.budget":{"$gte":100000000}},varProject).sort([("other_details.Cumulative_WW_Gross", -1),("charts.note_moyenne", -1)]).limit(50)
    return list(Best_Box_Office)

def Top_50():
    TOP_FILMS_50 = collection.find({"charts.nombre_critiques":{"$gte":5000}},varProject).sort([("charts.note_moyenne", -1)]).limit(50)
    return list(TOP_FILMS_50)


def recherche_film(nom_film):
    return list(collection.find({'nom_film_attache': nom_film}))[0]

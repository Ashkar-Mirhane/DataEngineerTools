from flask import Flask
from flask import Flask, redirect, url_for, render_template, request, flash
import pandas as pd
import functions as f

data = pd.read_csv('data_FINAL.csv')
data_lst = f.dataframe_to_list(data)

titre_top_film = ["Meilleurs films de 2016"]
listes = [[titre_top_film[0], f.c_film(titre_top_film[0]), f.recherche_annee(2016, data_lst)]]


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def acceuil():
    if request.method == 'POST':
        search = request.form['type_film']
        return render_template("recherche.html", search = search, type_film = f.lst_type_film())
    else:
        search = request.args.get('type_film')
        return render_template("index.html", liste_1_short = f.liste_alea(listes[0][2], 5), liste_1 = listes[0], film = f.liste_alea(data_lst, 1), type_film = f.lst_type_film())

@app.route('/<liste_top>')
def liste_film(liste_top):
    for elm in listes:
        if elm[1] == liste_top:
            data = elm
    return render_template("top_liste.html", data = data, type_film = f.lst_type_film())

@app.route('/fiche_film/<n_film>')
def fiche(n_film):
    for elm in data_lst:
        if f.c_film(elm[0]) == n_film:
            data = elm
    return render_template("fiche_film.html", name_film = data[0], image = data[13], note_sens_critique = data[8]['note_moyenne'], note_IMDB = float(".".join(data[10][0].split(','))), note_META = float(data[11]), budget = data[12]['budget'], box_office = data[12]['Cumulative_WW_Gross'], location = data[12]['location'], acteurs_principaux = data[7], duree = data[5], date_sortie = data[6], realisateur = data[4], type_film = data[2], resume = data[3], notes = data[15], moyenne_note = data[14], type_film_2 = f.lst_type_film() )


if __name__ == "__main__":
    app.run()



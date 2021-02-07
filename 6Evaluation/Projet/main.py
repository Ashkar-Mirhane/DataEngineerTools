from flask import Flask
from flask import Flask, redirect, url_for, render_template, request, flash
import pandas as pd

import mongo as m
import fonctions_utiles as f

lst_theme = m.liste_theme()
lst_TOP_realisateur = m.liste_realisateur()

titres_listes_top_film = [["Plus gros succès au BOX OFFICE", m.TOP_Box_Office()], ["TOP 50 Meilleurs films entre 2013 et 2019", m.Top_50()], ["Meilleurs réalisateurs de 2013 à 2019", m.TOP_meilleurs_realisateurs()]]

listes = []
for elm in titres_listes_top_film:
    listes.append([elm[0], f.c_film(elm[0]), elm[1]])



#PARTIE FLASK

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def acceuil():
    if request.method == 'POST':
        search = request.form['type_film']
        data = m.TOP_par_theme(f.c_film(search))
        return render_template("recherche.html", search = search, type_film = lst_theme, data = data, lst_rea = m.liste_realisateur())
    else:
        search = request.args.get('type_film')
        return render_template("acceuil.html", liste_1_short = f.liste_alea(listes[0][2], 5), liste_1 = listes[0], liste_2_short = f.liste_alea(listes[1][2], 5), liste_2 = listes[1], liste_3_short = f.liste_alea(listes[2][2], 5), liste_3 = listes[2], film = f.liste_alea(m.TOP_par_theme(f.c_film(lst_theme[f.r.randint(0, len(lst_theme)-1)])), 1)[0], type_film = lst_theme, lst_rea = m.liste_realisateur())


@app.route('/fiche_film/<n_film>',methods = ['POST', 'GET'])
def fiche(n_film):
    if request.method == 'POST':
        search = request.form['type_film']
        data = m.TOP_par_theme(f.c_film(search))
        return render_template("recherche.html", search = search, type_film = lst_theme, data = data)
    else:
        search = request.args.get('type_film')
        data = m.recherche_film(n_film)
        return render_template("fiche_film.html", name_film = data['nom_film'], image = data['nom_fichier_image'], note_sens_critique = data['charts']['note_moyenne'], note_IMDB = float(".".join(data['charts_IMDB'][0].split(','))), note_META = float(data['charts_METACRITIC']), budget = data['other_details']['budget'], box_office = data['other_details']['Cumulative_WW_Gross'], location = data['other_details']['location'], acteurs_principaux = data['acteurs_principaux'], duree = data['duree_film'], date_sortie = data['sortie_film'], realisateur = data['Realisateur'], type_film = data['theme_production'], resume = data['Synopsis'], notes = data['etoiles'], moyenne_note = data['note_moyenne'], type_film_2 = lst_theme )

@app.route('/<liste_top>',methods = ['POST', 'GET'])
def liste_film(liste_top):
    if request.method == 'POST':
        search = request.form['type_film']
        data = m.TOP_par_theme(f.c_film(search))
        return render_template("recherche.html", search = search, type_film = lst_theme, data = data)
    else:
        search = request.args.get('type_film')
        for elm in listes:
            if elm[1] == liste_top:
                data = elm
        return render_template("top_liste.html", data = data, type_film = lst_theme)

if __name__ == "__main__":
    app.run()



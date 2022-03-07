import code
from crypt import methods
from distutils.log import debug
from operator import index, methodcaller
from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import date
import os
import openai
from dotenv import load_dotenv




DATABASE = 'job.db'

# instancier une application Flask
app = Flask(__name__)
	
# il faut rajouter POST pour envoyer le résultat du form
@app.route("/", methods=["GET", "POST"])
# définir la route 'home'



#def liste_deroulante():

	#print("here")
	

	#return liste_dates,liste_villes,liste_contrats,liste_mots

#def construction_requete(date,ville,contrat,mot):

	
	#print(res_inter)
	#return res_inter

def home():
	conn = sql.connect(DATABASE)
	cursor = conn.cursor()

	cursor.execute("""select ville from lieu;""")
	liste_villes_raw = cursor.fetchall()
	liste_villes = [elt[0] for elt in liste_villes_raw]
	cursor.execute("""select DISTINCT(type_contrat) from contrat;""")
	liste_contrats_raw = cursor.fetchall()
	liste_contrats = [elt[0] for elt in liste_contrats_raw]

	cursor.execute("""select mot from motcle WHERE categorie_azure = 'Skill';""")
	liste_mots_raw = cursor.fetchall()
	liste_mots = [elt[0] for elt in liste_mots_raw]


	if request.method == "POST":
		ville = request.form.get("villes")
		contrat = request.form.get("typeDeContrat")
		mot = request.form.get("motsCles")


		if mot == 'pas de préférence':
			cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, GROUP_CONCAT(motcle.mot,', ') , ville, type_contrat FROM offre
			JOIN liaison ON liaison.offre_id = offre.id_offre
			JOIN motcle ON motcle.id_mot = liaison.mot_id
			JOIN lieu on lieu.id_lieu = offre.reference_lieu
			JOIN contrat on contrat.id_contrat = offre.reference_contrat
			WHERE categorie_azure = 'Skill'
			group by id_offre
			order by id_offre;""")
			res_mot = cursor.fetchall()

			if ville == 'pas de préférence':
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL,GROUP_CONCAT(motcle.mot,', ') , ville , type_contrat FROM offre 
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				JOIN lieu on lieu.id_lieu = offre.reference_lieu 
				WHERE categorie_azure = 'Skill'
				group by id_offre
				order by id_offre;""")
				res_ville = cursor.fetchall()
				
			
			else:
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, GROUP_CONCAT(motcle.mot,', ') , ville, type_contrat FROM offre 
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id
				JOIN lieu on lieu.id_lieu = offre.reference_lieu 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				WHERE lieu.ville = ?
				AND categorie_azure = 'Skill'
				group by id_offre
				order by id_offre;""",(ville,))
				res_ville = cursor.fetchall()
				

			if contrat == 'pas de préférence':
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, GROUP_CONCAT(motcle.mot,', '), ville, type_contrat FROM offre 
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				JOIN lieu on lieu.id_lieu = offre.reference_lieu
				WHERE categorie_azure = 'Skill'
				group by id_offre
				order by id_offre;""")
				res_contrat = cursor.fetchall()
				

			else:
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, GROUP_CONCAT(motcle.mot,', '), ville, type_contrat FROM offre
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id
				JOIN lieu on lieu.id_lieu = offre.reference_lieu 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				WHERE contrat.type_contrat = ?
				AND categorie_azure = 'Skill'
				group by id_offre
				order by id_offre;""",(contrat,))
				res_contrat = cursor.fetchall()
				

		else:
			cursor.execute("""SELECT offre.id_offre, intitule, resume_offre, lien_URL, motcle.mot, ville, type_contrat FROM offre
			JOIN liaison ON liaison.offre_id = offre.id_offre
			JOIN motcle ON motcle.id_mot = liaison.mot_id
			JOIN lieu on lieu.id_lieu = offre.reference_lieu
			JOIN contrat on contrat.id_contrat = offre.reference_contrat
			WHERE motcle.mot = ?
			AND categorie_azure = 'Skill'
			order by id_offre;""",(mot,))
			res_mot = cursor.fetchall()
		

			if ville == 'pas de préférence':
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, motcle.mot , ville , type_contrat FROM offre 
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				JOIN lieu on lieu.id_lieu = offre.reference_lieu 
				WHERE categorie_azure = 'Skill'
				order by id_offre;""")
				res_ville = cursor.fetchall()
				
				
			
			else:
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, motcle.mot , ville, type_contrat FROM offre 
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id
				JOIN lieu on lieu.id_lieu = offre.reference_lieu 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				WHERE lieu.ville = ?
				AND categorie_azure = 'Skill'
				order by id_offre;""",(ville,))
				res_ville = cursor.fetchall()
				print(len(res_ville))
				

			if contrat == 'pas de préférence':
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL,motcle.mot, ville, type_contrat FROM offre 
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				JOIN lieu on lieu.id_lieu = offre.reference_lieu
				WHERE categorie_azure = 'Skill'
				order by id_offre;""")
				res_contrat = cursor.fetchall()
				

			else:
				cursor.execute("""SELECT id_offre, intitule, resume_offre, lien_URL, motcle.mot, ville, type_contrat FROM offre
				JOIN liaison ON liaison.offre_id = offre.id_offre
				JOIN motcle ON motcle.id_mot = liaison.mot_id
				JOIN lieu on lieu.id_lieu = offre.reference_lieu 
				JOIN contrat on contrat.id_contrat = offre.reference_contrat
				WHERE contrat.type_contrat = ?
				AND categorie_azure = 'Skill'
				order by id_offre;""",(contrat,))
				res_contrat = cursor.fetchall()
		print(len(res_contrat))		
		print(cursor.execute("Select count(*) from offre ").fetchall())
		conn.close()
		intersection_set = set.intersection(set(res_ville),set(res_contrat),set(res_mot))
		res_inter = list(intersection_set)
		return render_template('home.html', msg = res_inter, villes=liste_villes, contrats=liste_contrats, 
								mots=liste_mots)

	if request.method == "GET":
		# requete sur toutes les localisations pour avoir une liste 
		# déroulante à insérer dans le input localisation
		# ajouter un paramètre en plus dans le return du home.html
		

		return render_template('home.html', villes=liste_villes, contrats=liste_contrats, 
								mots=liste_mots )

@app.route("/template_lm", methods = ['POST'])
def template_lm(): 
	conn = sql.connect(DATABASE)
	cursor = conn.cursor()       
	nom = request.form.get("nom")
	prenom = request.form.get("prenom")
	adresse = request.form.get("adresse")
	codePostal = request.form.get("codePostal")
	ville = request.form.get("ville")
	telephone = request.form.get("telephone")
	mail = request.form.get("mail")
	qualite = request.form.get("qualite")
	etudeEnCours = request.form.get("etudeEnCours")
	idAnnonce = request.form.get("idAnnonce") #requete mots clés sql
	list_formulaire = [nom, prenom, adresse, codePostal,ville, telephone, mail, qualite, etudeEnCours, idAnnonce]

			# si la liste ne contient que des chaînes vides
	if all(elem == '' for elem in list_formulaire):	
		return render_template('home.html', void_get = True)
	else:
		mots_cles = cursor.execute("""select mot from motcle inner join liaison ON liaison.mot_id = motcle.id_mot where liaison.offre_id=:id and motcle.categorie_azure= 'Skill';""",{"id" : idAnnonce}).fetchall()
		li_mots = []
		for i in mots_cles:
			for n in i :
				li_mots.append(n)
		li_mots=str(li_mots)
		mots_cles = li_mots[1:-1] + ' "qualiter": ' + qualite + '"format": lettre de motivation entreprise ,"étude" :'+ etudeEnCours +' "langue":français'		
		
		intituler = cursor.execute("select intitule from offre where id_offre=:id ;",{"id": idAnnonce}).fetchall()
		intituler= str(intituler)
		
		today = date.today()
		d1 = today.strftime("%d/%m/%Y")
					
		openai.api_key = os.getenv("OPENAI_API_KEY")
		response = openai.Completion.create(
			engine = "text-davinci-001",
			prompt = mots_cles,
			temperature=0.7,
			max_tokens=1151,
			top_p=1,
			frequency_penalty=0,
			presence_penalty=0,
			stop=["100"]

			)

		text = response.choices[0].text
		return render_template('template_lm.html', nom=nom, prenom=prenom , adresse=adresse, codePostal=codePostal,ville = ville, telephone=telephone, mail = mail, text=text, now = d1, intituler= intituler[3:-4])
	conn.commit()
	conn.close()

	

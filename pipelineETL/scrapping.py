# d'ou viennent les variables dans les fonctions ? ex : soup, ville, missing_coords_dict

import re
from datetime import datetime, timezone
import unicodedata
#from dateutil import tz
#from dateutil.parser import parse
import sqlite3
from pathlib import Path

import requests
from bs4 import BeautifulSoup
# geocoders sert à enrichir les champs de localisation manquants
from geopy.geocoders import Nominatim

# l'API google sert à récupérer les infos d'entreprises
from googleapiclient.discovery import build
#import config_api_google_search

# au lieu d'utiliser le module config_api_google_search on crée un .env
from dotenv import load_dotenv
import os

load_dotenv()

my_cse_id = os.getenv("my_cse_id")
my_api_key = os.getenv("my_api_key")


def coordonnees_entreprise(soup, ville, missing_coords_dict):
    dict_updated = missing_coords_dict
    listcoordo=[]
    avant_coordonnees = soup.find('ul', class_='list-unstyled action-secondary')
    if avant_coordonnees is not None:
        coordonnees = avant_coordonnees.find('a',href=re.compile('https://fr.mappy.com'))

    else:
        listcoordo.append(None)
        listcoordo.append(None)
    if coordonnees is not None:
        lien_coordo= coordonnees.get('href')
        lien_mppy = requests.get(lien_coordo)
        if lien_mppy.ok:
            text_to_search = str(lien_mppy.text)
            # Attention l'extreme ouest de la france a des longitudes négatives
            matching = re.search('"coordinates":{"lng":(-?[0-9.]+),"lat":(-?[0-9.]+)}', text_to_search)
            if matching is None:
                lng = None
                lat = None
            else:
                lng,lat = matching.groups()
            listcoordo.append(lng)
            listcoordo.append(lat)
    else:
        listcoordo.append(None)
        listcoordo.append(None)
    
    if None in listcoordo:
        if ville in missing_coords_dict.keys():
            listcoordo = missing_coords_dict[ville]
        else:
            if ville[-8:] == " (Dept.)":
                ville_mod = ville[:-8]
            else:
                ville_mod = ville
            geolocator = Nominatim(user_agent="P_3-G_3_collecte_offre_emploi")
            location = geolocator.geocode(ville_mod)
            if location is not None:
                listcoordo = [location.longitude, location.latitude]
            else:
                listcoordo = [None, None]
            dict_updated[ville] = listcoordo
    
    return(listcoordo, dict_updated)

def date_offre(soup):
    date_offre=soup.find('p',class_="t5 title-complementary")
    if date_offre is None:
        publie = None
        date = None
        numero_offre = None
    else:
        matching = re.search(r'(Publié|Actualisé) le (.*)\n\n- offre n°\n([0-9]+)',date_offre.text)
        publie, date, numero_offre = matching.groups()
    return publie, date, numero_offre

def description_offre(soup):
    description_offre = soup.find('div',class_="description col-sm-8 col-md-7")
    if description_offre is None:
        descriptiondeloffre= None
    else:
        #print(description_offre)
        descriptiondeloffre=description_offre.text
    #descriptiondeloffre.encode('ascii', errors='ignore')
    
    #descriptiondeloffre = unicodedata.normalize('NFKC', descriptiondeloffre)
    
    return(descriptiondeloffre)

def experience_offre(soup):
    """
    In: soup
    Out: regexed experience column
    """
    pattern = re.compile(r'(?P<full>(?P<debutant>[Dd][eé]butant [aA]ccept[eé])'
                     r'|(?<!ï¿½ )(?<!\()(?P<annee>\d?\d)(?=( [aA]n\(?s?\)?)|( ï¿½ \d [Aa]n\(?s?\)?))'
                     r'|(?P<mois>\d?\d)(?= [mM]ois)'
                     r'|(?P<expabs>[Ee]xp[eé]rience [eE]xig[ée]e) ?\(?\d?\)?$)')

    experience = soup.find('span',{"class" : ["skill-name"]}).text
    regexed = re.search(pattern, experience)

    if regexed is not None:
        if regexed.group('expabs') is not None:
            choice = None
        elif regexed.group('debutant') == 'Débutant accepté':
            choice = round(0, 2)
        elif regexed.group('annee') is not None:
            choice = round(float(regexed.group('annee')), 2)
        elif regexed.group('mois') is not None:
            choice = round((float(regexed.group('mois')) / 12), 2)
    else:
        choice = None
        
    return choice

def infos_entreprise(soup,limit):
    
    
    ###### on a plus besoin de créer ces variables qui sont récupérer du venv
    # my_api_key = config_api_google_search.my_api_key
    # my_cse_id = config_api_google_search.my_cse_id
    #######
    
    limit_local = limit
    entreprise_name = soup.select_one('#contents > div.container-fluid.gabarit-full-page.with-large-right-column > div > div.panel-center.col-md-8 > div > div.modal-details.modal-details-offre > div > div > div > div > div.media > div > h4')
    entreprise_lien = soup.select_one('#contents > div.container-fluid.gabarit-full-page.with-large-right-column > div > div.panel-center.col-md-8 > div > div.modal-details.modal-details-offre > div > div > div > div > div.media > div.media-body > dl > dd > a')
    if entreprise_name is not None:
        nom_entreprise = entreprise_name.text
    else:
        nom_entreprise = None
    if entreprise_lien is not None:
        lien_entreprise = entreprise_lien.text
    elif entreprise_name is not None:
        if limit_local < 100:
            print('-=-=-   try number', str(limit_local), '@ getting society\'s link from google API   -=-=-')
            print('nom de l\'entreprise', nom_entreprise)
            limit_local += 1
            try:
                service = build("customsearch", "v1", developerKey=my_api_key)
                lien_entreprise = service.cse().list(q=nom_entreprise, cx=my_cse_id).execute()['items'][0]['link'].strip()
            except:
                print('-o-o- Google API limit reached - appending None -o-o-')
                lien_entreprise = None
        else:
                lien_entreprise = None
    else:
        lien_entreprise = None
    return(nom_entreprise, lien_entreprise, limit_local)

def intitule_offre(soup):
    intit=soup.find("h1",{"class":"t2 title"})
    if intit is None:
        print("l'offre n'est plus disponible")
    else:
        intitvalid=soup.find("h1",{"class":"t2 title"}).text
    return(intitvalid)


def type_contrat_offre(soup):
    type_contrat = soup.find('dl',class_="icon-group").contents[1]
    if type_contrat is None:
        duree_contrat = None
        type_contrat = None
    else:
        matching = re.match(r'\n(.*)\n\n(.*)\n', type_contrat.text)
        duree_contrat, type_contrat = matching.groups()
    return duree_contrat, type_contrat

def ville_offre(soup):
    ville = soup.find("span",{"itemprop":"name"}) 
    if ville is None:
        villedeloffre = None
    else:
        villedeloffre= ville.text
    return(villedeloffre)

#Cette partie utilise la liste des liens vers les pages avec 20 offres chacune et va renvoyer la liste des liens vers l'offre inviduelle

def creation_liste_lien(liste_page):

    liste_lien=[]

    for elt in liste_page:
    
        r = requests.get(elt)
        soup = BeautifulSoup(r.text, 'html.parser')

        a = soup.findAll("a", {"class" : "media with-fav"})
    
        for c in a: 
            lien_complet="https://candidat.pole-emploi.fr"+c.get("href")
            liste_lien.append(lien_complet)
    #print(liste_lien)
    print(f'liste_lien - terminé')
    return(liste_lien)


# Cette partie ouvre la page qui correspond à la recherche avec le mots clé data 

def creation_liste_page(motCle):

    #motsCles=str(motsCles)
    URL="https://candidat.pole-emploi.fr/offres/recherche?motsCles="+ motCle +"&  offresPartenaires=true"
    print("URL de recherche: ", URL)
    r= requests.get(URL)
#A partir d'ici le serveur ne sont plus sollicités
    sc = r.status_code
    print("status code", sc)

    soup = BeautifulSoup(r.text, 'html.parser')

    print("Recherche des titres")
    total=soup.find("h1",{"class":"title"}).text
    print(total)
    if total.split()[0] == "Aucune":
        print(f'il n\'y a pas d\'offre pour {motCle}')
    else:
        totalnbr=int(total.split()[0])
        print("le nombre d'offre")
        print(totalnbr)
        range_deb=0
        range_fin=19
        imax=int((totalnbr - 1)/20)
        print(imax)

        liste_page=[]

        for i in range(imax+1):   
            print(range_deb, range_fin)
            lien_page="https://candidat.pole-emploi.fr/offres/recherche?motsCles="+motCle+"&offresPartenaires=true&range="+str(range_deb)+"-"+str(range_fin)+"&rayon=10&tri=0"
            print(lien_page)
            liste_page.append(lien_page)
            range_deb+=20
            range_fin+=20
        print(f'liste page - terminé pour {motCle}')
        return(liste_page)

def creation_tuple_fonction(liste_mots_Cle):
    dict_missing_coords = {}
    google_api_limit_current = 0
    marker = -1 # iterations count
    
    print(liste_mots_Cle)
    tuple_scrap = []
    for elt1 in liste_mots_Cle:
        
        liste_lien=creation_liste_lien(creation_liste_page(elt1))
        for elt2 in liste_lien:
#print(elt)
            marker += 1
            if marker%50 == 49:
                print('------------------------------------------')
                print('------------------------------------------')
                print(f'downloaded {marker + 1} offers this far')
                print('------------------------------------------')
                print('------------------------------------------')
    
    
            r = requests.get(elt2)
            
            if r.ok:
                mot_cle = elt1
                lien_URL = elt2
                soup = BeautifulSoup(r.text, 'html.parser')
                
                intitule = intitule_offre(soup)
                
                dicodateoffre = date_offre(soup)
              
                if dicodateoffre[0] == "Publié":
                    date_publication=dicodateoffre[1]
                    date_actualisation=None
                elif dicodateoffre[0] == "Actualisé":
                    date_actualisation=dicodateoffre[1]
                    date_publication=None
                else:
                    date_actualisation=None
                    date_publication=None
                numero_offre = dicodateoffre[2]
                description = description_offre(soup) 
                dicotypecontrat = type_contrat_offre(soup)
                duree_contrat = dicotypecontrat[0]
                type_contrat= dicotypecontrat[1]
                experience = experience_offre(soup)
                ville = ville_offre(soup)
                # gestion des coordonnées manquantes, pas besoin on verra par la suite
                # dicocoord=coordonnees_entreprise(soup,ville_offre(soup)[-1], dict_missing_coords)
                # dict_missing_coords = dicocoord[1]
                #longitude = dicocoord[0][0]
                #latitude = dicocoord[0][1]
                longitude = None
                latitude = None

                dicoentreprise=infos_entreprise(soup,google_api_limit_current)
                entreprise = dicoentreprise[0]
                url_entreprise = dicoentreprise[1]
                google_api_limit_current = dicoentreprise[2]
                
                tuple_scrap.append((
                    mot_cle,
                    lien_URL,
                    intitule,
                    date_publication,
                    date_actualisation,
                    numero_offre,
                    description,
                    duree_contrat,
                    type_contrat,
                    experience,
                    ville,
                    longitude,
                    latitude,
                    entreprise,
                    url_entreprise
                    ))
        #print(type(tuple_scrap))
        #print(tuple_scrap)
    return(tuple_scrap)
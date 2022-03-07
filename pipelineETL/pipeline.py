import SQLscripts
import scrapping
from pathlib import Path
import html


# certains caractères sont codés en html
mots_cles = [
    ####html.escape("développeur d'application"), 
    ####"Technicien supérieur systèmes et réseaux",
    ####"Administrateur d%27infrastructures sécurisées",
    ####"Développeur web et web mobile",
    "Développeur en intelligence artificielle"
    ####"Technicien helpdesk"
    ]

#mots_cles = ["NLP"]

# configuration des chemins vers la base de données et les scripts SQL
db_file_pole_emploi = "../app_web/job.db"

db_path_pole_emploi = Path(db_file_pole_emploi)
structure_script_path = "./structure.sql"
insertion_script_path = "./insertion.sql"

tuple_pole_emploi = scrapping.creation_tuple_fonction(mots_cles)
#print(tuple_pole_emploi)
# appel des fonctions d'execution des scripts
print("structure")
SQLscripts.sql_script_execution(structure_script_path, db_path_pole_emploi)
print("insertion")
SQLscripts.tuple_load(tuple_pole_emploi, db_path_pole_emploi)
SQLscripts.sql_script_execution(insertion_script_path, db_path_pole_emploi)
print("enrichissement avec spacy")
SQLscripts.spacy_pipeline(db_path_pole_emploi)
print("enrichissement avec azure")
SQLscripts.azure_pipeline(db_path_pole_emploi)
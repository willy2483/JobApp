import sqlite3
import summaryenrichment
import entityenrichment


def sql_script_execution(sql_script,db_path):
    """
    Prend en argument les scripts SQL pour les appliquer à la base de données en deuxième argument
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # running sql script for raw and clean table creation
    with open(sql_script, 'r') as sql_file:
        sql_for_execution = sql_file.read()
    cur.executescript(sql_for_execution)
    conn.commit()

    cur.close()
    conn.close()

def tuple_load(job_tuple_list,db_path):

    """
    Prend en argument la liste de tuples issue du scrapping et insert les tuples dans la table raw_data pour nettoyage dans clean_data
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM raw_data;")
    conn.commit()
    
    # each csv file is loaded in raw_data
    cur.executemany("INSERT INTO raw_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",job_tuple_list)
    conn.commit()
    
     
    cur.execute("""
    INSERT OR IGNORE INTO clean_data
    SELECT *
    FROM raw_data
    ;
    """)
    # test pour voir si on peut faire l'enrichissement depuis
    # le premier insert
    
    conn.commit()
    #à rajouter quand on met en place clean_data

    cur.close()
    conn.close()


def spacy_pipeline(db_path):

   
    """
    Prend en argument la base de données
    et sélectionne les offres qui n'ont pas encore de résumé et 
    enrichit la table offre en complétant le champ resume_offre à 
    partir des résumés fait par spacy
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # on regarde quelles description n'ont pas encore de résumé
    
    cur.execute("""SELECT id_offre, description_offre FROM offre
    WHERE resume_offre IS NULL;""")

    offers_to_summarize = cur.fetchall()

    for elt in offers_to_summarize:
        
        description = elt[1]
        summary = summaryenrichment.summarize_from_description(description)

        # on met à jour la table offre avec le résumé
        cur.execute("UPDATE offre SET resume_offre = ? WHERE id_offre = ?",(summary, elt[0]))
               
        conn.commit()

    cur.close()
    conn.close()


def azure_pipeline(db_path):

    ######################################################################
    # pour l'instant language code est fixé à français

    language_code = 'fr'
    ######################################################################

    """
    Prend en argument la base de données
    et insert les tuples issus de l'enrichissement par azure dans la table mot_clé 
    et met à jour la table liaison en conséquence avec les résultats du pipeline
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # on regarde quel offre n'ont pas encore d'entités détectées dans la limite de 1000 offres
    
    cur.execute("""SELECT id_offre, resume_offre FROM offre
    LEFT OUTER JOIN liaison ON offre.id_offre = liaison.offre_id
    WHERE liaison.offre_id IS NULL
    ;""")

    summary_to_enrich = cur.fetchall()
    conn.commit()
    
    
    
    print(summary_to_enrich)

    for elt in summary_to_enrich:

        # Il faudrait remettre cette partie au propre en inclant les résumés qui pose problème dans un log
        
        try:
        # spacy semble avoir des problèmes pour résumer certaines offres
            
                
            cat_list, ent_list = entityenrichment.entities_recognition(elt[1],language_code)

            # on écrit chaque couple (mot-clé, categorie_spacy) dans la table mots_clé
            for i in range(len(cat_list)):

                cur.execute("INSERT OR IGNORE INTO motcle (id_mot, mot, categorie_azure) VALUES (NULL,?,?)",(ent_list[i], cat_list[i]))
                conn.commit()

                cur.execute("SELECT id_mot,mot FROM motcle WHERE mot = ?",(ent_list[i],))
                is_in = cur.fetchall()

                
                cur.execute("INSERT OR IGNORE INTO liaison (offre_id, mot_id) VALUES (?,?)",(elt[0],is_in[0][0]))
                conn.commit()
        except:
            with open("log.txt", "a") as log:
                print(elt, file = log)
            continue
    cur.close()
    conn.close()






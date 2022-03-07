INSERT OR IGNORE INTO contrat ("type_contrat","duree_contrat","experience")
SELECT DISTINCT(contrat), duree_contrat,experience
FROM clean_data;

INSERT OR IGNORE INTO lieu ("ville","entreprise","url_entreprise","longitude","latitude")
SELECT DISTINCT(lieu), entreprise, url_entreprise, longitude, latitude
FROM clean_data;


/* Remplir dans l'ordre */
INSERT OR IGNORE INTO offre ("mot_cle_recherche","lien_URL","intitule","date_publication","date_actualisation","numero_offre","description_offre","resume_offre","reference_lieu","reference_contrat")
SELECT mot_cle_recherche, lien_URL, intitule, date_publication, date_actualisation, numero_offre, description_offre, NULL ,lieu.id_lieu, contrat.id_contrat
FROM clean_data
JOIN lieu
ON clean_data.lieu = lieu.ville
JOIN contrat
ON clean_data.contrat = contrat.type_contrat
;
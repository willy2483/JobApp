PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS raw_data (
            mot_cle_recherche TEXT,
            lien_URL TEXT,
            intitule TEXT,
            date_publication TEXT,
            date_actualisation TEXT,
            numero_offre TEXT,
            description_offre TEXT,
            duree_contrat TEXT,
            contrat TEXT,
            experience TEXT,
            lieu TEXT,
            longitude REAL,
            latitude REAL,
            entreprise TEXT,
            url_entreprise TEXT
            );


CREATE TABLE IF NOT EXISTS clean_data (
            mot_cle_recherche TEXT,
            lien_URL TEXT,
            intitule TEXT,
            date_publication TEXT,
            date_actualisation TEXT,
            numero_offre TEXT,
            description_offre TEXT,
            duree_contrat TEXT,
            contrat TEXT,
            experience TEXT,
            lieu TEXT,
            longitude REAL,
            latitude REAL,
            entreprise TEXT,
            url_entreprise TEXT,
            /* on considère que 2 offres avec le même 
            numéro correspondent à des doublons
            UNIQUE (intitule, lien, date_offre, entreprise, lieu, description_offre)
            */
            UNIQUE (numero_offre)
            );

CREATE TABLE IF NOT EXISTS contrat (
    id_contrat INTEGER NOT NULL,
    type_contrat TEXT,
    duree_contrat TEXT,
    experience TEXT,
    PRIMARY KEY (id_contrat),
    UNIQUE (duree_contrat,type_contrat,experience)
    );

CREATE TABLE IF NOT EXISTS lieu (
    id_lieu INTEGER NOT NULL,
    ville TEXT,
    entreprise TEXT,
    url_entreprise TEXT,
    longitude REAL,
    latitude REAL,
    PRIMARY KEY (id_lieu),
    UNIQUE (ville)
    );

/*
CREATE TABLE IF NOT EXISTS employeur (
    id_entreprise INTEGER NOT NULL,
    entreprise TEXT,
    url_entreprise TEXT,
    PRIMARY KEY (id_entreprise),
    UNIQUE (entreprise)
    );
*/
CREATE TABLE IF NOT EXISTS motcle (
    /*id_mot INTEGER PRIMARY KEY AUTOINCREMENT,*/
    id_mot INTEGER NOT NULL,
    mot TEXT,
    categorie_spacy TEXT,
    categorie_azure TEXT,
    PRIMARY KEY (id_mot),
    UNIQUE (mot)
    );

CREATE TABLE IF NOT EXISTS offre (
    id_offre INTEGER NOT NULL,
    mot_cle_recherche TEXT,
    lien_URL TEXT,
    intitule TEXT,
    date_publication TEXT,
    date_actualisation TEXT,
    numero_offre TEXT,
    description_offre TEXT,
    resume_offre TEXT,
    reference_lieu INT,
    reference_contrat INT,
    PRIMARY KEY (id_offre),
    FOREIGN KEY (reference_lieu) REFERENCES lieu(id_lieu),
    FOREIGN KEY (reference_contrat) REFERENCES contrat(id_contrat),
    UNIQUE (numero_offre)
    );

/*
CREATE TABLE IF NOT EXISTS offre_mots (
    id_offre_mots INTEGER NOT NULL,
    offre_id INTEGER NOT NULL,
    mot_id INTEGER NOT NULL,
    FOREIGN KEY (offre_id) REFERENCES offre (id_offre),
    FOREIGN KEY (mot_id) REFERENCES motscles (id_mot),
    PRIMARY KEY (id_offre_mots)
    );*/

CREATE TABLE IF NOT EXISTS liaison (
    offre_id INTEGER NOT NULL,
    mot_id INTEGER NOT NULL,
    FOREIGN KEY (offre_id) REFERENCES offre (id_offre),
    FOREIGN KEY (mot_id) REFERENCES motcle (id_mot),
    UNIQUE (offre_id,mot_id)
    /*PRIMARY KEY (offre_id, mot_id)*/
    );
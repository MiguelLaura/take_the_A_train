DROP TABLE IF EXISTS Gare;
DROP TABLE IF EXISTS Hotel;
DROP TABLE IF EXISTS DisposeHotel;
DROP TABLE IF EXISTS Taxi;
DROP TABLE IF EXISTS DisposeTaxi;
DROP TABLE IF EXISTS TransportPublic;
DROP TABLE IF EXISTS DisposeTransportPublic;
DROP TABLE IF EXISTS TypeTrain;
DROP TABLE IF EXISTS Train;
DROP TABLE IF EXISTS Ligne;
DROP TABLE IF EXISTS ArretLigne;
DROP TABLE IF EXISTS Calendrier;
DROP TABLE IF EXISTS DateException;
DROP TABLE IF EXISTS ConcerneCalendrier;
DROP TABLE IF EXISTS Voyage;
DROP TABLE IF EXISTS ArretVoyage;
DROP TABLE IF EXISTS Trajet;
DROP TABLE IF EXISTS ArretTrajet;
DROP TABLE IF EXISTS Voyageur;
DROP TABLE IF EXISTS Billet;
DROP TABLE IF EXISTS CompositionBillet;


DROP VIEW IF EXISTS v_DisposeHotel;


CREATE TABLE Gare (
    nom VARCHAR(20) NOT NULL,
    ville VARCHAR(20) NOT NULL,
    adresse VARCHAR(20) NOT NULL,
    pays VARCHAR(20) NOT NULL,
    PRIMARY KEY (nom, ville)
);

CREATE TABLE Hotel (
    nom VARCHAR(20) NOT NULL,
    adresse VARCHAR(20) NOT NULL,
    PRIMARY KEY (nom, adresse)
);

CREATE TABLE DisposeHotel (
    nom_gare VARCHAR(20) NOT NULL,
    ville_gare VARCHAR(20) NOT NULL,
    nom_hotel VARCHAR(20) NOT NULL,
    adresse_hotel VARCHAR(20) NOT NULL,
    PRIMARY KEY (nom_gare, ville_gare, nom_hotel, adresse_hotel),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville),
    FOREIGN KEY (nom_hotel, adresse_hotel) REFERENCES Hotel(nom, adresse)
);

CREATE VIEW v_DisposeHotel AS
SELECT d.nom_hotel, d.adresse_hotel
FROM  DisposeHotel d RIGHT OUTER JOIN Hotel h
ON h.nom = d.nom_hotel
AND h.adresse = d.adresse_hotel;

SELECT COUNT(*)
FROM (SELECT d.nom_hotel, d.adresse_hotel
FROM DisposeHotel d RIGHT OUTER JOIN Hotel h
ON h.nom = d.nom_hotel
AND h.adresse = d.adresse_hotel) a
GROUP BY (a.nom_hotel, a.adresse_hotel);


CREATE TABLE Taxi (
    num INT PRIMARY KEY,
    telephone VARCHAR(10) NOT NULL,
);

CREATE TABLE DisposeTaxi (
    nom_gare VARCHAR(20) NOT NULL,
    ville_gare VARCHAR(20) NOT NULL,
    num_taxi INT NOT NULL,
    PRIMARY KEY (nom_gare, ville_gare, num_taxi),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville),
    FOREIGN KEY (num_taxi) REFERENCES Taxi(num)
);

CREATE TABLE TransportPublic (
    num INT NOT NULL,
    PRIMARY KEY (num)
);

CREATE TABLE DisposeTransportPublic (
    nom_gare VARCHAR(20) NOT NULL,
    ville_gare VARCHAR(20) NOT NULL,
    num_transport_public INT NOT NULL,
    PRIMARY KEY (nom_gare, ville_gare, num_transport_public),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville),
    FOREIGN KEY (num_transport_public) REFERENCES TransportPublic(num)
);

CREATE TABLE TypeTrain (
    nom VARCHAR(20) NOT NULL,
    nb_places INT NOT NULL,
    vitesse INT NOT NULL,
    première_classe BOOLEAN NOT NULL,
    PRIMARY KEY (nom),
    CHECK (vitesse >= 0 AND nb_places >= 0)
);

CREATE TABLE Train (
    num INT NOT NULL,
    type_train VARCHAR(20) NOT NULL,
    PRIMARY KEY (num),
    FOREIGN KEY (type_train) REFERENCES TypeTrain(nom)
);

CREATE TABLE Ligne (
    num INT NOT NULL,
    type_train VARCHAR(20) NOT NULL,
    PRIMARY KEY (num),
    FOREIGN KEY (type_train) REFERENCES TypeTrain(nom),

    """check?? 
    une ligne doit relier au moins deux arrêts
    (Projection(Voyage, ligne) = Projection(Ligne, num)
    """
);




CREATE TABLE ArretLigne (
    num_arret INT NOT NULL,
    ligne INT NOT NULL,
    arrive BOOLEAN,
    nom_gare VARCHAR(20),
    ville_gare VARCHAR(20),
    PRIMARY KEY (num_arret, ligne),
    FOREIGN KEY (ligne) REFERENCES Ligne(num),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville),
    CHECK (num_arret >= 1)
);

CREATE TABLE Calendrier (
    id_calendrier INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    horaire TIME NOT NULL,
    lundi BOOLEAN NOT NULL,
    mardi BOOLEAN NOT NULL,
    mercredi BOOLEAN NOT NULL,
    jeudi BOOLEAN NOT NULL,
    vendredi BOOLEAN NOT NULL,
    samedi BOOLEAN NOT NULL,
    dimanche BOOLEAN NOT NULL,
    PRIMARY KEY (id_calendrier)
);

CREATE TABLE DateException (
    date_ DATE NOT NULL,
    ajout BOOLEAN NOT NULL,
    PRIMARY KEY (date_)
);
'''date_'''

CREATE TABLE ConcerneCalendrier (
    date_exception DATE NOT NULL,
    ajout_exception BOOLEAN NOT NULL,
    calendrier INT NOT NULL,
    FOREIGN KEY (date_exception, ajout_exception) REFERENCES DateException(date_, ajout),
    FOREIGN KEY (calendrier) REFERENCES Calendrier(id_calendrier),
    PRIMARY KEY (date_exception, ajout_exception, calendrier)
);

CREATE TABLE Voyage (
    id_voyage INT NOT NULL,
    ligne INT NOT NULL,
    train INT NOT NULL,
    calendrier INT NOT NULL,
    FOREIGN KEY (ligne) REFERENCES Ligne(num),
    FOREIGN KEY (train) REFERENCES Train(num),
    FOREIGN KEY (calendrier) REFERENCES Calendrier(id_calendrier),
    PRIMARY KEY (id_voyage)
);


CREATE TABLE ArretVoyage (
    num_arret INT NOT NULL,
    voyage INT NOT NULL,
    heure_depart TIME NOT NULL,
    heure_arrivee TIME NOT NULL,
    arret_ligne INT NOT NULL,
    ligne INT NOT NULL,
    PRIMARY KEY (num_arret, voyage),
    FOREIGN KEY (arret_ligne, ligne) REFERENCES ArretLigne(num_arret, ligne),
    FOREIGN KEY (ligne, voyage) REFERENCES Voyage(ligne, id_voyage)
);

CREATE TABLE Trajet (
    id_trajet INT NOT NULL,
    num_place INT NOT NULL,
    date_ DATE NOT NULL,
    PRIMARY KEY (id_trajet)
);
'''date_'''

CREATE TABLE ArretTrajet (
    trajet INT NOT NULL,
    num_arret_voyage INT NOT NULL,
    voyage INT NOT NULL,
    depart BOOLEAN NOT NULL,
    PRIMARY KEY (trajet, num_arret_voyage, voyage),
    FOREIGN KEY (trajet) REFERENCES Trajet(id_trajet),
    FOREIGN KEY (num_arret_voyage, voyage) REFERENCES ArretVoyage(num_arret, voyage)
);

CREATE TABLE Voyageur (
    nom VARCHAR(20) NOT NULL,
    prenom VARCHAR(20) NOT NULL,
    adresse VARCHAR(20) NOT NULL,
    telephone VARCHAR(10) NOT NULL,
    paiement VARCHAR(20) NOT NULL,
    carte INT,
    statut VARCHAR(20),
    occasionnel BOOLEAN NOT NULL,
    PRIMARY KEY (nom, prenom, adresse),

    CHECK (paiement = 'carte' OR paiement = 'cheque' OR paiement = 'monnaie' AND statut = 'bronze' OR statut = 'silver' OR statut = 'gold' OR statut = 'platine'),
    CHECK (occasionnel = FALSE AND carte NOT NULL AND statut NOT NULL OR occasionnel = true AND carte IS NULL AND statut IS NULL)
     
);

CREATE TABLE Billet (
    id_billet INT NOT NULL,
    assurance BOOLEAN NOT NULL,
    prix FLOAT NOT NULL,
    voyageur_nom VARCHAR(20) NOT NULL,
    voyageur_prenom VARCHAR(20) NOT NULL,
    voyageur_adresse VARCHAR(20) NOT NULL,''''''
    PRIMARY KEY (id_billet),
    FOREIGN KEY (voyageur_nom, voyageur_prenom, voyageur_adresse) REFERENCES Voyageur(nom, prenom, adresse)
);

CREATE TABLE CompositionBillet (
    billet INT NOT NULL,
    trajet INT NOT NULL,
    PRIMARY KEY (billet, trajet),
    FOREIGN KEY (billet) REFERENCES Billet(id_billet),
    FOREIGN KEY (trajet) REFERENCES Trajet(id_trajet)
);






"""
L'attribut date dans Trajet doit être une date présente dans le Calendrier du Voyage et non supprimée dans DateException, ou bien une date ajoutée dans DateException du Voyage.
Il faut s'assurer que l'horaire de Voyage (présente dans Calendrier) est égale à l'heure de départ du premier ArretVoyage.
Il faut s'assurer que le nombre de places réservées ne dépasse pas nb_places du TypeTrain pour chaque Voyage.
"""


CREATE VIEW vDisposeHotel
-- A faire
-- vues (fichier séparé ?) pour les projections, pour les conditions 2 et pour les contraintes en fin de document (Ligne x3, ConcerneCalendrier, Voyage, ArretVoyage x2, CompositionBillet)
-- INSERT (fichier séparé ?)
-- SELECT avec GROUP BY (fichier séparé ?)


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
    nom VARCHAR(20),
    ville VARCHAR(20),
    adresse VARCHAR(80) NOT NULL,
    pays VARCHAR(20) NOT NULL,
    PRIMARY KEY (nom, ville)
);

CREATE TABLE Hotel (
    nom VARCHAR(20),
    adresse VARCHAR(80),
    PRIMARY KEY (nom, adresse)
);

CREATE TABLE DisposeHotel (
    nom_gare VARCHAR(20),
    ville_gare VARCHAR(20),
    nom_hotel VARCHAR(20),
    adresse_hotel VARCHAR(80),
    PRIMARY KEY (nom_gare, ville_gare, nom_hotel, adresse_hotel),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville),
    FOREIGN KEY (nom_hotel, adresse_hotel) REFERENCES Hotel(nom, adresse)
);

CREATE TABLE Taxi (
    num INT PRIMARY KEY,
    telephone VARCHAR(10) NOT NULL
);

CREATE TABLE DisposeTaxi (
    nom_gare VARCHAR(20),
    ville_gare VARCHAR(20),
    num_taxi INT REFERENCES Taxi(num),
    PRIMARY KEY (nom_gare, ville_gare, num_taxi),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville)
);

CREATE TABLE TransportPublic (
    num INT PRIMARY KEY
);

CREATE TABLE DisposeTransportPublic (
    nom_gare VARCHAR(20),
    ville_gare VARCHAR(20),
    num_transport_public INT REFERENCES TransportPublic(num),
    PRIMARY KEY (nom_gare, ville_gare, num_transport_public),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville)
);

CREATE TABLE TypeTrain (
    nom VARCHAR(20) PRIMARY KEY,
    nb_places INT NOT NULL,
    vitesse INT NOT NULL,
    première_classe BOOLEAN NOT NULL,
    CHECK (vitesse >= 0 AND nb_places >= 0)
);

CREATE TABLE Train (
    num INT PRIMARY KEY,
    type_train VARCHAR(20) NOT NULL REFERENCES TypeTrain(nom)
);

CREATE TABLE Ligne (
    num INT PRIMARY KEY,
    type_train VARCHAR(20) NOT NULL REFERENCES TypeTrain(nom)
);

CREATE TABLE ArretLigne (
    num_arret INT,
    ligne INT REFERENCES Ligne(num),
    arrive BOOLEAN,
    nom_gare VARCHAR(20),
    ville_gare VARCHAR(20),
    PRIMARY KEY (num_arret, ligne),
    FOREIGN KEY (nom_gare, ville_gare) REFERENCES Gare(nom, ville),
    CHECK (num_arret >= 1)
);

CREATE TABLE Calendrier (
    id_calendrier INT PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    horaire TIME NOT NULL,
    lundi BOOLEAN NOT NULL,
    mardi BOOLEAN NOT NULL,
    mercredi BOOLEAN NOT NULL,
    jeudi BOOLEAN NOT NULL,
    vendredi BOOLEAN NOT NULL,
    samedi BOOLEAN NOT NULL,
    dimanche BOOLEAN NOT NULL
);

CREATE TABLE DateException (
    date_ DATE,
    ajout BOOLEAN,
    PRIMARY KEY (date_, ajout)
);

CREATE TABLE ConcerneCalendrier (
    date_exception DATE,
    ajout_exception BOOLEAN,
    calendrier INT REFERENCES Calendrier(id_calendrier),
    PRIMARY KEY (date_exception, ajout_exception, calendrier),
    FOREIGN KEY (date_exception, ajout_exception) REFERENCES DateException(date_, ajout)
);

CREATE TABLE Voyage (
    id_voyage INT PRIMARY KEY,
    ligne INT NOT NULL REFERENCES Ligne(num),
    train INT NOT NULL REFERENCES Train(num),
    calendrier INT NOT NULL REFERENCES Calendrier(id_calendrier)
);

CREATE TABLE ArretVoyage (
    num_arret INT,
    voyage INT REFERENCES Voyage(id_voyage),
    heure_depart TIME NOT NULL,
    heure_arrivee TIME NOT NULL,
    arret_ligne INT NOT NULL,
    ligne INT NOT NULL,
    PRIMARY KEY (num_arret, voyage),
    UNIQUE (arret_ligne, ligne, voyage),
    FOREIGN KEY (arret_ligne, ligne) REFERENCES ArretLigne(num_arret, ligne),
    CHECK (heure_depart <  heure_arrivee)
);

CREATE TABLE Trajet (
    id_trajet INT PRIMARY KEY,
    num_place INT NOT NULL,
    date_ DATE NOT NULL
);

CREATE TABLE ArretTrajet (
    trajet INT REFERENCES Trajet(id_trajet),
    num_arret_voyage INT,
    voyage INT,
    depart BOOLEAN NOT NULL,
    PRIMARY KEY (trajet, num_arret_voyage, voyage),
    FOREIGN KEY (num_arret_voyage, voyage) REFERENCES ArretVoyage(num_arret, voyage)
);

CREATE TABLE Voyageur (
    nom VARCHAR(20),
    prenom VARCHAR(20),
    adresse VARCHAR(80),
    telephone VARCHAR(10) NOT NULL,
    paiement VARCHAR(7) NOT NULL,
    carte INT,
    statut VARCHAR(7),
    occasionnel BOOLEAN NOT NULL,
    PRIMARY KEY (nom, prenom, adresse),
    CHECK ((paiement = 'carte' OR paiement = 'cheque' OR paiement = 'monnaie') AND (statut = 'bronze' OR statut = 'silver' OR statut = 'gold' OR statut = 'platine')),
    CHECK ((occasionnel = FALSE AND carte IS NOT NULL AND statut IS NOT NULL) OR (occasionnel = true AND carte IS NULL AND statut IS NULL))
);

CREATE TABLE Billet (
    id_billet INT PRIMARY KEY,
    assurance BOOLEAN NOT NULL,
    prix FLOAT NOT NULL,
    voyageur_nom VARCHAR(20) NOT NULL,
    voyageur_prenom VARCHAR(20) NOT NULL,
    voyageur_adresse VARCHAR(80) NOT NULL,
    FOREIGN KEY (voyageur_nom, voyageur_prenom, voyageur_adresse) REFERENCES Voyageur(nom, prenom, adresse)
);

CREATE TABLE CompositionBillet (
    billet INT REFERENCES Billet(id_billet),
    trajet INT REFERENCES Trajet(id_trajet),
    PRIMARY KEY (billet, trajet)
);


-- L'attribut date dans Trajet doit être une date présente dans le Calendrier du Voyage et non supprimée dans DateException, ou bien une date ajoutée dans DateException du Voyage.
-- Il faut s'assurer que l'horaire de Voyage (présente dans Calendrier) est égale à l'heure de départ du premier ArretVoyage.
-- Il faut s'assurer que le nombre de places réservées ne dépasse pas nb_places du TypeTrain pour chaque Voyage.


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

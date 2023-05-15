import psycopg2
from datetime import date


database = input("A quelle base de données voulez-vous vous connecter ? ")
host = input("Quel est l'host ? ")
user = input("Entrez votre nom d'utilisateur : ")
password = input("Entrez votre mot de passe : ")

# Connect to the PostgreSQL database server
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)


cur = conn.cursor()

def check_bdd():
    status = True

    # VIEWS vérifier les contraintes sur les projections

    sql = "SELECT * FROM v_DisposeHotel;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : l'hotel '%s' à l'adresse '%s' n'est relié à aucune gare." % row)
        status = False

    sql = "SELECT * FROM v_DisposeTaxi;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le taxi '%d' n'est relié à aucune gare." % row)
        status = False

    sql = "SELECT * FROM v_DisposeTransportPublic;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le transport public '%d' n'est relié à aucune gare." % row)
        status = False

    sql = "SELECT * FROM v_ArretLigne;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : la ligne '%d' doit être reliée à au moins 2 gares (actuellement relié à %d gare)." % (row[1], row[0]))
        status = False

    sql = "SELECT * FROM v_Voyage;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : la ligne '%d' doit être reliée à au moins 1 voyage." % row)
        status = False

    sql = "SELECT * FROM v_ConcerneCalendrier;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : la date-exception '%s' (ajout : %s) doit être reliée à au moins 1 calendrier." % row)
        status = False

    sql = "SELECT * FROM v_ArretVoyage;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le voyage '%d' doit être relié à au moins 2 arrêts de ligne (actuellement relié à %d arrêt)." % (row[1], row[0]))
        status = False

    sql = "SELECT * FROM v_ArretVoyage2;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le voyage '%d' est relié à la ligne '%d' mais ce n'est pas le cas d'au moins 1 de ses arrêts." % row)
        status = False

    sql = "SELECT * FROM v_ArretTrajet;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le trajet '%d' doit avoir exactement 2 arrêts (il en a actuellement %s)." % (row[1], row[0]))
        status = False

    sql = "SELECT * FROM v_CompositionBillet;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le billet '%d' n'a pas de trajet." % row)
        status = False

    sql = "SELECT * FROM v_LigneVoyageTypeTrain;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le voyage '%d' est assuré par un %s (train %s), mais sa ligne associée ('%s') est assurée par un %s" % (row[1], row[0], row[3], row[2], row[4]))
        status = False

    #===========================================================================================================
    # CHECK

    sql = "SELECT id_trajet, trajet_date, id_calendrier, date_debut, date_fin, lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche FROM v_CheckDate WHERE (trajet_date >= date_debut AND trajet_date <= date_fin AND ajout <> FALSE)"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        day = row[1].weekday()
        if not row[day + 5]:
            print("Erreur sur les données dans la base : la date (%s) du trajet '%d' est en contradiction avec le calendrier '%d' (date sur un jour de la semaine non possible)." % (row[1], row[0], row[2]))
            status = False

    sql = "SELECT id_trajet, trajet_date, id_calendrier FROM v_CheckDate WHERE (((trajet_date < date_debut OR trajet_date > date_fin) AND ajout <> TRUE) OR ajout = FALSE)"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : la date (%s) du trajet '%d' est en contradiction avec le calendrier '%d'." % (row[1], row[0], row[2]))
        status = False

    sql = "SELECT * FROM v_CheckTime;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le voyage '%d' est programmé a %s dans le calendrier, mais il part à %s d'après l'arrêt de départ." % (row[2], row[0], row[1]))
        status = False

    sql = "SELECT * FROM v_CheckPlace;"
    cur.execute(sql)
    row = cur.fetchone()
    while row:
        if row[0] < row[3]:
            print("Plus de places ont été vendues que le nombre de places dans le train pour le voyage %d du %s." % (row[2], row[1]))
            status = False
        if row[0] == row[3]:
            print("Le train du voyage %d le %s est complet." % (row[2], row[1]))
            status = False
        row = cur.fetchone()

    return status

# ===========================================================================================================
#
# SELECT requêtes


# Créer un voyageur
def creer_compte_voyageur():
    print("----- Création d'un compte voyageur -----")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    adresse = input("Adresse : ")
    telephone = input("Téléphone : ")
    paiement = input("Méthode de paiement (carte/cheque/monnaie) : ")
    occasionnel = input("Voyageur occasionnel ? oui/non (entrez autre chose que oui) : ")
    carte = None
    statut = None
    if occasionnel.lower() != "oui":
        carte = input("Numéro de carte : ")
        statut = input("Statut (bronze/silver/gold/platine) : ")
        try:
            carte = int(carte)
        except ValueError:
            print("\nERREUR : Veuillez entrer un entier pour le numéro de carte.")
            return
        if statut.lower() not in ["bronze", "silver", "gold", "platine"]:
            print("\nERREUR : Veuillez entrer 'bronze', 'silver', 'gold', ou 'platine' comme statut.")
            return
    # Conversion
    occasionnel = True if occasionnel.lower() == "oui" else False
    # Verification Donnees completes
    if not nom or not prenom or not adresse or not telephone or not paiement:
        print("\nERREUR : Veuillez fournir toutes les informations nécessaires pour créer le compte voyageur.")
        return
    if paiement.lower() not in ["carte", "cheque", "monnaie"]:
        print("\nERREUR : Veuillez entrer 'carte', 'cheque', ou 'monnaie' comme moyen de paiement.")
        return
    # Verification si le voyageur existe deja dans la base d
    cur.execute(
        "SELECT COUNT(*) FROM Voyageur WHERE nom = %s AND prenom = %s AND adresse = %s",
        (nom, prenom, adresse)
    )
    count = cur.fetchone()[0]
    if count > 0:
        print("\nERREUR : Le voyageur existe déjà dans la base de données.")
        return
    # Insertion du compte voyageur dans la base de données
    try:
        cur.execute(
            "INSERT INTO Voyageur (nom, prenom, adresse, telephone, paiement, carte, statut, occasionnel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nom, prenom, adresse, telephone, paiement, carte, statut, occasionnel)
        )
        conn.commit()
        print("\nLe compte voyageur a été créé avec succès.")
    except psycopg2.Error as e:
        print("\nERREUR : Une erreur s'est produite lors de la création du compte voyageur :", e)


def achat_billet(voyageur_nom, voyageur_prenom, voyageur_adresse, ligne, num_arret_voyage):
    try:
        # Voyageur existe-t-il ?
        cursor.execute(
            "SELECT COUNT(*) FROM Voyageur "
            "WHERE nom = %s AND prenom = %s AND adresse = %s",
            (voyageur_nom, voyageur_prenom, voyageur_adresse)
        )
    except psycopg2.Error as e:
        print("\nERREUR : Une erreur s'est produite : ", e)
        return

        traveler_exists = cursor.fetchone()[0]

        if not traveler_exists:
            print("Le voyageur n'existe pas vous devez d'abord le créer.")
            creer_compte_voyageur()

        # recupérer le prix du billet
        try:
            cursor.execute(
                "SELECT prix FROM Billet "
                "JOIN CompositionBillet ON Billet.id_billet = CompositionBillet.billet "
                "JOIN Trajet ON CompositionBillet.trajet = Trajet.id_trajet "
                "JOIN ArretTrajet ON Trajet.id_trajet = ArretTrajet.trajet "
                "WHERE voyageur_nom = %s AND voyageur_prenom = %s AND voyageur_adresse = %s "
                "AND ArretTrajet.num_arret_voyage = %s AND ArretTrajet.voyage = %s",
                (voyageur_nom, voyageur_prenom, voyageur_adresse, num_arret_voyage, ligne)
            )
        except psycopg2.Error as e:
            print("\nERREUR : Une erreur s'est produite : ", e)
            return

        prix = cursor.fetchone()[0]

        # Insertion d'un billet dans la base
        try:
            cursor.execute(
                "INSERT INTO Billet (assurance, prix, voyageur_nom, voyageur_prenom, voyageur_adresse) "
                "VALUES (FALSE, %s, %s, %s, %s) RETURNING id_billet",
                (prix, voyageur_nom, voyageur_prenom, voyageur_adresse)
            )
        except psycopg2.Error as e:
            print("\nERREUR : Une erreur s'est produite : ", e)
            return

        # recupère l'ID du billet
        billet_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()

        return prix, billet_id


# Consulter la liste des voyages
def consulter_voyages_proposes():
    print("----- Voyages proposés -----")
    try:
        cur.execute("SELECT ArretVoyage.ligne, ArretVoyage.voyage, ArretVoyage.num_arret, ArretLigne.nom_gare, ArretLigne.ville_gare, ArretVoyage.heure_depart, ArretVoyage.heure_arrivee FROM ArretVoyage JOIN ArretLigne ON Arretligne.ligne = ArretVoyage.ligne AND ArretLigne.num_arret = ArretVoyage.arret_ligne ORDER BY (ArretVoyage.ligne, ArretVoyage.voyage, ArretVoyage.num_arret)")
        voyages = cur.fetchall()
        if voyages:
            print("\nLigne, voyage, numéro d'arrêt, gare de départ, ville de départ, heure de depart, heure d'arrivée")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for voyage in voyages:
                print("%d, %d, %d, %s, %s, %s, %s" % voyage)
        else:
            print("\nAucun voyage n'est actuellement proposé.")
    except psycopg2.Error as e:
        print("\nERREUR : Une erreur s'est produite lors de la récupération des voyages proposés :", e)


# Consulter les horaires d'un train
def consulter_horaire_train(ville_depart, ville_arrivee):
    ville_depart = ville_depart.title()
    ville_arrivee = ville_arrivee.title()
    # SQL pour trouver train en fonction des infos
    cur.execute(
        """SELECT v1.voyage, v1.ligne, v1.heure_depart, v1.nom_gare AS gare_depart, v1.ville_gare AS ville_depart, v2.heure_arrivee, v2.nom_gare AS gare_arrivee, v2.ville_gare AS ville_arrivee
        FROM v_VilleVoyage v1
        JOIN v_VilleVoyage v2 ON v1.voyage = v2.voyage
        WHERE v1.num_arret_voyage < v2.num_arret_voyage AND v1.ville_gare = '%s' AND v2.ville_gare = '%s'"""
        % (ville_depart, ville_arrivee)
    )
    results = cur.fetchall()
    if results:
        print(f"\nHoraires des trains de {ville_depart} à {ville_arrivee} :")
        for row in results:
            print("Voyage ID : %s, Ligne : %s, Départ : %s, Gare : %s, Ville : %s, Arrivé : %s, Gare : %s, Ville : %s" % row)
    else:
        print(f"\nPas de train allant de {ville_depart} à {ville_arrivee}.")


# Consulter un aller simple en fonction de la date, de la gare, du départ et de l'arrivée donnés par l'utilisateur
def consulter_voyage_aller_simple_date_gare():
    date_trajet = date.fromisoformat(input("Entrer la date (YYYY-MM-DD) : "))
    ville_depart = input("Entrer la ville de depart : ").title()
    ville_arrivee = input("Entrer la ville d'arrivee : ").title()
    # SQL pour rechercher trajet en fonction des données entrees par le user
    cursor = conn.cursor()
    cursor.execute(
        """SELECT v1.voyage, v1.ligne, v1.heure_depart, v1.nom_gare AS gare_depart, v1.ville_gare AS ville_depart, v2.heure_arrivee, v2.nom_gare AS gare_arrivee, v2.ville_gare AS ville_arrivee, c.date_debut, c.date_fin, c.lundi, c.mardi, c.mercredi, c.jeudi, c.vendredi, c.samedi, c.dimanche, cc.date_exception, cc.ajout_exception
        FROM v_VilleVoyage v1
        JOIN v_VilleVoyage v2 ON v1.voyage = v2.voyage
        JOIN Voyage v ON v1.voyage = v.id_voyage
        JOIN Calendrier c ON v.calendrier = c.id_calendrier
        LEFT OUTER JOIN ConcerneCalendrier cc ON c.id_calendrier = cc.calendrier
        WHERE v1.num_arret_voyage < v2.num_arret_voyage AND v1.ville_gare = '%s' AND v2.ville_gare = '%s'"""
        % (ville_depart, ville_arrivee)
    )
    results = cursor.fetchall()
    if results:
        to_print = True
        for row in results:
            if (date_trajet >= row[8] and date_trajet <= row[9] and row[date_trajet.weekday() + 5] and row[17] != date_trajet) or (row[17] == date_trajet and row[18] == True):
                if to_print:
                    print(f"Voyages le {date_trajet} de {ville_depart} à {ville_arrivee}:")
                    to_print = False
                print("Date : %s, Voyage ID : %s, Ligne : %s, Départ : %s, Gare : %s, Ville : %s, Arrivé : %s, Gare : %s, Ville : %s" % (date_trajet, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        if to_print:
            print(f"Pas de trajet pour le {date_trajet} de {ville_depart} à {ville_arrivee}.")
    else:
        print(f"Pas de trajet pour le {date_trajet} de {ville_depart} à {ville_arrivee}.")


# Ajouter une gare
def ajouter_gare():
    sql = "SELECT nom, ville FROM Gare;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Gares dans la base de données :")
    for row in rows:
        print("Nom : %s\tVille : %s" % row)

    verif = 0
    while verif == 0 :
        nom = input("Nom de la gare : ")
        ville = input("Ville de la gare : ")
        sql = "SELECT nom FROM Gare WHERE nom='%s' AND ville='%s';" % (nom,ville)
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows :
            verif = 1
        else :
            print("Cette gare existe déjà.")
            print("\nVeuillez en saisir une autre.")

    adresse = input("Adresse : ")
    pays = input("Pays : ")

    try:
        sql = "INSERT INTO Gare VALUES ('%s','%s','%s','%s');" % (nom,ville,adresse,pays)
        cur.execute(sql)
        conn.commit()
        print("Gare ajoutée.")
    except psycopg2.Error as e:
        print("ERREUR :", e)
        return


# # Modifier une gare
# def modifier_gare():
#     sql = "SELECT nom, ville FROM Gare;"
#     cur.execute(sql)
#     rows = cur.fetchall()
#     print("Gares dans la base de données :")
#     for row in rows:
#         print("Nom : %s\tVille : %s" % row)
#
#     verif = 0
#     while verif == 0 :
#         nom = input("Nom de la gare : ")
#         ville = input("Ville de la gare : ")
#         sql = "SELECT nom FROM Gare WHERE nom='%s' AND ville='%s';" % (nom,ville)
#         cur.execute(sql)
#         rows = cur.fetchall()
#         if rows :
#             verif = 1
#         else :
#             print("Cette gare n'existe pas.")
#             print("\nVeuillez en saisir une autre.")
#
# A FINIR (concerne DisposeHotel, DisposeTaxi, DisposeTransportPublic, ArretLigne)


# Ajouter un train
def ajouter_train():
    sql = "SELECT * FROM Train;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Trains dans la base de données :")
    for row in rows:
        print("Numéro : %i\tType de trains : %s" % row)

    verif = 0
    while verif == 0 :
        try:
            train = int(input("Numéro du train : "))
        except ValueError:
            print("\nVeuillez entrer un numéro.")
            continue
        sql = "SELECT num FROM Train WHERE num=%i;" % train
        cur.execute(sql)
        rows = cur.fetchall()
        if not rows :
            verif = 1
        else :
            print("Le numéro de train existe déjà.")
            print("\nVeuillez en saisir un autre.")

    sql = "SELECT nom FROM TypeTrain;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Types de train dans la base de données :")
    for row in rows:
        print("%s"%(row))

    verif = 0
    while verif == 0 :
        type_train = input("Type de train : ")
        sql = "SELECT nom FROM TypeTrain WHERE nom='%s';" % type_train
        cur.execute(sql)
        rows = cur.fetchall()
        if rows :
            verif = 1
        else :
            print("Le type de train n'existe pas.")
            print("\nVeuillez en saisir un autre.")

    try:
        sql = "INSERT INTO Train VALUES (%i, '%s');" % (train, type_train)
        cur.execute(sql)
        conn.commit()
        print("Train ajouté.")
    except psycopg2.Error as e:
        print("ERREUR :", e)
        return


# Modifier un train
def modifier_train():
    sql = "SELECT * FROM Train;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Trains dans la base de données : ")
    for row in rows:
        print("Numéro : %i\tType de train : %s;" % row)

    verif = 0
    while verif == 0 :
        try:
            train = int(input("Numéro de train : "))
        except ValueError:
            print("\nVeuillez entrer un numéro.")
            continue
        sql = "SELECT num, type_train FROM Train WHERE num=%i;" % train
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            type_train = row[1]
            verif = 1
        else:
            print("Le numéro de train n'existe pas.")
            print("\nVeuillez en saisir un autre.")

    sql = "SELECT id_voyage FROM Voyage WHERE train=%i;" % train
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        id_voyage = row
        verif = 0
        while verif == 0 :
            try:
                nv_train = int(input("Par quel train voulez-vous remplacer le train du voyage %d ? " % id_voyage))
            except ValueError:
                print("\nVeuillez entrer un numéro.")
                continue
            sql = "SELECT num, type_train FROM Train WHERE num=%i;" % nv_train
            cur.execute(sql)
            row = cur.fetchone()
            if row and type_train == row[1]:
                verif = 1
            else:
                if not row:
                    print("Le numéro de train n'existe pas.")
                else:
                    print("Il faut un train du même type.")
                print("\nVeuillez en saisir un autre.")
        try:
            sql= "UPDATE Voyage SET train=%i WHERE train=%i;" % (nv_train, train)
            cur.execute(sql)
            conn.commit()
            print("Train mis à jour.")
        except psycopg2.Error as e:
            print("ERREUR :", e)
            return

    sql = "SELECT nom FROM TypeTrain;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Types de train dans la base de données :")
    for row in rows:
        print(row[0])

    verif = 0
    while verif == 0 :
        type_train = input("Type de train : ")
        sql = "SELECT nom FROM TypeTrain WHERE nom='%s';" % type_train
        cur.execute(sql)
        rows = cur.fetchall()
        if rows :
            verif = 1
        else :
            print("Le type de train n'existe pas.")
            print("\nVeuillez en saisir un autre.")
    try:
        sql = "UPDATE Train SET type_train='%s' WHERE num=%i;" % (type_train, train)
        cur.execute(sql)
        conn.commit()
        print("Type du train modifié.")
    except psycopg2.Error as e:
        print("ERREUR :", e)
        return


# Modifier un train
def modifier_train():
    sql = "SELECT * FROM Train;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Trains dans la base de données : ")
    for row in rows:
        print("Numéro : %i\tType de train : %s;" % row)

    verif = 0
    while verif == 0 :
        try:
            train = int(input("Numéro de train : "))
        except ValueError:
            print("\nVeuillez entrer un numéro.")
            continue
        sql = "SELECT num, type_train FROM Train WHERE num=%i;" % train
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            type_train = row[1]
            verif = 1
        else:
            print("Le numéro de train n'existe pas.")
            print("\nVeuillez en saisir un autre.")

    sql = "SELECT id_voyage FROM Voyage WHERE train=%i;" % train
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        id_voyage = row
        verif = 0
        while verif == 0 :
            try:
                nv_train = int(input("Par quel train voulez-vous remplacer le train du voyage %d ? " % id_voyage))
            except ValueError:
                print("\nVeuillez entrer un numéro.")
                continue
            sql = "SELECT num, type_train FROM Train WHERE num=%i;" % nv_train
            cur.execute(sql)
            row = cur.fetchone()
            if row and type_train == row[1]:
                verif = 1
            else:
                if not row:
                    print("Le numéro de train n'existe pas.")
                else:
                    print("Il faut un train du même type.")
                print("\nVeuillez en saisir un autre.")
        try:
            sql= "UPDATE Voyage SET train=%i WHERE train=%i;" % (nv_train, train)
            cur.execute(sql)
            conn.commit()
            print("Train mis à jour.")
        except psycopg2.Error as e:
            print("ERREUR :", e)
            return

    try:
        sql = "DELETE FROM Train WHERE num=%i;" % train
        cur.execute(sql)
        conn.commit()
        print("Train supprimé.")
    except psycopg2.Error as e:
        print("ERREUR :", e)
        return


# Statistiques

# Affiche le nombre de trajets par date (SELECT COUNT)
def nb_trajets_par_date():
    sql = "SELECT date_, COUNT(*) AS nombre_trajets FROM Trajet GROUP BY date_;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Voici le nombre de trajets par date :")
    for row in rows:
        print("\tDate : %s\tNombre de trajets : %s" % (row))

# Affiche le nombre de voyages par ligne de train (SELECT COUNT)
def nb_voyages_par_ligne():
    print("Nombre de voyages par ligne de train :")
    sql = "SELECT Ligne.num, COUNT(*) AS nombre_voyages FROM Voyage JOIN Ligne ON Voyage.ligne = Ligne.num GROUP BY Ligne.num;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows :
        print("\tLigne : %s\tNombre de voyages : %i"%(row))

# Affiche l'argent gagné par la société (SELECT SUM) (= total des prix des billets)
def argent_gagne():
    sql = "SELECT SUM(prix) AS somme_prix FROM Billet;"
    cur.execute(sql)
    row = cur.fetchall()
    print("Argent gagné par la société : %s" % row[0])

# Affiche la somme des prix des billets par voyageur (SELECT SUM)
def argent_par_voyageur():
    print("Somme des prix des billets par voyageur :")
    sql = "SELECT voyageur_nom, voyageur_prenom, voyageur_adresse, SUM(prix) AS somme_prix FROM Billet GROUP BY voyageur_nom, voyageur_prenom, voyageur_adresse;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\tNom : %s\tPrénom : %s\tAdresse : %s\tArgent dépensé : %s"% row)

# Afficher le nombre de voyages par jour de la semaine (SELECT CASE)
def nb_voyages_par_jour():
    print("Nombre de voyages par jour de la semaine :")
    sql = "SELECT CASE WHEN lundi THEN 'Lundi' WHEN mardi THEN 'Mardi' WHEN mercredi THEN 'Mercredi' WHEN jeudi THEN 'Jeudi' WHEN vendredi THEN 'Vendredi' WHEN samedi THEN 'Samedi' WHEN dimanche THEN 'Dimanche' END AS jour_semaine, COUNT(*) AS nombre_voyages FROM Calendrier JOIN Voyage ON Calendrier.id_calendrier = Voyage.calendrier GROUP BY jour_semaine;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\tJour : %s\tNombre de voyages : %i"%(row))

# Affiche le nom/prenom/adresse des/du voyageur.s ayant le statut bronze (SELECT WHERE)
def voyageur_bronze():
    print("Voyageurs ayant le statut bronze :")
    sql = "SELECT nom, prenom, adresse FROM Voyageur WHERE statut = 'bronze';"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\tNom : %s\tPrenom : %s\tAdresse : %s"%(row))

# Récupère le taux de remplissage des trains (en %)
def taux_remplissage():
    print("Taux de remplissage des trains :")
    sql = "SELECT id_voyage, date_, CAST((nb_billets * 100.0) / nb_places AS numeric(3,2)) AS taux_remplissage FROM v_CheckPlace;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\tNuméro de voyage : %i\tDate : %s\tTaux de remplissage : %s"%(row))



if check_bdd():

    # MENU

    print()
    choice = 1
    while choice == 1 or choice == 2:
        print("Choix du profil :")
        print ("\n1 : voyageur")
        print ("\n2 : membre de la société")
        print ("\nAutre numéro : sortie\n")
        try:
            choice = int(input("Votre choix : "))
        except ValueError:
            choice = 0
        if choice == 1:
            while choice in range(1, 10):
                print("\nChoix de l'action :")
                print("\n1 : créer un compte voyageur")
                print("\n2 : acheter un billet") # A CORRIGER
                print("\n3 : consulter la liste des voyages")
                print("\n4 : consulter les horaires de trains en fonction de la gare de départ et d'arrivée")
                print("\n5 : chercher un voyage aller simple en fonction de la date/gare donnée")
                print("\n6 : annuler (ou modifier un voyage)") # A FAIRE
                print("\n7 : revenir en arrière dans le menu")
                print("\nAutre numéro : sortie\n")
                try:
                    choice = int(input("Votre choix : "))
                except ValueError:
                    choice = 0
                if choice == 1:
                    print()
                    creer_compte_voyageur()
                    input()
                if choice == 2:
                    print("Achat d'un billet")
                    voyageur_nom = input("Entrez votre nom : ")
                    voyageur_prenom = input("Entrez votre prénom: ")
                    voyageur_adresse = input("Entrez votre adresse: ")
                    ligne = int(input("Entrez le numéro de la ligne: "))
                    num_arret_voyage = int(input("Entrez le numéro de l'arrêt: "))
                    prix, billet_id = achat_billet(voyageur_nom, voyageur_prenom, voyageur_adresse, ligne, num_arret_voyage)
                    print("Billet acheté avec succès!")
                    print("Prix de votre billet:", prix)
                    print("Numéro (id) du billet:", billet_id)
                if choice == 3:
                    print()
                    consulter_voyages_proposes()
                    input()
                if choice == 4:
                    print()
                    ville_depart = input("Entrez la gare de ville de départ : ")
                    ville_arrivee = input("Entrez la gare de ville d'arrivée : ")
                    consulter_horaire_train(ville_depart, ville_arrivee)
                    input()
                if choice == 5:
                    print()
                    consulter_voyage_aller_simple_date_gare()
                    input()
                if choice == 6:
                    print()
                    print("Fonction Python 6")
                    input()
                if choice == 7:
                    print()
                    choice = 1
                    break
        if choice == 2:
            while choice in range(1, 9):
                print("\nChoix de l'action :")
                print("\n1 : ajouter une gare")
                print("\n2 : modifier une gare") # A FAIRE -> même modèle que train, pas de supprimer()
                print("\n3 : ajouter un train")
                print("\n4 : supprimer un train")
                print("\n5 : modifier le type d'un train")
                print("\n6 : ajouter une ligne") # PROBLEMES
                print("\n7 : supprimer une ligne") # PROBLEMES
                print("\n8 : modifier une ligne") # PROBLEMES
                print("\n9 : statistiques sur la société")
                print("\n10 : revenir en arrière")
                print("\nAutre numéro : sortie")
                try:
                    choice = int(input("Votre choix : "))
                except ValueError:
                    choice = 0
                if choice == 1:
                    print()
                    ajouter_gare()
                    input()
                if choice == 2:
                    print()
                    print("Fonction Python 2")
                    input()
                if choice == 3:
                    print()
                    ajouter_train()
                    input()
                if choice == 4:
                    print()
                    modifier_train()
                    input()
                if choice == 5:
                    print()
                    supprimer_train()
                    input()
                if choice == 6:
                    print()
                    ajouter_ligne()
                    input()
                if choice == 7:
                    print()
                    supprimer_ligne()
                    input()
                if choice == 8:
                    print()
                    modifier_ligne()
                    input()
                if choice == 9:
                    print()
                    nb_trajets_par_date()
                    print()
                    nb_voyages_par_ligne()
                    print()
                    nb_voyages_par_jour()
                    print()
                    argent_gagne()
                    print()
                    argent_par_voyageur()
                    print()
                    voyageur_bronze()
                    print()
                    taux_remplissage()
                    print()
                    input()
                if choice == 10:
                    print()
                    choice = 1
                    break

    print("\nAu revoir")

conn.close()

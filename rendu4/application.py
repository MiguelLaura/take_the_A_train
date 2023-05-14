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
        print("Erreur sur les données dans la base : le trajet '%d' doit être relié à au moins 2 gares (actuellement relié à %d gare)." % (row[1], row[0]))
        status = False

    sql = "SELECT * FROM v_Voyage;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : la ligne '%s' doit être reliée à au moins 1 voyage." % row)
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

    # Check date
    # 1er cas:
    # - date complète date_début et date_fin
    # - date => jour vrai
    # - date.except => date = date_except avec ajout false
    #
    # 2e cas:
    # - date=date_except avec ajout true
    #
    sql = "SELECT id_trajet, trajet_date, id_calendrier, date_debut, date_fin, lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche FROM v_CheckDate WHERE (trajet_date >= date_debut AND trajet_date <= date_fin AND ajout)"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        day = row[1].weekday()
        if not row[day + 5]:
            print("Erreur sur les données dans la base : la date (%s) du trajet '%d' est en contradiction avec le calendrier '%d' (date sur un jour de la semaine non possible)." % (row[1], row[0], row[2]))
            status = False

    sql = "SELECT id_trajet, trajet_date, id_calendrier FROM v_CheckDate WHERE (((trajet_date < date_debut OR trajet_date > date_fin) AND NOT ajout) OR NOT ajout)"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : la date (%s) du trajet '%d' est en contradiction avec le calendrier '%d'." % (row[1], row[0], row[2]))
        status = False

    #  check time
    sql = "SELECT * FROM v_CheckTime;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("Erreur sur les données dans la base : le voyage '%d' est programmé a %s dans le calendrier, mais il part à %s d'après l'arrêt de départ." % (row[2], row[0], row[1]))
        status = False

    # check place
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

# INSERT un billet
# if row[0] == row[2]:
#     print("train complet")

# ===========================================================================================================
#
# SELECT requêtes

# Affiche le nombre de trajets par date (SELECT COUNT)
def nb_trajets_par_date():
    sql = "SELECT date_, COUNT(*) AS nombre_trajets FROM Trajet GROUP BY date_;"
    cur.execute(sql)
    rows = cur.fetchall()
    print("Voici le nombre de trajets par date :")
    for row in rows:
        print("\tDate : %s\tNombre de trajets : %s" % (row))

#Affiche le nombre de voyages par ligne de train (SELECT COUNT)
#Elisa
def nb_voyages_par_ligne():
    print("Nombre de voyages par ligne de train :\n")
    sql = "SELECT Ligne.num, COUNT(*) AS nombre_voyages FROM Voyage JOIN Ligne ON Voyage.ligne = Ligne.num GROUP BY Ligne.num;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows :
        print("\nLigne : %s\tNombre de voyages : %i"%(row))

#Affiche l'argent gagné par la société (SELECT SUM) (= total des prix des billets)
#Elisa
def argent_gagne():
    sql = "SELECT SUM(prix) AS somme_prix FROM Billet;"
    cur.execute(sql)
    row = cur.fetchall()
    print("Argent gagné par la société : %f"%(row))

#Affiche la somme des prix des billets par voyageur (SELECT SUM)
#Elisa
def argent_par_voyageur():
    print("Somme des prix des billets par voyageur :\n")
    sql = "SELECT voyageur_nom, voyageur_prenom, voyageur_adresse, SUM(prix) AS somme_prix FROM Billet GROUP BY voyageur_nom, voyageur_prenom, voyageur_adresse;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\nNom : %s\tPrénom : %s\tAdresse : %s\tArgent dépensé : %f"%(row))

#Afficher le nombre de voyages par jour de la semaine (SELECT CASE)
#Elisa
def nb_voyages_par_jour():
    print("Nombre de voyages par jour de la semaine :\n")
    sql = "SELECT CASE WHEN lundi THEN 'Lundi' WHEN mardi THEN 'Mardi' WHEN mercredi THEN 'Mercredi' WHEN jeudi THEN 'Jeudi' WHEN vendredi THEN 'Vendredi' WHEN samedi THEN 'Samedi' WHEN dimanche THEN 'Dimanche' END AS jour_semaine, COUNT(*) AS nombre_voyages FROM Calendrier JOIN Voyage ON Calendrier.id_calendrier = Voyage.calendrier GROUP BY jour_semaine;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\nJour : %s\tNombre de voyages : %i"%(row))

#Affiche le nom/prenom/adresse des/du voyageur.s ayant le statut bronze (SELECT WHERE)
#Elisa
def voyageur_bronze():
    print("Voyageurs ayant le statut bronze :\n")
    sql = "SELECT nom, prenom, adresse FROM Voyageur WHERE statut = 'bronze';"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\nNom : %s\tPrenom : %s\tAdresse : %s"%(row))

#Récupère le taux de remplissage des trains (en %)
#Elisa
def taux_remplissage():
    print("Taux de remplissage des trains :\n")
    sql = "SELECT id_voyage, date_, CAST((nb_billets * 100.0) / nb_places AS numeric(3,2)) AS taux_remplissage FROM v_CheckPlace;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print("\nNuméro de voyage : %i\tDate : %s\tTaux de remplissage : %f"%(row))

# Création d'un voyageur
#Elisa
def creer_voyageur():
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    adresse = input("Adresse : ")
    tel = input("Téléphone : ")
    paiement = input("Moyen de paiement : ")
    occas = input("Entrez 1 si vous voulez être un voyageur occasionnel, 0 sinon : ")
    
    sql = "SELECT * FROM Voyageur WHERE nom=%s AND prenom=%s AND adresse=%s;"%(nom,prenom,adresse)
    cur.execute(sql)
    rows = cur.fetchall()
    
    if rows :
        print("Vous êtes déjà inscrit.")
    else :
        if occas == 1:
            try :
                sql = "INSERT INTO Voyageur VALUES (%s,%s,%s,%s,%s,NULL,NULL,true);"%(nom,prenom,adresse,tel,paiement)
                cur.execute(sql)
                conn.commit()
            except psycopg2.Error as e:
                print("Erreur : ",e)
        else :
            verif = 0
            while verif == 0 :
                carte = int(input("Numéro de carte"))
                sql = "SELECT carte FROM Voyageur WHERE carte=%i;"%carte
                cur.execute(sql)
                rows = cur.fetchall()
                if not rows :
                    verif = 1
                else :
                    print("Le numéro de carte existe déjà.")
                    print("\n Veuillez en saisir un autre.")
            statut = input("Statut :")
            try :
                sql = "INSERT INTO Voyageur VALUES (%s,%s,%s,%s,%s,%i,%s,false);"%(nom,prenom,adresse,tel,paiement,carte,statut)
                cur.execute(sql)
                conn.commit()
            except psycopg2.Error as e:
                print("Erreur : ",e)

#creerVoyageur- nadia
def creer_compte_voyageur():
    print("----- Création d'un compte voyageur -----")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    adresse = input("Adresse : ")
    telephone = input("Téléphone : ")
    paiement = input("Méthode de paiement (carte/cheque/monnaie) : ")
    carte = input("Numéro de carte (optionnel) : ")
    statut = input("Statut (bronze/silver/gold/platine) : ")
    occasionnel = input("Voyageur occasionnel ? (oui/non) : ")
    # Conversion 
    occasionnel = True if occasionnel.lower() == "oui" else False
    # Verification Donnees completes
    if not nom or not prenom or not adresse or not telephone or not paiement:
        print("Veuillez fournir toutes les informations nécessaires pour créer le compte voyageur.")
        return
    # Verification si le voyageur existe deja dans la base d
    cursor.execute("SELECT COUNT(*) FROM Voyageur WHERE nom = %s AND prenom = %s AND adresse = %s",
                   (nom, prenom, adresse))
    count = cursor.fetchone()[0]
    if count > 0:
        print("Le voyageur existe déjà dans la base de données.")
        return
    # Insertion du compte voyageur dans la base de données
    try:
        cursor.execute("INSERT INTO Voyageur (nom, prenom, adresse, telephone, paiement, carte, statut, occasionnel) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (nom, prenom, adresse, telephone, paiement, carte, statut, occasionnel))
        conn.commit()
        print("Le compte voyageur a été créé avec succès.")
    except psycopg2.Error as e:
        print("Une erreur s'est produite lors de la création du compte voyageur :", e)

#fonction 3 nadia
def consulter_voyages_proposes():
    print("----- Voyages proposés -----")
    try:
        cursor.execute("SELECT Voyage.num, Ligne.num, Ligne.type_train, ArretLigne.nom_gare_depart, ArretLigne.ville_gare_depart, ArretLigne.nom_gare_arrivee, ArretLigne.ville_gare_arrivee, Voyage.date_depart, Voyage.date_arrivee FROM Voyage "
                       "JOIN Ligne ON Voyage.ligne = Ligne.num "
                       "JOIN ArretLigne ON Ligne.num = ArretLigne.ligne "
                       "WHERE ArretLigne.num_arret = 1") # num_arret=1
        voyages = cursor.fetchall()
        if voyages:
            print("Numéro de voyage\tNuméro de ligne\tType de ligne\tGare de départ\t\tVille de départ\t\tGare d'arrivée\t\tVille d'arrivée\t\tDate de départ\t\tDate d'arrivée")
            print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            for voyage in voyages:
                num_voyage, num_ligne, type_ligne, gare_depart, ville_depart, gare_arrivee, ville_arrivee, date_depart, date_arrivee = voyage
                print(f"{num_voyage}\t\t\t{num_ligne}\t\t\t{type_ligne}\t\t{gare_depart}\t\t{ville_depart}\t\t{gare_arrivee}\t\t{ville_arrivee}\t\t{date_depart}\t\t{date_arrivee}")
        else:
            print("Aucun voyage n'est actuellement proposé.")
    except psycopg2.Error as e:
        print("Une erreur s'est produite lors de la récupération des voyages proposés :", e)


#fonction4 nadia
def consulter_horaire_train(ville_depart, ville_arrivee):
    # SQL pour trouver train en fonction des infos
    cursor.execute('''
        SELECT DISTINCT Voyage.id_voyage, ArretVoyage.heure_depart, ArretVoyage.heure_arrivee
        FROM ArretVoyage
        INNER JOIN Ligne ON ArretVoyage.ligne = Ligne.num
        INNER JOIN Voyage ON ArretVoyage.voyage = Voyage.id_voyage
        INNER JOIN ArretLigne ON ArretVoyage.arret_ligne = ArretLigne.num_arret AND ArretLigne.ligne = Ligne.num
        INNER JOIN Gare AS GareDepart ON ArretLigne.nom_gare = GareDepart.nom AND ArretLigne.ville_gare = GareDepart.ville
        INNER JOIN Gare AS GareArrivee ON ArretLigne.nom_gare = GareArrivee.nom AND ArretLigne.ville_gare = GareArrivee.ville
        WHERE GareDepart.ville = ? AND GareArrivee.ville = ?
    ''', (ville_depart, ville_arrivee))
    results = cursor.fetchall()
    if results:
        print(f"Horaire Trains de {ville_depart} à {ville_arrivee}:")
        for row in results:
            voyage_id, heure-depart, heure_arrivee = row
            print(f"Voyage ID: {voyage_id}, Depart: {heure-depart}, Arrivé: {heure_arrivee}")
    else:
        print(f"Pas de train allant de {ville_depart} à {ville_arrivee}.")



#fonction 5 nadia renvoie aller simple  en fonction de la date/gare depart/arrivee donner par le user
def consulter_trajet_aller_simple_date_gare():
    date_trajet = input("Entrer la date (YYYY-MM-DD): ")
    station_depart = input("Entrer la gare de depart: ")
    station arrivee = input("Entrer la gare d'arrivee: ")
    # SQL pour rechercher trajet en fonction des données entrees par le user
    cursor.execute('''
        SELECT Trajet.id_trajet, Trajet.num_place, Trajet.date_
        FROM Trajet
        INNER JOIN ArretTrajet ON Trajet.id_trajet = ArretTrajet.trajet
        INNER JOIN ArretVoyage ON ArretTrajet.num_arret_voyage = ArretVoyage.num_arret
            AND ArretTrajet.voyage = ArretVoyage.voyage
        INNER JOIN ArretLigne ON ArretVoyage.arret_ligne = ArretLigne.num_arret
            AND ArretVoyage.ligne = ArretLigne.ligne
        INNER JOIN Gare AS GareDepart ON ArretLigne.nom_gare = GareDepart.nom
            AND ArretLigne.ville_gare = GareDepart.ville
        INNER JOIN Gare AS GareArrivee ON ArretLigne.nom_gare = GareArrivee.nom
            AND ArretLigne.ville_gare = GareArrivee.ville
        WHERE Trajet.date_ = ? AND GareDepart.ville = ? AND GareArrivee.ville = ?
    ''', (date_trajet, station_depart, station arrivee))

    results = cursor.fetchall()
    if results:
        print(f"Trajets le {date_trajet} de {station_depart} à {station arrivee}:")
        for row in results:
            trajet_id, num_place, trajet_date = row
            print(f"Trajet ID: {trajet_id}, Num Place: {num_place}, Date: {trajet_date}")
    else:
        print(f"Pas de trajet pour le {date_trajet} de {station_depart} à {station arrivee}.")

 

if check_bdd():

    # MENU

    # Pour le moment, comprend toutes les options dans Menu
    # mais on peut avoir besoin d'en enlever/rassembler
    # (pour-être des sous menus à faire dans les commandes Python)

    print()
    choice = 1
    while choice == 1 or choice == 2:
        print ("Si vous êtes un voyageur, entrez 1")
        print ("Si vous êtes un memebre de la société, entrez 2")
        print ("Pour sortir, entrez autre chose")
        try:
            choice = int(input())
        except ValueError:
            choice = 0
        if choice == 1:
            while choice in range(1, 10):
                print ("Pour créer un compte voyageur, entrez 1")#ok
                print ("Pour acheter un billet, entrez 2")
                print ("Pour consulter la liste des voyages, entrez 3")#ok
                print ("Pour consulter les horaires de trains en fonction de gare de départ et d'arrivée, entrez 4")#ok
                print ("Pour chercher un voyage aller simple en fonction de date/gare donnée, entrez 5") #ok
                print ("Pour chercher un voyage aller/retour en fonction des dates données , entrez 6")
                print ("Pour chercher un trajet en fonction du prix du billet, entrez 7") # ? on le garde ?
                print ("Pour annuler (ou modifier un voyage), entrez 8")
                print ("Pour revenir en arrière, entrez 10")
                print ("Pour sortir, entrez autre chose")
                try:
                    choice = int(input())
                except ValueError:
                    choice = 0
                if choice == 1:
                    print()
                    print("Fonction Python 1")
                    print()
                if choice == 2:
                    print()
                    print("Fonction Python 2")
                    print()
                if choice == 3:
                    print()
                    print("Fonction Python 3")
                    consulter_voyages_proposes()
                if choice == 4:
                    print()
                    print("Fonction Python 4")                    
                    ville_depart = input("Entrer la gare de ville de départ : ")
                    ville_arrivee = input("Entrer la gare de ville d'arrivée: ")
consulter_horaire_train(ville_depart, ville_arrivee)
                if choice == 5:
                    print()
                    print("Fonction Python 5")
                    print()
                if choice == 6:
                    print()
                    print("Fonction Python 6")
                    print()
                if choice == 7:
                    print()
                    print("Fonction Python 7")
                    print()
                if choice == 8:
                    print()
                    print("Fonction Python 8")
                    print()
                if choice == 9:
                    print()
                    print("Fonction Python 9")
                    print()
                if choice == 10:
                    choice = 1
                    print()
                    break
        if choice == 2:
            while choice in range(1, 8):
                print ("Pour gérer les voyages, entrez 1")
                print ("Pour créer un calendrier, entrez 2")
                print ("Pour gérer les gares, entrez 3")
                print ("Pour gérer les trains, entrez 4")
                print ("Pour gérer les lignes, entrez 5")
                print ("Pour obtenir des statistiques sur la société, entrez 6")
                print ("Pour revenir en arrière, entrez 7")
                print ("Pour sortir, entrez autre chose")
                try:
                    choice = int(input())
                except ValueError:
                    choice = 0
                if choice == 1:
                    print()
                    print("Fonction Python 1")
                    creerVoyageur()
                    print()
                if choice == 2:
                    print()
                    print("Fonction Python 2")
                    print()
                if choice == 3:
                    print()
                    print("Fonction Python 3")
                    print()
                if choice == 4:
                    print()
                    print("Fonction Python 4")
                    print()
                if choice == 5:
                    print()
                    print("Fonction Python 5")
                    print()
                if choice == 6:
                    print()
                    nb_trajets_par_date()
                    nb_voyages_par_ligne()
                    nb_voyages_par_jour()
                    argent_gagne()
                    argent_par_voyageur()
                    voyageur_bronze()
                    taux_remplissage()
                    print()
                if choice == 7:
                    choice = 1
                    print()
                    break

    print("Au revoir")

conn.close()

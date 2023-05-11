import psycopg2


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

# VIEWS
sql = "SELECT * FROM v_DisposeHotel;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : l'hotel '%s' à l'adresse '%s' n'est relié à aucune gare." % row)

sql = "SELECT * FROM v_DisposeTaxi;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le taxi '%d' n'est relié à aucune gare." % row)

sql = "SELECT * FROM v_DisposeTransportPublic;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le transport public '%d' n'est relié à aucune gare." % row)

sql = "SELECT * FROM v_ArretLigne;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le trajet '%d' doit être relié à au moins 2 gares (actuellement relié à %d gare)." % (row[1], row[0]))

sql = "SELECT * FROM v_Voyage;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : la ligne '%s' doit être reliée à au moins 1 voyage." % row)

sql = "SELECT * FROM v_ConcerneCalendrier;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : la date-exception '%s' (ajout : %s) doit être reliée à au moins 1 calendrier." % row)

sql = "SELECT * FROM v_ArretVoyage;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le voyage '%d' doit être relié à au moins 2 arrêts de ligne (actuellement relié à %d arrêt)." % (row[1], row[0]))

sql = "SELECT * FROM v_ArretVoyage2;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le voyage '%d' est relié à la ligne '%d' mais ce n'est pas le cas d'au moins 1 de ses arrêts." % row)

sql = "SELECT * FROM v_ArretTrajet;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le trajet '%d' doit avoir exactement 2 arrêt (il en a actuellement %s)." % (row[1], row[0]))

sql = "SELECT * FROM v_CompositionBillet;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le billet '%d' n'a pas de trajet." % row)

sql = "SELECT * FROM v_LigneVoyageTypeTrain;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le voyage '%d' est assuré par un %s (train %s), mais sa ligne associée ('%s') est assurée par un %s" % (row[1], row[0], row[3], row[2], row[4]))


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
# sql = "SELECT * FROM v_CheckTime cd
# WHERE ((trajet_date >= date_debut) AND (trajet_date <= date_fin) AND NOT(trajet_date == date_exception AND ajout == false)) OR (trajet_date == date_exception AND ajout == true);"
# cur.execute(sql)
# row = cur.fetchall()

#  check time
sql = "SELECT * FROM v_CheckTime;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Erreur sur les données dans la base : le voyage '%d' est programmé a µs dans le calendrier, mais il part à %s d'après l'arrêt de départ." % (row[2], row[0], row[1]))


# check place
sql = "SELECT * FROM v_CheckPlace;"
cur.execute(sql)
row = cur.fetchone()
while row:
    if row[0] < row[3]:
        print("Plus de places ont été vendues que le nombre de places dans le train pour le voyage %d du %s." % (row[2], row[1]))
    if row[0] == row[3]:
        print("Le train du voyage %d le %s est complet." % (row[2], row[1]))
    row = cur.fetchone()

# INSERT un billet
# if row[0] == row[2]:
#     print("train complet")
#
# #===========================================================================================================
#
# SELECT requêtes

# Affiche le nombre de trajets par date (SELECT COUNT)
sql = "SELECT date_, COUNT(*) AS nombre_trajets FROM Trajet GROUP BY date_;"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print("Date : %s\tNombre de trajets : %s" % (row))

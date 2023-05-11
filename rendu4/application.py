import psycopg2


# Connect to the PostgreSQL database server
con = psycopg2.connect(
    host="localhost",
    port =1114,
    database="postgres",
    user="postgres",
    password="hu1999414"
)

cur = con.cursor()

#views
sql = "SELECT * FROM v_DisposeHotel;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_DisposeTaxi;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_DisposeTransportPublic;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_ArretLigne;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_Voyage;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_ConcerneCalendrier;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_ArretVoyage;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_ArretVoyage2;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_ArretTrajet;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_CompositionBillet;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)

sql = "SELECT * FROM v_LigneVoyageTypeTrain;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        print(row)



#===========================================================================================================
#CHECK
# Check date
1er cas:
- date complète date_début et date_fin
- date => jour vrai
- date.except => date = date_except avec ajout false

2e cas:
- date=date_except avec ajout true

sql = "SELECT * FROM v_CheckTime cd 
WHERE ((trajet_date >= date_debut) AND (trajet_date <= date_fin) AND NOT(trajet_date == date_exception AND ajout == false)) OR (trajet_date == date_exception AND ajout == true);"
cur.execute(sql)
row = cur.fetchall()
# check place
sql = "SELECT * FROM v_CheckPlace;"
cur.execute(sql)
row = cur.fetchone()
while row:
    if row[0] < row[2]:
        print("err")
    if row[0] == row[2]:
        print("train complet")
    print(row)

# INSERT un billet
if row[0] == row[2]:
    print("train complet")

#===========================================================================================================

#SELECT requêtes
#Affiche le nombre de trajets par date (SELECT COUNT)
sql = "SELECT date_, COUNT(*) AS nombre_trajets FROM Trajet GROUP BY date_;"
cur.execute(sql)
rows = cur.fetchall()
if rows:
    for row in rows:
        date_ = row[0]
        nombre_trajets = row[1]
        print("Date:", date_, "Nombre de trajets:", nombre_trajets)

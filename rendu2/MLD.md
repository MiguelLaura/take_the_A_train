Gare(#nom: string, #adresse: string, ville: string, pays: string) avec ville NOT NULL, pays NOT NULL

Hotel(#nom: string, #adresse: string)

Taxi(#num: int, telephone: string) avec telephone NOT NULL

TransportPublic(#num: int)

DisposeHotel(#nom_gare=>Gare.nom, #adresse_gare=>Gare.adresse, #nom_hotel=>Hotel.nom, #adresse_hotel=>Hotel.adresse) avec Projection(DisposeHotel, nom_hotel, adresse_hotel) = Projection(Hotel, nom, adresse)

DisposeTaxi(#nom_gare=>Gare.nom, #adresse_gare=>Gare.adresse, #num=> Taxi.num) avec Projection(DisposeTaxi, num) = Projection(Taxi, num)

DisposeTransportPublic(#nom_gare=>Gare.nom, #adresse_gare=>Gare.adresse, #num=> TransportPublic.num) avec Projection(DisposeTransportPublic, num) = Projection(TransportPublic, num)

Ligne(#num: int, type_train=>TypeTrain.nom) avec type_train NOT NULL

TypeTrain(#nom: string, nb_places: int, vitesse: int, premiere_classe: bool) avec nb_places NOT NULL, vitesse NOT NULL, premiere_classe NOT NULL, vitesse >=0, nb_places >=0

Train(#num: int, type_train=>TypeTrain.nom) avec type_train NOT NULL

Voyage(#id: int, num_ligne=>Ligne.num, num_train=>Train.num, calendrier=>Calendrier.id) avec num_ligne NOT NULL, num_train NOT NULL, calendrier NOT NULL, Projection(Voyage, num)=Projection(Ligne, num)

Calendrier(#id: int, date_debut: date, date_fin: date, horaire: time, lundi: bool, mardi: bool, mercredi: bool, jeudi: bool, vendredi: bool, samedi: bool, dimanche: bool) avec date_debut NOT NULL, date_fin NOT NULL, horaire NOT NULL, lundi NOT NULL, mardi NOT NULL, mercredi NOT NULL, jeudi NOT NULL, vendredi NOT NULL, samedi NOT NULL, dimanche NOT NULL

DateException(#id: int, date: date, ajout: bool) avec date NOT NULL, ajout NOT NULL

ConcerneCalendrier(#id_calendrier=>Calendrier.id, #id_date_exception=>DateException.id) avec Projection(ConcerneCalendrier, id_date_exception) = Projection(DateException, id)

ArretLigne(#nom_gare=>Gare.nom, #adresse_gare=>Gare.adresse, #num_ligne=>Ligne.num, #num_arret: int, arrive:bool) avec arrive NOT NULL, num_arret >= 1, Projection(ArretLigne, num) = Projection(Ligne, num)

ArretVoyage(#nom_gare=>ArretLigne.nom_gare, #adresse_gare=>ArretLigne.adresse_gare, #num_ligne=>ArretLigne.num_ligne, #num_arret_ligne=>ArretLigne.num_arret, #voyage=>Voyage.id, #num_arret: int, heure_depart: time, heure_arrive: time) avec num_arret NOT NULL, heure_depart > heure_arrive

Trajet(#id: int, num_place: int, date: date) avec date NOT NULL, num_place NOT NULL

ArretTrajet(#id_trajet=>Trajet.id, #nom_gare=>ArretVoyage.nom_gare, #adresse_gare=>ArretVoyage.adresse_gare, #num_ligne=>ArretVoyage.num_ligne, #num_arret_ligne=>ArretVoyage.num_arret_ligne, #voyage=>ArretVoyage.voyage, #num_arret_voyage=>ArretVoyage.num_arret, depart: bool) avec depart NOT NULL, Projection(ArretTrajet, id_trajet) = Projection(Trajet, id)

ComposeDeTrajet(#id_billet=> Billet.id, #id_Trajet=>Trajet.id) avec Projection(ComposedeTrajet, id_billet) = Projection(Billet, id)

Billet(#id: int, assurance: bool, prix: float) avec assurance NOT NULL, prix NOT NULL

# Comment faire les méthodes ? Gare GMT(), Billet annulation/modification
# Comment dire 2..n ? ArretLigne - Ligne / arretTrajet - trajet / arretVoyage - Voyage
# Héritage attribut dans Billet
# sur arretVoyage, heure arrive null <=> num_arret = 0, heure depart num <=> num arret max
# contraintes de la note UML
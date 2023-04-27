Tous les attributs sont considérés NOT NULL (exceptions précisées).

Gare (#nom : str, #ville : str, adresse : str, pays : str)

Hôtel (#nom : str, #adresse : str)

DisposeHôtel (#nom_gare => Gare.nom, # ville_gare => Gare.ville, #nom_hôtel => Hôtel.nom, #adresse_hôtel => Hôtel.adresse) avec < Projection(DisposeHôtel, nom_gare, ville_gare) = Projection(Gare, nom, ville) >

Taxi (#num : int, telephone : str)

DisposeTaxi (#nom_gare => Gare.nom, # ville_gare => Gare.ville, #num_taxi => Taxi.num) avec < Projection(DisposeTaxi, nom_gare, ville_gare) = Projection(Gare, nom, ville) >

TransportPublic (#num : int)

DisposeTransportPublic (#nom_gare => Gare.nom, # ville_gare => Gare.ville, #num_transport_public => TransportPublic.num) avec < Projection(DisposeTransportPublic, nom_gare, ville_gare) = Projection(Gare, nom, ville) >

TypeTrain (#nom : str, nb_places : int, vitesse : int, première_classe : bool) avec < vitesse ≥ 0, nb_places ≥ 0 >

Train (#num : int, type_train => TypeTrain.nom)

Ligne (#num : int, type_train => TypeTrain.nom) avec < (Projection(Ligne,num) = Projection(ArretLigne,ligne))
AND (Une ligne doit relier au moins deux arrêts) >

ArrêtLigne (#num_arrêt : int, #ligne => Ligne.num, arrivé : bool, nom_gare => Gare.nom, ville_gare => Gare.ville) avec < num_arret ≥ 1 >

Calendrier (#id_calendrier : int, date_début : date, date_fin : date, horaire : time, lundi : bool, mardi : bool, mercredi : bool, jeudi : bool, vendredi : bool, samedi : bool, dimanche : bool)

DateException (#date : date, #ajout : bool)

ConcerneCalendrier (#date_exception => DateException.date, #ajout_exception => DateException.ajout, #calendrier => Calendrier.id_calendrier) avec < Projection(ConcerneCalendrier, calendrier) = Projection(Calendrier, id_calendrier) >

Voyage (#id_voyage : int, ligne => Ligne.num, train => Train.num, calendrier => Calendrier.id_calendrier) avec < Projection(Jointure(Train,Voyage, Train.num = Voyage.train), type_train) = Projection(Ligne, type_train) >

ArrêtVoyage (#num_arrêt : int, #voyage => Voyage.id_voyage, heure_départ : time, heure_arrivée : time, arrêt_ligne => ArrêtLigne.num_arrêt, ligne => ArrêtLigne.ligne)
Avec < (Projection(ArrêtVoyage, ligne, voyage) = Projection(Voyage, ligne, id_voyage))
AND (Projection(ArrêtVoyage, voyage) = Projection(Voyage, id_voyage))
AND (Un voyage possède au moins deux arrêts)
AND (heure_départ <  heure_arrivée) >

Trajet (#id_trajet : int, num_arrêt_voyage => ArrêtVoyage.num_arrêt, voyage => ArrêtVoyage.voyage, num_place : int, date : date)
Avec < (Projection(ArrêtVoyage, voyage, num_arrêt) = Projection(Trajet, voyage, num_arrêt_voyage))
AND (Un trajet possède au moins deux arrêts de voyage) >

ArrêtTrajet (#trajet => Trajet.id_trajet, # num_arrêt_voyage => ArrêtVoyage.num_arrêt, #voyage => ArrêtVoyage.voyage), départ : bool)

Voyageur (#nom : str, #prenom : str, #adresse : str, telephone : str, paiement : str, carte : int, statut ; str, occasionnel : bool) avec < (paiement = ‘carte’ OR paiement = ‘chèque’ OR paiement = ‘monnaie’)
AND (statut = ‘bronze’ OR statut = ‘silver’ OR statut = ‘gold’ OR statut = ‘platine’)
AND (occasionnel = false AND carte NOT NULL AND statut NOT NULL)
AND (occasionnel = true AND carte NULL AND statut NULL) >

Billet (#id_billet : int, assurance : bool, prix : float, voyageur_nom => Voyageur.nom, voyageur_prenom => Voyageur.prenom, voyageur_adresse => Voyageur.adresse)

CompositionBillet (#billet => Billet.id_billet, #trajet => Trajet.id_trajet)
Avec < Projection(CompositionBillet, trajet) = Projection(Trajet, id_trajet) >


id_voyage, id_billet, id_trajet et id_calendrier ont été créé pour pouvoir identifier chaque objet d’une classe.

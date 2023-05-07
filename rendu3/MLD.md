Tous les attributs sont considérés NOT NULL (exceptions précisées).

Gare (#nom : str, #ville : str, adresse : str, pays : str)

Hôtel (#nom : str, #adresse : str)

DisposeHôtel (#nom_gare => Gare.nom, #ville_gare => Gare.ville, #nom_hôtel => Hôtel.nom, #adresse_hôtel => Hôtel.adresse) avec <
    Projection(DisposeHotel, nom_hôtel, adresse_hôtel) = Projection(Hôtel, nom, adresse)
    >

Taxi (#num : int, telephone : str)

DisposeTaxi (#nom_gare => Gare.nom, #ville_gare => Gare.ville, #num_taxi => Taxi.num) avec <
    Projection(DisposeTaxi, num_taxi) = Projection(Taxi, num)
    >

TransportPublic (#num : int)

DisposeTransportPublic (#nom_gare => Gare.nom, #ville_gare => Gare.ville, #num_transport_public => TransportPublic.num) avec <
    Projection(DisposeTransportPublic, num_transport_public) = Projection(TransportPublic, num)
    >

TypeTrain (#nom : str, nb_places : int, vitesse : int, première_classe : bool) avec <
    (vitesse ≥ 0)
    AND (nb_places ≥ 0)
    >

Train (#num : int, type_train => TypeTrain.nom)

Ligne (#num : int, type_train => TypeTrain.nom) avec <
    (Projection(Ligne, num) = Projection(ArrêtLigne, ligne))
    AND (une ligne doit relier au moins deux arrêts)
    AND (Projection(Voyage, ligne) = Projection(Ligne, num))
    >

ArrêtLigne (#num_arrêt : int, #ligne => Ligne.num, arrivé : bool, nom_gare => Gare.nom, ville_gare => Gare.ville) avec <
    num_arret ≥ 1
    >

Calendrier (#id_calendrier : int, date_début : date, date_fin : date, horaire : time, lundi : bool, mardi : bool, mercredi : bool, jeudi : bool, vendredi : bool, samedi : bool, dimanche : bool)

DateException (#date : date, #ajout : bool)

ConcerneCalendrier (#date_exception => DateException.date, #ajout_exception => DateException.ajout, #calendrier => Calendrier.id_calendrier) avec <
    Projection(ConcerneCalendrier, date_exception, ajout_exception) = Projection(DateException, date, ajout)
    >

Voyage (#id_voyage : int, ligne => Ligne.num, train => Train.num, calendrier => Calendrier.id_calendrier) avec <
    Projection(Jointure(Train, Voyage, Train.num = Voyage.train), type_train) = Projection(Ligne, type_train)
    >

ArrêtVoyage (#num_arrêt : int, #voyage => Voyage.id_voyage, heure_départ : time, heure_arrivée : time, arrêt_ligne => ArrêtLigne.num_arrêt, ligne => ArrêtLigne.ligne)
avec <
    (Projection(ArrêtVoyage, ligne, voyage) = Projection(Voyage, ligne, id_voyage))
    AND (Projection(ArrêtVoyage, voyage) = Projection(Voyage, id_voyage))
    AND (Un voyage possède au moins deux arrêts)
    AND (heure_départ >  heure_arrivée)
    AND (arrêt_ligne, ligne, voyage) KEY
    >

Trajet (#id_trajet : int,  num_place : int, date : date)

ArrêtTrajet (#trajet => Trajet.id_trajet, # num_arrêt_voyage => ArrêtVoyage.num_arrêt, #voyage => ArrêtVoyage.voyage, départ : bool) avec <
    (Projection(ArrêtTrajet, trajet) = Projection(Trajet, id_trajet))
    AND (Un trajet possède exactement deux arrêts de voyage)
    >

Voyageur (#nom : str, #prenom : str, #adresse : str, telephone : str, paiement : str, carte : int, statut : str, occasionnel : bool) avec <
    (paiement = ‘carte’ OR paiement = ‘chèque’ OR paiement = ‘monnaie’)
    AND (statut = ‘bronze’ OR statut = ‘silver’ OR statut = ‘gold’ OR statut = ‘platine’)
    AND ((occasionnel = false AND carte NOT NULL AND statut NOT NULL) OR (occasionnel = true AND carte IS NULL AND statut IS NULL))
    >

Billet (#id_billet : int, assurance : bool, prix : float, voyageur_nom => Voyageur.nom, voyageur_prenom => Voyageur.prenom, voyageur_adresse => Voyageur.adresse)

CompositionBillet (#billet => Billet.id_billet, #trajet => Trajet.id_trajet) avec <
    Projection(CompositionBillet, billet) = Projection(Billet, id_billet)
    >


id_voyage, id_billet, id_trajet et id_calendrier ont été créé pour pouvoir identifier chaque objet d’une classe (clés artificielles).

On fait le choix d'un héritage par classe mère car la classe mère a des associations, et l'héritage est presque complet. Occasionnel est à True si le voyageur est occasionnel (les attributs statut et carte sont donc nuls), sinon occasionnal est à False et c'est un voyageur régulier (attributs carte et statut non nuls) car l'héritage est exclusif et la classe mère est abstraite.

L'attribut date dans Trajet doit être une date présente dans le Calendrier du Voyage et non supprimée dans DateException, ou bien une date ajoutée dans DateException du Voyage.

Il faut s'assurer que l'horaire de Voyage (présente dans Calendrier) est égale à l'heure de départ du premier ArretVoyage.

Il faut s'assurer que le nombre de places réservées ne dépasse pas nb_places du TypeTrain pour chaque Voyage.

# Gare

<b>Nom</b> : le nom de la gare.

<b>Adresse</b> : c’est un string comportant un numéro de rue et une rue.

<b>Ville</b> : on suppose que 2 villes n’ont pas 2 fois le même nom.

<b>Pays</b> : on ajoute cet attribut pour justifier le besoin d'une zone horaire.

<b>GMT</b> est une méthode permettant d'obtenir la zone horaire.

<b>(nom, ville)</b> est clé car on suppose que deux gares peuvent avoir le même nom. Cependant, les noms des gares d’une même ville sont différents.

# Taxi, TransportPublic, Hotel

Ces classes sont associées à Gare. Chacune de ces classes possède des attributs propres, d’où le choix de faire des classes différentes pour chacune.

Pour <b>Taxi</b>, on a un attribut num qui est un numéro d'identification de taxi, et telephone qui est le numéro de téléphone pour réserver le taxi (l’attribut est un string, en effet, on suppose que le numéro de téléphone peut avoir des indicatifs différents de type « +33, +34, +212… »).

Pour <b>TransportPublic</b>, l'attribut num permet d'identifier la ligne de transport.

Pour <b>Hotel</b>, les attributs nom et adresse permettent d'identifier l'hôtel.

Une gare dispose de plusieurs hôtels/taxis/transports ou aucun à proximité. Les taxis/transports desservent au moins une gare (sinon ils n'auraient pas d'intérêt pour notre base de données) et potentiellement plusieurs gares. De la même façon, un hôtel est proche d'au moins une gare, et de potentiellement plusieurs.

# Ligne

Une ligne est identifiée par son numéro (qui est donc unique).

# ArretLigne

<b>num_arret</b> : c'est la position de l'arret au sein de la ligne correspondante.

<b>arrive</b> : à True, cela signifie qu'il s'agit du dernier arrêt de la ligne.

Un arrêt est propre à une ligne et à une gare. Une gare comprend des arrêt ou non et une ligne est composée d'au moins 2 arrêts (un départ et une arrivée).

# Voyage

Un voyage est associé à une ligne exactement et une ligne peut être assurée par plusieurs voyages.

# ArretVoyage

<b>num_arret</b> : c'est la position de l'arrêt au sein du voyage correspondant.

<b>heure_arrive</b> : c'est l'heure à laquelle le train arrive de cet arrêt.

<b>heure_depart</b> : c'est l'heure à laquelle le train part de cet arrêt.

Un arrêt est relié à un unique voyage. Un voyage est composé d'au moins 2 arrêts. Un arrêt de voyage est un arrêt de la ligne. Tous les arrêts de la ligne ne sont pas forcément un arrêt du voyage.

# Trajet

<b>num_place</b> : numéro de la place du passager.

<b>date</b> : la date du trajet.

<b>Durée()</b> permet de calculer la durée du trajet.

Un trajet est relié à 2 arrêts d'un même voyage. Les arrêts d'un voyage peuvent être reliés à plusieurs trajets.

# ArretTrajet

<b>depart</b> : indique si l'arrêt correspond au départ du trajet.

# Billet

<b>assurance</b> : indique si une assurance est comprise dans le billet.

<b>prix</b> : le prix du billet.

<b>Annulation()</b> est une méthode permettant d'annuler un billet.

<b>Modification(assurance:boolean)</b> est une méthode permettant de modifier le billet (une modification n'est possible que lorsqu'une assurance a été choisie).

Un billet est composé de un ou plusieurs trajets. Un trajet n'est pas forcément associé à un billet (un billet peut avoir été annulé) et peut être associé à plusieurs billets.

# Voyageur

<b>nom</b> : le nom du voyageur.

<b>prenom</b> : le prenom du voyageur.

<b>adresse</b> : l'adresse du voyageur.

<b>telephone</b> : l’attribut est un string, en effet, on suppose que le numéro de téléphone peut avoir des indicatifs différents de type « +33, +34, +212… ».

<b>paiment</b> : l’attribut paiement est de type énumération, on considère qu’il existe 3 modes de paiement : carte, chèque, monnaie.

<b>(nom, prenom, adresse)</b> : on suppose que des voyageurs peuvent avoir le même nom et prénom mais dans ce cas ils ont une adresse différente.

Un voyageur possède aucun ou plusieurs billets, et un billet est possédé par exactement un voyageur.

Un voyageur est soit un voyageur occasionnel, soit un régulier : la classe voyageur est donc abstraite. L’héritage est presque complet.

## Régulier

<b>carte</b> : numéro de carte du voyageur.

<b>statut</b> : le statut est une énumération. On suppose qu’il existe 4 statuts : bronze, silver, gold, platine.

# Calendrier

« Les voyages sont programmés de manière périodique selon un calendrier hebdomadaire ». On choisit d’ajouter la classe Calendrier, le terme « hebdomadaire » est représenté par des booléens représentant les jours de la semaine (pour indiquer tous les jours sauf le dimanche, tous les attributs sont à True et dimanche est à False).

<b>date_debut</b> : date de début de la période du calendrier.

<b>date_fin</b> : date de fin de la période du calendrier.

<b>horaire</b> : horaire de départ associé à un voyage.

Un calendrier sert pour 0 ou plusieurs voyages. Un voyage est associé à un calendrier (dans le cas où une nouvelle période pour le voyage est créée, on doit créer un nouveau voyage).

# Exception

Exception sert pour représenter les dates exceptions (jours fériés par exemple) où on supprime/ajoute des voyages.

<b>date</b> : l’attribut date représente les dates d’exceptions.

<b>ajout</b> : booléen mis à 1 s’il y a ajout de voyage et 0 sinon.

# Train

<b>num</b> : le numéro du train qui est unique et toujours renseigné (c'est donc la clé).

Un voyage est effectué par un train. Un train peut effectuer plusieurs voyages.

# TypeTrain

<b>nom</b> : le nom d'un train est unique. C'est donc la clé.

<b>nb_places</b> : le nombre de places maximum dans un train de ce type.

<b>vitesse</b> : la vitesse moyenne du train.

<b>premiere_classe</b> : un booléen. S'il est à True, le train possède une première classe. Tous les trains possèdent une seconde classe.

Un train est d'exactement un type. Plusieurs trains peuvent être du même type. Une ligne est toujours assurée par le même type de train. Un type de train peut ne rouler sur aucune ligne, sur une seule ligne ou sur plusieurs lignes.

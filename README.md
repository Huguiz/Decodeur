# Decodeur

<br>

## Installation & utilisation du décodeur :

![logo_dec](/docs/logo_dec.ico)

### Prérequis

- Dernière version de VLC installée, puis exécuter en admin via cmd (en prenant les guillemets) :
    ```
    "C:\Program Files\VideoLAN\VLC\vlc-cache-gen.exe" "C:\Program Files\VideoLAN\VLC\plugins"
    ```
- Utiliser un écran full HD (recommandé)
- Mise à l’échelle de l’écran à 100% (paramètre d’affichage Windows)
- Avoir une partition C: sur sa machine
- Un minimum de puissance (carte graphique) pour lire les médias

<br>

Lancer l’exécutable **Decodeur.exe**<br>

Au premier démarrage, l’application va demander une IP sur laquelle elle va écouter les demandes.<br>

Renseignez l’IPattribuée à une carte réseau de la machine. La boite de dialogue ne se fermera pas tant qu’une IP n’est pas trouvée.<br>

Une fois l’IP trouvée, le décodeur se lance par défaut en quadra.<br>

A ce stade le décodeur est fonctionnel. Lors de la première utilisation du décodeur, il est conseillé de suivre les informations ci-dessous pour comprendre son fonctionnement et également faire des essais de commutation.<br>

Le curseur est invisible par défaut. Appuyez sur la touche c pour basculer son état.<br>

Ensuite, fermez le décodeur en appuyant sur « echap » (attention à bien être sur la fenêtre de celui-ci).<br>

Ensuite coller le fichier **Media** dans `C:\Decodeur\`   *(optionnel, contient des médias pour faire des essais de commutation)*

<br>

Un fichier de configuration a également été créée : decodeurConf.ini, voici son contenu :
- IPdecodeur → IP d’écoute
- PORTdecodeur → Port d’écoute (défaut = 50050)
- PrepoType → Type de préposition actuelle (1 = single, 4 = quad, 9 = nano, 16 = 4x4, 6, 8 ,13 = custom)
- BorderColor → Couleur des bordures
- BackgroundColor → Couleur par défaut des moniteurs

<br>

Ci-dessous la liste des couleurs disponibles :

![colors](/docs/colors.png)

<br>

Liste des prépositions existantes :


![prepo](/docs/prepo.png)

<br>

## Installation & utilisation du SDK :

![logo_sdk](/docs/logo_sdk.ico)

### Prérequis

- Avoir une partition C: sur sa machine

<br>

Lancer l’exécutable **SDK.exe** :

![sdk_menu](/docs/sdk_menu.png)

<br>

### Partie haute

![sdk_haut](/docs/sdk_haut.png)

1. URL du média à lire. Le média doit être joignable depuis le décodeur. Pour lire une caméra, il est conseillé de la lire en amont sur VLC. Si le résultat est positif, copier-coller l’URL. Si le média n’est pas lisible sur VLC, il ne le sera pas non plus sur le décodeur.
Attention, pour lire une caméra, il faut rajouter à la fin de l’URL ` :network-caching=0` afin d’éviter la latence dans la lecture de la vidéo.
2. Numéro du moniteur sur lequel envoyer les commandes. Si le moniteur n’existe pas, le décodeur nous l’informera dans la section ` Log Décodeur ` (voir plus bas).
3. Permet d’envoyer l’URL au décodeur. Un retour sera fait dans la partie ` Log SDK ` (voir plus bas).
4. Ajoute l’URL dans la liste des caméras acquises (voir plus bas).

<br>

### Partie centrale

![sdk_centre](/docs/sdk_centre.png)

1. Liste des médias enregistrés, contient par défaut les images et vidéos du dossier **Media**. Cette liste est sauvegardée à la fermeture du programme. Un double-clic sur un média permet de le mettre dans la section URL (vu précédemment), ce qui évite à l’utilisateur de réécrire l’URL.
2. Met le média sélectionné dans la section URL (la même fonction que le double-clic), ce qui évite à l’utilisateur de réécrire l’URL.
3. Ajoute le média sélectionné dans le tableau des caméras cyclique. Ouvre un pop-up demandant le DWELL.
4. Supprime le ou les médias sélectionnés.
5. Supprime le ou les médias sélectionnés du tableau caméra cyclique.
6. Modifie la position du média dans le cyclique.
7. Envoi le cyclique au décodeur. Utilise le n° moniteur vu précédemment.
8. Liste des médias du cyclique avec leur DWELL associé

<br>

### Partie basse

![sdk_bas](/docs/sdk_bas.png)



1. Log du SDK, c’est ici que le SDK nous fait un retour de nos actions. Dès le démarrage, il envoie un signal de vie au décodeur.
2. Log du décodeur, fait un retour en cas de demande à un signal de vie, de n° moniteur inconnue, de préposition inconnue ou commande incomprise.
3. Envoi d’un signal de vie pour savoir si le décodeur est en ligne.
4. Met au noir le moniteur sélectionné (commute l’image située dans C:\Decodeur\Media\default.png).
5. Change la préposition du décodeur par celle choisie.
6. Changer la préposition en custom (actuellement existant : 6, 8 et 13). Voir la liste des prépositions disponible dans la partie installation du décodeur.
7. IP et port du décodeur cible. Des essais locaux (en loopback, 127.0.0.1) sont possibles, mais il faut d’abord lancer le décodeur (et bien modifier son IP d’écoute dans le fichier decodeurConf.ini), et ensuite le SDK.
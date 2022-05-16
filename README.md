# rfid pyton raspberry pi
[mfrc522 PyPI](https://pypi.org/project/mfrc522/#description)  
[mariadb PyPI](https://pypi.org/project/mariadb/)  
[pygame](https://pypi.org/project/pygame/)

github developer settings personal access tokens  

```bash
apache2
php
php-mysql
mariadb-server

```

## À ajouter ?
- [x] voir le nom attribué à l’id
- [x] sur l’écran d’attente voir les derniers pointages
- avoir une scène de confirmation récapitulatif
- couleur de orif 
    - #005BA9 bannière, titre
    - #DBCEB1 fond
    - #AE9B70 text
    - #FFFFFF
    https://coolors.co/005ba9-dd1c1a-dbceb1-386641-3c362a
- wait screen avec rebond du text avec les bords
- [x] 5 dernières décroisant
- [x] nom, prénom
- [x] temps limite
- horaire d'allumage du Raspberry Pi
- écran de confirmation du nom d'utilisateur entrer lors de la création



## sécurité
- stockage temporaire des noms
- hacher (sha2) les ids des badges
- chiffrement de la connexion avec la base de données

## à corrigé
- [x] scene with unknow badge
- [x] request log with unknow badge
- [x] somme heures plus 24 heures
- [ ] désactiver la mise en veille de l'écran
- [ ] les câbles ?
- [ ] requête log quand le bouton est appuyé


## bug
- plus de 12 logs dans le détail d'un provoque un empilement des caractère
- Utilisateur peut mettre un nom vide
- Utilisateur peut mettre un nom à double

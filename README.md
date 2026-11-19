# Objectif 100 % : site GTA 6 en français et en anglais

Un site de fan avec six outils pour GTA 6, en français à la racine du site et en anglais dans `/en/` :

- **Codes de triche** : les 61 codes, les combinaisons connues, le défi qui débloque chaque code, et un suivi de ceux que tu as. Chaque combinaison s'affiche en grand (écran allumé pendant qu'on la tape), et toutes les combinaisons s'enregistrent en une image à garder sur son téléphone, avec l'adresse du site dessus.
- **Trophées** : les 55 trophées traduits, les 28 cachés masqués contre les spoilers, et un tracker du platine avec image de progression à partager.
- **Place** : calcule si les 212 Go passent sur ta console et le temps de téléchargement selon ton débit.
- **Problèmes de lancement** : les solutions, problème par problème, sur PS5 et Xbox.
- **Infos** : les réponses vérifiées (durée de vie, prix, online, PC…), avec leurs sources.
- **Bons plans** : la page Black Friday (consoles, SSD, accessoires) avec liens affiliés.

Le nom « Objectif 100 % » ne contient pas « GTA » exprès : Take-Two défend ses marques de près, et un nom neutre te permettra de réutiliser le site pour les prochains gros jeux.

## Le look

L'ambiance reprend celle du jeu sans rien lui emprunter : une autoroute côtière au coucher du soleil, des palmiers en silhouette et le soleil qui se couche entre les poteaux du panneau. Les panneaux restent des panneaux routiers : vert pour les outils, bleu pour les infos, jaune pour la prudence. Le rose et le corail servent aux boutons et aux liens.

Tout est dessiné pour le site : aucun logo, aucune police ni aucune image officielle de Rockstar. Garde cette règle si tu ajoutes des visuels.

## La version anglaise

- Les pages anglaises sont dans `src/pages/en/`, avec leurs propres adresses (`/en/gta-6-cheats/`, `/en/gta-6-trophies/`…). Un bouton EN/FR dans le menu passe d'une langue à l'autre, et Google sait quelle version montrer grâce aux balises `hreflang`.
- La progression des trophées et des codes est la même dans les deux langues : un visiteur peut changer de langue sans rien perdre.
- Les traductions des trophées et des codes sont dans les fichiers de données, dans le champ `en` de chaque élément.
- Si tu ajoutes une page, mets dans sa première ligne `"alt"` avec l'adresse de sa traduction (par exemple `"alt": "gta-6-cheats"`).

## Ce qui tourne tout seul

Une fois en ligne, GitHub reconstruit et republie le site :

- **chaque jour** : les dernières vidéos officielles de Rockstar sont récupérées, le compteur « disponible depuis X jours » avance, et le bandeau temporaire disparaît après sa date de fin ;
- **les 21, 23, 25, 27 et 29 novembre** : une tâche planifiée cherche les nouvelles combinaisons de codes de triche et t'envoie le fichier `gta6-codes-maj.json` à déposer (voir plus bas) ;
- **selon la date** : la page Bons plans et les bandeaux passent seuls du Black Friday (jusqu'au 30 novembre) à Noël (du 1er au 25 décembre), puis à une version sans saison ;
- **après chaque modification** : les pages sont signalées à Bing et aux moteurs IndexNow, qui les indexent plus vite (Bing sert aussi aux recherches de ChatGPT et Copilot) ;
- **à chaque modification** d'un fichier (par exemple une nouvelle combinaison de code), sans rien faire de plus ;
- **la pub et l'affiliation** s'activent dès que tu mets tes identifiants dans `site.json`.

Ce que tu dois faire toi-même : la mise en ligne (une fois), les comptes Amazon et AdSense, et faire connaître le site (Discord, Reddit, TikTok). Sans visiteurs, pas de revenus.

> Sur un dépôt public, GitHub met en pause les tâches quotidiennes après 60 jours sans modification. N'importe quelle modification les relance.

## Mise en ligne gratuite (environ 10 minutes)

1. Crée un compte sur [github.com](https://github.com) si tu n'en as pas.
2. Clique sur **New repository**, nomme-le `objectif100`, coche **Public**, puis **Create repository**.
3. Clique sur **uploading an existing file** et glisse **tout le contenu** de ce dossier, y compris le dossier caché `.github`.
   - Sur Mac, `Cmd + Maj + .` affiche les dossiers cachés dans le Finder.
   - Si `.github` ne passe pas : **Add file > Create new file**, tape `.github/workflows/site.yml` comme nom et colle le contenu du fichier.
4. Clique sur **Commit changes**.
5. Va dans **Settings > Pages**, et dans **Source**, choisis **GitHub Actions**.
6. Va dans l'onglet **Actions** : la publication tourne. Au bout d'une minute ou deux, ton site est en ligne à `https://TON-PSEUDO.github.io/objectif100/`.
7. Ouvre `site.json` sur GitHub (icône crayon) et remplace `ton-pseudo` par ton vrai pseudo dans `url`. Enregistre : le site se reconstruit tout seul.
8. Ajoute le site dans [Google Search Console](https://search.google.com/search-console) et envoie `sitemap.xml` pour qu'il apparaisse dans Google.

Si tu avais déjà mis en ligne une version précédente : remplace simplement tous les fichiers par ceux de ce dossier, y compris le nouveau dossier `src/pages/en`, et supprime `assets/trophees.js` s'il existe encore.

## Brancher les revenus

Tout se règle dans `site.json` :

| Champ | À quoi ça sert |
|---|---|
| `amazon_tag` | Ton identifiant [Amazon Partenaires](https://partenaires.amazon.fr) (ex. `objectif100-21`). Tous les liens d'achat des pages françaises deviennent affiliés, et la mention obligatoire s'affiche toute seule. |
| `amazon_en` | Pour les pages anglaises : `domaine` (par défaut `www.amazon.com`) et `tag`, ton identifiant [Amazon Associates](https://affiliate-program.amazon.com) américain (ex. `objectif100-20`). C'est un compte séparé du compte français. |
| `adsense_client` | Ton identifiant AdSense (`ca-pub-…`). La pub automatique s'active et le fichier `ads.txt` est créé. |
| `domaine_perso` | Ton nom de domaine (ex. `objectif100.fr`, environ 10 € par an). Obligatoire pour AdSense, qui refuse les adresses en `github.io`. |
| `editeur` | Ton nom, statut, SIRET, adresse et e-mail pour les mentions légales. |
| `bandeaux` | Les bandeaux en haut des pages, chacun avec `texte` et `lien` en français, `texte_en` et `lien_en` en anglais, et ses dates `du` et `jusqua`. Le premier dont la période contient aujourd'hui s'affiche : Black Friday jusqu'au 30 novembre, puis Noël du 1er au 24 décembre. |
| `google_site_verification` | Le code de vérification de [Google Search Console](https://search.google.com/search-console) (méthode « Balise HTML »). Tu peux coller la balise entière : le code est extrait tout seul. |
| `cloudflare_analytics` | Facultatif : le jeton de [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/), gratuit et sans cookie, pour voir tes visites. Tu peux coller le code entier. La page Confidentialité le mentionne alors toute seule. |
| `indexnow` | La clé IndexNow du site, déjà générée. Ne la change pas. |

Ce qu'il faut savoir sur Amazon :

- la commission est de 1 % sur les jeux et les consoles, mais de 3 % sur l'informatique et l'électronique (SSD, casques, TV) : c'est pour ça que la page Bons plans met le stockage et les écrans en avant ;
- tu touches une commission sur tout le panier commandé dans les 24 heures après le clic, pas seulement sur le produit du lien : pendant le Black Friday, ça compte beaucoup ;
- Amazon demande généralement 3 ventes dans les 180 premiers jours pour valider ton compte.

Pour AdSense en France :

- active le message de consentement RGPD de Google dans **Confidentialité et messages** : c'est gratuit et obligatoire pour afficher de la pub en Europe ;
- AdSense refuse souvent les sites trop récents ou trop légers : commence par Amazon, et fais ta demande quand le site aura plus de pages utiles.

Pour la version anglaise : dans ton compte Amazon Associates américain, active **OneLink** et relie-y tes comptes d'autres pays (Royaume-Uni, Canada…). Les visiteurs de ces pays seront alors envoyés vers leur Amazon, et la vente compte quand même.

Pour le domaine : achète-le chez un registrar (OVH, Gandi, Cloudflare…), mets-le dans `domaine_perso`, puis dans **Settings > Pages > Custom domain** sur GitHub. Ajoute chez le registrar un enregistrement `CNAME` vers `TON-PSEUDO.github.io`.

## Avant d'encaisser

- Les revenus de pub et d'affiliation sont des revenus à déclarer. Le statut de micro-entrepreneur est le plus simple pour démarrer.
- Remplis la partie `editeur` de `site.json` : les mentions légales sont obligatoires pour un site qui rapporte de l'argent.
- Ne mets jamais de logo, d'image ou de visuel officiel de Rockstar sur le site.

## Mettre à jour les codes de triche

### Avec le fichier envoyé par la tâche planifiée

Quand tu reçois `gta6-codes-maj.json` :

1. Sur GitHub, ouvre ton dépôt, puis le dossier `data`.
2. Clique sur **Add file > Upload files** et dépose le fichier. Il remplace l'ancien.
3. Clique sur **Commit changes**. Le site se reconstruit tout seul en quelques minutes, en français et en anglais.

Le fichier ne contient que les combinaisons confirmées par au moins deux sources. Une combinaison invalide ou un code inconnu est ignoré, sans casser le site.

### À la main

Dans `data/gta6-codes.json`, remplis le champ `sequence` du code concerné avec une lettre par touche de la croix directionnelle :

- `H` pour haut, `B` pour bas, `G` pour gauche, `D` pour droite ;
- exemple : `"sequence": "HDBGHGBD"` donne ↑ → ↓ ← ↑ ← ↓ →.

Mets `"sequence_a_confirmer": true` si une seule source donne la combinaison, et `"condition_a_confirmer": true` si le défi n'est pas sûr. Retire ces champs quand c'est confirmé. Change aussi la date `maj` en haut du fichier.

## Contenus de saison

Dans une page de `src/pages`, entoure un passage pour qu'il ne s'affiche qu'à certaines dates :

```
<!--jusquau 2026-11-30--> texte du Black Friday <!--fin-->
<!--du 2026-12-01 au 2026-12-25--> texte de Noël <!--fin-->
<!--apartir 2026-12-26--> texte sans saison <!--fin-->
```

Le titre Google d'une page peut changer aussi : dans sa première ligne, la liste `"saisons"` donne un `titre` et une `description` pour chaque période. Le site se reconstruit chaque matin, donc le changement se fait tout seul.

Pour voir le site à une autre date : `python3 build.py --offline --date=2026-12-05`.

## Mettre à jour les trophées

La liste officielle est dans `data/gta6-trophees.json`. Pour chaque trophée :

- `type` : `platine`, `or`, `argent` ou `bronze` ;
- `cache: true` masque le nom et la condition derrière « Voir le trophée (spoiler) » ;
- `astuce` ajoute une ligne de conseil sous la condition ;
- `manquable: true` affiche une plaque jaune « Manquable ».

Ne change jamais l'`id` d'un trophée ou d'un code une fois publié : c'est lui qui retrouve la progression des visiteurs.

Écris les descriptions avec tes propres mots plutôt que de copier un autre site.

## Tester sur ton ordinateur (facultatif)

Avec Python 3 installé (sur Mac, il est souvent déjà là ; tape `python3` dans le Terminal pour vérifier) :

```
python3 build.py --offline
python3 -m http.server --directory dist 8000
```

Puis ouvre `http://localhost:8000`. Ajoute `--date=2026-12-05` à la première commande pour voir le site comme à Noël.

## Organisation des fichiers

```
site.json                 réglages (adresse, revenus, éditeur, bandeau)
data/gta6-codes.json      codes de triche
data/gta6-trophees.json   trophées
data/gta6-codes-maj.json  nouvelles combinaisons envoyées par la tâche planifiée (facultatif)
src/layout.html           gabarit commun à toutes les pages
src/pages/*.html          contenu de chaque page en français
src/pages/en/*.html       contenu de chaque page en anglais
assets/                   style, scripts (app.js, tracker.js, place.js), icônes, palmiers, images de partage
build.py                  construit le site dans dist/
.github/workflows/        publication automatique
```

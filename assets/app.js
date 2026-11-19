/* Objectif 100 % : scripts communs (panneau d'accueil, partage, image de progression). */
(function () {
  'use strict';
  var ESP = ' ';
  var FINE = ' ';
  var POLICE = '"DIN Condensed", "DIN Alternate", Bahnschrift, "Roboto Condensed", "Arial Narrow", "DejaVu Sans Condensed", sans-serif';
  var EN = (document.documentElement.lang || '').slice(0, 2) === 'en';
  var T = EN ? {
    dans: 'In', jour: 'd', aujourdhui: 'Out today',
    depuis: function (n) { return 'Out for ' + n + ESP + 'day' + (n > 1 ? 's' : ''); },
    lienCopie: 'Link copied.',
    imageEtLien: 'Image downloaded and link copied: post them together.',
    image: 'Image downloaded: post it with the site link.',
    partagee: 'Image shared.',
    fichier: 'gta-6-progress.png'
  } : {
    dans: 'Dans', jour: 'j', aujourdhui: 'Sorti aujourd’hui',
    depuis: function (n) { return 'Depuis ' + n + ESP + 'jour' + (n > 1 ? 's' : ''); },
    lienCopie: 'Lien copié.',
    imageEtLien: 'Image téléchargée et lien copié' + FINE + ': publie-les ensemble.',
    image: 'Image téléchargée' + FINE + ': publie-la avec le lien du site.',
    partagee: 'Image partagée.',
    fichier: 'progression-gta-6.png'
  };
  // Silhouette de palmier (générée par outils/palmiers.py), dans sa boîte x, y, l, h.
  var PALMIER = { d: 'M99.3 317.7 97.1 310.1 94.2 302.6 91.8 295.1 90.5 287.4 89.6 279.7 88.4 272.1 87.9 264.5 87.9 256.9 87.4 249.4 87.0 241.9 87.4 234.4 87.8 227.0 87.9 219.5 88.4 212.1 89.5 204.8 90.4 197.5 91.1 190.1 92.6 182.9 94.3 175.7 95.6 168.4 97.3 161.1 99.5 154.1 101.7 146.9 103.7 139.7 106.2 132.7 109.1 125.7 111.9 118.7 114.7 111.6 118.0 104.7 121.5 97.8 114.5 94.2 111.0 101.2 107.6 108.3 104.1 115.3 100.9 122.3 98.1 129.6 95.3 136.7 92.4 143.9 90.0 151.1 88.0 158.5 85.7 165.8 83.5 173.2 82.0 180.7 80.5 188.2 78.8 195.6 77.5 203.2 76.8 210.8 75.8 218.5 74.8 226.1 74.4 233.9 74.3 241.7 73.9 249.5 73.6 257.3 74.2 265.2 74.6 273.1 74.7 281.1 75.4 289.2 76.2 297.2 76.1 305.5 75.9 313.9 76.7 322.3ZM118.5 94.9 112.7 92.3 106.8 90.2 104.9 88.7 100.5 88.8 100.4 85.9 94.2 88.2 95.0 84.0 88.0 88.3 88.9 83.1 81.7 89.1 82.3 83.3 75.4 90.7 75.4 84.6 69.2 93.1 68.4 87.0 63.0 96.1 61.4 90.5 56.7 100.0 54.5 95.1 50.5 104.5 47.7 100.7 44.4 109.8 41.1 107.2 38.2 115.8 34.6 114.6 32.0 122.6 28.3 122.9 25.8 130.1 22.1 132.0 19.7 138.3 16.1 141.8 13.5 147.2 10.2 152.5 7.4 156.9 4.3 163.8 2.3 167.9 2.3 167.9 4.9 164.6 9.4 158.2 12.3 155.9 15.5 148.6 19.7 147.9 21.6 139.7 27.1 140.7 27.7 131.5 34.5 134.4 33.8 124.2 41.8 128.8 39.9 117.5 48.9 124.0 46.0 111.6 55.8 120.0 52.0 106.4 62.5 116.5 58.1 102.0 68.9 113.7 64.1 98.2 75.0 111.4 70.1 95.3 80.7 109.5 76.2 93.0 85.9 107.7 82.2 91.5 90.8 105.9 88.1 90.7 95.4 103.7 94.1 90.6 99.7 100.9 100.1 91.2 104.0 96.8 106.1 92.6 111.8 94.5 117.5 97.1ZM118.9 95.2 114.3 90.7 109.8 86.8 108.6 84.8 104.9 83.1 106.0 80.8 100.1 80.0 102.5 77.2 95.2 77.4 98.5 74.0 90.3 75.4 94.0 71.4 85.4 73.9 89.0 69.3 80.5 73.0 83.6 68.0 75.6 72.6 78.0 67.5 70.7 72.8 72.3 67.8 65.8 73.5 66.5 69.0 60.9 74.9 60.7 71.0 56.1 76.7 55.1 73.8 51.2 79.1 49.7 77.3 46.3 82.1 44.4 81.5 41.5 85.6 39.3 86.4 36.7 89.6 34.4 91.9 31.9 94.2 29.6 97.9 27.9 100.1 27.9 100.1 30.0 98.8 33.6 95.9 36.0 95.4 38.3 91.4 41.9 92.7 43.0 87.5 47.8 90.7 47.7 84.1 53.5 89.3 52.4 81.2 59.1 88.6 57.0 78.9 64.5 88.5 61.7 77.1 69.5 88.8 66.3 75.9 74.3 89.6 71.0 75.2 78.7 90.6 75.6 75.0 82.9 91.7 80.2 75.3 86.8 92.7 84.9 76.2 90.5 93.5 89.5 77.6 94.2 94.0 94.2 79.6 98.0 94.0 98.9 82.0 102.0 93.3 103.5 85.1 106.1 91.5 108.2 88.6 112.7 92.5 117.1 96.8ZM119.1 95.5 116.7 90.8 114.2 86.4 113.7 84.7 111.7 82.1 112.9 80.9 109.1 78.1 111.6 77.1 106.5 74.4 109.9 73.6 104.0 71.1 108.0 70.2 101.4 68.0 105.7 67.0 98.8 65.3 103.2 64.1 96.2 62.9 100.4 61.5 93.6 60.9 97.4 59.2 90.9 59.1 94.3 57.3 88.3 57.7 90.9 55.9 85.6 56.7 87.5 54.9 82.9 55.9 84.0 54.4 80.2 55.5 80.6 54.5 77.5 55.5 77.2 55.1 74.9 55.8 74.0 56.3 72.2 56.4 71.0 57.9 70.0 58.5 70.0 58.5 71.2 58.7 72.9 58.7 74.5 59.6 75.3 58.2 77.6 60.9 77.7 57.9 80.6 62.7 80.1 57.9 83.3 64.9 82.4 58.3 85.8 67.3 84.8 58.9 88.1 69.9 87.3 59.9 90.2 72.6 89.7 61.2 92.2 75.3 92.2 62.8 94.2 77.9 94.6 64.8 96.2 80.4 97.1 67.0 98.3 82.7 99.6 69.6 100.4 84.8 102.1 72.6 102.7 86.7 104.6 75.8 105.2 88.1 107.1 79.4 107.9 89.0 109.6 83.3 110.8 89.0 112.2 87.6 114.5 91.9 116.9 96.5ZM119.2 95.8 118.6 91.9 118.0 88.2 117.8 86.8 117.4 84.4 118.3 83.9 116.8 80.8 118.5 81.0 116.2 77.4 118.4 78.0 115.5 74.2 118.1 75.1 114.9 71.1 117.7 72.2 114.3 68.3 117.2 69.4 113.7 65.6 116.5 66.7 113.1 63.1 115.7 64.2 112.4 60.7 114.8 61.7 111.8 58.6 113.8 59.4 111.2 56.6 112.8 57.3 110.6 54.8 111.7 55.3 109.9 53.2 110.5 53.5 109.3 51.8 109.3 51.9 108.6 50.5 108.1 50.6 108.0 49.4 106.8 49.5 106.4 49.2 106.4 49.2 106.5 50.0 106.0 50.7 106.9 52.4 106.5 51.7 107.2 55.0 107.1 52.8 107.4 57.7 107.7 54.1 107.7 60.4 108.3 55.7 107.9 63.3 108.9 57.4 108.1 66.2 109.5 59.3 108.4 69.1 110.1 61.4 108.7 72.0 110.7 63.7 109.1 74.8 111.4 66.1 109.5 77.6 112.0 68.8 110.1 80.2 112.6 71.6 110.8 82.7 113.2 74.6 111.6 84.9 113.8 77.9 112.6 86.8 114.4 81.2 113.8 88.4 115.0 84.8 115.3 89.2 115.7 88.6 116.2 92.3 116.8 96.2ZM116.8 95.8 117.6 91.4 118.4 87.2 118.5 85.6 119.2 82.9 118.0 82.4 120.0 78.9 117.8 79.0 120.8 75.1 118.0 75.7 121.7 71.5 118.4 72.5 122.5 68.1 118.9 69.3 123.3 65.0 119.7 66.2 124.1 62.1 120.6 63.3 125.0 59.4 121.6 60.5 125.8 56.9 122.7 57.9 126.6 54.7 124.0 55.5 127.5 52.6 125.3 53.2 128.3 50.8 126.7 51.2 129.2 49.2 128.2 49.4 130.0 47.8 129.7 48.0 130.9 46.6 131.3 46.8 131.9 45.7 132.9 46.1 133.5 45.9 133.5 45.9 133.2 46.7 133.5 47.4 132.5 49.2 132.8 48.2 131.9 51.9 132.0 49.2 131.5 54.8 131.2 50.4 131.1 57.8 130.5 51.9 130.8 60.8 129.7 53.6 130.4 63.9 128.9 55.5 130.1 67.0 128.1 57.7 129.6 70.1 127.2 60.1 129.1 73.2 126.4 62.8 128.5 76.2 125.6 65.6 127.7 79.0 124.8 68.7 126.9 81.7 124.0 72.0 125.8 84.1 123.2 75.6 124.6 86.1 122.4 79.4 123.1 87.7 121.5 83.4 121.3 88.5 120.7 87.6 120.0 91.8 119.2 96.2ZM116.9 95.4 120.0 89.9 123.0 84.9 123.5 82.8 126.3 79.9 124.4 78.4 129.5 75.5 126.0 74.1 132.7 71.5 128.1 70.0 136.0 67.9 130.7 66.3 139.2 64.8 133.6 62.8 142.5 62.2 136.9 59.7 145.8 60.1 140.6 57.1 149.2 58.4 144.6 55.0 152.5 57.2 148.9 53.6 155.9 56.5 153.3 52.9 159.2 56.3 157.7 53.0 162.6 56.5 162.1 54.0 166.0 57.3 166.3 55.7 169.3 58.5 170.2 58.1 172.6 60.2 173.9 61.1 175.9 62.4 177.3 64.6 178.4 66.0 178.4 66.0 176.9 65.6 174.5 64.4 172.5 64.9 171.4 62.3 168.3 64.9 168.3 60.7 164.2 65.6 165.3 59.6 160.4 66.9 162.2 58.9 156.9 68.8 159.2 58.7 153.7 71.1 156.2 58.9 151.0 73.7 153.2 59.5 148.5 76.3 150.1 60.6 146.2 78.9 147.0 62.1 143.9 81.4 143.9 64.2 141.6 83.6 140.8 66.6 139.2 85.6 137.7 69.6 136.5 87.2 134.5 73.0 133.6 88.4 131.4 76.9 130.5 88.9 128.2 81.3 126.9 88.4 125.1 86.1 122.1 91.1 119.1 96.6ZM117.2 95.1 122.3 90.7 127.4 86.8 128.6 84.8 132.8 83.4 131.7 80.8 138.2 80.6 135.7 77.2 143.6 78.4 140.4 74.2 149.1 76.9 145.7 71.9 154.5 76.1 151.4 70.4 160.0 75.9 157.6 69.8 165.5 76.3 163.9 70.3 170.9 77.4 170.3 71.7 176.4 79.2 176.7 74.1 181.8 81.6 183.0 77.5 187.2 84.7 189.1 81.8 192.6 88.4 194.9 86.8 198.0 92.8 200.6 92.7 203.4 97.7 206.1 99.3 208.7 103.4 211.5 106.5 214.1 109.6 216.7 114.4 218.5 117.3 218.5 117.3 216.2 115.3 212.2 111.2 209.5 110.2 207.0 105.0 202.9 105.8 201.7 99.5 196.3 102.3 196.4 94.6 189.9 99.5 191.2 90.3 183.5 97.4 185.9 86.7 177.4 96.0 180.7 83.8 171.5 95.3 175.5 81.4 166.0 95.1 170.3 79.8 160.9 95.3 165.1 78.7 156.1 95.8 159.9 78.3 151.7 96.3 154.8 78.4 147.5 96.6 149.6 79.3 143.5 96.7 144.4 80.7 139.5 96.2 139.2 82.8 135.4 94.9 134.0 85.5 131.0 92.3 128.7 88.8 123.8 92.6 118.8 96.9ZM117.5 94.9 122.9 92.7 128.3 91.1 130.1 90.0 134.1 90.2 134.4 87.7 139.9 90.1 139.6 86.4 145.6 90.7 145.3 86.1 151.4 92.1 151.5 86.9 157.1 94.2 157.9 88.8 162.8 97.1 164.3 91.9 168.5 100.7 170.7 96.0 174.2 105.1 176.9 101.2 179.9 110.2 183.0 107.4 185.6 116.1 189.0 114.4 191.2 122.7 194.8 122.4 196.9 130.0 200.5 131.2 202.5 138.1 206.0 140.7 208.1 146.9 211.5 151.1 213.8 156.4 216.8 162.2 219.4 166.7 222.1 174.0 223.9 178.3 223.9 178.3 221.6 174.7 217.3 167.9 214.8 165.1 211.7 157.6 208.0 156.3 206.1 148.1 201.2 148.3 200.5 139.4 194.5 141.1 194.9 131.4 187.9 134.7 189.4 124.2 181.3 129.1 183.8 117.7 174.9 124.2 178.2 111.9 168.7 120.0 172.7 106.9 162.8 116.4 167.2 102.7 157.1 113.4 161.6 99.2 151.8 110.9 156.2 96.4 146.9 108.6 150.7 94.3 142.5 106.5 145.2 93.0 138.3 104.2 139.8 92.5 134.4 101.3 134.3 92.6 130.7 97.4 128.9 93.5 123.7 94.9 118.5 97.1ZM118.0 94.8 114.4 95.0 110.9 95.7 109.7 95.7 107.1 97.0 106.4 95.4 103.4 98.8 102.6 96.1 99.6 101.1 98.6 97.8 95.9 103.9 94.5 100.3 92.2 107.3 90.4 103.7 88.6 111.1 86.4 107.8 84.9 115.4 82.4 112.6 81.3 120.3 78.5 118.1 77.6 125.7 74.8 124.3 74.0 131.5 71.1 131.1 70.3 137.9 67.6 138.5 66.7 144.8 64.1 146.5 63.1 152.2 60.7 155.0 59.4 160.1 57.4 164.0 55.8 168.5 54.1 173.6 52.2 177.5 50.8 183.7 49.7 187.3 49.7 187.3 51.3 184.2 54.4 178.3 55.8 175.8 58.0 169.5 60.3 167.9 61.6 161.1 64.8 160.6 65.2 153.2 69.3 153.7 68.8 145.9 73.8 147.4 72.4 139.1 78.2 141.6 76.0 132.8 82.4 136.3 79.6 127.0 86.6 131.4 83.2 121.7 90.6 127.0 86.8 116.9 94.4 122.9 90.4 112.7 98.0 119.2 93.9 109.0 101.3 115.8 97.5 105.8 104.3 112.5 101.0 103.1 106.9 109.2 104.5 100.9 109.1 105.7 108.0 99.2 110.8 101.4 111.5 98.1 114.7 97.4 118.0 97.2ZM118.0 94.8 121.7 94.9 125.4 95.5 126.6 95.4 129.3 96.6 130.0 95.0 133.2 98.3 133.9 95.6 137.1 100.5 138.0 97.2 140.9 103.2 142.3 99.6 144.8 106.4 146.5 102.8 148.6 110.2 150.8 106.8 152.4 114.4 154.9 111.6 156.3 119.2 158.9 117.0 160.1 124.5 162.9 123.1 163.9 130.3 166.7 129.8 167.7 136.6 170.4 137.2 171.5 143.4 174.1 145.1 175.2 150.8 177.7 153.5 179.0 158.6 181.2 162.5 182.8 167.0 184.6 172.1 186.6 175.9 188.1 182.1 189.3 185.7 189.3 185.7 187.6 182.7 184.4 176.8 182.9 174.3 180.6 168.0 178.3 166.5 176.9 159.6 173.6 159.2 173.1 151.9 168.9 152.4 169.3 144.6 164.3 146.2 165.6 137.8 159.8 140.5 161.8 131.6 155.3 135.3 158.1 125.9 151.0 130.5 154.3 120.7 146.9 126.2 150.6 116.0 142.9 122.2 146.9 111.8 139.2 118.6 143.2 108.2 135.8 115.3 139.5 105.1 132.7 112.1 135.8 102.5 129.9 108.9 132.1 100.5 127.5 105.4 128.5 98.9 125.6 101.2 124.9 97.8 121.5 97.3 118.0 97.2ZM112.0 96.0a6 6 0 1 0 12 0a6 6 0 1 0 -12 0Z', x: 0, y: 43, l: 226, h: 277 };

  // Panneau d'accueil : compte à rebours, puis « disponible depuis ».
  var panneau = document.querySelector('[data-cible]');
  if (panneau) {
    var cible = Date.parse(panneau.getAttribute('data-cible'));
    var titre = panneau.querySelector('[data-titre]');
    var detail = panneau.querySelector('[data-detail]');
    var compte = panneau.querySelector('[data-compte]');
    var chapo = document.querySelector('[data-chapo]');
    var majPanneau = function () {
      var ecart = cible - Date.now();
      if (ecart > 0) {
        var minutes = Math.ceil(ecart / 60000);
        var j = Math.floor(minutes / 1440);
        var h = Math.floor((minutes % 1440) / 60);
        var m = minutes % 60;
        var morceaux = [];
        if (j) morceaux.push(j + ESP + T.jour);
        if (j || h) morceaux.push(h + ESP + 'h');
        if (!j) morceaux.push(m + ESP + 'min');
        compte.textContent = T.dans + ' ' + morceaux.join(' ');
      } else {
        var jours = Math.floor(-ecart / 86400000);
        titre.textContent = panneau.getAttribute('data-apres-titre') || titre.textContent;
        detail.textContent = panneau.getAttribute('data-apres-detail') || detail.textContent;
        compte.textContent = jours === 0 ? T.aujourdhui : T.depuis(jours);
        if (chapo && chapo.getAttribute('data-apres')) chapo.textContent = chapo.getAttribute('data-apres');
      }
    };
    if (!isNaN(cible) && titre && detail && compte) {
      majPanneau();
      setInterval(majPanneau, 20000);
    }
  }

  function adresseCanonique() {
    var lien = document.querySelector('link[rel="canonical"]');
    return lien && lien.href && lien.href.indexOf('ton-pseudo') === -1 ? lien.href : location.href.split('#')[0];
  }

  function adresseCourte() {
    try {
      var u = new URL(adresseCanonique());
      var chemin = u.pathname.replace(/[^/]+\/?$/, '').replace(/\/$/, '');
      return u.host + chemin;
    } catch (e) { return location.host; }
  }

  function copierLien(texte, url, dire, apresImage) {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;
    navigator.clipboard.writeText(texte + ' ' + url).then(function () {
      dire(apresImage ? T.imageEtLien : T.lienCopie);
    }, function () {});
  }

  // Partage texte : feuille de partage du téléphone, sinon copie du lien.
  document.addEventListener('click', function (e) {
    var bouton = e.target.closest ? e.target.closest('[data-partage]') : null;
    if (!bouton) return;
    var texte = bouton.getAttribute('data-texte') || document.title;
    var url = bouton.getAttribute('data-url') || adresseCanonique();
    if (navigator.share) {
      navigator.share({ title: document.title, text: texte, url: url }).catch(function () {});
    } else {
      copierLien(texte, url, function (message) {
        var avant = bouton.textContent;
        bouton.textContent = message;
        setTimeout(function () { bouton.textContent = avant; }, 2200);
      }, false);
    }
  });

  // Image de progression au format portrait (1080 × 1350), à publier en story ou sur Discord :
  // le panneau vert devant un coucher de soleil, le soleil entre les deux poteaux.
  function arrondi(ctx, x, y, l, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + l, y, x + l, y + h, r);
    ctx.arcTo(x + l, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + l, y, r);
    ctx.closePath();
  }

  function police(ctx, texte, taille, poids, largeurMax) {
    var t = taille;
    do {
      ctx.font = poids + ' ' + t + 'px ' + POLICE;
      t -= 4;
    } while (ctx.measureText(texte).width > largeurMax && t > 24);
  }

  // Réduit le texte jusqu'à une taille minimale, puis le coupe avec « … » s'il ne tient toujours pas.
  function ajuster(ctx, texte, taille, poids, largeurMax, minimum) {
    var t = taille;
    ctx.font = poids + ' ' + t + 'px ' + POLICE;
    while (ctx.measureText(texte).width > largeurMax && t > minimum) {
      t -= 2;
      ctx.font = poids + ' ' + t + 'px ' + POLICE;
    }
    if (ctx.measureText(texte).width <= largeurMax) return texte;
    var coupe = texte;
    while (coupe.length > 1 && ctx.measureText(coupe + '\u2026').width > largeurMax) coupe = coupe.slice(0, -1);
    return coupe.replace(/\s+$/, '') + '\u2026';
  }

  function degrade(ctx, x0, y0, x1, y1, arrets) {
    var g = ctx.createLinearGradient(x0, y0, x1, y1);
    arrets.forEach(function (a) { g.addColorStop(a[0], a[1]); });
    return g;
  }

  function palmier(ctx, x, y, hauteur, miroir) {
    if (!window.Path2D || !PALMIER.d) return;
    var k = hauteur / PALMIER.h;
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(miroir ? -k : k, k);
    ctx.translate(-PALMIER.x - PALMIER.l * 0.39, -(PALMIER.y + PALMIER.h));
    ctx.fillStyle = '#150c25';
    ctx.fill(new Path2D(PALMIER.d));
    ctx.restore();
  }

  function dessinerCarte(o) {
    var L = 1080, H = 1350, HORIZON = 1000, ROUTE = 1165;
    var c = document.createElement('canvas');
    c.width = L;
    c.height = H;
    var ctx = c.getContext('2d');
    var pct = Math.max(0, Math.min(100, Number(o.pct) || 0));
    var marque = document.querySelector('.marque > span:last-child');
    var x, y, i;

    ctx.fillStyle = degrade(ctx, 0, 0, 0, HORIZON, [[0, '#1b1230'], [0.3, '#4b1f66'], [0.55, '#9b2f80'],
      [0.76, '#e8467f'], [0.9, '#ff7a5c'], [1, '#ffd98a']]);
    ctx.fillRect(0, 0, L, HORIZON);

    var halo = ctx.createRadialGradient(540, HORIZON, 80, 540, HORIZON, 480);
    halo.addColorStop(0, 'rgba(255, 214, 140, 0.7)');
    halo.addColorStop(1, 'rgba(255, 130, 90, 0)');
    ctx.fillStyle = halo;
    ctx.fillRect(0, HORIZON - 480, L, 480);
    ctx.beginPath();
    ctx.arc(540, HORIZON, 150, Math.PI, 0);
    ctx.fillStyle = degrade(ctx, 0, HORIZON - 150, 0, HORIZON, [[0, '#fff1c2'], [1, '#ffb35c']]);
    ctx.fill();

    ctx.fillStyle = 'rgba(62, 22, 70, 0.78)';
    ctx.fillRect(0, HORIZON - 26, L, 5);
    for (x = 18; x < L; x += 56) ctx.fillRect(x, HORIZON - 22, 4, 22);

    ctx.fillStyle = degrade(ctx, 0, HORIZON, 0, ROUTE, [[0, '#b4487e'], [0.45, '#5b2468'], [1, '#2b1747']]);
    ctx.fillRect(0, HORIZON, L, ROUTE - HORIZON);
    for (y = HORIZON + 8, i = 0; y < ROUTE - 8; y += 13, i++) {
      var l = 300 * (1 - (y - HORIZON) / (ROUTE - HORIZON)) + 50;
      ctx.fillStyle = 'rgba(255, 214, 140, ' + Math.max(0.08, 0.62 - i * 0.05) + ')';
      ctx.fillRect(540 - l / 2 + (i % 2 ? 16 : -12), y, l, 4);
    }

    palmier(ctx, 70, ROUTE + 4, 900, false);
    palmier(ctx, 1015, ROUTE + 4, 720, true);

    ctx.fillStyle = '#2a2238';
    ctx.fillRect(0, ROUTE, L, H - ROUTE);
    ctx.fillStyle = 'rgba(255, 138, 76, 0.6)';
    ctx.fillRect(0, ROUTE, L, 4);
    ctx.fillStyle = '#ffc94a';
    for (x = 24; x < L; x += 112) ctx.fillRect(x, ROUTE + 28, 60, 6);

    ctx.fillStyle = degrade(ctx, 0, 0, 22, 0, [[0, '#6d5a86'], [1, '#2f2342']]);
    ctx.save();
    ctx.translate(318, 0);
    ctx.fillRect(0, 780, 22, ROUTE - 780);
    ctx.translate(422, 0);
    ctx.fillRect(0, 780, 22, ROUTE - 780);
    ctx.restore();

    arrondi(ctx, 90, 150, 900, 640, 36);
    ctx.fillStyle = '#0b6b4f';
    ctx.fill();
    arrondi(ctx, 108, 168, 864, 604, 24);
    ctx.lineWidth = 7;
    ctx.strokeStyle = '#fff6ee';
    ctx.stroke();

    ctx.fillStyle = '#fff6ee';
    ctx.font = '700 46px ' + POLICE;
    var onglet = ctx.measureText('GTA 6').width + 44;
    arrondi(ctx, 160, 222, onglet, 70, 12);
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.fillText('GTA 6', 182, 274);

    police(ctx, o.titre, 104, '700', 760);
    ctx.fillText(o.titre, 160, 420);
    police(ctx, o.ligne, 58, '400', 760);
    ctx.fillText(o.ligne, 160, 498);

    arrondi(ctx, 160, 548, 760, 44, 8);
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.fill();
    ctx.save();
    arrondi(ctx, 160, 548, 760, 44, 8);
    ctx.clip();
    ctx.fillStyle = degrade(ctx, 160, 0, 920, 0, [[0, '#ffc94a'], [0.5, '#ff8a4c'], [1, '#ff4f9b']]);
    ctx.fillRect(160, 548, 760 * pct / 100, 44);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    for (x = 160; x < 920; x += 46) ctx.fillRect(x, 567, 28, 6);
    ctx.restore();

    ctx.fillStyle = '#fff6ee';
    ctx.font = '700 132px ' + POLICE;
    ctx.fillText(pct + (EN ? '' : ESP) + '%', 160, 730);

    ctx.font = '700 54px ' + POLICE;
    ctx.fillText(marque ? marque.textContent : 'Objectif 100' + ESP + '%', 90, 1262);
    ctx.fillStyle = '#c6b8da';
    ctx.font = '400 40px ' + POLICE;
    ctx.fillText(adresseCourte(), 90, 1316);
    return c;
  }

  // Flèche de la croix directionnelle, dessinée (indépendante des polices du téléphone).
  function fleche(ctx, cx, cy, taille, direction) {
    var angle = { H: -Math.PI / 2, D: 0, B: Math.PI / 2, G: Math.PI }[direction];
    if (angle === undefined) return;
    var s = taille / 2;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle);
    ctx.beginPath();
    ctx.moveTo(s * 0.95, 0);
    ctx.lineTo(s * 0.1, -s * 0.72);
    ctx.lineTo(s * 0.1, -s * 0.28);
    ctx.lineTo(-s * 0.9, -s * 0.28);
    ctx.lineTo(-s * 0.9, s * 0.28);
    ctx.lineTo(s * 0.1, s * 0.28);
    ctx.lineTo(s * 0.1, s * 0.72);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  // Planche des combinaisons connues, sur deux colonnes, au format d'un écran de téléphone.
  function dessinerPlanche(o) {
    var L = 1080, MARGE = 48, GOUTTIERE = 40, ENTETE = 380, LIGNE = 150, PIED = 220, HORIZON = 300;
    var colonne = (L - 2 * MARGE - GOUTTIERE) / 2;
    var codes = o.codes || [];
    var H = ENTETE + Math.ceil(codes.length / 2) * LIGNE + PIED;
    var c = document.createElement('canvas');
    c.width = L;
    c.height = H;
    var ctx = c.getContext('2d');
    var marque = document.querySelector('.marque > span:last-child');
    var x;

    ctx.fillStyle = '#1b1230';
    ctx.fillRect(0, 0, L, H);
    ctx.fillStyle = degrade(ctx, 0, 0, 0, HORIZON, [[0, '#4b1f66'], [0.42, '#9b2f80'], [0.7, '#e8467f'], [0.88, '#ff7a5c'], [1, '#ffd98a']]);
    ctx.fillRect(0, 0, L, HORIZON);
    ctx.beginPath();
    ctx.arc(890, HORIZON, 96, Math.PI, 0);
    ctx.fillStyle = degrade(ctx, 0, HORIZON - 96, 0, HORIZON, [[0, '#fff1c2'], [1, '#ffb35c']]);
    ctx.fill();
    ctx.fillStyle = 'rgba(62, 22, 70, 0.7)';
    ctx.fillRect(0, HORIZON - 18, L, 3);
    for (x = 12; x < L; x += 44) ctx.fillRect(x, HORIZON - 15, 3, 15);
    ctx.fillStyle = degrade(ctx, 0, HORIZON, 0, HORIZON + 44, [[0, '#b4487e'], [1, '#2b1747']]);
    ctx.fillRect(0, HORIZON, L, 44);
    palmier(ctx, 1046, HORIZON + 46, 330, true);

    arrondi(ctx, MARGE, 46, 720, 214, 26);
    ctx.fillStyle = '#0b6b4f';
    ctx.fill();
    arrondi(ctx, MARGE + 13, 59, 694, 188, 16);
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#fff6ee';
    ctx.stroke();
    ctx.fillStyle = '#fff6ee';
    police(ctx, o.titre || '', 64, '700', 620);
    ctx.fillText(o.titre || '', MARGE + 48, 150);
    police(ctx, o.sousTitre || '', 38, '400', 620);
    ctx.fillText(o.sousTitre || '', MARGE + 48, 212);

    codes.forEach(function (code, n) {
      var x0 = MARGE + (n % 2) * (colonne + GOUTTIERE);
      var y0 = ENTETE + Math.floor(n / 2) * LIGNE;
      var touches = String(code.sequence || '').split('');
      var ecart = 6;
      var taille = Math.min(40, Math.floor((colonne - (touches.length - 1) * ecart) / Math.max(1, touches.length)));
      ctx.fillStyle = '#fff6ee';
      ctx.fillText(ajuster(ctx, code.nom, 34, '700', colonne, 18), x0, y0 + 34);
      touches.forEach(function (t, k) {
        var tx = x0 + k * (taille + ecart);
        var ty = y0 + 58;
        arrondi(ctx, tx, ty, taille, taille, 7);
        ctx.fillStyle = '#261a42';
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#46365f';
        ctx.stroke();
        ctx.fillStyle = '#fff6ee';
        fleche(ctx, tx + taille / 2, ty + taille / 2, taille * 0.62, t);
      });
    });

    var bas = H - PIED;
    ctx.fillStyle = degrade(ctx, MARGE, 0, L - MARGE, 0, [[0, '#ffc94a'], [0.5, '#ff8a4c'], [1, '#ff4f9b']]);
    ctx.fillRect(MARGE, bas + 24, L - 2 * MARGE, 5);
    ctx.fillStyle = '#c6b8da';
    police(ctx, o.avertissement || '', 32, '400', L - 2 * MARGE);
    ctx.fillText(o.avertissement || '', MARGE, bas + 84);
    ctx.fillStyle = '#fff6ee';
    ctx.font = '700 46px ' + POLICE;
    ctx.fillText(marque ? marque.textContent : 'Objectif 100' + ESP + '%', MARGE, bas + 150);
    ctx.fillStyle = '#c6b8da';
    ctx.font = '400 34px ' + POLICE;
    ctx.fillText(adresseCourte(), MARGE, bas + 196);
    return c;
  }

  function telecharger(blob, nom, dire) {
    var lien = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = lien;
    a.download = nom;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(lien); }, 4000);
    dire(T.image);
  }

  // Feuille de partage du téléphone avec l'image ; sinon téléchargement de l'image et copie du lien.
  function partagerCanvas(canvas, texte, nom, elEtat) {
    var dire = function (message) { if (elEtat) elEtat.textContent = message; };
    var url = adresseCanonique();
    if (!canvas || !canvas.toBlob) {
      copierLien(texte, url, dire, false);
      return;
    }
    canvas.toBlob(function (blob) {
      if (!blob) { copierLien(texte, url, dire, false); return; }
      var fichier = null;
      try { fichier = new File([blob], nom, { type: 'image/png' }); } catch (e) { fichier = null; }
      if (fichier && navigator.canShare && navigator.canShare({ files: [fichier] })) {
        navigator.share({ files: [fichier], title: document.title, text: texte + ' ' + url })
          .then(function () { dire(T.partagee); }, function (err) {
            if (!err || err.name !== 'AbortError') telecharger(blob, nom, dire);
          });
        return;
      }
      telecharger(blob, nom, dire);
      copierLien(texte, url, dire, true);
    }, 'image/png');
  }

  function partagerCarte(o, elEtat) {
    var canvas;
    try { canvas = dessinerCarte(o); } catch (e) { canvas = null; }
    partagerCanvas(canvas, o.texte, T.fichier, elEtat);
  }

  function partagerPlanche(o, elEtat) {
    var canvas;
    try { canvas = dessinerPlanche(o); } catch (e) { canvas = null; }
    partagerCanvas(canvas, o.texte, o.fichier || T.fichier, elEtat);
  }

  window.O100 = { partagerCarte: partagerCarte, dessinerCarte: dessinerCarte,
    partagerPlanche: partagerPlanche, dessinerPlanche: dessinerPlanche };
})();

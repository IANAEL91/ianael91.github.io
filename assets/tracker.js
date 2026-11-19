/* Trackers (trophées, codes de triche) : progression enregistrée sur l'appareil, filtres et partage. */
(function () {
  'use strict';

  function normaliser(texte) {
    return String(texte || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  }

  function initialiser(racine) {
    var cle = 'o100:' + racine.getAttribute('data-tracker');
    var items = Array.prototype.slice.call(racine.querySelectorAll('li[data-id]'));
    var total = items.length;
    var q = function (selecteur) { return racine.querySelector(selecteur); };
    var elFaits = q('[data-faits]');
    var elTotal = q('[data-total]');
    var elPct = q('[data-pct]');
    var barre = q('.route');
    var rempli = q('.route__rempli');
    var boutonsFiltre = Array.prototype.slice.call(racine.querySelectorAll('[data-filtre]'));
    var selectCat = q('[data-categorie]');
    var connus = q('[data-connus]');
    var recherche = q('[data-recherche]');
    var reveler = q('[data-reveler]');
    var carte = q('[data-carte]');
    var raz = q('[data-raz]');
    var vide = q('[data-vide]');
    var etatCarte = q('[data-carte-etat]');
    var filtre = 'tous';
    var etat = { n: 0, pct: 0 };

    function lire(suffixe, defaut) {
      try {
        var brut = localStorage.getItem(cle + suffixe);
        return brut === null ? defaut : JSON.parse(brut);
      } catch (e) { return defaut; }
    }
    function ecrire(suffixe, valeur) {
      try { localStorage.setItem(cle + suffixe, JSON.stringify(valeur)); } catch (e) { /* stockage indisponible */ }
    }
    function caseDe(li) { return li.querySelector('input[type="checkbox"]'); }

    function majProgression(sauver) {
      var ids = items.filter(function (li) { return caseDe(li).checked; })
        .map(function (li) { return li.getAttribute('data-id'); });
      if (sauver) ecrire(':trophees', ids);
      etat.n = ids.length;
      etat.pct = total ? Math.round(ids.length / total * 100) : 0;
      elFaits.textContent = etat.n;
      if (elTotal) elTotal.textContent = total;
      elPct.textContent = etat.pct;
      rempli.style.width = etat.pct + '%';
      barre.setAttribute('aria-valuenow', String(etat.pct));
    }

    function filtrer() {
      var cat = selectCat ? selectCat.value : '';
      var seulementConnus = connus ? connus.checked : false;
      var mots = recherche ? normaliser(recherche.value).split(/\s+/).filter(Boolean) : [];
      var visibles = 0;
      items.forEach(function (li) {
        var fait = caseDe(li).checked;
        var texte = li.getAttribute('data-texte') || '';
        var ok = (filtre === 'tous' || (filtre === 'faits') === fait) &&
          (!cat || li.getAttribute('data-cat') === cat) &&
          (!seulementConnus || li.getAttribute('data-connu') === '1') &&
          mots.every(function (m) { return texte.indexOf(m) !== -1; });
        li.hidden = !ok;
        if (ok) visibles++;
      });
      if (vide) vide.hidden = visibles > 0;
    }

    var faits = lire(':trophees', []);
    items.forEach(function (li) {
      var box = caseDe(li);
      box.checked = faits.indexOf(li.getAttribute('data-id')) !== -1;
      li.classList.toggle('is-fait', box.checked);
      box.addEventListener('change', function () {
        li.classList.toggle('is-fait', box.checked);
        majProgression(true);
        filtrer();
      });
    });

    boutonsFiltre.forEach(function (b) {
      b.addEventListener('click', function () {
        filtre = b.getAttribute('data-filtre');
        boutonsFiltre.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        filtrer();
      });
    });
    if (selectCat) selectCat.addEventListener('change', filtrer);
    if (connus) connus.addEventListener('change', filtrer);
    if (recherche) recherche.addEventListener('input', filtrer);

    if (reveler) {
      var details = Array.prototype.slice.call(racine.querySelectorAll('details.revele'));
      var appliquer = function (actif, sauver) {
        details.forEach(function (d) { d.open = actif; });
        reveler.setAttribute('aria-pressed', String(actif));
        reveler.textContent = actif ? (racine.getAttribute('data-libelle-masquer') || 'Masquer les trophées cachés')
          : (racine.getAttribute('data-libelle-reveler') || 'Révéler les trophées cachés');
        if (sauver) ecrire(':reveler', actif);
      };
      reveler.addEventListener('click', function () { appliquer(reveler.getAttribute('aria-pressed') !== 'true', true); });
      if (lire(':reveler', false)) appliquer(true, false);
    }

    if (carte) {
      carte.addEventListener('click', function () {
        var modele = racine.getAttribute('data-partage-modele') || document.title;
        var texte = modele.replace('{pct}', etat.pct).replace('{n}', etat.n).replace('{total}', total);
        var ligne = etat.n + '\u00a0' + (racine.getAttribute('data-sur') || 'sur') + ' ' + total + ' ' + (racine.getAttribute('data-unite') || '');
        if (window.O100 && window.O100.partagerCarte) {
          window.O100.partagerCarte({
            titre: racine.getAttribute('data-carte-titre') || document.title,
            ligne: ligne.trim(),
            pct: etat.pct,
            texte: texte
          }, etatCarte);
        }
      });
    }

    if (raz) {
      var libelle = raz.textContent;
      var confirmer = racine.getAttribute('data-libelle-confirmer') || 'Confirmer\u202f: tout décocher';
      var arme = false;
      var minuterie;
      raz.addEventListener('click', function () {
        if (!arme) {
          arme = true;
          raz.textContent = confirmer;
          minuterie = setTimeout(function () { arme = false; raz.textContent = libelle; }, 4000);
          return;
        }
        clearTimeout(minuterie);
        arme = false;
        raz.textContent = libelle;
        items.forEach(function (li) { caseDe(li).checked = false; li.classList.remove('is-fait'); });
        majProgression(true);
        filtrer();
      });
    }

    // Codes : une combinaison en grand, l'écran reste allumé pendant qu'on la tape.
    var dialogue = q('[data-dialogue]');
    if (dialogue) {
      var titreGrand = dialogue.querySelector('[data-grand-titre]');
      var suiteGrand = dialogue.querySelector('[data-grand-sequence]');
      var symboles = { H: '\u2191', B: '\u2193', G: '\u2190', D: '\u2192' };
      var noms = {};
      try { noms = JSON.parse(dialogue.getAttribute('data-noms') || '{}'); } catch (e) { noms = {}; }
      var verrou = null;
      racine.addEventListener('click', function (ev) {
        var bouton = ev.target.closest ? ev.target.closest('[data-grand]') : null;
        var li = bouton ? bouton.closest('li[data-sequence]') : null;
        if (!li) return;
        var touches = (li.getAttribute('data-sequence') || '').split('').filter(function (c) { return symboles[c]; });
        var nom = li.querySelector('.code__nom');
        titreGrand.textContent = nom ? nom.textContent : '';
        suiteGrand.innerHTML = '';
        touches.forEach(function (c) {
          var puce = document.createElement('li');
          puce.textContent = symboles[c];
          suiteGrand.appendChild(puce);
        });
        suiteGrand.setAttribute('aria-label', (dialogue.getAttribute('data-prefixe') || '') +
          touches.map(function (c) { return noms[c] || c; }).join(', '));
        if (dialogue.showModal) dialogue.showModal(); else dialogue.setAttribute('open', '');
        if (navigator.wakeLock && navigator.wakeLock.request) {
          navigator.wakeLock.request('screen').then(function (v) { verrou = v; }, function () {});
        }
      });
      dialogue.addEventListener('click', function (ev) {
        if (ev.target.closest && ev.target.closest('[data-fermer]')) {
          if (dialogue.close) dialogue.close(); else dialogue.removeAttribute('open');
        }
      });
      dialogue.addEventListener('close', function () {
        if (verrou) { verrou.release().catch(function () {}); verrou = null; }
      });
    }

    // Codes : toutes les combinaisons connues dans une image à garder sur son téléphone.
    var planche = q('[data-planche]');
    if (planche) {
      planche.addEventListener('click', function () {
        var codes = items.filter(function (li) { return li.getAttribute('data-sequence'); }).map(function (li) {
          var nom = li.querySelector('.code__nom');
          var doute = li.getAttribute('data-a-confirmer') ? ' ' + (planche.getAttribute('data-libelle-a-confirmer') || '') : '';
          return { nom: (nom ? nom.textContent : '') + doute, sequence: li.getAttribute('data-sequence') };
        });
        if (window.O100 && window.O100.partagerPlanche) {
          window.O100.partagerPlanche({
            titre: planche.getAttribute('data-titre'),
            sousTitre: (planche.getAttribute('data-sous-titre') || '').replace('{n}', codes.length),
            avertissement: planche.getAttribute('data-avertissement'),
            texte: planche.getAttribute('data-texte'),
            fichier: planche.getAttribute('data-fichier'),
            codes: codes
          }, etatCarte);
        }
      });
    }

    majProgression(false);
    filtrer();
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-tracker]'), initialiser);
})();

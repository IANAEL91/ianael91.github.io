/* Calculateur : place et temps de téléchargement pour GTA 6. */
(function () {
  'use strict';
  var TAILLE = 212; // Go, chiffre annoncé par Rockstar
  var CLE = 'o100:place';
  var ESP = ' ';
  var FINE = ' ';
  var form = document.getElementById('calcul');
  if (!form) return;

  var EN = (document.documentElement.lang || '').slice(0, 2) === 'en';
  var nombre = new Intl.NumberFormat(EN ? 'en-US' : 'fr-FR', { maximumFractionDigits: 0 });
  var go = function (n) { return nombre.format(n) + ESP + (EN ? 'GB' : 'Go'); };
  var T = EN ? {
    contexte: function (utile, pct) { return 'On this console, about ' + go(utile) + ' is usable in total: GTA 6 takes ' + pct + '%.'; },
    sansContexte: 'Check the exact free space in your console’s storage settings.',
    entrer: 'Enter your free space',
    entrerTexte: 'We’ll tell you right away if the ' + go(TAILLE) + ' fits.',
    ok: 'It fits',
    reste: function (n) { return 'You’ll have about ' + go(n) + ' left after installing.'; },
    manque: function (n) { return 'You’re ' + go(n) + ' short'; },
    manqueTexte: 'Free up space before you start the download. The fixes are just below.',
    temps: function (debit, duree) { return 'At ' + nombre.format(debit) + ESP + 'Mbps: about ' + duree; },
    sansDebit: 'Add your speed to estimate the download time.',
    jour: 'd'
  } : {
    contexte: function (utile, pct) { return 'Sur cette console, environ ' + go(utile) + ' sont utilisables au total' + FINE + ': GTA 6 en prend ' + pct + ESP + '%.'; },
    sansContexte: 'Regarde l’espace libre exact dans les paramètres de stockage de ta console.',
    entrer: 'Entre ton espace libre',
    entrerTexte: 'On te dit tout de suite si les ' + go(TAILLE) + ' passent.',
    ok: 'Ça passe',
    reste: function (n) { return 'Il te restera environ ' + go(n) + ' après l’installation.'; },
    manque: function (n) { return 'Il te manque ' + go(n); },
    manqueTexte: 'Libère de la place avant de lancer le téléchargement. Les solutions sont juste en dessous.',
    temps: function (debit, duree) { return 'À ' + nombre.format(debit) + ESP + 'Mb/s' + FINE + ': environ ' + duree; },
    sansDebit: 'Ajoute ton débit pour estimer le temps de téléchargement.',
    jour: 'j'
  };

  var champConsole = form.elements.console;
  var champLibre = form.elements.libre;
  var champDebit = form.elements.debit;
  var puces = Array.prototype.slice.call(form.querySelectorAll('[data-debit]'));
  var contexte = document.getElementById('contexte');
  var resultat = document.getElementById('resultat');
  var resTitre = document.getElementById('res-titre');
  var resTexte = document.getElementById('res-texte');
  var resTemps = document.getElementById('res-temps');
  var conseils = Array.prototype.slice.call(document.querySelectorAll('[data-conseils]'));

  function lire(champ) {
    var brut = String(champ.value).replace(/\s/g, '').replace(',', '.');
    if (brut === '') return null;
    var v = parseFloat(brut);
    return isFinite(v) && v >= 0 ? v : null;
  }

  function duree(heures) {
    var min = Math.max(1, Math.round(heures * 60));
    if (min < 60) return min + ESP + 'min';
    var h = Math.floor(min / 60);
    var m = min % 60;
    if (h < 48) return h + ESP + 'h' + (m ? ESP + (m < 10 ? '0' : '') + m : '');
    return Math.floor(h / 24) + ESP + T.jour + ESP + (h % 24) + ESP + 'h';
  }

  function couleur(classe) {
    resultat.className = 'sign resultat' + (classe ? ' ' + classe : '');
  }

  function calculer() {
    var choix = champConsole.options[champConsole.selectedIndex];
    var famille = choix.getAttribute('data-famille');
    var utile = Number(choix.getAttribute('data-utile'));
    contexte.textContent = utile ? T.contexte(utile, Math.round(TAILLE / utile * 100)) : T.sansContexte;

    var libre = lire(champLibre);
    var debit = lire(champDebit);
    conseils.forEach(function (bloc) { bloc.hidden = true; });

    if (libre === null) {
      couleur('sign--bleu');
      resTitre.textContent = T.entrer;
      resTexte.textContent = T.entrerTexte;
    } else if (libre >= TAILLE) {
      couleur('');
      resTitre.textContent = T.ok;
      resTexte.textContent = T.reste(libre - TAILLE);
    } else {
      couleur('sign--jaune');
      resTitre.textContent = T.manque(Math.ceil(TAILLE - libre));
      resTexte.textContent = T.manqueTexte;
      conseils.forEach(function (bloc) { if (bloc.getAttribute('data-conseils') === famille) bloc.hidden = false; });
    }

    resTemps.textContent = debit ? T.temps(debit, duree(TAILLE * 8000 / (debit * 3600))) : T.sansDebit;

    puces.forEach(function (p) {
      p.setAttribute('aria-pressed', String(debit !== null && Number(p.getAttribute('data-debit')) === debit));
    });
    sauver();
  }

  function sauver() {
    try {
      localStorage.setItem(CLE, JSON.stringify({ c: champConsole.value, l: champLibre.value, d: champDebit.value }));
    } catch (e) { /* stockage indisponible : on continue sans mémoriser */ }
  }

  function restaurer() {
    try {
      var s = JSON.parse(localStorage.getItem(CLE) || 'null');
      if (!s) return;
      if (s.c && form.querySelector('option[value="' + s.c + '"]')) champConsole.value = s.c;
      if (s.l) champLibre.value = s.l;
      if (s.d) champDebit.value = s.d;
    } catch (e) { /* rien à restaurer */ }
  }

  puces.forEach(function (p) {
    p.addEventListener('click', function () {
      champDebit.value = p.getAttribute('data-debit');
      calculer();
    });
  });
  form.addEventListener('input', calculer);
  form.addEventListener('change', calculer);
  form.addEventListener('submit', function (e) { e.preventDefault(); calculer(); });

  restaurer();
  calculer();
})();

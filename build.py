#!/usr/bin/env python3
"""
Construit le site bilingue (français à la racine, anglais dans /en/) dans le dossier dist/.

  python build.py            build normal : récupère les vidéos officielles de Rockstar
  python build.py --offline  sans réseau : garde le cache des vidéos
  python build.py --preview  liens vers index.html, pour ouvrir le site sans serveur
  python build.py --date=2026-12-05   construit le site comme ce jour-là (contenu de Noël...)
  python build.py --indexnow          après construction, signale les pages à Bing et IndexNow

Aucune dépendance : seulement la bibliothèque standard de Python (3.9 ou plus).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote_plus, urlparse

RACINE = Path(__file__).resolve().parent
SRC = RACINE / "src"
PAGES = SRC / "pages"
ASSETS = RACINE / "assets"
DATA = RACINE / "data"
DIST = RACINE / "dist"

APERCU = "--preview" in sys.argv
HORS_LIGNE = "--offline" in sys.argv or APERCU

ESP = " "   # espace insécable
FLECHES = {"H": "↑", "B": "↓", "G": "←", "D": "→"}
TYPES_TROPHEE = ("platine", "or", "argent", "bronze")
NS_YOUTUBE = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
MACRO = re.compile(r"\{\{\s*([a-z_]+)(?::([^}]*))?\s*\}\}")
PARIS = dt.timezone(dt.timedelta(hours=1))  # heure d'hiver, suffisant pour comparer des dates
# Contenu de saison dans les pages :
#   <!--jusquau 2026-11-30--> ... <!--fin-->   affiché jusqu'à cette date incluse
#   <!--du 2026-12-01 au 2026-12-25--> ... <!--fin-->
#   <!--apartir 2026-12-26--> ... <!--fin-->
PERIODE = re.compile(
    r"<!--\s*(?:du\s+(\d{4}-\d{2}-\d{2})\s+au\s+(\d{4}-\d{2}-\d{2})|jusquau\s+(\d{4}-\d{2}-\d{2})"
    r"|apartir\s+(\d{4}-\d{2}-\d{2}))\s*-->(.*?)<!--\s*fin\s*-->", re.S)


def date_forcee():
    """--date=AAAA-MM-JJ : construit le site comme si on était ce jour-là (pour vérifier Noël, par exemple)."""
    for arg in sys.argv[1:]:
        if arg.startswith("--date="):
            jour = dt.date.fromisoformat(arg.split("=", 1)[1])
            return dt.datetime(jour.year, jour.month, jour.day, 12, tzinfo=PARIS).astimezone(dt.timezone.utc)
    return None

TEXTES = {
    "fr": {
        "og_locale": "fr_FR", "og_image": "og.png", "in_language": "fr-FR",
        "evitement": "Aller au contenu", "menu_label": "Menu principal",
        "menu": [("codes-de-triche-gta-6", "Codes"), ("trophees-gta-6", "Trophées"),
                 ("place-gta-6", "Place"), ("infos-gta-6", "Infos")],
        "pied_avertissement": "Site de fan non officiel, non affilié à Rockstar Games ni à Take-Two Interactive. "
                              "Grand Theft Auto et GTA sont des marques de Take-Two Interactive.",
        "pied_liens": [("problemes-gta-6", "Problèmes de lancement"), ("bons-plans-gta-6", "Bons plans"),
                       ("mentions-legales", "Mentions légales"), ("confidentialite", "Confidentialité")],
        "langue_lien": "EN", "langue_titre": "Read this page in English",
        "affiliation": "Liens affiliés&#8239;: en tant que Partenaire Amazon, je réalise un bénéfice sur les achats "
                       "remplissant les conditions requises.",
        "videos_titre": "Dernières vidéos officielles",
        "videos_texte": "Mises à jour chaque jour depuis la chaîne YouTube de Rockstar Games.",
        "jours": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
        "mois": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
                 "octobre", "novembre", "décembre"],
        "mois_courts": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.",
                        "nov.", "déc."],
        "hero_avant_titre": "Déblocage en France", "hero_apres_titre": "Disponible en France",
        "hero_depuis_le": "Depuis le {jour}", "hero_aujourdhui": "Sorti aujourd’hui",
        "hero_depuis": "Depuis {n} jour{s}", "hero_dans": "Dans",
        "hero_chapo_avant": "Sur PS5 et Xbox Series X|S, à minuit heure de Paris. Prépare la place maintenant, "
                            "puis suis tes trophées ici.",
        "hero_chapo_apres": "Sur PS5 et Xbox Series X|S. Codes de triche, trophées, place et problèmes de lancement\u202f: "
                            "tout ce qu’il faut pour GTA 6, en français.",
        "a_completer": "[À compléter]",
        "types": {"platine": "Platine", "or": "Or", "argent": "Argent", "bronze": "Bronze"},
        "fleches": {"H": "haut", "B": "bas", "G": "gauche", "D": "droite"},
        "combinaison": "Combinaison\u202f: ", "combinaison_inconnue": "Combinaison pas encore connue",
        "combinaison_a_confirmer": "Combinaison à confirmer", "pour_debloquer": "Pour le débloquer&#8239;:",
        "a_confirmer": " (à confirmer)", "condition_inconnue": "Pas encore connue.",
        "categorie": "Catégorie", "toutes_categories": "Toutes les catégories", "afficher": "Afficher",
        "progression": "Progression", "partager": "Partager ma progression", "tout_decocher": "Tout décocher",
        "confirmer": "Confirmer\u202f: tout décocher", "sources": "Sources", "sources_liste": "Sources de la liste",
        "manquable": "Manquable", "trophee_cache": "Trophée caché ({cat})", "voir_trophee": "Voir le trophée (spoiler)",
        "reveler": "Révéler les trophées cachés", "masquer": "Masquer les trophées cachés",
        "t_compte": "trophées", "t_unite": "du platine", "t_pied": "{v} visibles, {c} cachés",
        "t_modele": "J’en suis à {pct} % du platine de GTA 6 ({n} sur {total} trophées).", "t_carte": "Mon platine",
        "t_libelles": ("Tous", "À faire", "Obtenus"), "t_vide": "Aucun trophée dans ce filtre.",
        "t_attente_titre": "Liste officielle pas encore publiée",
        "c_compte": "codes débloqués", "c_unite": "des codes", "c_pied": "{k} combinaisons connues",
        "c_modele": "J’ai débloqué {n} codes de triche sur {total} dans GTA 6.", "c_carte": "Mes codes de triche",
        "c_libelles": ("Tous", "À débloquer", "Débloqués"), "c_vide": "Aucun code ne correspond à ta recherche.",
        "c_connue": "Combinaison connue", "c_chercher": "Chercher un code",
        "c_placeholder": "Chercher (ex. Banshee, munitions)", "sur": "sur", "esp_pct": ESP,
        "og_alt": "Panneau routier vert devant un coucher de soleil\u202f: codes de triche et trophées de GTA 6",
        "maj": "Mis à jour le {date}",
        "mesure_audience": "<h2>Mesure d’audience</h2>\n  <p>Le site compte ses visites avec Cloudflare Web Analytics, "
                           "sans cookie ni stockage sur ton appareil, et sans te suivre d’un site à l’autre.</p>",
        "grand": "Afficher en grand", "fermer": "Fermer",
        "grand_aide": "Sors le téléphone du jeu, puis entre la combinaison avec la croix directionnelle.",
        "planche": "Enregistrer les combinaisons en image", "planche_titre": "Codes de triche GTA 6",
        "planche_sous_titre": "{n} combinaisons connues",
        "planche_avertissement": "Un code actif bloque les trophées\u202f: sauvegarde avant.",
        "planche_texte": "Les combinaisons des codes de triche de GTA 6\u202f:",
        "planche_fichier": "codes-de-triche-gta-6.png",
    },
    "en": {
        "og_locale": "en_US", "og_image": "og-en.png", "in_language": "en",
        "evitement": "Skip to content", "menu_label": "Main menu",
        "menu": [("gta-6-cheats", "Cheats"), ("gta-6-trophies", "Trophies"),
                 ("gta-6-storage", "Storage"), ("gta-6-info", "Info")],
        "pied_avertissement": "Unofficial fan site, not affiliated with Rockstar Games or Take-Two Interactive. "
                              "Grand Theft Auto and GTA are trademarks of Take-Two Interactive.",
        "pied_liens": [("gta-6-problems", "Launch problems"), ("gta-6-deals", "Deals"),
                       ("legal-notice", "Legal notice"), ("privacy", "Privacy")],
        "langue_lien": "FR", "langue_titre": "Lire cette page en français",
        "affiliation": "Affiliate links: as an Amazon Associate I earn from qualifying purchases.",
        "videos_titre": "Latest official videos",
        "videos_texte": "Updated daily from the Rockstar Games YouTube channel.",
        "jours": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "mois": ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                 "October", "November", "December"],
        "mois_courts": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "hero_avant_titre": "Unlocks worldwide", "hero_apres_titre": "Out now",
        "hero_depuis_le": "Since {jour}", "hero_aujourdhui": "Out today",
        "hero_depuis": "Out for {n} day{s}", "hero_dans": "In",
        "hero_chapo_avant": "On PS5 and Xbox Series X|S, at midnight local time. Make room now, then track your "
                            "trophies here.",
        "hero_chapo_apres": "On PS5 and Xbox Series X|S. Cheat codes, trophies, storage and launch fixes: "
                            "everything you need for GTA 6.",
        "a_completer": "[To be completed]",
        "types": {"platine": "Platinum", "or": "Gold", "argent": "Silver", "bronze": "Bronze"},
        "fleches": {"H": "up", "B": "down", "G": "left", "D": "right"},
        "combinaison": "Sequence: ", "combinaison_inconnue": "Sequence not found yet",
        "combinaison_a_confirmer": "Sequence to be confirmed", "pour_debloquer": "To unlock:",
        "a_confirmer": " (to be confirmed)", "condition_inconnue": "Not known yet.",
        "categorie": "Category", "toutes_categories": "All categories", "afficher": "Show",
        "progression": "Progress", "partager": "Share my progress", "tout_decocher": "Uncheck all",
        "confirmer": "Confirm: uncheck all", "sources": "Sources", "sources_liste": "List sources",
        "manquable": "Missable", "trophee_cache": "Hidden trophy ({cat})", "voir_trophee": "Show trophy (spoiler)",
        "reveler": "Reveal hidden trophies", "masquer": "Hide hidden trophies",
        "t_compte": "trophies", "t_unite": "of the platinum", "t_pied": "{v} visible, {c} hidden",
        "t_modele": "I’m {pct}% of the way to the GTA 6 platinum ({n} of {total} trophies).", "t_carte": "My platinum",
        "t_libelles": ("All", "To do", "Earned"), "t_vide": "No trophy matches this filter.",
        "t_attente_titre": "Official list not published yet",
        "c_compte": "codes unlocked", "c_unite": "of the codes", "c_pied": "{k} known sequences",
        "c_modele": "I’ve unlocked {n} of {total} cheat codes in GTA 6.", "c_carte": "My cheat codes",
        "c_libelles": ("All", "Locked", "Unlocked"), "c_vide": "No code matches your search.",
        "c_connue": "Known sequence", "c_chercher": "Search a code",
        "c_placeholder": "Search (e.g. Banshee, ammo)", "sur": "of", "esp_pct": "",
        "og_alt": "Green road sign at sunset: GTA 6 cheat codes and trophies",
        "maj": "Updated {date}",
        "mesure_audience": "<h2>Audience measurement</h2>\n  <p>The site counts visits with Cloudflare Web Analytics, "
                           "without cookies or storage on your device, and without tracking you across sites.</p>",
        "grand": "Show full screen", "fermer": "Close",
        "grand_aide": "Bring out the in-game phone, then enter the sequence with the d-pad.",
        "planche": "Save the sequences as an image", "planche_titre": "GTA 6 cheat codes",
        "planche_sous_titre": "{n} known sequences",
        "planche_avertissement": "An active cheat blocks trophies: save first.",
        "planche_texte": "GTA 6 cheat code sequences:",
        "planche_fichier": "gta-6-cheat-codes.png",
    },
}

AVERTISSEMENTS: list[str] = []


def avertir(message: str) -> None:
    if message not in AVERTISSEMENTS:
        AVERTISSEMENTS.append(message)


def e(texte) -> str:
    """Échappe un texte pour l'insérer dans du HTML."""
    return html.escape(str(texte), quote=True)


def lire_json(chemin: Path, defaut=None):
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return defaut
    except json.JSONDecodeError as exc:
        sys.exit(f"Erreur dans {chemin.relative_to(RACINE)} : {exc}")


def pour_recherche(*morceaux: str) -> str:
    """Texte en minuscules et sans accents, pour la recherche côté navigateur."""
    texte = " ".join(m for m in morceaux if m)
    sans_accents = "".join(c for c in unicodedata.normalize("NFD", texte) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sans_accents.lower()).strip()


def slug_sur(valeur: str, defaut: str) -> str:
    return re.sub(r"[^a-z0-9_-]", "", str(valeur or "").lower()) or defaut


def local(element: dict, cle: str, langue: str, defaut: str = "") -> str:
    """Champ traduit si disponible (element["en"][cle]), sinon le champ français."""
    if langue != "fr":
        traduit = (element.get(langue) or {}).get(cle)
        if traduit:
            return str(traduit)
    return str(element.get(cle) or defaut)


def analyser_flux(xml_brut: bytes, mots_cles: list[str], maximum: int) -> list[dict]:
    """Garde les vidéos du flux YouTube dont le titre contient un des mots-clés."""
    racine = ET.fromstring(xml_brut)
    motifs = [re.compile(r"(?<!\w)" + re.escape(m.casefold()) + r"(?!\w)") for m in mots_cles if m.strip()]
    videos = []
    for entree in racine.findall("a:entry", NS_YOUTUBE):
        vid = (entree.findtext("yt:videoId", default="", namespaces=NS_YOUTUBE) or "").strip()
        titre = (entree.findtext("a:title", default="", namespaces=NS_YOUTUBE) or "").strip()
        publie = (entree.findtext("a:published", default="", namespaces=NS_YOUTUBE) or "").strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", vid) or not titre:
            continue
        if motifs and not any(m.search(titre.casefold()) for m in motifs):
            continue
        videos.append({"id": vid, "titre": titre, "date": publie[:10]})
        if len(videos) >= maximum:
            break
    return videos


def texte_brut(fragment: str) -> str:
    sans_balises = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(sans_balises)).strip()


def jsonld(donnees: dict) -> str:
    contenu = json.dumps(donnees, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">{contenu}</script>'


def faq_jsonld(fragment: str) -> str:
    paires = re.findall(
        r'<section class="faq__item">\s*<h2>(.*?)</h2>\s*<div class="faq__reponse">(.*?)</div>',
        fragment, re.S)
    if not paires:
        return ""
    return jsonld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": texte_brut(q),
             "acceptedAnswer": {"@type": "Answer", "text": texte_brut(r)}}
            for q, r in paires
        ],
    })


def sources_html(sources: list[dict], intro: str) -> str:
    liens = [f'<a href="{e(s.get("url", ""))}" rel="noopener">{e(s.get("nom", ""))}</a>'
             for s in sources or [] if s.get("url")]
    return f'<p class="source">{intro}&#8239;: {", ".join(liens)}</p>' if liens else ""


def sequence_html(sequence: str, t: dict) -> str:
    touches = [c for c in sequence.upper() if c in FLECHES]
    if not touches:
        return f'<p class="sequence sequence--inconnue">{e(t["combinaison_inconnue"])}</p>'
    libelle = t["combinaison"] + ", ".join(t["fleches"][c] for c in touches)
    puces = "".join(f"<li>{FLECHES[c]}</li>" for c in touches)
    return f'<ol class="sequence" aria-label="{e(libelle)}">{puces}</ol>'


def chemin_page(langue: str, slug: str) -> str:
    """Chemin de la page depuis la racine du site, avec une barre finale."""
    debut = "" if langue == "fr" else f"{langue}/"
    return debut + (f"{slug}/" if slug else "")


class Site:
    def __init__(self) -> None:
        self.cfg = lire_json(RACINE / "site.json", {}) or {}
        domaine = (self.cfg.get("domaine_perso") or "").strip().strip("/")
        url = ("https://" + domaine) if domaine else (self.cfg.get("url") or "").strip()
        self.url = url.rstrip("/")
        self.domaine = domaine
        self.base = (urlparse(self.url).path.rstrip("/") + "/") if self.url else "/"
        self.maintenant = date_forcee() or dt.datetime.now(dt.timezone.utc)
        self.version = self.maintenant.strftime("%Y%m%d%H%M")
        self.sortie = dt.datetime.fromisoformat(self.cfg.get("sortie") or "2026-11-19T00:00:00+01:00")
        self.trophees = lire_json(DATA / "gta6-trophees.json", {}) or {}
        self.codes = lire_json(DATA / "gta6-codes.json", {}) or {}
        self.codes_ajoutes = self.appliquer_maj_codes()
        self.videos = self.recuperer_videos()
        self.client_pub = self.verifier_adsense()
        self.verifier_config()

    def appliquer_maj_codes(self) -> int:
        """Ajoute les combinaisons du fichier data/gta6-codes-maj.json (envoyé par la tâche automatique)."""
        maj = lire_json(DATA / "gta6-codes-maj.json", None)
        if not isinstance(maj, dict):
            return 0
        par_id = {c.get("id"): c for c in self.codes.get("liste") or []}
        ajouts = 0
        for cid, info in (maj.get("sequences") or {}).items():
            code = par_id.get(cid)
            brut = info.get("sequence") if isinstance(info, dict) else info
            sequence = re.sub(r"\s", "", str(brut or "")).upper()
            if not code:
                avertir(f"Mise à jour des codes : identifiant inconnu « {cid} », ignoré.")
                continue
            if not re.fullmatch(r"[HBGD]{4,16}", sequence):
                avertir(f"Mise à jour des codes : combinaison invalide pour « {cid} » ({sequence}), ignorée.")
                continue
            if code.get("sequence") != sequence:
                code["sequence"] = sequence
                ajouts += 1
            code.pop("sequence_a_confirmer", None)
        for cid, info in (maj.get("conditions") or {}).items():
            code = par_id.get(cid)
            if not code or not isinstance(info, dict):
                continue
            if (info.get("fr") or "").strip():
                code["condition"] = info["fr"].strip()
                code.pop("condition_a_confirmer", None)
            if (info.get("en") or "").strip():
                code.setdefault("en", {})["condition"] = info["en"].strip()
        connues = {s.get("url") for s in self.codes.get("sources") or []}
        for source in maj.get("sources") or []:
            if isinstance(source, dict) and source.get("url") and source["url"] not in connues:
                self.codes.setdefault("sources", []).append({"nom": source.get("nom") or source["url"], "url": source["url"]})
                connues.add(source["url"])
        if maj.get("maj"):
            self.codes["maj"] = max(str(self.codes.get("maj") or ""), str(maj["maj"]))
        return ajouts

    # ---------- vérifications ----------
    def verifier_config(self) -> None:
        if not self.url or "ton-pseudo" in self.url:
            avertir("Mets l'adresse de ton site dans site.json (champ url) pour le sitemap et les liens de partage.")
        editeur = self.cfg.get("editeur") or {}
        if not all((editeur.get(c) or "").strip() for c in ("nom", "statut", "adresse", "email")):
            avertir("Mentions légales incomplètes : remplis la partie editeur de site.json avant d'activer la pub ou l'affiliation.")
        if not (self.cfg.get("amazon_tag") or "").strip():
            avertir("Pas d'identifiant Amazon Partenaires (amazon_tag) : les liens d'achat français ne rapportent rien pour l'instant.")
        if not ((self.cfg.get("amazon_en") or {}).get("tag") or "").strip():
            avertir("Pas d'identifiant Amazon Associates pour la version anglaise (amazon_en.tag).")

    def verifier_adsense(self) -> str:
        client = (self.cfg.get("adsense_client") or "").strip()
        if client and not re.fullmatch(r"ca-pub-\d{10,20}", client):
            avertir(f"Identifiant AdSense invalide ({client}) : il doit ressembler à ca-pub-1234567890123456. Pub désactivée.")
            return ""
        return client

    # ---------- liens ----------
    def lien(self, slug: str, prefixe: str, langue: str) -> str:
        chemin = chemin_page(langue, "" if slug in ("", "index") else slug)
        cible = (prefixe + chemin) or "./"
        return cible + ("index.html" if APERCU else "")

    def amazon(self, requete: str, langue: str) -> str:
        if langue == "fr":
            domaine, tag = "www.amazon.fr", (self.cfg.get("amazon_tag") or "").strip()
        else:
            reglage = self.cfg.get("amazon_en") or {}
            domaine = (reglage.get("domaine") or "www.amazon.com").strip()
            tag = (reglage.get("tag") or "").strip()
        url = f"https://{domaine}/s?k=" + quote_plus(requete.strip())
        return url + (f"&tag={quote_plus(tag)}" if tag else "")

    def note_affiliation(self, langue: str) -> str:
        tag = self.cfg.get("amazon_tag") if langue == "fr" else (self.cfg.get("amazon_en") or {}).get("tag")
        if not (tag or "").strip():
            return ""
        return f'<p class="discret affiliation">{TEXTES[langue]["affiliation"]}</p>'

    # ---------- blocs dynamiques ----------
    def dans_periode(self, du=None, jusqua=None) -> bool:
        jour = self.maintenant.astimezone(PARIS).date()
        try:
            if du and jour < dt.date.fromisoformat(str(du)):
                return False
            if jusqua and jour > dt.date.fromisoformat(str(jusqua)):
                return False
        except ValueError:
            avertir(f"Date invalide ({du or ''} {jusqua or ''}) : format attendu AAAA-MM-JJ.")
        return True

    def appliquer_periodes(self, fragment: str) -> str:
        def remplacer(m: re.Match) -> str:
            du, au, jusquau, apartir, contenu = m.groups()
            return contenu if self.dans_periode(du or apartir, au or jusquau) else ""
        return PERIODE.sub(remplacer, fragment)

    def meta_saison(self, meta: dict) -> dict:
        resultat = dict(meta)
        for saison in meta.get("saisons") or []:
            if isinstance(saison, dict) and self.dans_periode(saison.get("du"), saison.get("jusqua")):
                resultat.update({k: v for k, v in saison.items() if k in ("titre", "description")})
        return resultat

    def bandeau(self, prefixe: str, langue: str, slug: str) -> str:
        """Le premier bandeau de site.json dont la période contient aujourd'hui (Black Friday, puis Noël...)."""
        liste = self.cfg.get("bandeaux")
        if not isinstance(liste, list):
            liste = [self.cfg.get("bandeau") or {}]
        suffixe = "" if langue == "fr" else f"_{langue}"
        for b in liste:
            if not isinstance(b, dict):
                continue
            texte = (b.get("texte" + suffixe) or "").strip()
            cible = (b.get("lien" + suffixe) or "").strip()
            if not texte or not self.dans_periode(b.get("du"), b.get("jusqua")):
                continue
            if cible and cible == slug:
                return ""
            return f'<p class="bandeau"><a href="{self.lien(cible, prefixe, langue)}">{e(texte)}</a></p>'
        return ""

    def date_longue(self, d: dt.date, langue: str) -> str:
        t = TEXTES[langue]
        if langue == "fr":
            return f"{'1er' if d.day == 1 else d.day} {t['mois'][d.month - 1]} {d.year}"
        return f"{t['mois'][d.month - 1]} {d.day}, {d.year}"

    def ligne_maj(self, donnees: dict, langue: str) -> str:
        try:
            jour = dt.date.fromisoformat(str(donnees.get("maj") or ""))
        except ValueError:
            return ""
        return f'<p class="discret maj">{e(TEXTES[langue]["maj"].format(date=self.date_longue(jour, langue)))}</p>'

    # ---------- outils de suivi (Search Console, mesure d'audience, IndexNow) ----------
    def code_verification(self) -> str:
        brut = (self.cfg.get("google_site_verification") or "").strip()
        m = re.search(r'content="([^"]+)"', brut)
        code = m.group(1) if m else brut
        return code if re.fullmatch(r"[A-Za-z0-9_-]{10,100}", code or "") else ""

    def jeton_cloudflare(self) -> str:
        brut = (self.cfg.get("cloudflare_analytics") or "").strip()
        m = re.search(r'"token"\s*:\s*"([^"]+)"', brut)
        jeton = m.group(1) if m else brut
        if jeton and not re.fullmatch(r"[A-Za-z0-9]{16,64}", jeton):
            avertir("Jeton Cloudflare Web Analytics invalide (cloudflare_analytics) : mesure d'audience désactivée.")
            return ""
        return jeton

    def cle_indexnow(self) -> str:
        cle = (self.cfg.get("indexnow") or "").strip()
        return cle if re.fullmatch(r"[A-Za-z0-9-]{8,128}", cle) else ""

    def signaler_indexnow(self) -> None:
        """Prévient Bing et les autres moteurs IndexNow que les pages ont changé (appelé après une publication)."""
        cle = self.cle_indexnow()
        if not cle or not self.url or "ton-pseudo" in self.url:
            print("IndexNow : rien à signaler (adresse du site ou clé manquante).")
            return
        corps = json.dumps({"host": urlparse(self.url).hostname, "key": cle,
                            "keyLocation": f"{self.url}/{cle}.txt", "urlList": self.urls_sitemap}).encode("utf-8")
        requete = urllib.request.Request("https://api.indexnow.org/indexnow", data=corps, method="POST",
                                         headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(requete, timeout=20) as reponse:
                print(f"IndexNow : {len(self.urls_sitemap)} pages signalées (réponse {reponse.status}).")
        except Exception as exc:  # jamais bloquant
            print(f"IndexNow : envoi impossible ({exc}).")

    def date_jour(self, d: dt.datetime, langue: str) -> str:
        t = TEXTES[langue]
        if langue == "fr":
            return f"{t['jours'][d.weekday()]} {d.day} {t['mois'][d.month - 1]}"
        return f"{t['jours'][d.weekday()]}, {t['mois'][d.month - 1]} {d.day}"

    def hero(self, langue: str) -> str:
        t = TEXTES[langue]
        s = self.sortie
        ecart = (s - self.maintenant).total_seconds()
        jour_txt = self.date_jour(s, langue)
        apres_titre = t["hero_apres_titre"]
        apres_detail = t["hero_depuis_le"].format(jour=jour_txt)
        if ecart > 0:
            minutes = int(-(-ecart // 60))
            j, reste = divmod(minutes, 1440)
            h, m = divmod(reste, 60)
            unite_jour = "j" if langue == "fr" else "d"
            morceaux = []
            if j:
                morceaux.append(f"{j}{ESP}{unite_jour}")
            if j or h:
                morceaux.append(f"{h}{ESP}h")
            if not j:
                morceaux.append(f"{m}{ESP}min")
            titre = t["hero_avant_titre"]
            detail = f"{jour_txt[0].upper()}{jour_txt[1:]}, 00{ESP}h{ESP}00" if langue == "fr" else jour_txt
            distance = f"{t['hero_dans']} " + " ".join(morceaux)
            chapo = t["hero_chapo_avant"]
        else:
            jours = int(-ecart // 86400)
            titre, detail, chapo = apres_titre, apres_detail, t["hero_chapo_apres"]
            distance = t["hero_aujourdhui"] if jours == 0 else t["hero_depuis"].format(n=jours, s="s" if jours > 1 else "")
        return (
            '<div class="hero__scene">\n'
            '  <div class="hero__soleil" aria-hidden="true"></div>\n'
            '  <div class="hero__pont" aria-hidden="true"></div>\n'
            '  <div class="hero__mer" aria-hidden="true"></div>\n'
            '  <div class="hero__palmier hero__palmier--gauche" aria-hidden="true"></div>\n'
            '  <div class="hero__palmier hero__palmier--droite" aria-hidden="true"></div>\n'
            '  <div class="hero__route" aria-hidden="true"></div>\n'
            '  <div class="hero__panneau">\n'
            f'    <div class="sign sign--hero" data-cible="{e(s.isoformat())}" '
            f'data-apres-titre="{e(apres_titre)}" data-apres-detail="{e(apres_detail)}">\n'
            f'      <h1 id="hero-titre"><span class="sign__route">GTA 6</span>'
            f'<span class="sign__titre" data-titre>{e(titre)}</span></h1>\n'
            f'      <p class="sign__detail" data-detail>{e(detail)}</p>\n'
            f'      <p class="sign__distance" data-compte>{e(distance)}</p>\n'
            '    </div>\n'
            '    <div class="poteaux" aria-hidden="true"></div>\n'
            '  </div>\n'
            '</div>\n'
            f'<p class="chapo" data-chapo data-apres="{e(t["hero_chapo_apres"])}">{e(chapo)}</p>'
        )

    def recuperer_videos(self) -> list[dict]:
        cache = lire_json(DATA / "videos-cache.json", []) or []
        if HORS_LIGNE:
            return cache
        yt = self.cfg.get("youtube") or {}
        if (yt.get("channel_id") or "").strip():
            flux = "https://www.youtube.com/feeds/videos.xml?channel_id=" + quote_plus(yt["channel_id"].strip())
        elif (yt.get("user") or "").strip():
            flux = "https://www.youtube.com/feeds/videos.xml?user=" + quote_plus(yt["user"].strip())
        else:
            return cache
        try:
            requete = urllib.request.Request(flux, headers={"User-Agent": "Mozilla/5.0 (objectif100 build)"})
            with urllib.request.urlopen(requete, timeout=20) as reponse:
                videos = analyser_flux(reponse.read(), yt.get("mots_cles") or [], int(yt.get("max") or 6))
        except Exception as exc:  # réseau, XML invalide... on garde le cache
            avertir(f"Vidéos YouTube non récupérées ({exc}) : le cache est utilisé.")
            return cache
        try:
            (DATA / "videos-cache.json").write_text(
                json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError:
            pass
        return videos

    def bloc_videos(self, langue: str) -> str:
        if not self.videos:
            return ""
        t = TEXTES[langue]
        items = []
        for v in self.videos:
            vid = e(v.get("id", ""))
            date_html = ""
            try:
                d = dt.date.fromisoformat(v.get("date", ""))
                mois = t["mois_courts"][d.month - 1]
                texte_date = f"{d.day}{ESP}{mois} {d.year}" if langue == "fr" else f"{mois} {d.day}, {d.year}"
                date_html = f'<time class="videos__date" datetime="{d.isoformat()}">{texte_date}</time>'
            except ValueError:
                pass
            items.append(
                f'<li><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">'
                f'<img src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" alt="" width="320" height="180" loading="lazy">'
                f'<span class="videos__titre">{e(v.get("titre", ""))}</span></a>{date_html}</li>')
        return ('<section class="bloc" aria-labelledby="videos-titre">\n'
                f'  <h2 id="videos-titre">{e(t["videos_titre"])}</h2>\n'
                f'  <p class="discret">{e(t["videos_texte"])}</p>\n'
                f'  <ul class="videos__liste">{"".join(items)}</ul>\n'
                '</section>')

    # ---------- trackers ----------
    @staticmethod
    def entete_tracker(t: dict, cle: str, compte: str, unite: str, pied_droit: str, modele: str,
                       carte: str, libelles: tuple, options: str, extras: str = "") -> str:
        tous, afaire, faits = libelles
        return f'''<div class="tracker" data-tracker="{e(cle)}" data-unite="{e(compte)}" data-partage-modele="{e(modele)}" data-carte-titre="{e(carte)}" data-libelle-reveler="{e(t["reveler"])}" data-libelle-masquer="{e(t["masquer"])}" data-libelle-confirmer="{e(t["confirmer"])}" data-sur="{e(t["sur"])}">
  <div class="sign etat" aria-live="polite">
    <p class="sign__titre"><span data-faits>0</span> {e(t["sur"])} <span data-total>0</span> {e(compte)}</p>
    <div class="route" role="progressbar" aria-label="{e(t["progression"])}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span class="route__rempli"></span></div>
    <p class="etat__pied"><span><span data-pct>0</span>{t["esp_pct"]}% {e(unite)}</span><span>{e(pied_droit)}</span></p>
  </div>
  <div class="outils">
    <div class="segment" role="group" aria-label="{e(t["afficher"])}">
      <button type="button" data-filtre="tous" aria-pressed="true">{e(tous)}</button>
      <button type="button" data-filtre="afaire" aria-pressed="false">{e(afaire)}</button>
      <button type="button" data-filtre="faits" aria-pressed="false">{e(faits)}</button>
    </div>
    <label class="visuellement-cache" for="categorie-{e(cle)}">{e(t["categorie"])}</label>
    <select id="categorie-{e(cle)}" data-categorie><option value="">{e(t["toutes_categories"])}</option>{options}</select>
    {extras}
  </div>'''

    @staticmethod
    def pied_tracker(t: dict, vide: str, boutons: str = "") -> str:
        return f'''  <p class="discret vide" data-vide hidden>{e(vide)}</p>
  <p class="boutons">
    <button type="button" class="bouton" data-carte>{e(t["partager"])}</button>{boutons}
    <button type="button" class="bouton bouton--contour" data-raz>{e(t["tout_decocher"])}</button>
  </p>
  <p class="discret carte-etat" data-carte-etat aria-live="polite"></p>'''

    def bloc_trophees(self, langue: str) -> str:
        t = TEXTES[langue]
        donnees = self.trophees
        liste = donnees.get("liste") or []
        if donnees.get("statut") != "officiel" or not liste:
            return f'<div class="sign sign--jaune attente" role="note"><p class="sign__titre">{e(t["t_attente_titre"])}</p></div>'
        categories = (donnees.get("categories_en") if langue != "fr" else None) or donnees.get("categories") or {}
        utilisees: list[str] = []
        lignes = []
        caches = 0
        for i, tr in enumerate(liste, start=1):
            tid = slug_sur(tr.get("id"), f"t{i:02d}")
            cat = str(tr.get("categorie") or "divers")
            if cat not in utilisees:
                utilisees.append(cat)
            typ = str(tr.get("type") or "bronze").lower()
            nom = str(tr.get("nom") or "")
            desc = local(tr, "description", langue).strip()
            astuce = local(tr, "astuce", langue).strip()
            type_txt = t["types"].get(typ, typ.capitalize())
            cat_txt = categories.get(cat, cat.capitalize())
            desc_html = f'<p class="trophee__desc">{e(desc)}</p>' if desc else ""
            if tr.get("cache"):
                caches += 1
                visible = t["trophee_cache"].format(cat=cat_txt.lower())
                corps = (f'<details class="revele"><summary>{e(t["voir_trophee"])}</summary>'
                         f'<p class="trophee__vrai-nom">{e(nom)}</p>{desc_html}</details>')
            else:
                visible = nom
                corps = desc_html
            astuce_html = f'<p class="trophee__astuce">{e(astuce)}</p>' if astuce else ""
            plaque = f'<p class="plaque">{e(t["manquable"])}</p>' if tr.get("manquable") else ""
            lignes.append(
                f'<li class="trophee{" trophee--cache" if tr.get("cache") else ""}" data-id="{tid}" '
                f'data-cat="{e(cat)}" data-type="{e(typ)}" data-texte="{e(pour_recherche(nom, desc, cat_txt))}">'
                f'<input type="checkbox" id="t-{tid}">'
                f'<label for="t-{tid}"><span class="trophee__nom">{e(visible)}</span>'
                f'<span class="trophee__type">{e(type_txt)}</span></label>'
                f'{corps}{astuce_html}{plaque}</li>')
        options = "".join(f'<option value="{e(c)}">{e(categories.get(c, c.capitalize()))}</option>'
                          for c in utilisees)
        extras = f'<button type="button" class="puce" data-reveler aria-pressed="false">{e(t["reveler"])}</button>'
        entete = self.entete_tracker(
            t, "gta6", t["t_compte"], t["t_unite"], t["t_pied"].format(v=len(liste) - caches, c=caches),
            t["t_modele"], t["t_carte"], t["t_libelles"], options, extras)
        note = local(donnees, "note", langue) if langue == "fr" else (donnees.get(f"note_{langue}") or "")
        note_html = f'<p class="discret">{e(note)}</p>' if note else ""
        return (entete + f'\n  <ul class="trophees">{"".join(lignes)}</ul>\n'
                + self.pied_tracker(t, t["t_vide"]) + "\n</div>\n"
                + note_html + sources_html(donnees.get("sources") or [], t["sources_liste"]))

    def bloc_codes(self, langue: str) -> str:
        t = TEXTES[langue]
        donnees = self.codes
        liste = donnees.get("liste") or []
        if not liste:
            return ""
        categories = (donnees.get("categories_en") if langue != "fr" else None) or donnees.get("categories") or {}
        utilisees: list[str] = []
        lignes = []
        connus = 0
        for i, code in enumerate(liste, start=1):
            cid = slug_sur(code.get("id"), f"c{i:02d}")
            cat = str(code.get("categorie") or "joueur")
            if cat not in utilisees:
                utilisees.append(cat)
            sequence = str(code.get("sequence") or "")
            connu = bool(sequence)
            connus += connu
            nom = local(code, "nom", langue)
            effet = local(code, "effet", langue)
            condition = local(code, "condition", langue, t["condition_inconnue"])
            cat_txt = categories.get(cat, cat.capitalize())
            a_confirmer = (f'<p class="plaque">{e(t["combinaison_a_confirmer"])}</p>'
                           if code.get("sequence_a_confirmer") else "")
            cond_note = t["a_confirmer"] if code.get("condition_a_confirmer") else ""
            attr_seq = f' data-sequence="{e(sequence.upper())}"' if connu else ""
            if connu and code.get("sequence_a_confirmer"):
                attr_seq += ' data-a-confirmer="1"'
            grand = f'<button type="button" class="lien-bouton" data-grand>{e(t["grand"])}</button>' if connu else ""
            lignes.append(
                f'<li class="code" data-id="{cid}" data-cat="{e(cat)}" data-connu="{1 if connu else 0}"{attr_seq} '
                f'data-texte="{e(pour_recherche(nom, effet, condition, cat_txt))}">'
                f'<input type="checkbox" id="c-{cid}">'
                f'<label for="c-{cid}"><span class="code__nom">{e(nom)}</span>'
                f'<span class="code__cat">{e(cat_txt)}</span></label>'
                f'<p class="code__effet">{e(effet)}</p>'
                f'{sequence_html(sequence, t)}{grand}{a_confirmer}'
                f'<p class="code__condition"><span>{t["pour_debloquer"]}</span> {e(condition)}{e(cond_note)}</p></li>')
        options = "".join(f'<option value="{e(k)}">{e(categories.get(k, k.capitalize()))}</option>'
                          for k in utilisees)
        extras = (f'<label class="interrupteur"><input type="checkbox" data-connus> {e(t["c_connue"])}</label>\n'
                  f'    <label class="visuellement-cache" for="recherche-codes">{e(t["c_chercher"])}</label>\n'
                  '    <input type="search" id="recherche-codes" class="recherche" data-recherche '
                  f'placeholder="{e(t["c_placeholder"])}" autocomplete="off">')
        entete = self.entete_tracker(
            t, "gta6-codes", t["c_compte"], t["c_unite"], t["c_pied"].format(k=connus),
            t["c_modele"], t["c_carte"], t["c_libelles"], options, extras)
        note = donnees.get("note") if langue == "fr" else donnees.get(f"note_{langue}")
        note_html = f'<p class="discret">{e(note)}</p>' if note else ""
        planche = (f'\n    <button type="button" class="bouton bouton--contour" data-planche '
                   f'data-titre="{e(t["planche_titre"])}" data-sous-titre="{e(t["planche_sous_titre"])}" '
                   f'data-avertissement="{e(t["planche_avertissement"])}" data-texte="{e(t["planche_texte"])}" '
                   f'data-fichier="{e(t["planche_fichier"])}" data-libelle-a-confirmer="{e(t["a_confirmer"].strip())}">'
                   f'{e(t["planche"])}</button>') if connus else ""
        noms = json.dumps(t["fleches"], ensure_ascii=False)
        dialogue = (f'\n  <dialog class="grand" data-dialogue aria-labelledby="grand-titre" '
                    f'data-prefixe="{e(t["combinaison"])}" data-noms="{e(noms)}">\n'
                    '    <p class="grand__titre" id="grand-titre" data-grand-titre></p>\n'
                    '    <ol class="sequence sequence--grande" data-grand-sequence></ol>\n'
                    f'    <p class="grand__aide">{e(t["grand_aide"])}</p>\n'
                    f'    <p class="boutons"><button type="button" class="bouton" data-fermer>{e(t["fermer"])}</button></p>\n'
                    '  </dialog>')
        return (entete + f'\n  <ul class="codes">{"".join(lignes)}</ul>\n'
                + self.pied_tracker(t, t["c_vide"], planche) + dialogue + "\n</div>\n"
                + note_html + sources_html(donnees.get("sources") or [], t["sources"]))

    # ---------- pages ----------
    def menu(self, courant: str, prefixe: str, langue: str) -> str:
        liens = []
        for slug, libelle in TEXTES[langue]["menu"]:
            actif = ' aria-current="page"' if slug == courant else ""
            liens.append(f'<a href="{self.lien(slug, prefixe, langue)}"{actif}>{e(libelle)}</a>')
        return "".join(liens)

    def pied_liens(self, prefixe: str, langue: str) -> str:
        return " ".join(f'<a href="{self.lien(slug, prefixe, langue)}">{e(libelle)}</a>'
                        for slug, libelle in TEXTES[langue]["pied_liens"])

    def editeur(self, langue: str) -> dict:
        ed = self.cfg.get("editeur") or {}
        vide = TEXTES[langue]["a_completer"]

        def champ(cle: str) -> str:
            valeur = (ed.get(cle) or "").strip()
            return e(valeur) if valeur else vide

        email = (ed.get("email") or "").strip()
        siret = (ed.get("siret") or "").strip()
        return {
            "editeur_nom": champ("nom"),
            "editeur_statut": champ("statut"),
            "editeur_adresse": champ("adresse"),
            "editeur_email": f'<a href="mailto:{e(email)}">{e(email)}</a>' if email else vide,
            "editeur_siret": f"<br>SIRET&#8239;: {e(siret)}" if siret else "",
        }

    def rendre_page(self, layout: str, langue: str, slug: str, meta: dict, fragment: str) -> None:
        t = TEXTES[langue]
        fragment = self.appliquer_periodes(fragment)
        meta = self.meta_saison(meta)
        if slug == "404":
            prefixe, sortie = self.base, DIST / "404.html"
        else:
            profondeur = chemin_page(langue, slug).count("/")
            prefixe = "../" * profondeur
            sortie = DIST / chemin_page(langue, slug) / "index.html"
        nom = self.cfg.get("nom_site") or ""
        titre = meta.get("titre") or nom
        canonical = self.url + "/" + ("" if slug == "404" else chemin_page(langue, slug))

        autre = "en" if langue == "fr" else "fr"
        alt = meta.get("alt")
        head = []
        langue_html = ""
        if alt is not None and slug != "404":
            urls = {langue: canonical, autre: self.url + "/" + chemin_page(autre, alt)}
            for code in ("fr", "en"):
                head.append(f'<link rel="alternate" hreflang="{code}" href="{e(urls[code])}">')
            head.append(f'<link rel="alternate" hreflang="x-default" href="{e(urls["en"])}">')
            langue_html = (f'<a class="langue" href="{self.lien(alt, prefixe, autre)}" hreflang="{autre}" '
                           f'lang="{autre}" title="{e(t["langue_titre"])}">{e(t["langue_lien"])}</a>')
        if slug == "":
            head.append(jsonld({"@context": "https://schema.org", "@type": "WebSite",
                                "name": nom, "url": canonical, "inLanguage": t["in_language"]}))
        if slug == "404":
            head.append('<meta name="robots" content="noindex">')
        head.append(faq_jsonld(fragment))
        verification = self.code_verification()
        if verification:
            head.append(f'<meta name="google-site-verification" content="{e(verification)}">')

        pub = ""
        if self.client_pub:
            pub = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'
                   f'?client={e(self.client_pub)}" crossorigin="anonymous"></script>')

        scripts = "".join(f'<script src="{prefixe}assets/{e(s)}?v={self.version}" defer></script>'
                          for s in meta.get("scripts", []))
        jeton = self.jeton_cloudflare()
        if jeton:
            scripts += ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
                        "data-cf-beacon='{\"token\": \"" + jeton + "\"}'></script>")

        valeurs = {
            "lang": langue,
            "titre": e(titre),
            "titre_complet": e(f"{titre} | {nom}" if nom and titre != nom else titre),
            "description": e(meta.get("description", "")),
            "canonical": e(canonical),
            "url": e(self.url),
            "nom_site": e(nom),
            "racine": prefixe,
            "version": self.version,
            "og_locale": t["og_locale"],
            "og_image": t["og_image"],
            "evitement": e(t["evitement"]),
            "menu_label": e(t["menu_label"]),
            "menu": self.menu(meta.get("nav", ""), prefixe, langue),
            "langue": langue_html,
            "pied_avertissement": e(t["pied_avertissement"]),
            "pied_liens": self.pied_liens(prefixe, langue),
            "scripts": scripts,
            "head_extra": "\n".join(h for h in head if h),
            "pub_head": pub,
            "bandeau": self.bandeau(prefixe, langue, slug),
            "og_alt": e(t["og_alt"]),
            "maj_codes": self.ligne_maj(self.codes, langue),
            "maj_trophees": self.ligne_maj(self.trophees, langue),
            "mesure_audience": t["mesure_audience"] if jeton else "",
            "hero": self.hero(langue) if "{{hero}}" in fragment else "",
            "videos": self.bloc_videos(langue) if "{{videos}}" in fragment else "",
            "trophees": self.bloc_trophees(langue) if "{{trophees}}" in fragment else "",
            "codes": self.bloc_codes(langue) if "{{codes}}" in fragment else "",
            "note_affiliation": self.note_affiliation(langue),
            **self.editeur(langue),
        }

        def remplacer(m: re.Match) -> str:
            cle, arg = m.group(1), m.group(2)
            if cle == "lien":
                return self.lien((arg or "").strip(), prefixe, langue)
            if cle == "lien_fr":
                return self.lien((arg or "").strip(), prefixe, "fr")
            if cle == "lien_en":
                return self.lien((arg or "").strip(), prefixe, "en")
            if cle == "amazon":
                return e(self.amazon(arg or "", langue))
            if cle in valeurs:
                return valeurs[cle]
            avertir(f"Macro inconnue {{{{{cle}}}}} dans la page « {langue}/{slug or 'index'} ».")
            return ""

        page = layout.replace("{{contenu}}", fragment.strip())
        page = MACRO.sub(remplacer, page)
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(page, encoding="utf-8")

    def ecrire_annexes(self, pages: list[tuple[str, str, dict, str]]) -> None:
        shutil.copytree(ASSETS, DIST / "assets")
        (DIST / "data").mkdir(exist_ok=True)
        (DIST / "data" / "videos.json").write_text(json.dumps(self.videos, ensure_ascii=False), encoding="utf-8")

        urls = []
        self.urls_sitemap = []
        for langue, slug, meta, _ in pages:
            if slug == "404" or meta.get("sitemap") is False:
                continue
            self.urls_sitemap.append(self.url + "/" + chemin_page(langue, slug))
            urls.append(f"  <url><loc>{e(self.url + '/' + chemin_page(langue, slug))}</loc></url>")
        (DIST / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
        (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {self.url}/sitemap.xml\n",
                                         encoding="utf-8")
        if self.client_pub:
            editeur_pub = self.client_pub.replace("ca-", "", 1)
            (DIST / "ads.txt").write_text(f"google.com, {editeur_pub}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
        if self.domaine:
            (DIST / "CNAME").write_text(self.domaine + "\n", encoding="utf-8")
        (DIST / ".nojekyll").write_text("", encoding="utf-8")
        if self.cle_indexnow():
            (DIST / f"{self.cle_indexnow()}.txt").write_text(self.cle_indexnow(), encoding="utf-8")

        nom = self.cfg.get("nom_site") or "Objectif 100 %"
        manifeste = {
            "name": nom,
            "short_name": "Objectif 100",
            "lang": "fr",
            "start_url": "./",
            "scope": "./",
            "display": "standalone",
            "background_color": "#1b1230",
            "theme_color": "#1b1230",
            "icons": [
                {"src": "assets/icone-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "assets/icone-512.png", "sizes": "512x512", "type": "image/png"},
                {"src": "assets/icone.svg", "sizes": "any", "type": "image/svg+xml"},
            ],
        }
        (DIST / "manifest.webmanifest").write_text(json.dumps(manifeste, ensure_ascii=False, indent=2),
                                                   encoding="utf-8")

    def construire(self) -> int:
        if DIST.exists():
            shutil.rmtree(DIST)
        DIST.mkdir(parents=True)
        layout = (SRC / "layout.html").read_text(encoding="utf-8")
        pages = []
        for langue, dossier in (("fr", PAGES), ("en", PAGES / "en")):
            for fichier in sorted(dossier.glob("*.html")):
                brut = fichier.read_text(encoding="utf-8")
                m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", brut, re.S)
                meta = json.loads(m.group(1)) if m else {}
                fragment = brut[m.end():] if m else brut
                slug = "" if fichier.stem == "index" else fichier.stem
                pages.append((langue, slug, meta, fragment))
        slugs = {(l, s) for l, s, _, _ in pages}
        for langue, slug, meta, _ in pages:
            alt = meta.get("alt")
            autre = "en" if langue == "fr" else "fr"
            if alt is not None and (autre, alt) not in slugs:
                avertir(f"Traduction introuvable : la page {langue}/{slug or 'index'} renvoie vers {autre}/{alt or 'index'}.")
        for langue, slug, meta, fragment in pages:
            self.rendre_page(layout, langue, slug, meta, fragment)
        self.ecrire_annexes(pages)
        return len(pages)


def main() -> None:
    site = Site()
    n = site.construire()
    print(f"Site construit dans dist/ : {n} pages.")
    if site.codes_ajoutes:
        print(f"  + {site.codes_ajoutes} combinaison(s) ajoutée(s) depuis data/gta6-codes-maj.json")
    for message in AVERTISSEMENTS:
        print(f"  ! {message}")
    if "--indexnow" in sys.argv:
        site.signaler_indexnow()


if __name__ == "__main__":
    main()

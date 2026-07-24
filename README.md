# Secret Beauty — Assistante IA

Assistante virtuelle pour Secret Beauty, entreprise camerounaise de cosmétique et de soins
de beauté (manucure, pédicure, soins du visage, vente de produits cosmétiques).

Ce projet permet aux clients de discuter avec une IA qui répond automatiquement à leurs
questions sur les services, les produits, les horaires et le mode de commande.

## Fonctionnalités

- Chat en temps réel avec une IA connectée au catalogue produits réel
- Interface responsive, thème clair/sombre
- Historique des conversations sauvegardé en base de données
- Catalogue produits dynamique (modifiable sans toucher au code)
- Respect de la confidentialité : l'IA ne révèle jamais d'informations internes
  (fournisseurs, marges, données personnelles)

## Stack technique

**Backend**
- Python / Flask
- SQLite (base de données)
- OpenRouter (API IA)

**Frontend**
- HTML / CSS / JavaScript (vanilla)
- marked.js (rendu Markdown → HTML)

## Structure du projet

secret-beauty/
├── backend/
│ ├── app.py
│ ├── config.py
│ ├── database/
│ │ ├── secret_beauty.db
│ │ ├── schema.sql
│ │ └── seed.sql
│ ├── routes/
│ │ └── chat.py
│ ├── services/
│ │ ├── ia_service.py
│ │ └── db_service.py
│ ├── requirements.txt
│ └── .env
└── frontend/
├── index.html
├── style.css
└── script.js

## Installation en local

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd secret-beauty
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

Crée un fichier `.env` dans `backend/` :
OPENROUTER_API_KEY=ta_cle_ici
DATABASE_PATH=database/secret_beauty.db

Initialise la base de données :
```bash
python -m services.db_service
```

Lance le serveur :
```bash
python app.py
```
Le backend tourne sur `http://127.0.0.1:5000`.

### 3. Frontend
Dans un autre terminal :
```bash
cd frontend
python -m http.server 5500
```
Ouvre `http://127.0.0.1:5500` dans le navigateur.

## Base de données

5 tables : `clients`, `conversations`, `messages`, `produits`, `rendez_vous`.
Le schéma complet est dans `backend/database/schema.sql`.

## Déploiement

Prévu sur Render (backend + frontend servis ensemble via Flask).
Variable d'environnement `OPENROUTER_API_KEY` à configurer sur la plateforme d'hébergement.

## Auteur

Franc — développeur du projet, dans le cadre de ses activités de développement de solutions
pour petites entreprises.

## Statut

Projet en développement actif.
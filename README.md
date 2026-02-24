# Smart-Recruit API

API de gestion de recrutement assistée par Intelligence Artificielle utilisant Google Gemini pour l'analyse de compatibilité candidat-offre.

## Description

Smart-Recruit est une API REST qui permet à un cabinet de recrutement de :
- Gérer des candidats et leurs profils
- Créer et gérer des offres d'emploi
- Soumettre des candidatures
- Analyser automatiquement la compatibilité candidat-offre avec l'IA Gemini

##  Technologies Utilisées

- **Flask** 3.0.0 - Framework web Python
- **Flask-SQLAlchemy** 3.1.1 - ORM pour la gestion de base de données
- **PostgreSQL** - Base de données relationnelle
- **Flask-Marshmallow** 0.15.0 - Validation et sérialisation des données
- **Google Gemini 2.0** - Intelligence artificielle pour l'analyse de compatibilité
- **Python** 3.13
--pip install psycopg2-binary  

##  Fonctionnalités

###  Gestion des Candidats (CRUD)
- Création de profils candidats avec validation
- Unicité des emails
- Stockage du parcours professionnel et diplômes

###  Gestion des Offres d'Emploi (CRUD)
- Création d'offres avec description détaillée
- Liste des compétences requises (JSON)
- Définition du salaire proposé

### Gestion des Candidatures
- Soumission de candidatures
- Prévention des doublons
- Vérification d'existence candidat/offre

###  Analyse IA avec Gemini
- Score de compatibilité (0-100)
- Justification détaillée
- Analyse basée sur compétences, expérience et formation

###  Architecture Technique
- **Blueprints** pour la modularisation
- **Service Layer** pour la logique métier (IA)
- **Validation Marshmallow** systématique
- **Gestion d'erreurs** centralisée (404, 500, 400, 409)
- **Variables d'environnement** sécurisées (.env)

##  Structure du Projet
```
smart-recruit-api/
├── models/                      # Modèles SQLAlchemy
│   ├── __init__.py             # Initialisation DB
│   ├── candidat.py             # Modèle Candidat
│   ├── offre_emploi.py         # Modèle OffreEmploi
│   └── candidature.py          # Modèle Candidature
├── schemas/                     # Schémas Marshmallow
│   ├── __init__.py             # Initialisation Marshmallow
│   ├── candidat_schema.py      # Validation Candidat
│   ├── offre_schema.py         # Validation OffreEmploi
│   └── candidature_schema.py   # Validation Candidature
├── routes/                      # Blueprints Flask
│   ├── __init__.py             # Enregistrement des routes
│   ├── candidat_routes.py      # Routes /candidates
│   ├── offre_routes.py         # Routes /offers
│   └── candidature_routes.py   # Routes /apply
├── services/                    # Logique métier
│   ├── __init__.py
│   └── ai_service.py           # Service d'analyse IA Gemini
├── venv/                        # Environnement virtuel
├── .env                         # Variables d'environnement (non versionné)
├── .gitignore                   # Fichiers à ignorer
├── app.py                       # Point d'entrée de l'application
├── config.py                    # Configuration de l'app
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

##  Installation

### Prérequis

- Python 3.9 ou supérieur
- PostgreSQL 12 ou supérieur
- Clé API Google Gemini ([obtenir ici](https://makersuite.google.com/app/apikey))

### 1. Cloner le Projet
```bash
git clone https://github.com/votre-username/smart-recruit-api.git
cd smart-recruit-api
```

### 2. Créer l'Environnement Virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer PostgreSQL
```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE smart_recruit;

# Quitter psql
\q
```

### 5. Configuration des Variables d'Environnement

Créer un fichier `.env` à la racine du projet :
```env
DATABASE_URL=postgresql://postgres:abba@localhost:5432/smart_recruit
GEMINI_API_KEY= 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
SECRET_KEY=c8a343a888cc4452862ffacb75a9d644c82c4eb532e8dc9d2f82e088aa5f3ef6
```

 **Important** : Ne jamais versionner le fichier `.env` !

### 6. Lancer l'Application
```bash
python app.py
```

L'API sera accessible sur **http://localhost:5000**

---

## ⚙️ Configuration

### Fichier `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Fichier `.env` exemple

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_recruit
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SECRET_KEY=c8a343a888cc4452862ffacb75a9d644c82c4eb532e8dc9d2f82e088aa5f3ef6
```

---

## 📡 Endpoints de l'API

### 🏠 Route Principale

```http
GET /
```

**Réponse :**

```json
{
  "message": "Smart-Recruit API",
  "version": "1.0.0",
  "status": "running"
}
```

### 👥 Candidats

#### Lister tous les candidats

```http
GET /api/candidates
```

**Réponse (200) :**

```json
{
  "success": true,
  "candidats": [
    {
      "id": 1,
      "nom": "Fatou Sall",
      "email": "fatou.sall@email.com",
      "bio": "Développeuse Full Stack...",
      "diplome": "Master en IA",
      "date_inscription": "2024-01-30T12:00:00"
    }
  ],
  "total": 1
}
```

#### Créer un candidat

```http
POST /api/candidates
Content-Type: application/json

{
  "nom": "Fatou Sall",
  "email": "fatou.sall@email.com",
  "bio": "Développeuse Full Stack avec 5 ans d'expérience en Python, Flask et React.",
  "diplome": "Master en Intelligence Artificielle"
}
```

**Validations :**
- Nom : 2-100 caractères
- Email : format valide et unique
- Bio : 10-2000 caractères
- Diplôme : 2-200 caractères

###  Offres d'Emploi

#### Créer une offre

```http
POST /api/offers
Content-Type: application/json

{
  "titre": "Développeur Python Senior - Dakar",
  "description": "Nous recherchons un développeur Python expérimenté...",
  "competences": ["Python", "Flask", "PostgreSQL", "Docker", "Git"],
  "salaire": 500000
}
```

**Validations :**
- Titre : 5-200 caractères
- Description : 20-5000 caractères
- Compétences : 1-20 compétences
- Salaire : nombre positif

###  Analyse IA

#### Analyser la compatibilité

```http
POST /api/offers/1/analyze-match
Content-Type: application/json

{
  "candidat_id": 1
}
```

**Réponse (200) - Mode Gemini :**

```json
{
  "success": true,
  "analyse": {
    "score": 87,
    "justification": "Profil très pertinent avec 5 ans d'expérience en Python/Flask.",
    "source": "gemini-ai"
  }
}
```

**Réponse (200) - Mode Fallback :**

```json
{
  "success": true,
  "analyse": {
    "score": 78,
    "justification": "Bon profil. Compétences: Python, Flask - Profil expérimenté",
    "source": "algorithme-local"
  }
}
```

---

##  Frontend

### Accéder au Frontend

```
http://localhost:5000
```

### Fonctionnalités de l'interface
-  Dashboard avec statistiques
-  Liste des candidats avec recherche
-  Liste des offres avec détails
-  Formulaires de création/modification
-  Analyse IA interactive
-  Notifications toast
-  Design responsive (mobile-friendly)

### Couleurs du thème

| Couleur | Code | Usage |
|---------|------|-------|
| Vert menthe | `#14b89f` | Actions positives |
| Rouge corail | `#fa5252` | Actions/alertes |
| Blanc | `#ffffff` | Fond principal |

---

##  Tests

### Test avec cURL (Windows CMD)

```bash
# 1. Créer un candidat
curl -X POST http://localhost:5000/api/candidates ^
  -H "Content-Type: application/json" ^
  -d "{\"nom\":\"Test User\",\"email\":\"test@email.com\",\"bio\":\"Developpeur Python avec experience\",\"diplome\":\"Master Info\"}"

# 2. Lister les candidats
curl http://localhost:5000/api/candidates

# 3. Créer une offre
curl -X POST http://localhost:5000/api/offers ^
  -H "Content-Type: application/json" ^
  -d "{\"titre\":\"Dev Python Senior\",\"description\":\"Recherchons developpeur Python experimente\",\"competences\":[\"Python\",\"Flask\"],\"salaire\":500000}"
```

---

##  Analyse IA

### Mode Gemini (Prioritaire)

Utilise Google Gemini 2.0 pour une analyse détaillée et naturelle.

**Avantages :**
- Analyse contextuelle approfondie
- Justifications naturelles et détaillées
- Compréhension sémantique des compétences

### Mode Fallback (Automatique)

Si Gemini n'est pas disponible, le système bascule automatiquement sur un algorithme intelligent local.

**Critères d'évaluation :**

| Critère | Points max |
|---------|------------|
| Compétences techniques | 40 |
| Niveau de diplôme | 20 |
| Expérience professionnelle | 25 |
| Pertinence du profil | 15 |
| **Total** | **100** |

---

##  Gestion des Erreurs

### Codes HTTP

| Code | Signification | Exemple |
|------|---------------|---------|
| 200 | Succès | GET réussi |
| 201 | Créé | POST réussi |
| 400 | Requête invalide | Données manquantes |
| 404 | Non trouvé | Ressource inexistante |
| 409 | Conflit | Email déjà utilisé |
| 500 | Erreur serveur | Erreur interne |

---

## 🗄 Base de Données

### Schéma des tables

#### Table `candidats`

| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| nom | VARCHAR(100) | NOT NULL |
| email | VARCHAR(120) | UNIQUE, NOT NULL |
| bio | TEXT | |
| diplome | VARCHAR(200) | |
| date_inscription | DATETIME | DEFAULT NOW |

#### Table `offres_emploi`

| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| titre | VARCHAR(200) | NOT NULL |
| description | TEXT | |
| competences | JSON | |
| salaire | FLOAT | |
| date_creation | DATETIME | DEFAULT NOW |

#### Table `candidatures`

| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| candidat_id | INTEGER | FOREIGN KEY |
| offre_id | INTEGER | FOREIGN KEY |
| date_depot | DATETIME | DEFAULT NOW |
| | | UNIQUE(candidat_id, offre_id) |

---

##  Sécurité

| Mesure | Description |
|--------|-------------|
| Variables d'environnement | Clés sensibles dans .env |
| Validation Marshmallow | Vérification systématique des données |
| SQLAlchemy ORM | Protection contre les injections SQL |
| CORS configuré | Contrôle des origines autorisées |
| Gestion d'erreurs | Pas d'exposition des erreurs internes |
| Timeout API | Limite de 15-20s sur appels externes |

---

##  Statistiques du Projet

```
 Fichiers : ~20 fichiers Python/HTML/JS
 Lignes de code : ~2000 lignes
 Endpoints API : 12 routes
 Pages Frontend : 3 sections
 Temps de réponse : <100ms (local), <3s (Gemini)
```

---

##  Développement Futur

-  Authentification JWT
-  Pagination des résultats
-  Filtres de recherche avancés
-  Notifications par email
-  Dashboard administrateur
-  Export PDF des candidatures
-  Tests unitaires (pytest)
-  Documentation Swagger/OpenAPI
-  Dockerisation
-  Déploiement cloud (Heroku/AWS)

---

##  Auteur

**[Votre Nom]**
- 📧 Email : votre.email@example.com
- 🔗 GitHub : github.com/votre-username
- 💼 LinkedIn : linkedin.com/in/votre-profil

*Projet d'examen Flask - Master Informatique*

---

## 📄 Licence

```
MIT License

Copyright (c) 2024 [Votre Nom]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

##  Remerciements

- Flask Documentation
- SQLAlchemy Documentation
- Marshmallow Documentation
- Google Gemini API
- TailwindCSS
- Font Awesome

---

##  Support

Pour toute question ou problème :
-  Créer une issue sur GitHub
-  Consulter la documentation
-  Contacter l'auteur

---

<div align="center">

 **Si ce projet vous a été utile, n'hésitez pas à mettre une étoile !** 

</div>
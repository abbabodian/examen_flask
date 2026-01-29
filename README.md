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
GEMINI_API_KEY= AIzaSyB4bV3STl3xoQPGQ6Hwfh2RKp_NGTWBllY (nombre quota atteint)
SECRET_KEY=c8a343a888cc4452862ffacb75a9d644c82c4eb532e8dc9d2f82e088aa5f3ef6
```

 **Important** : Ne jamais versionner le fichier `.env` !

### 6. Lancer l'Application
```bash
python app.py
```

L'API sera accessible sur **http://localhost:5000**

##  Endpoints de l'API

###  Route Principale

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations sur l'API |

**Exemple de réponse :**
```json
{
  "message": "Smart-Recruit API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": { ... }
}
```

---

###  Gestion des Candidats

#### Créer un Candidat

**POST** `/api/candidates`

**Body :**
```json
{
  "nom": "Fatou Sall",
  "email": "fatou.sall@email.com",
  "bio": "Développeuse Full Stack avec 4 ans d'expérience en Python, Flask, React et PostgreSQL. Passionnée par l'IA et le développement d'APIs modernes.",
  "diplome": "Master en Intelligence Artificielle"
}
```

**Réponse (201 Created) :**
```json
{
  "message": "Candidat créé avec succès",
  "candidat": {
    "id": 1,
    "nom": "Fatou Sall",
    "email": "fatou.sall@email.com",
    "bio": "Développeuse Full Stack...",
    "diplome": "Master en Intelligence Artificielle",
    "date_inscription": "2026-01-16T01:45:23.123456"
  }
}
```

**Validations :**
- Nom : 2-100 caractères
- Email : format valide et unique
- Bio : 10-2000 caractères
- Diplôme : 2-200 caractères

---

###  Gestion des Offres d'Emploi

#### Créer une Offre

**POST** `/api/offers`

**Body :**
```json
{
  "titre": "Développeur Python Senior - Dakar",
  "description": "Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe tech innovante à Dakar. Vous travaillerez sur des projets d'IA, de développement d'APIs REST et d'intégration de solutions cloud.",
  "competences": ["Python", "Flask", "PostgreSQL", "API REST", "Docker", "Git"],
  "salaire": 60000
}
```

**Réponse (201 Created) :**
```json
{
  "message": "Offre créée avec succès",
  "offre": {
    "id": 1,
    "titre": "Développeur Python Senior - Dakar",
    "description": "Nous recherchons...",
    "competences": ["Python", "Flask", "PostgreSQL", "API REST", "Docker", "Git"],
    "salaire": 60000.0,
    "date_creation": "2026-01-16T01:45:23.123456"
  }
}
```

**Validations :**
- Titre : 5-200 caractères
- Description : 20-5000 caractères
- Compétences : 1-20 compétences
- Salaire : nombre positif

---

###  Gestion des Candidatures

#### Soumettre une Candidature

**POST** `/api/apply`

**Body :**
```json
{
  "candidat_id": 1,
  "offre_id": 1
}
```

**Réponse (201 Created) :**
```json
{
  "message": "Candidature soumise avec succès",
  "candidature": {
    "id": 1,
    "candidat_id": 1,
    "offre_id": 1,
    "date_depot": "2026-01-16T01:45:23.123456"
  }
}
```

**Validations :**
- Candidat doit exister
- Offre doit exister
- Pas de candidature en double

---

###  Lister les Candidats d'une Offre

**GET** `/api/offers/<id>/candidates`

**Exemple :** `GET /api/offers/1/candidates`

**Réponse (200 OK) :**
```json
{
  "offre_id": 1,
  "offre_titre": "Développeur Python Senior - Dakar",
  "nombre_candidats": 2,
  "candidats": [
    {
      "id": 1,
      "nom": "Fatou Sall",
      "email": "fatou.sall@email.com",
      "bio": "Développeuse Full Stack...",
      "diplome": "Master en Intelligence Artificielle"
    },
    {
      "id": 2,
      "nom": "Mamadou Diop",
      "email": "mamadou.diop@email.com",
      "bio": "Développeur Backend...",
      "diplome": "Master en Génie Logiciel"
    }
  ]
}
```

---

###  Analyse IA de Compatibilité

#### Analyser la Compatibilité Candidat-Offre

**POST** `/api/offers/<id>/analyze-match`

**Body :**
```json
{
  "candidat_id": 1
}
```

**Réponse (200 OK) :**
```json
{
  "offre": {
    "id": 1,
    "titre": "Développeur Python Senior - Dakar"
  },
  "candidat": {
    "id": 1,
    "nom": "Fatou Sall"
  },
  "analyse": {
    "score": 87,
    "justification": "Profil très pertinent avec 4 ans d'expérience en Python, Flask et PostgreSQL. Compétences en IA correspondent parfaitement aux besoins."
  }
}
```

**Comment ça fonctionne :**
1. L'API récupère l'offre et le candidat
2. Envoie un prompt structuré à Google Gemini 2.0
3. Gemini analyse et retourne un score (0-100) + justification
4. L'API parse et renvoie le résultat au format JSON

---

##  Tests

### Test avec curl (Windows CMD)
```bash
# 1. Créer un candidat
curl -X POST http://localhost:5000/api/candidates -H "Content-Type: application/json" -d "{\"nom\":\"Jean Dupont\",\"email\":\"jean@email.com\",\"bio\":\"Developpeur Python avec 5 ans d experience\",\"diplome\":\"Master Informatique\"}"

# 2. Créer une offre
curl -X POST http://localhost:5000/api/offers -H "Content-Type: application/json" -d "{\"titre\":\"Dev Python\",\"description\":\"Nous recherchons un developpeur Python experimente\",\"competences\":[\"Python\",\"Flask\"],\"salaire\":45000}"

# 3. Soumettre une candidature
curl -X POST http://localhost:5000/api/apply -H "Content-Type: application/json" -d "{\"candidat_id\":1,\"offre_id\":1}"

# 4. Analyser avec l'IA
curl -X POST http://localhost:5000/api/offers/1/analyze-match -H "Content-Type: application/json" -d "{\"candidat_id\":1}"
```

### Test avec Postman

1. Importer la collection depuis le fichier `api_tests.http`
2. Exécuter les requêtes dans l'ordre
3. Vérifier les codes de statut et les réponses JSON

### Vérifier les Données dans PostgreSQL
```bash
psql -U postgres -d smart_recruit
```
```sql
-- Voir tous les candidats
SELECT * FROM candidats;

-- Voir toutes les offres
SELECT * FROM offres_emploi;

-- Voir toutes les candidatures avec détails
SELECT 
    c.id,
    cand.nom as candidat,
    o.titre as offre,
    c.date_depot
FROM candidatures c
JOIN candidats cand ON c.candidat_id = cand.id
JOIN offres_emploi o ON c.offre_id = o.id
ORDER BY c.date_depot DESC;

-- Statistiques
SELECT 
    (SELECT COUNT(*) FROM candidats) as nb_candidats,
    (SELECT COUNT(*) FROM offres_emploi) as nb_offres,
    (SELECT COUNT(*) FROM candidatures) as nb_candidatures;
```

---

## ⚠️ Gestion des Erreurs

L'API retourne des erreurs en JSON avec des codes HTTP appropriés :

### 400 Bad Request - Données Invalides
```json
{
  "error": "Données invalides",
  "details": {
    "email": ["Format d'email invalide"],
    "bio": ["La bio doit contenir entre 10 et 2000 caractères"]
  }
}
```

### 404 Not Found - Ressource Inexistante
```json
{
  "error": "Resource not found",
  "message": "La ressource demandée n'existe pas"
}
```

### 409 Conflict - Conflit de Données
```json
{
  "error": "Un candidat avec cet email existe déjà"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "Une erreur interne s'est produite"
}
```

---

## 🔐 Sécurité

- Clé API Gemini stockée dans `.env` (non versionné)
- Validation systématique des données avec Marshmallow
- Prévention des injections SQL via SQLAlchemy ORM
- Gestion des erreurs centralisée
- Timeout sur les appels API externes (20s)

---

## Modèles de Données

### Candidat
```python
- id: Integer (PK)
- nom: String(100)
- email: String(120) UNIQUE
- bio: Text
- diplome: String(200)
- date_inscription: DateTime
```

### OffreEmploi
```python
- id: Integer (PK)
- titre: String(200)
- description: Text
- competences: JSON
- salaire: Float
- date_creation: DateTime
```

### Candidature
```python
- id: Integer (PK)
- candidat_id: Integer (FK → candidats.id)
- offre_id: Integer (FK → offres_emploi.id)
- date_depot: DateTime
- UNIQUE(candidat_id, offre_id)
```

---

##  Développement Futur

- [ ] Authentification JWT
- [ ] Pagination des résultats
- [ ] Filtres de recherche avancés
- [ ] Notifications par email
- [ ] Dashboard administrateur
- [ ] Export PDF des candidatures
- [ ] Tests unitaires (pytest)
- [ ] Documentation Swagger/OpenAPI

---

##  Auteur

**Votre Nom**  
Projet d'examen Flask - Gestion de Recrutement avec IA

---

## 📄 Licence

MIT License - Projet académique

---

## 🙏 Remerciements

- Flask Documentation
- SQLAlchemy Documentation
- Marshmallow Documentation
- Google Gemini API Documentation
- Stack Overflow Community

---

##  Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Consulter la documentation des technologies utilisées
- Contacter l'auteur

---

** Si ce projet vous a été utile, n'hésitez pas à mettre une étoile sur GitHub !**
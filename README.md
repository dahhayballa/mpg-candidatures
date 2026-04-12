# 🚀 MPG Candidatures — AI-Powered Candidate Evaluation System

## 📌 Description

MPG Candidatures est une application intelligente permettant de gérer et d’évaluer automatiquement les candidatures pour l’EETFP-MPG (École des Mines, Pétrole & Gaz, Nouakchott).

Le système utilise l’intelligence artificielle pour analyser les dossiers des candidats (CV, lettres, documents) et attribuer un score basé sur une grille officielle.

---

## 🧠 Fonctionnalités principales

* 📂 Lecture automatique des fichiers :

  * PDF
  * Images (JPG, PNG…)
  * DOCX
* 🤖 Évaluation automatique avec IA (Claude API)
* 📊 Calcul de score basé sur une grille officielle (/100)
* 🔎 Détection automatique de la spécialité
* 📈 Dashboard avec statistiques
* 📤 Export CSV des candidatures
* 📋 Génération de liste d’attente (Excel)
* 🔁 Reprise automatique avec système de checkpoint

---

## 🏗️ Architecture

Le projet suit une **Clean Architecture** :

```
core/
  ├── domain/
  ├── use_cases/

infrastructure/
  ├── persistence/

app/
  ├── Flask API
```

---

## ⚙️ Technologies utilisées

* Python (Flask)
* SQLite
* Claude API (Anthropic)
* Pillow (images)
* pdfplumber / PyPDF2 (PDF)
* docx2txt (DOCX)

---

## 🚀 Installation

```bash
git clone https://github.com/dahhayballa/mpg-candidatures.git
cd mpg-candidatures

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔐 Configuration

Créer un fichier `config.py` :

```python
DB_PATH = "database.db"
ATTACHMENTS_DIR = "attachments"
ANTHROPIC_API_KEY = "your_api_key"
FLASK_PORT = 5000
FLASK_DEBUG = True
```

---

## ▶️ Lancer l’application

```bash
python app.py
```

Puis ouvrir :

```
http://localhost:5000
```

---

## 🤖 Lancer le scoring IA

```bash
python ai_score_v3.py
```

---

## 📤 Export des données

* CSV : `/api/export/csv`
* Liste d’attente : `/api/export/attente`

---

## 📊 API endpoints

* `/api/stats`
* `/api/candidates`
* `/api/candidate/<id>`
* `/api/candidate/<id>/evaluate`
* `/api/candidate/<id>/retenir`

---

## ⚠️ Améliorations futures

* 🔐 Authentification JWT
* ☁️ Déploiement cloud (Render / Docker)
* 📊 Interface React
* ⚡ Optimisation coût IA

---

## 👨‍💻 Auteur

Mohamed Haibla
Master 2 MPIAGE — ISCAE
Projet de gestion intelligente des candidatures

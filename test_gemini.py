import requests
import json

# ============================================
# CONFIGURATION
# ============================================

GEMINI_API_KEY = "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"

print("=" * 60)
print("🔍 TEST DE CONNEXION GEMINI API")
print("=" * 60)

# ============================================
# TEST 1: Requête simple
# ============================================

print("\n" + "-" * 40)
print("🤖 Test 1: Requête simple")
print("-" * 40)

url = f"https://openrouter.ai/api/v1?key={GEMINI_API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Réponds au format JSON: {\"score\": 75, \"justification\": \"Test réussi\"}"
                }
            ]
        }
    ]
}

try:
    response = requests.post(url, json=payload, timeout=10)
    print(f"Status HTTP: {response.status_code}")

    if response.status_code == 200:
        # result = response.json()
        # text = result['candidates'][0]['content']['parts'][0]['text']
        print(" SUCCESS!")
        # print(f"Réponse: {text}")

    elif response.status_code == 429:
        print(" QUOTA DÉPASSÉ (429)")
        print(" Votre quota gratuit est épuisé")
        print(" Solutions:")
        print(" 1. Attendez quelques minutes")
        print(" 2. Créez une nouvelle clé API")
        print(" 3. Utilisez le mode fallback (algorithme local)")

    elif response.status_code == 403:
        print(" ACCÈS REFUSÉ (403)")
        print(" La clé API est invalide ou désactivée")

    elif response.status_code == 400:
        print(" REQUÊTE INVALIDE (400)")
        print(f" Détails: {response.text[:200]}")

    else:
        print(f" ERREUR: {response.text[:200]}")

except requests.Timeout:
    print(" TIMEOUT - Le serveur ne répond pas")

except requests.ConnectionError:
    print(" ERREUR DE CONNEXION - Vérifiez votre internet")

except Exception as e:
    print(f" EXCEPTION: {e}")

# ============================================
# TEST 2: Simulation analyse candidat-offre
# ============================================

print("\n" + "-" * 40)
print(" Test 2: Analyse Candidat-Offre")
print("-" * 40)

prompt_analyse = """
Analyse la compatibilité entre cette offre et ce candidat.

OFFRE D'EMPLOI:
- Titre: Développeur Python Senior
- Description: Nous recherchons un développeur Python expérimenté
- Compétences requises: Python, Flask, PostgreSQL, Docker, Git
- Salaire: 500000 FCFA

CANDIDAT:
- Nom: Fatou Sall
- Bio: Développeuse Full Stack avec 5 ans d'expérience en Python, Flask et Django.
  Passionnée par le développement d'APIs REST et les bonnes pratiques.
- Diplôme: Master en Informatique

Réponds UNIQUEMENT avec ce format JSON exact (sans markdown, sans texte autour):
{"score": <nombre entre 0 et 100>, "justification": "<explication en 2-3 phrases maximum>"}
"""

payload_analyse = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt_analyse
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.3,
        "maxOutputTokens": 200
    }
}

try:
    response = requests.post(url, json=payload_analyse, timeout=15)
    print(f"Status HTTP: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']

        print(" SUCCESS!")
        print(f"Réponse brute: {text}")

        # Essayer de parser le JSON
        # try:
        #     clean_text = text.strip()
        #     clean_text = clean_text.replace('```json', '').replace('```', '').strip()
        #     analysis = json.loads(clean_text)
        #     print(f"\n Score: {analysis.get('score')}%")
        #     print(f" Justification: {analysis.get('justification')}")
        #     print("\n PARSING JSON RÉUSSI!")
        # except json.JSONDecodeError as e:
        #     print(f"\n Impossible de parser le JSON: {e}")
        #     print(" La réponse n'est pas un JSON valide")

    elif response.status_code == 429:
        print(" QUOTA DÉPASSÉ - Mode fallback recommandé")

    else:
        print(f" ERREUR: {response.text[:300]}")

except Exception as e:
    print(f" EXCEPTION: {e}")

# ============================================
# TEST 3: Vérifier les modèles disponibles
# ============================================

print("\n" + "-" * 40)
print("📋 Test 3: Modèles disponibles")
print("-" * 40)

try:
    url_models = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
    response = requests.get(url_models, timeout=10)

    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"✅ {len(models)} modèles trouvés:")

        gemini_models = [
            m for m in models
            if 'gemini' in m.get('name', '').lower()
        ]

        for model in gemini_models[:5]:
            name = model.get('name', 'N/A').replace('models/', '')
            print(f"  {name}")

    else:
        print(f" Erreur: {response.status_code}")

except Exception as e:
    print(f" Exception: {e}")

# ============================================
# RÉSUMÉ FINAL
# ============================================

print("\n" + "=" * 60)
print("📋 RÉSUMÉ")
print("=" * 60)
print(f"Clé API: {GEMINI_API_KEY[:15]}...{GEMINI_API_KEY[-5:]}")
print("Modèle utilisé: gemini-2.0-flash")
print("=" * 60)

import requests

GEMINI_API_KEY = "AIzaSyBjJDrKDKTxlOU5gcuZA1ybZndjioJh4Uo"

print("="*70)
print("TEST DE LA NOUVELLE CLÉ API GEMINI")
print("="*70)
print(f"\nClé API: {GEMINI_API_KEY[:15]}...{GEMINI_API_KEY[-10:]}\n")

# Test avec gemini-2.0-flash
print("-"*70)
print("TEST: Modèle gemini-2.0-flash")
print("-"*70)

url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Réponds juste 'Bonjour, je fonctionne !' en une phrase."
        }]
    }]
}

try:
    response = requests.post(url, json=payload, timeout=10)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        print(" SUCCESS - La clé fonctionne parfaitement !")
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Réponse de Gemini: {text}\n")
        print("="*70)
        print(" VOUS POUVEZ UTILISER CETTE CLÉ !")
        print("="*70)
    elif response.status_code == 429:
        print(" ERREUR 429 - Quota dépassé")
        print("Cette clé a aussi atteint son quota.")
    elif response.status_code == 403:
        print(" ERREUR 403 - Accès refusé")
        print("Clé API invalide ou restrictions d'accès.")
    elif response.status_code == 404:
        print(" ERREUR 404 - Modèle non trouvé")
        print("Le modèle n'est pas accessible avec cette clé.")
    else:
        print(f" ERREUR {response.status_code}")
        print(f"Détails: {response.text[:300]}")
        
except Exception as e:
    print(f" EXCEPTION: {e}")

print("\n")
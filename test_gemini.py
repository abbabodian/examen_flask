import requests
import json

# Votre clé API
GEMINI_API_KEY = "AIzaSyDov2Ilzo4PffUNVV0T679vGIAlchDU1j4"

print("="*70)
print(" TEST COMPLET DE LA CLÉ API GEMINI")
print("="*70)
print(f"\nClé API: {GEMINI_API_KEY[:15]}...{GEMINI_API_KEY[-10:]}\n")

# Test 1: Modèle gemini-pro (v1)
print("-"*70)
print("TEST 1: Modèle gemini-pro (API v1)")
print("-"*70)

url1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Réponds juste 'Bonjour' en une phrase."
        }]
    }]
}

try:
    response = requests.post(url1, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(" SUCCESS - L'API fonctionne !")
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Réponse de Gemini: {text}\n")
    else:
        print(f" ERREUR {response.status_code}")
        print(f"Message: {response.json().get('error', {}).get('message', 'N/A')}\n")
        
except Exception as e:
    print(f" EXCEPTION: {e}\n")

# Test 2: Modèle gemini-pro (v1beta)
print("-"*70)
print("TEST 2: Modèle gemini-pro (API v1beta)")
print("-"*70)

url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

try:
    response = requests.post(url2, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(" SUCCESS - L'API fonctionne !")
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Réponse de Gemini: {text}\n")
    else:
        print(f" ERREUR {response.status_code}")
        print(f"Message: {response.json().get('error', {}).get('message', 'N/A')}\n")
        
except Exception as e:
    print(f" EXCEPTION: {e}\n")

# Test 3: Modèle gemini-1.5-flash (v1beta)
print("-"*70)
print("TEST 3: Modèle gemini-1.5-flash (API v1beta)")
print("-"*70)

url3 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

try:
    response = requests.post(url3, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(" SUCCESS - L'API fonctionne !")
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Réponse de Gemini: {text}\n")
    else:
        print(f" ERREUR {response.status_code}")
        print(f"Message: {response.json().get('error', {}).get('message', 'N/A')}\n")
        
except Exception as e:
    print(f" EXCEPTION: {e}\n")

# Test 4: Modèle gemini-1.5-pro (v1beta)
print("-"*70)
print("TEST 4: Modèle gemini-1.5-pro (API v1beta)")
print("-"*70)

url4 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

try:
    response = requests.post(url4, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(" SUCCESS - L'API fonctionne !")
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        print(f"Réponse de Gemini: {text}\n")
    else:
        print(f" ERREUR {response.status_code}")
        print(f"Message: {response.json().get('error', {}).get('message', 'N/A')}\n")
        
except Exception as e:
    print(f" EXCEPTION: {e}\n")

# Test 5: Lister les modèles disponibles
print("-"*70)
print("TEST 5: Liste des modèles disponibles")
print("-"*70)

list_url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"

try:
    response = requests.get(list_url, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(" SUCCESS - Modèles accessibles:")
        models = response.json()
        
        generation_models = []
        for model in models.get('models', []):
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                generation_models.append(model['name'])
        
        if generation_models:
            print(f"\n Modèles disponibles pour generateContent ({len(generation_models)}):")
            for model in generation_models:
                print(f"  ✓ {model}")
        else:
            print(" Aucun modèle disponible pour generateContent")
            print("\nTous les modèles:")
            for model in models.get('models', [])[:5]:
                print(f"  - {model.get('name')} : {model.get('supportedGenerationMethods', [])}")
    else:
        print(f" ERREUR {response.status_code}")
        print(f"Message: {response.json().get('error', {}).get('message', 'N/A')}")
        
except Exception as e:
    print(f" EXCEPTION: {e}")

print("\n" + "="*70)
print(" TESTS TERMINÉS")
print("="*70)

# Recommandations
print("\n RECOMMANDATIONS:")
print("-"*70)
print("Cherchez le premier test avec  SUCCESS")
print("Si TEST 2 ou 3 ou 4 fonctionne, utilisez cette URL dans ai_service.py")
print("Si TEST 5 liste des modèles, utilisez un des modèles listés")
print("="*70 + "\n")
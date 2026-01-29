import requests

GEMINI_API_KEY = "AIzaSyB4bV3STl3xoQPGQ6Hwfh2RKp_NGTWBllY"

print(" Test final avec gemini-2.0-flash...\n")

url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Réponds au format JSON: {\"score\": 75, \"justification\": \"Test réussi\"}"
        }]
    }]
}

response = requests.post(url, json=payload, timeout=10)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    text = result['candidates'][0]['content']['parts'][0]['text']
    print(f" SUCCESS!\nRéponse: {text}")
else:
    print(f" ERREUR: {response.text[:200]}")
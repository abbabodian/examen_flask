import os
import json
import requests
from dotenv import load_dotenv
import random

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'votre_clé_api_gemini_ici')

class AIService:
    
    @staticmethod
    def analyser_compatibilite(offre, candidat):
        """
        Analyse la compatibilité entre une offre et un candidat via Gemini
        Fallback automatique si Gemini n'est pas disponible
        """
        
        # Essayer d'abord Gemini si la clé est configurée
        if GEMINI_API_KEY and GEMINI_API_KEY != "votre_clé_api_gemini_ici":
            gemini_result = AIService._try_gemini(offre, candidat)
            
            # Si Gemini fonctionne, retourner le résultat
            if gemini_result and "error" not in gemini_result:
                print("[INFO]  Utilisation de Gemini AI")
                return gemini_result
            
            # Si erreur, afficher et utiliser le fallback
            if gemini_result and "error" in gemini_result:
                print(f"[WARNING]  Gemini non disponible: {gemini_result.get('error')}")
        
        print("[INFO]  Utilisation du mode fallback (algorithme local)")
        return AIService._fallback_analysis(offre, candidat)
    
    @staticmethod
    def _try_gemini(offre, candidat):
        """Essayer d'appeler Gemini API"""
        try:
            # URL avec le modèle gemini-2.0-flash
            url = f"https://openrouter.ai/api/v1?key={GEMINI_API_KEY}"
            
            prompt = f"""Analyse la compatibilité entre cette offre d'emploi et ce candidat.

OFFRE D'EMPLOI:
Titre: {offre.titre}
Description: {offre.description}
Compétences requises: {', '.join(offre.competences)}
Salaire proposé: {offre.salaire} FCFA

CANDIDAT:
Nom: {candidat.nom}
Parcours professionnel: {candidat.bio}
Diplôme: {candidat.diplome}

Réponds UNIQUEMENT avec un objet JSON (sans markdown, sans balises) contenant:
- "score": un nombre entre 0 et 100
- "justification": un texte de maximum 180 caractères

Format exact: {{"score": 85, "justification": "Explication courte"}}"""
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 300
                }
            }
            
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            # Gérer les différentes erreurs
            if response.status_code == 429:
                return {"error": "Quota Gemini dépassé (429)"}
            elif response.status_code == 403:
                return {"error": "Accès Gemini refusé (403)"}
            elif response.status_code == 404:
                return {"error": "Modèle Gemini non trouvé (404)"}
            elif response.status_code != 200:
                return {"error": f"Erreur Gemini {response.status_code}"}
            
            # Parser la réponse
            result = response.json()
            
            if 'candidates' not in result or len(result['candidates']) == 0:
                return {"error": "Réponse vide de Gemini"}
            
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            text_response = text_response.strip().replace('```json', '').replace('```', '').strip()
            
            # Parser le JSON
            try:
                analysis = json.loads(text_response)
            except json.JSONDecodeError:
                # Essayer de trouver le JSON dans le texte
                import re
                json_match = re.search(r'\{[^}]+\}', text_response)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    return {"error": "Format JSON invalide de Gemini"}
            
            # Valider la structure
            if 'score' not in analysis or 'justification' not in analysis:
                return {"error": "Clés manquantes dans la réponse Gemini"}
            
            return {
                "score": max(0, min(100, int(analysis['score']))),
                "justification": str(analysis['justification'])[:200],
                "source": "gemini-ai"
            }
            
        except requests.Timeout:
            return {"error": "Timeout Gemini"}
        except requests.ConnectionError:
            return {"error": "Connexion Gemini impossible"}
        except Exception as e:
            return {"error": f"Exception: {str(e)}"}
    
    @staticmethod
    def _fallback_analysis(offre, candidat):
        """
        Analyse automatique sans IA - Algorithme intelligent de scoring
        
        Critères d'évaluation:
        - Compétences techniques (40 points max)
        - Niveau de diplôme (20 points max)
        - Expérience professionnelle (25 points max)
        - Pertinence du profil (15 points max)
        """
        score = 0
        justification_parts = []
        
        # ============================================================
        # 1. ANALYSE DES COMPÉTENCES (40 points maximum)
        # ============================================================
        competences_offre = [c.lower() for c in offre.competences]
        bio_lower = candidat.bio.lower()
        
        competences_trouvees = []
        for comp in competences_offre:
            if comp in bio_lower:
                competences_trouvees.append(comp)
        
        if competences_offre:
            # Calculer le pourcentage de compétences trouvées
            pourcentage_comp = len(competences_trouvees) / len(competences_offre)
            score_competences = pourcentage_comp * 40
            score += score_competences
            
            # Construire la justification selon le niveau de correspondance
            if pourcentage_comp >= 0.8:  # 80% ou plus
                justification_parts.append(f"Excellent match: {len(competences_trouvees)}/{len(competences_offre)} compétences")
            elif pourcentage_comp >= 0.6:  # 60-79%
                justification_parts.append(f"Bonnes compétences: {len(competences_trouvees)}/{len(competences_offre)}")
            elif pourcentage_comp >= 0.3:  # 30-59%
                justification_parts.append(f"Compétences partielles: {len(competences_trouvees)}/{len(competences_offre)}")
            elif len(competences_trouvees) > 0:
                justification_parts.append(f"Quelques compétences pertinentes")
            else:
                justification_parts.append("Compétences à développer")
        
        # ============================================================
        # 2. ANALYSE DU DIPLÔME (20 points maximum)
        # ============================================================
        diplome_keywords = {
            'doctorat': 20,
            'phd': 20,
            'master': 20,
            'ingénieur': 20,
            'ingenieur': 20,
            'licence': 15,
            'bachelor': 15,
            'bac+5': 20,
            'bac+4': 18,
            'bac+3': 15,
            'bac+2': 12,
            'bts': 12,
            'dut': 12,
            'bac': 10
        }
        
        diplome_lower = candidat.diplome.lower()
        diplome_score = 0
        for keyword, points in diplome_keywords.items():
            if keyword in diplome_lower:
                diplome_score = max(diplome_score, points)  # Prendre le plus haut
        
        score += diplome_score
        
        # ============================================================
        # 3. ANALYSE DE L'EXPÉRIENCE (25 points maximum)
        # ============================================================
        experience_keywords = [
            # Années d'expérience
            ('10 ans', 25), ('dix ans', 25),
            ('9 ans', 24), ('neuf ans', 24),
            ('8 ans', 23), ('huit ans', 23),
            ('7 ans', 21), ('sept ans', 21),
            ('6 ans', 19), ('six ans', 19),
            ('5 ans', 17), ('cinq ans', 17),
            ('4 ans', 15), ('quatre ans', 15),
            ('3 ans', 13), ('trois ans', 13),
            ('2 ans', 11), ('deux ans', 11),
            ('1 an', 9), ('un an', 9),
            
            # Niveaux de séniorité
            ('expert', 25),
            ('senior', 22),
            ('expérimenté', 20),
            ('confirmé', 18),
            ('intermédiaire', 14),
            ('junior', 10),
            ('débutant', 8),
            ('stage', 6)
        ]
        
        experience_score = 0
        experience_found = False
        for keyword, points in experience_keywords:
            if keyword in bio_lower:
                experience_score = max(experience_score, points)
                experience_found = True
        
        score += experience_score
        
        # Ajouter à la justification si expérience significative
        if experience_score >= 18:
            justification_parts.append("Profil expérimenté")
        elif experience_score >= 12:
            justification_parts.append("Expérience pertinente")
        elif experience_found:
            justification_parts.append("Profil junior")
        
        # ============================================================
        # 4. ANALYSE DE LA PERTINENCE (15 points maximum)
        # ============================================================
        # Vérifier les mots-clés importants du titre dans la bio
        titre_words = [w.lower() for w in offre.titre.split() if len(w) > 3]
        matching_title_words = sum(1 for word in titre_words if word in bio_lower)
        
        if matching_title_words > 0:
            pertinence_score = min(15, matching_title_words * 6)
            score += pertinence_score
            
            if matching_title_words >= 3:
                justification_parts.append("Profil très aligné")
        
        # Bonus : mots-clés positifs dans la bio
        bonus_keywords = ['passionné', 'motivé', 'dynamique', 'autonome', 'rigoureux', 'polyvalent']
        bonus_found = sum(1 for kw in bonus_keywords if kw in bio_lower)
        if bonus_found >= 2:
            score += min(5, bonus_found * 2)
        
        # ============================================================
        # 5. NORMALISATION ET VARIATION ALÉATOIRE
        # ============================================================
        # Normaliser le score entre 0 et 100
        score = min(100, max(0, int(score)))
        
        # Ajouter une petite variation aléatoire pour plus de réalisme
        # (+/- 3 points maximum)
        variation = random.randint(-3, 3)
        score = max(0, min(100, score + variation))
        
        # ============================================================
        # 6. CONSTRUCTION DE LA JUSTIFICATION FINALE
        # ============================================================
        if score >= 85:
            prefix = "Excellent profil!"
        elif score >= 70:
            prefix = "Très bon profil."
        elif score >= 55:
            prefix = "Bon profil."
        elif score >= 40:
            prefix = "Profil acceptable."
        else:
            prefix = "Profil à considérer avec formation."
        
        # Assembler la justification (max 180 caractères)
        if justification_parts:
            justification = f"{prefix} {' - '.join(justification_parts[:2])}"
        else:
            justification = f"{prefix} Voir détails du profil pour évaluation complète."
        
        # Limiter strictement à 180 caractères
        justification = justification[:180]
        
        # ============================================================
        # 7. RETOUR DU RÉSULTAT
        # ============================================================
        return {
            "score": score,
            "justification": justification,
            "source": "algorithme-local"
        }
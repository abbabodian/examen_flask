// ============================================
// Configuration de l'API
// ============================================
const API_URL = '/api';

// Variables globales
let candidatsCache = [];
let offresCache = [];
let pendingAction = null;

// ============================================
// Vérification de la connexion API
// ============================================
async function checkApiStatus() {
    const statusDot = document.getElementById('api-status');
    const statusText = document.getElementById('api-status-text');
    
    try {
        const response = await fetch(`${API_URL}/candidates`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            statusDot.className = 'w-2 h-2 bg-green-500 rounded-full';
            statusText.textContent = 'API connectée';
            statusText.className = 'text-xs text-green-600';
            return true;
        }
    } catch (error) {
        console.error('API Status Error:', error);
    }
    
    statusDot.className = 'w-2 h-2 bg-red-500 rounded-full';
    statusText.textContent = 'API hors ligne';
    statusText.className = 'text-xs text-red-600';
    return false;
}

// ============================================
// Affichage des notifications Toast
// ============================================
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-yellow-500';
    const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    
    toast.innerHTML = `
        <div class="${bgColor} text-white px-6 py-4 rounded-xl shadow-2xl flex items-center space-x-3">
            <i class="fas ${icon} text-xl"></i>
            <span class="font-medium">${message}</span>
        </div>
    `;
    toast.classList.remove('hidden');
    
    setTimeout(() => toast.classList.add('hidden'), 4000);
}

// ============================================
// Navigation entre sections
// ============================================
function showSection(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    document.getElementById(`section-${section}`).classList.remove('hidden');
    
    updateNavButtons(section);
    
    if (section === 'analyse') {
        chargerOptionsAnalyse();
    }
}

function updateNavButtons(activeSection) {
    const buttons = ['candidats', 'offres', 'analyse'];
    
    buttons.forEach(section => {
        const btn = document.getElementById(`btn-${section}`);
        if (btn) {
            btn.classList.remove('bg-green-500', 'bg-red-500', 'bg-white', 'text-white', 'text-gray-600');
            
            if (section === activeSection) {
                btn.classList.add('bg-green-500', 'text-white');
            } else {
                btn.classList.add('bg-white', 'text-gray-600');
            }
        }
    });
}

// ============================================
// GESTION DES CANDIDATS
// ============================================

// Créer un candidat
document.getElementById('form-candidat')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('btn-submit-candidat');
    const originalContent = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Création...';
    submitBtn.disabled = true;
    
    const data = {
        nom: document.getElementById('candidat-nom').value.trim(),
        email: document.getElementById('candidat-email').value.trim(),
        bio: document.getElementById('candidat-bio').value.trim(),
        diplome: document.getElementById('candidat-diplome').value.trim()
    };
    
    try {
        const response = await fetch(`${API_URL}/candidates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast(`Candidat "${data.nom}" créé avec succès !`);
            e.target.reset();
            await chargerCandidats();
        } else {
            const errorMsg = result.error || result.message || 'Erreur lors de la création';
            const details = result.details ? '\n' + Object.values(result.details).flat().join('\n') : '';
            showToast(errorMsg + details, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Erreur de connexion à l\'API', 'error');
    } finally {
        submitBtn.innerHTML = originalContent;
        submitBtn.disabled = false;
    }
});

// Charger les candidats
async function chargerCandidats() {
    const liste = document.getElementById('liste-candidats');
    const countSpan = document.getElementById('count-candidats');
    const badgeNav = document.getElementById('badge-candidats');
    
    liste.innerHTML = `
        <div class="text-center py-8">
            <i class="fas fa-spinner fa-spin text-4xl text-green-500"></i>
            <p class="mt-4 text-gray-500">Chargement...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`${API_URL}/candidates`);
        const result = await response.json();
        
        console.log('Candidats response:', result);
        
        if (response.ok && result.success) {
            candidatsCache = result.candidats || [];
            const count = candidatsCache.length;
            
            if (countSpan) countSpan.textContent = count;
            if (badgeNav) badgeNav.textContent = count;
            
            if (count === 0) {
                liste.innerHTML = `
                    <div class="text-center py-12 text-gray-400">
                        <i class="fas fa-users text-6xl mb-4"></i>
                        <p class="text-lg">Aucun candidat</p>
                        <p class="text-sm">Créez votre premier candidat</p>
                    </div>
                `;
                return;
            }
            
            afficherCandidats(candidatsCache);
        } else {
            throw new Error(result.error || 'Erreur serveur');
        }
    } catch (error) {
        console.error('Error loading candidates:', error);
        liste.innerHTML = `
            <div class="text-center py-8 text-red-500">
                <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                <p>Erreur de chargement</p>
                <button onclick="chargerCandidats()" class="mt-4 px-4 py-2 bg-red-100 rounded-lg">
                    <i class="fas fa-redo mr-2"></i>Réessayer
                </button>
            </div>
        `;
    }
}

// Afficher les candidats
function afficherCandidats(candidats) {
    const liste = document.getElementById('liste-candidats');
    
    liste.innerHTML = candidats.map((c, index) => `
        <div class="bg-white border border-gray-200 p-4 rounded-xl hover:shadow-lg transition mb-3">
            <div class="flex items-start justify-between">
                <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                        ${c.nom.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h4 class="font-bold text-gray-800">${escapeHtml(c.nom)}</h4>
                        <p class="text-sm text-gray-500">${escapeHtml(c.email)}</p>
                        <span class="inline-block bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full mt-1">
                            <i class="fas fa-graduation-cap mr-1"></i>${escapeHtml(c.diplome)}
                        </span>
                    </div>
                </div>
                <button onclick="supprimerCandidat(${c.id}, '${escapeHtml(c.nom)}')" 
                        class="text-red-500 hover:bg-red-100 p-2 rounded-lg transition">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Supprimer un candidat
async function supprimerCandidat(id, nom) {
    if (!confirm(`Supprimer le candidat "${nom}" ?`)) return;
    
    try {
        const response = await fetch(`${API_URL}/candidates/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast('Candidat supprimé');
            await chargerCandidats();
        } else {
            showToast(result.error || 'Erreur', 'error');
        }
    } catch (error) {
        showToast('Erreur de connexion', 'error');
    }
}

// ============================================
// GESTION DES OFFRES
// ============================================

document.getElementById('form-offre')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('btn-submit-offre');
    const originalContent = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publication...';
    submitBtn.disabled = true;
    
    const competencesInput = document.getElementById('offre-competences').value;
    const competences = competencesInput.split(',').map(c => c.trim()).filter(c => c.length > 0);
    
    const data = {
        titre: document.getElementById('offre-titre').value.trim(),
        description: document.getElementById('offre-description').value.trim(),
        competences: competences,
        salaire: parseFloat(document.getElementById('offre-salaire').value)
    };
    
    try {
        const response = await fetch(`${API_URL}/offers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast(`Offre "${data.titre}" publiée !`);
            e.target.reset();
            await chargerOffres();
        } else {
            showToast(result.error || 'Erreur', 'error');
        }
    } catch (error) {
        showToast('Erreur de connexion', 'error');
    } finally {
        submitBtn.innerHTML = originalContent;
        submitBtn.disabled = false;
    }
});

// Charger les offres
async function chargerOffres() {
    const liste = document.getElementById('liste-offres');
    const countSpan = document.getElementById('count-offres');
    const badgeNav = document.getElementById('badge-offres');
    
    liste.innerHTML = `
        <div class="text-center py-8">
            <i class="fas fa-spinner fa-spin text-4xl text-red-500"></i>
            <p class="mt-4 text-gray-500">Chargement...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`${API_URL}/offers`);
        const result = await response.json();
        
        console.log('Offres response:', result);
        
        if (response.ok && result.success) {
            offresCache = result.offres || [];
            const count = offresCache.length;
            
            if (countSpan) countSpan.textContent = count;
            if (badgeNav) badgeNav.textContent = count;
            
            if (count === 0) {
                liste.innerHTML = `
                    <div class="text-center py-12 text-gray-400">
                        <i class="fas fa-briefcase text-6xl mb-4"></i>
                        <p class="text-lg">Aucune offre</p>
                        <p class="text-sm">Publiez votre première offre</p>
                    </div>
                `;
                return;
            }
            
            afficherOffres(offresCache);
        } else {
            throw new Error(result.error || 'Erreur serveur');
        }
    } catch (error) {
        console.error('Error loading offers:', error);
        liste.innerHTML = `
            <div class="text-center py-8 text-red-500">
                <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                <p>Erreur de chargement</p>
            </div>
        `;
    }
}

// Afficher les offres
function afficherOffres(offres) {
    const liste = document.getElementById('liste-offres');
    
    liste.innerHTML = offres.map((o, index) => `
        <div class="bg-white border border-gray-200 p-4 rounded-xl hover:shadow-lg transition mb-3">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h4 class="font-bold text-gray-800">${escapeHtml(o.titre)}</h4>
                    <p class="text-sm text-gray-600 mt-1">${escapeHtml(o.description).substring(0, 100)}...</p>
                    <div class="flex flex-wrap gap-1 mt-2">
                        ${(o.competences || []).slice(0, 4).map(c => `
                            <span class="bg-red-100 text-red-700 text-xs px-2 py-1 rounded-full">${escapeHtml(c)}</span>
                        `).join('')}
                    </div>
                    <p class="text-green-600 font-bold mt-2">
                        <i class="fas fa-money-bill-wave mr-1"></i>${formatSalaire(o.salaire)} FCFA
                    </p>
                </div>
                <button onclick="supprimerOffre(${o.id}, '${escapeHtml(o.titre)}')" 
                        class="text-red-500 hover:bg-red-100 p-2 rounded-lg transition">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Supprimer une offre
async function supprimerOffre(id, titre) {
    if (!confirm(`Supprimer l'offre "${titre}" ?`)) return;
    
    try {
        const response = await fetch(`${API_URL}/offers/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast('Offre supprimée');
            await chargerOffres();
        } else {
            showToast(result.error || 'Erreur', 'error');
        }
    } catch (error) {
        showToast('Erreur de connexion', 'error');
    }
}

// ============================================
// ANALYSE IA
// ============================================

async function chargerOptionsAnalyse() {
    // Charger candidats si pas en cache
    if (candidatsCache.length === 0) {
        try {
            const res = await fetch(`${API_URL}/candidates`);
            const data = await res.json();
            if (data.success) candidatsCache = data.candidats || [];
        } catch (e) {}
    }
    
    // Charger offres si pas en cache
    if (offresCache.length === 0) {
        try {
            const res = await fetch(`${API_URL}/offers`);
            const data = await res.json();
            if (data.success) offresCache = data.offres || [];
        } catch (e) {}
    }
    
    // Remplir les selects
    const optionsOffres = '<option value="">-- Choisir une offre --</option>' +
        offresCache.map(o => `<option value="${o.id}">${escapeHtml(o.titre)}</option>`).join('');
    
    const optionsCandidats = '<option value="">-- Choisir un candidat --</option>' +
        candidatsCache.map(c => `<option value="${c.id}">${escapeHtml(c.nom)}</option>`).join('');
    
    document.getElementById('analyse-offre').innerHTML = optionsOffres;
    document.getElementById('analyse-candidat').innerHTML = optionsCandidats;
    document.getElementById('offre-candidatures').innerHTML = optionsOffres;
    document.getElementById('postuler-offre').innerHTML = optionsOffres;
    document.getElementById('postuler-candidat').innerHTML = optionsCandidats;
}

async function analyserCompatibilite() {
    const offreId = document.getElementById('analyse-offre').value;
    const candidatId = document.getElementById('analyse-candidat').value;
    
    if (!offreId || !candidatId) {
        showToast('Sélectionnez une offre et un candidat', 'error');
        return;
    }
    
    const resultatDiv = document.getElementById('resultat-analyse');
    resultatDiv.innerHTML = `
        <div class="text-center py-12">
            <i class="fas fa-spinner fa-spin text-4xl text-green-500"></i>
            <p class="mt-4">Analyse IA en cours...</p>
        </div>
    `;
    resultatDiv.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_URL}/offers/${offreId}/analyze-match`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ candidat_id: parseInt(candidatId) })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            const score = result.analyse.score;
            const scoreColor = score >= 70 ? 'green' : score >= 50 ? 'yellow' : 'red';
            
            resultatDiv.innerHTML = `
                <div class="bg-${scoreColor}-50 border-2 border-${scoreColor}-200 rounded-xl p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-xl font-bold">Résultat de l'Analyse</h4>
                        <div class="w-20 h-20 rounded-full bg-${scoreColor}-500 flex items-center justify-center text-white text-2xl font-bold">
                            ${score}%
                        </div>
                    </div>
                    <div class="bg-white rounded-lg p-4 mb-4">
                        <p class="text-gray-700">${result.analyse.justification}</p>
                    </div>
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div class="bg-white p-3 rounded">
                            <p class="text-gray-500">Candidat</p>
                            <p class="font-bold">${result.candidat.nom}</p>
                        </div>
                        <div class="bg-white p-3 rounded">
                            <p class="text-gray-500">Offre</p>
                            <p class="font-bold">${result.offre.titre}</p>
                        </div>
                    </div>
                </div>
            `;
            showToast('Analyse terminée !');
        } else {
            resultatDiv.innerHTML = `
                <div class="bg-red-50 border border-red-200 rounded-xl p-4">
                    <p class="text-red-600">${result.error || 'Erreur lors de l\'analyse'}</p>
                </div>
            `;
        }
    } catch (error) {
        resultatDiv.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-xl p-4">
                <p class="text-red-600">Erreur de connexion</p>
            </div>
        `;
    }
}

async function postulerOffre() {
    const offreId = document.getElementById('postuler-offre').value;
    const candidatId = document.getElementById('postuler-candidat').value;
    
    if (!offreId || !candidatId) {
        showToast('Sélectionnez une offre et un candidat', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/apply`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                candidat_id: parseInt(candidatId),
                offre_id: parseInt(offreId)
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showToast('Candidature envoyée !');
        } else {
            showToast(result.error || 'Erreur', 'error');
        }
    } catch (error) {
        showToast('Erreur de connexion', 'error');
    }
}

async function voirCandidatures() {
    const offreId = document.getElementById('offre-candidatures').value;
    const liste = document.getElementById('liste-candidatures');
    
    if (!offreId) {
        liste.innerHTML = '<p class="text-gray-400 text-center py-8">Sélectionnez une offre</p>';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/offers/${offreId}/candidates`);
        const result = await response.json();
        
        if (response.ok && result.success) {
            if (result.candidats.length === 0) {
                liste.innerHTML = '<p class="text-gray-400 text-center py-8">Aucune candidature</p>';
                return;
            }
            
            liste.innerHTML = result.candidats.map(c => `
                <div class="bg-white border rounded-lg p-4 mb-2">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">
                            ${c.nom.charAt(0)}
                        </div>
                        <div>
                            <p class="font-bold">${c.nom}</p>
                            <p class="text-sm text-gray-500">${c.email}</p>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        liste.innerHTML = '<p class="text-red-500 text-center">Erreur</p>';
    }
}

// ============================================
// UTILITAIRES
// ============================================

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatSalaire(salaire) {
    if (!salaire) return '0';
    return parseInt(salaire).toLocaleString('fr-FR');
}

// ============================================
// INITIALISATION
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Smart-Recruit Frontend initialized');
    
    await checkApiStatus();
    showSection('candidats');
    
    await Promise.all([
        chargerCandidats(),
        chargerOffres()
    ]);
    
    // Vérifier l'API périodiquement
    setInterval(checkApiStatus, 30000);
});
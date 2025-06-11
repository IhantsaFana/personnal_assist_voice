/**
 * Assistant Vocal Biblique - Script principal
 * Gère la reconnaissance vocale et l'interaction avec l'API
 */

class VoiceAssistant {
    constructor() {
        this.initializeElements();
        this.initializeSpeechRecognition();
        this.setupEventListeners();
    }

    /**
     * Initialise les références aux éléments DOM
     * @private
     */
    initializeElements() {
        this.elements = {
            speakButton: document.getElementById('speakButton'),
            statusElement: document.getElementById('statusIndicator'),
            userCommandElement: document.getElementById('userCommand'),
            assistantResponseElement: document.getElementById('assistantResponse')
        };

        if (!this.validateElements()) {
            throw new Error('Required DOM elements not found');
        }
    }

    /**
     * Valide que tous les éléments nécessaires sont présents
     * @private
     * @returns {boolean}
     */
    validateElements() {
        return Object.values(this.elements).every(element => element !== null);
    }

    /**
     * Initialise la reconnaissance vocale
     * @private
     */
    initializeSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.handleError('La reconnaissance vocale n\'est pas supportée par votre navigateur.');
            this.elements.speakButton.disabled = true;
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.configureRecognition();
    }

    /**
     * Configure les paramètres de la reconnaissance vocale
     * @private
     */
    configureRecognition() {
        this.recognition.lang = 'fr-FR';
        this.recognition.continuous = false;
        this.recognition.interimResults = false;

        this.recognition.onstart = () => this.handleRecognitionStart();
        this.recognition.onend = () => this.handleRecognitionEnd();
        this.recognition.onerror = (event) => this.handleRecognitionError(event);
        this.recognition.onresult = (event) => this.handleRecognitionResult(event);
    }

    /**
     * Configure les écouteurs d'événements
     * @private
     */
    setupEventListeners() {
        this.elements.speakButton.addEventListener('click', () => this.toggleRecognition());
    }

    /**
     * Démarre ou arrête la reconnaissance vocale
     * @private
     */
    toggleRecognition() {
        if (this.elements.speakButton.classList.contains('listening')) {
            this.recognition.stop();
        } else {
            this.clearMessages();
            this.recognition.start();
        }
    }

    /**
     * Gère le début de la reconnaissance
     * @private
     */
    handleRecognitionStart() {
        this.updateStatus('listening', 'fas fa-microphone-alt', 'Écoute en cours...');
        this.elements.speakButton.classList.add('active', 'listening');
        this.elements.speakButton.disabled = true;
    }

    /**
     * Gère la fin de la reconnaissance
     * @private
     */
    handleRecognitionEnd() {
        this.updateStatus('ready', 'fas fa-microphone', 'Prêt à écouter');
        this.elements.speakButton.classList.remove('active', 'listening');
        this.elements.speakButton.disabled = false;
    }

    /**
     * Gère les erreurs de reconnaissance
     * @private
     * @param {SpeechRecognitionErrorEvent} event 
     */
    handleRecognitionError(event) {
        this.handleError(`Erreur de reconnaissance : ${event.error}`);
        this.elements.speakButton.classList.remove('active', 'listening');
        this.elements.speakButton.disabled = false;
    }

    /**
     * Gère les résultats de la reconnaissance
     * @private
     * @param {SpeechRecognitionEvent} event 
     */
    handleRecognitionResult(event) {
        const transcript = event.results[0][0].transcript;
        this.elements.userCommandElement.textContent = transcript;
        this.updateStatus('processing', 'fas fa-cog fa-spin', 'Traitement en cours...');
        this.sendToAPI(transcript);
    }

    /**
     * Envoie la transcription à l'API
     * @private
     * @param {string} text 
     */
    async sendToAPI(text) {
        try {
            const response = await fetch('/api/process_audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erreur serveur');
            }

            this.handleAPIResponse(data);
        } catch (error) {
            this.handleError(`Erreur de communication : ${error.message}`);
        }
    }

    /**
     * Gère la réponse de l'API
     * @private
     * @param {Object} data 
     */
    handleAPIResponse(data) {
        if (data.error) {
            this.handleError(data.error);
            return;
        }

        this.elements.assistantResponseElement.textContent = data.response;
        this.updateStatus('success', 'fas fa-check-circle', 'Réponse prête');

        if (data.redirect) {
            setTimeout(() => window.open(data.redirect, '_blank'), 1000);
        }
    }

    /**
     * Met à jour l'indicateur de statut
     * @private
     * @param {string} className 
     * @param {string} iconClass 
     * @param {string} message 
     */
    updateStatus(className, iconClass, message) {
        this.elements.statusElement.className = `status-indicator ${className}`;
        this.elements.statusElement.innerHTML = `<i class="${iconClass}"></i><span>${message}</span>`;
    }

    /**
     * Gère les erreurs
     * @private
     * @param {string} message 
     */
    handleError(message) {
        console.error(message);
        this.updateStatus('error', 'fas fa-exclamation-triangle', message);
        this.elements.assistantResponseElement.textContent =
            "Je suis désolé, j'ai rencontré une erreur. Pouvez-vous réessayer ?";
    }

    /**
     * Efface les messages
     * @private
     */
    clearMessages() {
        this.elements.userCommandElement.textContent = '';
        this.elements.assistantResponseElement.textContent = '';
    }
}

// Initialisation quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    try {
        window.voiceAssistant = new VoiceAssistant();
    } catch (error) {
        console.error('Erreur d\'initialisation:', error);
        document.getElementById('statusIndicator').innerHTML =
            '<i class="fas fa-exclamation-triangle"></i><span>Erreur d\'initialisation de l\'assistant</span>';
    }
});
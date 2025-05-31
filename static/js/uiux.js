// Créer les formes flottantes
function createFloatingShapes() {
    const container = document.getElementById('floatingShapes');
    const shapes = ['circle', 'triangle', 'square'];

    for (let i = 0; i < 6; i++) {
        const shape = document.createElement('div');
        const shapeType = shapes[Math.floor(Math.random() * shapes.length)];

        shape.className = `shape shape-${shapeType}`;
        shape.style.left = Math.random() * 100 + '%';
        shape.style.top = Math.random() * 100 + '%';
        shape.style.animationDelay = Math.random() * 8 + 's';
        shape.style.animationDuration = (Math.random() * 4 + 6) + 's';

        container.appendChild(shape);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    createFloatingShapes();

    // Éléments DOM
    const speakButton = document.getElementById('speakButton');
    const statusIndicator = document.getElementById('statusIndicator');
    const userCommandElement = document.getElementById('userCommand');
    const assistantResponseElement = document.getElementById('assistantResponse');
    const userMessage = document.getElementById('userMessage');
    const assistantMessage = document.getElementById('assistantMessage');
    const micIcon = document.getElementById('micIcon');
    const pulseRings = document.getElementById('pulseRings');

    // Vérifier si la reconnaissance vocale est supportée
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        updateStatus('error', 'fas fa-exclamation-triangle', 'Reconnaissance vocale non supportée');
        speakButton.disabled = true;
        return;
    }

    // Initialiser la reconnaissance vocale
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = 'fr-FR';
    recognition.continuous = false;
    recognition.interimResults = false;

    function updateStatus(type, icon, text) {
        statusIndicator.className = `status-indicator ${type}`;
        statusIndicator.innerHTML = `<i class="${icon}"></i><span>${text}</span>`;
    }

    function showMessage(element) {
        setTimeout(() => {
            element.classList.add('show');
        }, 100);
    }

    function hideMessages() {
        userMessage.classList.remove('show');
        assistantMessage.classList.remove('show');
    }

    // Événements de reconnaissance vocale
    recognition.onstart = function () {
        speakButton.classList.add('listening');
        pulseRings.style.display = 'block';
        micIcon.className = 'fas fa-stop';
        updateStatus('listening', 'fas fa-microphone-alt', 'Je vous écoute...');
        speakButton.disabled = true;
        hideMessages();
    };

    recognition.onend = function () {
        speakButton.classList.remove('listening');
        pulseRings.style.display = 'none';
        micIcon.className = 'fas fa-microphone';
        speakButton.disabled = false;
    };

    recognition.onerror = function (event) {
        updateStatus('error', 'fas fa-exclamation-triangle', 'Erreur de reconnaissance');
        speakButton.classList.remove('listening');
        pulseRings.style.display = 'none';
        micIcon.className = 'fas fa-microphone';
        speakButton.disabled = false;
    };

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        userCommandElement.textContent = transcript;
        showMessage(userMessage);

        updateStatus('processing', 'fas fa-cog fa-spin', 'Traitement en cours...');
        assistantResponseElement.innerHTML = '<div class="thinking-animation"><div class="thinking-dot"></div><div class="thinking-dot"></div><div class="thinking-dot"></div></div>';
        showMessage(assistantMessage);

        sendCommandToServer(transcript);
    };

    function sendCommandToServer(command) {
        fetch('/process_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: command
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    assistantResponseElement.textContent = data.text;
                    updateStatus('', 'fas fa-check-circle', 'Réponse générée');

                    if (data.redirect) {
                        setTimeout(() => {
                            window.open(data.redirect, '_blank');
                        }, 1000);
                    }
                } else {
                    assistantResponseElement.textContent = data.error || 'Une erreur est survenue';
                    updateStatus('error', 'fas fa-exclamation-triangle', 'Erreur de traitement');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                assistantResponseElement.textContent = 'Erreur de connexion au serveur';
                updateStatus('error', 'fas fa-wifi', 'Connexion impossible');
            });
    }

    speakButton.addEventListener('click', function () {
        if (speakButton.classList.contains('listening')) {
            recognition.stop();
        } else {
            userCommandElement.textContent = '';
            assistantResponseElement.textContent = '';
            hideMessages();
            recognition.start();
        }
    });

    // Fonction de test
    window.sendTextCommand = function (text) {
        userCommandElement.textContent = text;
        showMessage(userMessage);
        sendCommandToServer(text);
    };
});
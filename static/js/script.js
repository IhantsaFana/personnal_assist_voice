document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const speakButton = document.getElementById('speakButton');
    const statusElement = document.getElementById('status');
    const userCommandElement = document.getElementById('userCommand');
    const assistantResponseElement = document.getElementById('assistantResponse');
    
    // Vérifier si la reconnaissance vocale est supportée par le navigateur
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        statusElement.textContent = 'La reconnaissance vocale n\'est pas supportée par votre navigateur.';
        speakButton.disabled = true;
        return;
    }
    
    // Initialiser l'objet de reconnaissance vocale
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    // Configuration de la reconnaissance vocale
    recognition.lang = 'fr-FR';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    // Événement lorsque la reconnaissance vocale démarre
    recognition.onstart = function() {
        statusElement.textContent = 'Écoute en cours... Parlez maintenant';
        speakButton.disabled = true;
    };
    
    // Événement lorsque la reconnaissance vocale s'arrête
    recognition.onend = function() {
        statusElement.textContent = 'Écoute terminée';
        speakButton.disabled = false;
    };
    
    // Événement lorsqu'une erreur se produit
    recognition.onerror = function(event) {
        statusElement.textContent = 'Erreur lors de la reconnaissance : ' + event.error;
        speakButton.disabled = false;
    };
    
    // Événement lorsqu'un résultat est disponible
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        userCommandElement.textContent = transcript;
        statusElement.textContent = 'Traitement de votre commande...';
        
        // Envoyer la commande au serveur Flask
        sendCommandToServer(transcript);
    };
    
    // Fonction pour envoyer la commande au serveur
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
                statusElement.textContent = 'Commande traitée avec succès';
                
                // Gestion de la redirection si nécessaire
                if (data.redirect) {
                    setTimeout(() => {
                        window.open(data.redirect, '_blank');
                    }, 1000); // Attendre 1 seconde pour que l'utilisateur entende la réponse vocale
                }
            } else {
                assistantResponseElement.textContent = data.error || 'Une erreur est survenue';
                statusElement.textContent = 'Erreur lors du traitement de la commande';
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            assistantResponseElement.textContent = 'Erreur de connexion au serveur';
            statusElement.textContent = 'Erreur de connexion';
        });
    }
    
    // Événement de clic sur le bouton Parler
    speakButton.addEventListener('click', function() {
        // Réinitialiser les champs
        userCommandElement.textContent = '';
        assistantResponseElement.textContent = '';
        
        // Démarrer la reconnaissance vocale
        recognition.start();
    });
    
    // Fonction pour envoyer du texte manuellement (pour les tests)
    window.sendTextCommand = function(text) {
        userCommandElement.textContent = text;
        sendCommandToServer(text);
    };
});
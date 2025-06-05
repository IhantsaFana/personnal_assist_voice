document.addEventListener('DOMContentLoaded', function () {
    // Éléments DOM
    const speakButton = document.getElementById('speakButton');
    const statusElement = document.getElementById('statusIndicator');
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
    recognition.onstart = function () {
        statusElement.textContent = 'Écoute en cours... Parlez maintenant';
        speakButton.disabled = true;

        // Ajouter la classe active pour l'animation
        speakButton.classList.add('active');
    };

    // Événement lorsque la reconnaissance vocale s'arrête
    recognition.onend = function () {
        statusElement.textContent = 'Écoute terminée';
        speakButton.disabled = false;

        // Retirer la classe active
        speakButton.classList.remove('active');
    };

    // Événement lorsqu'une erreur se produit
    recognition.onerror = function (event) {
        statusElement.textContent = 'Erreur lors de la reconnaissance : ' + event.error;
        speakButton.disabled = false;
        speakButton.classList.remove('active');
    };

    // Événement lorsqu'un résultat est disponible
    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        userCommandElement.textContent = transcript;
        statusElement.innerHTML = '<i class="fas fa-pray"></i><span>Je médite sur votre question...</span>';

        // Envoyer la question au serveur via l'API Vercel
        fetch('/api/process_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: transcript })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                assistantResponseElement.textContent = data.response;
                statusElement.innerHTML = '<i class="fas fa-bible"></i><span>Réponse prête</span>';
            })
            .catch(error => {
                console.error('Erreur:', error);
                statusElement.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>Erreur: ' + error.message + '</span>';
                assistantResponseElement.textContent = "Je suis désolé, j'ai rencontré une erreur. Pouvez-vous réessayer ?";
            });
    };

    // Gestionnaire de clic pour le bouton de parole
    speakButton.addEventListener('click', function () {
        recognition.start();
    });
});
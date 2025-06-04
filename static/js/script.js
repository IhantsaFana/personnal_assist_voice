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
    };

    // Événement lorsque la reconnaissance vocale s'arrête
    recognition.onend = function () {
        statusElement.textContent = 'Écoute terminée';
        speakButton.disabled = false;
    };

    // Événement lorsqu'une erreur se produit
    recognition.onerror = function (event) {
        statusElement.textContent = 'Erreur lors de la reconnaissance : ' + event.error;
        speakButton.disabled = false;
    };

    // Événement lorsqu'un résultat est disponible
    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        userCommandElement.textContent = transcript;
        statusElement.innerHTML = '<i class="fas fa-pray"></i><span>Je médite sur votre question...</span>';

        // Envoyer la question au serveur Flask
        fetch('/process_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: transcript })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    assistantResponseElement.textContent = data.text;
                } else {
                    assistantResponseElement.textContent = "Je suis désolé, je n'ai pas pu comprendre votre question. Pouvez-vous la reformuler différemment?";
                }
                statusElement.innerHTML = '<i class="fas fa-bible"></i><span>Posez une question sur la Bible ou la foi chrétienne</span>';
            })
            .catch(error => {
                console.error('Error:', error);
                assistantResponseElement.textContent = "Une erreur s'est produite. Prions et réessayons.";
                statusElement.innerHTML = '<i class="fas fa-bible"></i><span>Posez une question sur la Bible ou la foi chrétienne</span>';
            });

    };

    // Événement de clic sur le bouton Parler
    speakButton.addEventListener('click', function () {
        // Réinitialiser les champs
        userCommandElement.textContent = '';
        assistantResponseElement.textContent = '';

        // Démarrer la reconnaissance vocale
        recognition.start();
    });

});

document.addEventListener('DOMContentLoaded', function() {
    const conversationBox = document.querySelector('.conversation_box');
    const promptInput = document.getElementById('prompt');
    const sendIcon = document.querySelector('.icon-right');

    function addMessage(text, isUser = true) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user' : 'ai'); 

        messageDiv.textContent = text;
        conversationBox.appendChild(messageDiv);
        conversationBox.scrollTop = conversationBox.scrollHeight; 
    }

    function handleSend() {
        const userMessage = promptInput.value.trim();
        if (userMessage === '') return;

        addMessage(userMessage, true); 
        promptInput.value = ''; 

        setTimeout(() => {
            addMessage('Reply from AI chat bot', false); 
        }, 500);
    }

    sendIcon.addEventListener('click', handleSend);
    promptInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault(); 
            handleSend();
        }
    });
});
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const messagesContainer = document.getElementById('messages');
const fileUpload = document.getElementById('file-upload');
const uploadStatus = document.getElementById('upload-status');
const imageUploadBtn = document.getElementById('image-upload-btn');
const imageInput = document.getElementById('image-input');
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeImageBtn = document.getElementById('remove-image');

let currentImageBase64 = null;
let chatHistory = [];

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// File Upload
fileUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadStatus.textContent = 'Uploading...';

    try {
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        uploadStatus.textContent = 'Upload complete!';
        setTimeout(() => uploadStatus.textContent = '', 3000);
        addSystemMessage(`File uploaded: ${file.name}`);
    } catch (error) {
        uploadStatus.textContent = 'Upload failed.';
        console.error('Error:', error);
    }
});

// Image Upload
imageUploadBtn.addEventListener('click', () => imageInput.click());

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        currentImageBase64 = e.target.result;
        imagePreview.src = currentImageBase64;
        imagePreviewContainer.style.display = 'inline-block';
    };
    reader.readAsDataURL(file);
});

removeImageBtn.addEventListener('click', () => {
    currentImageBase64 = null;
    imageInput.value = '';
    imagePreviewContainer.style.display = 'none';
});

// Send Message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message && !currentImageBase64) return;

    // Add user message to UI
    addUserMessage(message, currentImageBase64);

    // Prepare request
    const payload = {
        message: message,
        history: chatHistory,
        image: currentImageBase64
    };

    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    currentImageBase64 = null;
    imageInput.value = '';
    imagePreviewContainer.style.display = 'none';

    // Add loading indicator
    const loadingId = addLoadingMessage();

    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        // Remove loading
        removeMessage(loadingId);

        // Add assistant response
        addAssistantMessage(data.response);

        // Update history
        chatHistory.push({ role: "user", content: message });
        chatHistory.push({ role: "assistant", content: data.response });

    } catch (error) {
        removeMessage(loadingId);
        addSystemMessage('Error sending message. Please try again.');
        console.error('Error:', error);
    }
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// UI Helpers
function addUserMessage(text, image) {
    const div = document.createElement('div');
    div.className = 'message user';
    let content = '';
    if (image) {
        content += `<img src="${image}" alt="User Image">`;
    }
    if (text) {
        content += `<div class="content">${text}</div>`;
    }
    div.innerHTML = content;
    messagesContainer.appendChild(div);
    scrollToBottom();
}

function addAssistantMessage(text) {
    const div = document.createElement('div');
    div.className = 'message assistant';
    // Convert newlines to <br> for basic formatting
    const formattedText = text.replace(/\n/g, '<br>');
    div.innerHTML = `<div class="content">${formattedText}</div>`;
    messagesContainer.appendChild(div);
    scrollToBottom();
}

function addSystemMessage(text) {
    const div = document.createElement('div');
    div.className = 'message system';
    div.innerHTML = `<div class="content">${text}</div>`;
    messagesContainer.appendChild(div);
    scrollToBottom();
}

function addLoadingMessage() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'message assistant';
    div.innerHTML = `<div class="content"><i class="fas fa-spinner fa-spin"></i> Thinking...</div>`;
    messagesContainer.appendChild(div);
    scrollToBottom();
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

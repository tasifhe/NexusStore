// Chat functionality for GameAssetHub
class ChatWidget {
    constructor() {
        this.chatWidget = document.getElementById('chatWidget');
        this.chatToggle = document.getElementById('chatToggle');
        this.chatClose = document.getElementById('chatClose');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.chatSend = document.getElementById('chatSend');
        this.sessionId = null;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        if (!this.chatWidget) return;
        
        // Event listeners
        this.chatToggle.addEventListener('click', () => this.toggleChat());
        this.chatClose.addEventListener('click', () => this.closeChat());
        this.chatSend.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Initialize chat session
        this.initSession();
    }
    
    async initSession() {
        try {
            const response = await fetch('/chat/api/session/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                }
            });
            
            const data = await response.json();
            if (data.success) {
                this.sessionId = data.session_id;
                this.loadChatHistory();
            }
        } catch (error) {
            console.error('Error initializing chat session:', error);
        }
    }
    
    async loadChatHistory() {
        if (!this.sessionId) return;
        
        try {
            const response = await fetch(`/chat/api/history/${this.sessionId}/`);
            const data = await response.json();
            
            if (data.success && data.history.length > 0) {
                this.chatMessages.innerHTML = '';
                data.history.forEach(msg => {
                    this.displayMessage(msg.content, msg.type);
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        this.chatWidget.classList.add('show');
        this.chatWidget.style.display = 'flex';
        this.isOpen = true;
        this.chatInput.focus();
    }
    
    closeChat() {
        this.chatWidget.classList.remove('show');
        this.chatWidget.style.display = 'none';
        this.isOpen = false;
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;
        
        // Display user message
        this.displayMessage(message, 'user');
        this.chatInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/chat/api/message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            if (data.success) {
                this.displayMessage(data.response, 'bot');
                if (data.session_id) {
                    this.sessionId = data.session_id;
                }
            } else {
                this.displayMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.displayMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }
    
    displayMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = this.formatMessage(content);
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        // Add animation
        messageDiv.classList.add('fade-in');
    }
    
    formatMessage(content) {
        // Convert line breaks to HTML breaks
        content = content.replace(/\n/g, '<br>');
        
        // Convert **text** to bold
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert *text* to italic
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convert URLs to links
        content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
        
        return content;
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <span class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </span>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    hideTypingIndicator() {
        const typingIndicator = this.chatMessages.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }
}

// Additional chat styles
const chatStyles = `
.typing-indicator {
    opacity: 0.7;
}

.typing-dots {
    display: inline-block;
}

.typing-dots span {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #999;
    margin: 0 2px;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) {
    animation-delay: -0.32s;
}

.typing-dots span:nth-child(2) {
    animation-delay: -0.16s;
}

@keyframes typing {
    0%, 80%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

.message-content {
    word-wrap: break-word;
    line-height: 1.4;
}

.message-content strong {
    font-weight: 600;
}

.message-content em {
    font-style: italic;
}

.message-content a {
    color: #007bff;
    text-decoration: underline;
}

.message-content a:hover {
    text-decoration: none;
}
`;

// Inject chat styles
const styleSheet = document.createElement('style');
styleSheet.textContent = chatStyles;
document.head.appendChild(styleSheet);

// Initialize chat widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatWidget();
});

// Export for use in other modules
window.ChatWidget = ChatWidget;
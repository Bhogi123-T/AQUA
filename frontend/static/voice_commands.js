// 🎙️ AI Voice Command Navigation Functions
let recognition = null;
let isVoiceCommandActive = false;

function initVoiceCommands() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        
        const htmlLang = document.documentElement.lang || 'en';
        recognition.lang = htmlLang === 'en' ? 'en-IN' : htmlLang + '-IN';

        recognition.onresult = function(event) {
            const last = event.results.length - 1;
            const command = event.results[last][0].transcript.toLowerCase().trim();
            console.log('Voice Command Received:', command);
            
            const toggleBtn = document.getElementById('voice-command-toggle');
            if (toggleBtn) {
                toggleBtn.style.background = 'rgba(255, 193, 7, 0.3)'; // Processing Yellow
            }
            
            // Send voice command to Backend NLP Processor
            fetch('/api/voice-command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ command: command })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    if (typeof speakText === 'function') speakText(data.message);
                    
                    setTimeout(() => {
                        if (data.action === 'navigate' && data.url) {
                            window.location.href = data.url;
                        } else if (data.action === 'system' && data.command === 'stop_voice') {
                            toggleVoiceCommands();
                        }
                    }, 1500);
                    
                    if (isVoiceCommandActive && data.action !== 'system' && toggleBtn) {
                        toggleBtn.style.background = 'rgba(0, 255, 136, 0.3)';
                    }
                } else {
                    if (toggleBtn) toggleBtn.style.background = 'rgba(255, 0, 85, 0.3)';
                    setTimeout(() => {
                        if (isVoiceCommandActive && toggleBtn) toggleBtn.style.background = 'rgba(0, 255, 136, 0.3)';
                    }, 1000);
                }
            })
            .catch(err => {
                console.error("Backend connection failed", err);
                if (typeof speakText === 'function') speakText("Backend connection failed.");
                if (toggleBtn) toggleBtn.style.background = 'rgba(255, 0, 85, 0.3)';
                setTimeout(() => {
                    if (isVoiceCommandActive && toggleBtn) toggleBtn.style.background = 'rgba(0, 255, 136, 0.3)';
                }, 1000);
            });
        };

        recognition.onerror = function(event) {
            console.error('Voice Recognition Error:', event.error);
        };
        
        recognition.onend = function() {
            if (isVoiceCommandActive) {
                try {
                    recognition.start();
                } catch (e) {}
            }
        }
    } else {
        console.warn('Speech Recognition API not supported in this browser.');
        const toggleBtn = document.getElementById('voice-command-toggle');
        if (toggleBtn) toggleBtn.style.display = 'none';
    }
}

function toggleVoiceCommands() {
    if (!recognition) {
        initVoiceCommands();
    }
    if (!recognition) return;

    const toggleBtn = document.getElementById('voice-command-toggle');
    const icon = document.getElementById('voice-command-icon');
    const text = document.getElementById('voice-command-text');

    isVoiceCommandActive = !isVoiceCommandActive;

    if (isVoiceCommandActive) {
        try {
            recognition.start();
            if (toggleBtn) {
                toggleBtn.style.background = 'rgba(0, 255, 136, 0.3)';
                toggleBtn.style.borderColor = '#00ff88';
            }
            if (icon) icon.innerText = '🔴';
            if (text) text.innerText = 'LISTENING...';
            if (typeof speakText === 'function') speakText("Voice Command Active. Say home, farmer, or lab.");
        } catch (e) {
            console.error('Recognition start error', e);
        }
    } else {
        try {
            recognition.stop();
            if (toggleBtn) {
                toggleBtn.style.background = 'linear-gradient(90deg, rgba(0, 255, 136, 0.1), rgba(0, 210, 255, 0.1))';
                toggleBtn.style.borderColor = 'var(--accent)';
            }
            if (icon) icon.innerText = '🎙️';
            if (text) text.innerText = 'VOICE COMMAND (OFF)';
        } catch (e) {
            console.error('Recognition stop error', e);
        }
    }
}

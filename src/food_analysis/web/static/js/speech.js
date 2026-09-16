/**
 * CookCast AI - Hands-free Voice Control & Speech Synthesis Fallback
 */

class SpeechController {
    constructor(onCommandCallback) {
        this.onCommand = onCommandCallback;
        this.recognition = null;
        this.isListening = false;
        this.hasSpeechRec = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
        this.initRecognition();
    }

    initRecognition() {
        if (!this.hasSpeechRec) {
            console.warn("Web Speech Recognition is not supported in this browser.");
            return;
        }

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRec();
        this.recognition.lang = 'ko-KR';
        this.recognition.continuous = true;
        this.recognition.interimResults = false;

        this.recognition.onresult = (event) => {
            const last = event.results.length - 1;
            const transcript = event.results[last][0].transcript.trim();
            console.log("🎤 Voice command heard:", transcript);
            this.handleTranscript(transcript);
        };

        this.recognition.onerror = (event) => {
            console.warn("Speech recognition error:", event.error);
        };

        this.recognition.onend = () => {
            if (this.isListening) {
                try {
                    this.recognition.start();
                } catch (e) {
                    console.log("Speech restart ignored:", e);
                }
            }
        };
    }

    handleTranscript(text) {
        const lower = text.toLowerCase().replace(/\s+/g, '');

        if (lower.includes('다음') || lower.includes('넥스트') || lower.includes('넘어가')) {
            this.onCommand('next', text);
        } else if (lower.includes('이전') || lower.includes('뒤로') || lower.includes('전단계')) {
            this.onCommand('prev', text);
        } else if (lower.includes('다시') || lower.includes('반복') || lower.includes('리플레이')) {
            this.onCommand('replay', text);
        } else if (lower.includes('멈춰') || lower.includes('정지') || lower.includes('일시정지') || lower.includes('스톱')) {
            this.onCommand('pause', text);
        } else if (lower.includes('시작') || lower.includes('재생') || lower.includes('플레이') || lower.includes('계속')) {
            this.onCommand('play', text);
        } else if (lower.includes('타이머')) {
            this.onCommand('timer', text);
        } else {
            this.onCommand('unknown', text);
        }
    }

    toggle() {
        if (!this.hasSpeechRec) {
            alert("현재 브라우저는 음성 인식을 지원하지 않습니다. Chrome/Edge 브라우저를 권장합니다.");
            return false;
        }

        if (this.isListening) {
            this.isListening = false;
            this.recognition.stop();
            return false;
        } else {
            this.isListening = true;
            try {
                this.recognition.start();
            } catch (e) {
                console.error("Recognition start failed:", e);
            }
            return true;
        }
    }

    /**
     * Browser Web Speech Synthesis Fallback
     */
    speakBrowserTTS(text, onEnd) {
        if (!('speechSynthesis' in window)) {
            if (onEnd) onEnd();
            return;
        }
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'ko-KR';
        utterance.rate = 0.95;
        utterance.pitch = 1.0;
        if (onEnd) {
            utterance.onend = onEnd;
            utterance.onerror = onEnd;
        }
        window.speechSynthesis.speak(utterance);
    }
}

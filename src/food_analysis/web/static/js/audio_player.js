/**
 * CookCast AI - Hands-Free Audio Player & Timer Engine
 */

class AudioChefPlayer {
    constructor() {
        this.audioEl = document.getElementById('audioElement');
        this.steps = [];
        this.stepAudios = [];
        this.currentStepIdx = 0;
        this.isPlaying = false;
        
        // Timer state
        this.timerInterval = null;
        this.remainingSeconds = 0;
        this.totalTimerSeconds = 0;
        this.isTimerRunning = false;

        // UI elements
        this.playIcon = document.getElementById('playIcon');
        this.playStatusText = document.getElementById('playStatusText');
        this.waveformEl = document.getElementById('waveformVisualizer');
        this.currentStepTitle = document.getElementById('currentStepTitle');
        this.currentSpokenScript = document.getElementById('currentSpokenScript');
        this.currentStepTipBox = document.getElementById('currentStepTipBox');
        this.currentStepTipText = document.getElementById('currentStepTipText');
        this.currentHeatBadge = document.getElementById('currentHeatBadge');
        this.stepPillsContainer = document.getElementById('stepPillsContainer');
        this.timerDisplay = document.getElementById('timerDisplay');
        this.timerProgressCircle = document.getElementById('timerProgressCircle');
        this.btnTimerStartPause = document.getElementById('btnTimerStartPause');

        this.initAudioEvents();
    }

    initAudioEvents() {
        this.audioEl.addEventListener('play', () => {
            this.isPlaying = true;
            this.playIcon.className = 'fa-solid fa-pause';
            this.playStatusText.textContent = '일시정지';
            this.waveformEl.classList.add('playing');
        });

        this.audioEl.addEventListener('pause', () => {
            this.isPlaying = false;
            this.playIcon.className = 'fa-solid fa-play';
            this.playStatusText.textContent = '재생';
            this.waveformEl.classList.remove('playing');
        });

        this.audioEl.addEventListener('ended', () => {
            this.isPlaying = false;
            this.playIcon.className = 'fa-solid fa-play';
            this.playStatusText.textContent = '재생';
            this.waveformEl.classList.remove('playing');

            // If this step has an associated timer, automatically start it
            const currentStep = this.steps[this.currentStepIdx];
            if (currentStep && currentStep.timer_seconds && !this.isTimerRunning) {
                this.startTimer(currentStep.timer_seconds);
            }
        });

        this.audioEl.addEventListener('error', (e) => {
            console.warn("Audio playback error, falling back to Web Speech Synthesis:", e);
            this.waveformEl.classList.remove('playing');
            this.playStatusText.textContent = '재생';
            this.playIcon.className = 'fa-solid fa-play';
        });
    }

    loadRecipe(recipeData, audioData) {
        this.steps = recipeData.steps || [];
        this.stepAudios = audioData.step_audios || [];
        this.currentStepIdx = 0;
        this.stopTimer();

        this.renderStepPills();
        this.selectStep(0, false);
    }

    renderStepPills() {
        this.stepPillsContainer.innerHTML = '';
        this.steps.forEach((step, idx) => {
            const btn = document.createElement('button');
            btn.className = `step-pill-btn ${idx === this.currentStepIdx ? 'active' : ''}`;
            btn.textContent = `${step.step_number}단계: ${step.title}`;
            btn.addEventListener('click', () => {
                this.selectStep(idx, true);
            });
            this.stepPillsContainer.appendChild(btn);
        });
    }

    selectStep(index, autoPlay = true) {
        if (index < 0 || index >= this.steps.length) return;
        this.currentStepIdx = index;

        const step = this.steps[index];
        const audioInfo = this.stepAudios.find(a => a.step_number === step.step_number);

        // Update Pill styles
        const pills = this.stepPillsContainer.querySelectorAll('.step-pill-btn');
        pills.forEach((p, i) => {
            p.classList.toggle('active', i === index);
        });

        // Update Teleprompter Info
        this.currentStepTitle.textContent = `${step.step_number}단계: ${step.title}`;
        this.currentSpokenScript.textContent = `"${step.audio_script}"`;
        this.currentHeatBadge.textContent = step.heat_level || '없음';

        if (step.tips) {
            this.currentStepTipBox.style.display = 'flex';
            this.currentStepTipText.textContent = step.tips;
        } else {
            this.currentStepTipBox.style.display = 'none';
        }

        // Setup Timer for this step
        this.stopTimer();
        if (step.timer_seconds) {
            this.initTimerUI(step.timer_seconds);
        } else {
            this.timerDisplay.textContent = '--:--';
            this.updateTimerProgress(0);
        }

        // Set audio source
        if (audioInfo && audioInfo.audio_url) {
            this.audioEl.src = audioInfo.audio_url;
            if (autoPlay) {
                this.playAudio();
            }
        } else {
            // Fallback to text speech
            if (autoPlay && window.speechController) {
                window.speechController.speakBrowserTTS(step.audio_script);
            }
        }
    }

    togglePlay() {
        if (this.isPlaying) {
            this.pauseAudio();
        } else {
            this.playAudio();
        }
    }

    playAudio() {
        if (this.audioEl.src) {
            this.audioEl.play().catch(err => {
                console.warn("Autoplay was prevented or audio failed:", err);
                const step = this.steps[this.currentStepIdx];
                if (step && window.speechController) {
                    window.speechController.speakBrowserTTS(step.audio_script);
                }
            });
        }
    }

    pauseAudio() {
        this.audioEl.pause();
    }

    nextStep() {
        if (this.currentStepIdx < this.steps.length - 1) {
            this.selectStep(this.currentStepIdx + 1, true);
        } else {
            window.showToast("🎉 모든 조리 단계를 완료했습니다! 맛있게 드세요.");
        }
    }

    prevStep() {
        if (this.currentStepIdx > 0) {
            this.selectStep(this.currentStepIdx - 1, true);
        }
    }

    replayStep() {
        this.selectStep(this.currentStepIdx, true);
    }

    /* ----------------------------------------------------
       Timer Engine & Chime Synthesizer
       ---------------------------------------------------- */
    initTimerUI(totalSec) {
        this.totalTimerSeconds = totalSec;
        this.remainingSeconds = totalSec;
        this.renderTimerText(totalSec);
        this.updateTimerProgress(1);
    }

    toggleTimer() {
        if (this.isTimerRunning) {
            this.pauseTimer();
        } else {
            this.startTimer(this.remainingSeconds > 0 ? this.remainingSeconds : this.totalTimerSeconds);
        }
    }

    startTimer(seconds) {
        this.stopTimer();
        this.remainingSeconds = seconds;
        if (!this.totalTimerSeconds) this.totalTimerSeconds = seconds;
        this.isTimerRunning = true;
        this.btnTimerStartPause.innerHTML = '<i class="fa-solid fa-pause"></i>';

        this.renderTimerText(this.remainingSeconds);
        this.updateTimerProgress(this.remainingSeconds / this.totalTimerSeconds);

        this.timerInterval = setInterval(() => {
            this.remainingSeconds--;
            if (this.remainingSeconds <= 0) {
                this.stopTimer();
                this.playChimeSound();
                window.showToast("⏰ 타이머 완료! 다음 단계로 넘어갈 준비를 해주세요.");
            } else {
                this.renderTimerText(this.remainingSeconds);
                this.updateTimerProgress(this.remainingSeconds / this.totalTimerSeconds);
            }
        }, 1000);
    }

    pauseTimer() {
        clearInterval(this.timerInterval);
        this.isTimerRunning = false;
        this.btnTimerStartPause.innerHTML = '<i class="fa-solid fa-play"></i>';
    }

    stopTimer() {
        clearInterval(this.timerInterval);
        this.isTimerRunning = false;
        this.btnTimerStartPause.innerHTML = '<i class="fa-solid fa-play"></i>';
    }

    renderTimerText(sec) {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        this.timerDisplay.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }

    updateTimerProgress(fraction) {
        const circumference = 2 * Math.PI * 24; // r=24 approx 150.79
        const offset = circumference - (fraction * circumference);
        this.timerProgressCircle.style.strokeDasharray = `${circumference}`;
        this.timerProgressCircle.style.strokeDashoffset = `${offset}`;
    }

    playChimeSound() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const ctx = new AudioContext();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
            osc.frequency.setValueAtTime(880.00, ctx.currentTime + 0.15); // A5
            gain.gain.setValueAtTime(0.3, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.8);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.85);
        } catch (e) {
            console.log("Web Audio Chime failed:", e);
        }
    }
}

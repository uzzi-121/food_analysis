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

        // Synchronized Step Image Elements
        this.activeStepImg = document.getElementById('activeStepImg');
        this.activeStepBadge = document.getElementById('activeStepBadge');
        this.activeStepCaptionText = document.getElementById('activeStepCaptionText');

        this.initAudioEvents();
    }

    initAudioEvents() {
        if (!this.audioEl) return;
        this.audioEl.addEventListener('play', () => {
            this.isPlaying = true;
            if (this.playIcon) this.playIcon.className = 'fa-solid fa-pause';
            if (this.playStatusText) this.playStatusText.textContent = '일시정지';
            if (this.waveformEl) this.waveformEl.classList.add('playing');
        });

        this.audioEl.addEventListener('pause', () => {
            this.isPlaying = false;
            if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
            if (this.playStatusText) this.playStatusText.textContent = '재생';
            if (this.waveformEl) this.waveformEl.classList.remove('playing');
        });

        this.audioEl.addEventListener('ended', () => {
            this.isPlaying = false;
            if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
            if (this.playStatusText) this.playStatusText.textContent = '재생';
            if (this.waveformEl) this.waveformEl.classList.remove('playing');

            // If this step has an associated timer, automatically start it
            const currentStep = this.steps[this.currentStepIdx];
            if (currentStep && currentStep.timer_seconds && !this.isTimerRunning) {
                this.startTimer(currentStep.timer_seconds);
            }
        });

        this.audioEl.addEventListener('error', (e) => {
            console.warn("Audio playback error, falling back to Web Speech Synthesis:", e);
            if (this.waveformEl) this.waveformEl.classList.remove('playing');
            if (this.playStatusText) this.playStatusText.textContent = '재생';
            if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
        });
    }

    loadRecipe(recipeData, audioData) {
        this.recipe = recipeData;
        this.steps = recipeData.steps || [];
        this.stepAudios = audioData.step_audios || [];
        this.currentStepIdx = 0;
        this.stopTimer();

        // Update Recipe Header
        const titleEl = document.getElementById('procedureRecipeTitle');
        if (titleEl) titleEl.textContent = recipeData.title;

        const timeEl = document.getElementById('procedureEstimatedTime');
        if (timeEl) {
            const totalMin = (recipeData.prep_time_min || 0) + (recipeData.cook_time_min || 0);
            timeEl.textContent = `${totalMin > 0 ? totalMin + '분 소요' : '15분 소요'}`;
        }

        this.renderStepPills();
        // Start immediately on Step 0 and read speech
        this.selectStep(0, true);
    }

    renderStepPills() {
        if (!this.stepPillsContainer) return;
        this.stepPillsContainer.innerHTML = '';
        this.steps.forEach((step, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `stepper-pill-btn ${idx === this.currentStepIdx ? 'active' : ''}`;
            btn.innerHTML = `<span class="pill-num">0${step.step_number}</span> <span class="pill-title">${step.title}</span>`;
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

        // Cancel any existing speech synthesis before switching
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }

        // 1. Update Stepper Progress Bar & Active State
        const progressFill = document.getElementById('stepperProgressBarFill');
        if (progressFill) {
            const percent = ((index + 1) / this.steps.length) * 100;
            progressFill.style.width = `${percent}%`;
        }

        const progressText = document.getElementById('procedureStepProgressText');
        if (progressText) {
            progressText.textContent = `총 ${this.steps.length}단계 중 ${index + 1}단계 진행 중`;
        }

        if (this.stepPillsContainer) {
            const pills = this.stepPillsContainer.querySelectorAll('.stepper-pill-btn');
            pills.forEach((p, i) => {
                p.classList.toggle('active', i === index);
                p.classList.toggle('completed', i < index);
            });
        }

        // 2. Update Step Top Badges & Meta
        const numPill = document.getElementById('currentStepNumPill');
        if (numPill) numPill.textContent = `STEP 0${step.step_number}`;

        if (this.currentHeatBadge) {
            this.currentHeatBadge.textContent = step.heat_level || '없음';
            this.currentHeatBadge.className = 'heat-badge';
            if (step.heat_level) {
                if (step.heat_level.includes('강불')) this.currentHeatBadge.classList.add('heat-high');
                else if (step.heat_level.includes('약불')) this.currentHeatBadge.classList.add('heat-low');
                else if (step.heat_level.includes('중')) this.currentHeatBadge.classList.add('heat-med');
            }
        }

        const timerBadge = document.getElementById('currentStepTimerBadge');
        const timerText = document.getElementById('currentStepTimerText');
        if (timerBadge && timerText) {
            if (step.timer_seconds) {
                timerBadge.style.display = 'inline-flex';
                const m = Math.floor(step.timer_seconds / 60);
                const s = step.timer_seconds % 60;
                timerText.textContent = `${m > 0 ? m + '분 ' : ''}${s > 0 ? s + '초' : ''}`;
            } else {
                timerBadge.style.display = 'none';
            }
        }

        // 3. Update Step Title & Guide Description
        if (this.currentStepTitle) {
            this.currentStepTitle.textContent = step.title;
        }
        const guideEl = document.getElementById('currentStepGuideText');
        if (guideEl) {
            guideEl.textContent = step.guide_text;
        }

        // 4. Update Spoken Audio Script
        if (this.currentSpokenScript) {
            this.currentSpokenScript.textContent = `"${step.audio_script}"`;
        }

        // 5. Update Chef Secret Tip Box
        if (this.currentStepTipBox && this.currentStepTipText) {
            if (step.tips) {
                this.currentStepTipBox.style.display = 'flex';
                this.currentStepTipText.textContent = `셰프 팁: ${step.tips}`;
            } else {
                this.currentStepTipBox.style.display = 'none';
            }
        }

        // 6. Update Inline Timer Widget
        const inlineTimer = document.getElementById('stepInlineTimer');
        this.stopTimer();
        if (inlineTimer) {
            if (step.timer_seconds) {
                inlineTimer.style.display = 'flex';
                this.initTimerUI(step.timer_seconds);
            } else {
                inlineTimer.style.display = 'none';
            }
        }

        // 7. Update Synchronized Right-Side Visual Image Card with subtle transition
        if (this.activeStepImg) {
            this.activeStepImg.style.opacity = '0.3';
            setTimeout(() => {
                this.activeStepImg.src = step.image_url || `/static/images/steps/default_step${Math.min(step.step_number, 3)}.svg`;
                this.activeStepImg.alt = step.image_alt || `${step.title} 조리 과정`;
                this.activeStepImg.style.opacity = '1';
            }, 120);
        }
        if (this.activeStepCaptionText) {
            this.activeStepCaptionText.textContent = `${step.step_number}단계: ${step.title}`;
        }

        // 8. Update Navigation Buttons
        const btnPrev = document.getElementById('btnPrevStep');
        const btnNext = document.getElementById('btnNextStep');
        if (btnPrev) {
            btnPrev.disabled = (index === 0);
            btnPrev.classList.toggle('disabled', index === 0);
        }
        if (btnNext) {
            if (index === this.steps.length - 1) {
                btnNext.innerHTML = '🎉 요리 완성! <i class="fa-solid fa-check"></i>';
                btnNext.classList.add('btn-finish-cooking');
            } else {
                btnNext.innerHTML = '다음 단계 <i class="fa-solid fa-arrow-right"></i>';
                btnNext.classList.remove('btn-finish-cooking');
            }
        }

        // 9. Read Current Step's Text via Audio / TTS
        if (audioInfo && audioInfo.audio_url) {
            this.audioEl.src = audioInfo.audio_url;
            if (autoPlay) {
                this.playAudio();
            }
        } else {
            // Browser Web Speech Synthesis Fallback
            if (autoPlay && window.speechController) {
                this.isPlaying = true;
                if (this.playIcon) this.playIcon.className = 'fa-solid fa-pause';
                if (this.playStatusText) this.playStatusText.textContent = '일시정지';
                if (this.waveformEl) this.waveformEl.classList.add('playing');

                window.speechController.speakBrowserTTS(step.audio_script, () => {
                    this.isPlaying = false;
                    if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
                    if (this.playStatusText) this.playStatusText.textContent = '재생';
                    if (this.waveformEl) this.waveformEl.classList.remove('playing');

                    // If step has timer, start it after speech
                    if (step.timer_seconds && !this.isTimerRunning) {
                        this.startTimer(step.timer_seconds);
                    }
                });
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
        const step = this.steps[this.currentStepIdx];
        if (this.audioEl && this.audioEl.src && !this.audioEl.src.endsWith('#')) {
            this.audioEl.play().catch(err => {
                console.warn("Autoplay was prevented or audio failed, using Web Speech API:", err);
                if (step && window.speechController) {
                    this.isPlaying = true;
                    if (this.playIcon) this.playIcon.className = 'fa-solid fa-pause';
                    if (this.playStatusText) this.playStatusText.textContent = '일시정지';
                    if (this.waveformEl) this.waveformEl.classList.add('playing');
                    window.speechController.speakBrowserTTS(step.audio_script, () => {
                        this.isPlaying = false;
                        if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
                        if (this.playStatusText) this.playStatusText.textContent = '재생';
                        if (this.waveformEl) this.waveformEl.classList.remove('playing');
                    });
                }
            });
        } else if (step && window.speechController) {
            this.isPlaying = true;
            if (this.playIcon) this.playIcon.className = 'fa-solid fa-pause';
            if (this.playStatusText) this.playStatusText.textContent = '일시정지';
            if (this.waveformEl) this.waveformEl.classList.add('playing');
            window.speechController.speakBrowserTTS(step.audio_script, () => {
                this.isPlaying = false;
                if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
                if (this.playStatusText) this.playStatusText.textContent = '재생';
                if (this.waveformEl) this.waveformEl.classList.remove('playing');
            });
        }
    }

    pauseAudio() {
        if (this.audioEl) this.audioEl.pause();
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        this.isPlaying = false;
        if (this.playIcon) this.playIcon.className = 'fa-solid fa-play';
        if (this.playStatusText) this.playStatusText.textContent = '재생';
        if (this.waveformEl) this.waveformEl.classList.remove('playing');
    }

    nextStep() {
        if (this.currentStepIdx < this.steps.length - 1) {
            this.selectStep(this.currentStepIdx + 1, true);
        } else {
            window.showToast("🎉 축하합니다! 모든 조리 단계를 성공적으로 마쳤습니다. 맛있게 드세요!");
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

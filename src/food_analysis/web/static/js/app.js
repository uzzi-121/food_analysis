/**
 * CookCast AI — Stitch Inspired AI-Native Natural Intent Frontend Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // Application State
    const state = {
        ingredients: [],
        uploadedPhotoFile: null,
        candidateRecipes: [],
        currentRecipe: null,
        currentAudioData: null
    };

    // DOM Elements: Views
    const sectionInput = document.getElementById('sectionInput');
    const sectionRecipes = document.getElementById('sectionRecipes');
    const sectionCooking = document.getElementById('sectionCooking');

    // DOM Elements: Inputs & Prompt
    const photoInput = document.getElementById('photoInput');
    const dropzone = document.getElementById('dropzone');
    const dropzonePreview = document.getElementById('dropzonePreview');
    const previewImg = document.getElementById('previewImg');
    const btnRemovePhoto = document.getElementById('btnRemovePhoto');
    const btnTriggerPhoto = document.getElementById('btnTriggerPhoto');
    const modePhotoBtn = document.getElementById('modePhotoBtn');
    const modeTextBtn = document.getElementById('modeTextBtn');

    const textIngredientInput = document.getElementById('textIngredientInput');
    const btnAddTextIngredient = document.getElementById('btnAddTextIngredient');
    const ingredientTagContainer = document.getElementById('ingredientTagContainer');
    const tagCount = document.getElementById('tagCount');
    const btnClearAllTags = document.getElementById('btnClearAllTags');
    const btnFindRecipes = document.getElementById('btnFindRecipes');
    const recipeCardsContainer = document.getElementById('recipeCardsContainer');
    const btnBackToInput = document.getElementById('btnBackToInput');
    const btnBackToRecipes = document.getElementById('btnBackToRecipes');

    // DOM Elements: Cooking View Meta
    const heroTitle = document.getElementById('heroTitle');
    const heroSubtitle = document.getElementById('heroSubtitle');
    const heroEmoji = document.getElementById('heroEmoji');
    const heroMatchRate = document.getElementById('heroMatchRate');
    const heroTotalTime = document.getElementById('heroTotalTime');
    const heroServings = document.getElementById('heroServings');
    const requiredIngList = document.getElementById('requiredIngList');
    const seasoningRatioList = document.getElementById('seasoningRatioList');
    const chefSecretList = document.getElementById('chefSecretList');

    // DOM Elements: Controls & Feedback
    const voiceFeedbackBanner = document.getElementById('voiceFeedbackBanner');
    const voiceCommandStatus = document.getElementById('voiceCommandStatus');

    // Instantiate Audio Player
    window.audioPlayer = new AudioChefPlayer();

    // Instantiate Voice Controller
    window.speechController = new SpeechController((command, rawText) => {
        console.log("Speech command triggered:", command, rawText);
        if (voiceFeedbackBanner) {
            voiceFeedbackBanner.style.backgroundColor = "rgba(139, 92, 246, 0.35)";
            setTimeout(() => {
                voiceFeedbackBanner.style.backgroundColor = "rgba(18, 20, 31, 0.85)";
            }, 1500);
        }

        if (command === 'next') {
            if (voiceCommandStatus) voiceCommandStatus.textContent = `🎙️ "${rawText}" ➡️ 다음 단계로 이동합니다.`;
            window.audioPlayer.nextStep();
        } else if (command === 'prev') {
            if (voiceCommandStatus) voiceCommandStatus.textContent = `🎙️ "${rawText}" ➡️ 이전 단계로 이동합니다.`;
            window.audioPlayer.prevStep();
        } else if (command === 'replay') {
            if (voiceCommandStatus) voiceCommandStatus.textContent = `🎙️ "${rawText}" ➡️ 현재 단계를 다시 재생합니다.`;
            window.audioPlayer.replayStep();
        } else if (command === 'pause') {
            if (voiceCommandStatus) voiceCommandStatus.textContent = `🎙️ "${rawText}" ➡️ 재생을 일시정지합니다.`;
            window.audioPlayer.pauseAudio();
        } else if (command === 'play') {
            if (voiceCommandStatus) voiceCommandStatus.textContent = `🎙️ "${rawText}" ➡️ 재생을 시작합니다.`;
            window.audioPlayer.playAudio();
        } else if (command === 'timer') {
            if (voiceCommandStatus) voiceCommandStatus.textContent = `🎙️ "${rawText}" ➡️ 타이머를 시작합니다.`;
            window.audioPlayer.toggleTimer();
        }
    });

    // ----------------------------------------------------
    // Toast Notification Utility (Stitch Dark Neon Style)
    // ----------------------------------------------------
    window.showToast = function (message) {
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.position = 'fixed';
            toastContainer.style.bottom = '24px';
            toastContainer.style.right = '24px';
            toastContainer.style.zIndex = '9999';
            toastContainer.style.display = 'flex';
            toastContainer.style.flexDirection = 'column';
            toastContainer.style.gap = '8px';
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.style.background = 'rgba(21, 24, 36, 0.95)';
        toast.style.backdropFilter = 'blur(16px)';
        toast.style.border = '1px solid rgba(139, 92, 246, 0.4)';
        toast.style.borderRadius = '12px';
        toast.style.padding = '12px 18px';
        toast.style.color = '#F3F4F6';
        toast.style.fontSize = '0.85rem';
        toast.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(139, 92, 246, 0.25)';
        toast.style.transition = 'all 0.25s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(12px)';
        toast.innerHTML = `<i class="fa-solid fa-sparkles" style="color: #8B5CF6; margin-right: 8px;"></i> ${message}`;

        toastContainer.appendChild(toast);
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        });

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(8px)';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    };

    // ----------------------------------------------------
    // View Navigation Logic
    // ----------------------------------------------------
    function goToStep(stepNumber) {
        if (sectionInput) sectionInput.classList.remove('active');
        if (sectionRecipes) sectionRecipes.classList.remove('active');
        if (sectionCooking) sectionCooking.classList.remove('active');

        if (stepNumber === 1) {
            if (sectionInput) sectionInput.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else if (stepNumber === 2) {
            if (sectionRecipes) sectionRecipes.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else if (stepNumber === 3) {
            if (sectionCooking) sectionCooking.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    // ----------------------------------------------------
    // Ingredient Tag Rendering
    // ----------------------------------------------------
    function renderTags() {
        if (!ingredientTagContainer) return;
        ingredientTagContainer.innerHTML = '';
        if (tagCount) tagCount.textContent = state.ingredients.length;

        state.ingredients.forEach((item, idx) => {
            const chip = document.createElement('div');
            chip.className = 'ingredient-chip';
            chip.innerHTML = `
                <span>${item.name}</span>
                <span class="chip-qty">${item.quantity_estimate || '적당량'}</span>
                <i class="fa-solid fa-xmark chip-delete" data-idx="${idx}" title="삭제"></i>
            `;
            chip.querySelector('.chip-delete').addEventListener('click', (e) => {
                e.stopPropagation();
                removeIngredient(idx);
            });
            ingredientTagContainer.appendChild(chip);
        });
    }

    function addIngredient(name, category = "기타", quantity = "적당량") {
        const trimmed = name.trim();
        if (!trimmed) return;
        if (state.ingredients.some(i => i.name === trimmed)) return;

        state.ingredients.push({
            name: trimmed,
            category: category,
            quantity_estimate: quantity,
            freshness: "신선함"
        });
        renderTags();
    }

    function removeIngredient(index) {
        state.ingredients.splice(index, 1);
        renderTags();
    }

    // Global quick intent preset handler (One-click natural language execution)
    window.applyIntentPreset = function(queryText) {
        if (textIngredientInput) {
            textIngredientInput.value = queryText;
        }
        if (btnFindRecipes) {
            btnFindRecipes.click();
        }
    };

    // ----------------------------------------------------
    // Input Event Listeners
    // ----------------------------------------------------
    if (textIngredientInput) {
        textIngredientInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                btnFindRecipes.click();
            }
        });
    }

    if (btnClearAllTags) {
        btnClearAllTags.addEventListener('click', () => {
            state.ingredients = [];
            renderTags();
            if (textIngredientInput) textIngredientInput.value = '';
        });
    }

    // Mode toggles
    if (modePhotoBtn && modeTextBtn) {
        modePhotoBtn.addEventListener('click', () => {
            modePhotoBtn.classList.add('active');
            modeTextBtn.classList.remove('active');
            photoInput.click();
        });
        modeTextBtn.addEventListener('click', () => {
            modeTextBtn.classList.add('active');
            modePhotoBtn.classList.remove('active');
            textIngredientInput.focus();
        });
    }

    // Plus attachment button
    if (btnTriggerPhoto) {
        btnTriggerPhoto.addEventListener('click', () => {
            photoInput.click();
        });
    }

    // Photo input & preview
    if (photoInput) {
        photoInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handlePhotoFile(e.target.files[0]);
            }
        });
    }

    if (btnRemovePhoto) {
        btnRemovePhoto.addEventListener('click', (e) => {
            e.stopPropagation();
            state.uploadedPhotoFile = null;
            photoInput.value = '';
            if (dropzonePreview) dropzonePreview.style.display = 'none';
        });
    }

    // Drag & Drop on prompt card
    if (dropzone) {
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = 'rgba(139, 92, 246, 0.7)';
        });
        dropzone.addEventListener('dragleave', () => {
            dropzone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        });
        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handlePhotoFile(e.dataTransfer.files[0]);
            }
        });
    }

    async function handlePhotoFile(file) {
        state.uploadedPhotoFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImg) previewImg.src = e.target.result;
            if (dropzonePreview) dropzonePreview.style.display = 'inline-flex';
        };
        reader.readAsDataURL(file);

        window.showToast("📷 Gemini Vision이 냉장고 사진 속 식재료를 분석 중입니다...");
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('/api/v1/ingredients/extract', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.ingredients && data.ingredients.length > 0) {
                data.ingredients.forEach(ing => {
                    if (!state.ingredients.some(existing => existing.name === ing.name)) {
                        state.ingredients.push(ing);
                    }
                });
                renderTags();
                window.showToast(`✨ ${data.raw_summary}`);
            }
        } catch (err) {
            console.error("Vision extract error:", err);
            window.showToast("사진 분석 중 오류가 발생했습니다. 자연어로 요리를 요청해보세요!");
        }
    }

    // ----------------------------------------------------
    // Step 1 ➡️ Step 2: Natural Language Intent Discovery
    // ----------------------------------------------------
    if (btnFindRecipes) {
        btnFindRecipes.addEventListener('click', async () => {
            const query = textIngredientInput ? textIngredientInput.value.trim() : '';
            const hasIngredients = state.ingredients.length > 0;

            if (!query && !hasIngredients) {
                window.showToast("만들고 싶은 요리나 식재료를 입력해 주세요 (예: 비 오는 날 얼큰한 국물)");
                if (textIngredientInput) textIngredientInput.focus();
                return;
            }

            btnFindRecipes.disabled = true;
            btnFindRecipes.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i>`;

            const contextIngs = state.ingredients.map(i => i.name);

            try {
                let candidates = [];
                if (query) {
                    window.showToast("🧠 AI가 사용자의 요리 의도와 취향을 분석하고 있습니다...");
                    const res = await fetch('/api/v1/recipes/discover', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            query: query,
                            context_ingredients: contextIngs
                        })
                    });
                    candidates = await res.json();
                } else {
                    const res = await fetch('/api/v1/recipes/recommend', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ ingredients: contextIngs })
                    });
                    candidates = await res.json();
                }

                state.candidateRecipes = candidates;
                renderRecipeCards(candidates, query);
                goToStep(2);
            } catch (err) {
                console.error("Discovery error:", err);
                window.showToast("레시피 분석 중 오류가 발생했습니다.");
            } finally {
                btnFindRecipes.disabled = false;
                btnFindRecipes.innerHTML = `<i class="fa-solid fa-arrow-up"></i>`;
            }
        });
    }

    if (btnBackToInput) {
        btnBackToInput.addEventListener('click', () => {
            goToStep(1);
        });
    }

    // ----------------------------------------------------
    // Render Recipe Cards (Stitch Style with AI Reasoning)
    // ----------------------------------------------------
    function renderRecipeCards(candidates, userQuery = '') {
        if (!recipeCardsContainer) return;
        recipeCardsContainer.innerHTML = '';

        candidates.forEach((c, idx) => {
            const card = document.createElement('div');
            card.className = 'recipe-card';

            const tagsHtml = c.tags.map(t => `<span style="font-size: 0.72rem; color: #A78BFA; background: rgba(139, 92, 246, 0.12); padding: 2px 8px; border-radius: 9999px;">${t}</span>`).join(' ');

            const reasoningHtml = c.ai_reasoning ? `
                <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 10px; padding: 10px 12px; margin-bottom: 1rem; font-size: 0.84rem; color: #DDD6FE; line-height: 1.45;">
                    <div style="display: flex; align-items: center; gap: 6px; font-weight: 600; font-size: 0.76rem; color: #A78BFA; margin-bottom: 3px;">
                        <i class="fa-solid fa-sparkles"></i> AI 맞춤 추천 이유
                    </div>
                    ${c.ai_reasoning}
                </div>
            ` : '';

            card.innerHTML = `
                <div>
                    <div class="recipe-card-header">
                        <div class="recipe-emoji-badge">${c.thumbnail_emoji}</div>
                        <span class="match-gauge-pill">
                            <i class="fa-solid fa-fire"></i> 적합도 ${c.intent_score || c.match_rate}%
                        </span>
                    </div>
                    <h3 class="recipe-title">${c.title}</h3>
                    <p class="recipe-desc">${c.description}</p>
                    
                    ${reasoningHtml}

                    <div class="recipe-meta-row">
                        <span class="recipe-meta-item">
                            <i class="fa-regular fa-clock"></i> ${c.estimated_time_minutes}분 소요
                        </span>
                        <span>•</span>
                        <span class="recipe-meta-item">
                            <i class="fa-solid fa-chart-simple"></i> ${c.difficulty}
                        </span>
                    </div>

                    <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 1.25rem;">
                        ${tagsHtml}
                    </div>

                    <div style="font-size: 0.76rem; color: var(--text-muted); margin-bottom: 1.25rem;">
                        <i class="fa-brands fa-youtube" style="color: #F43F5E; margin-right: 4px;"></i> ${c.source_reference}
                    </div>
                </div>

                <button type="button" class="btn-select-recipe">
                    <span>이 요리로 핸즈프리 조리 시작</span>
                    <i class="fa-solid fa-arrow-right" style="margin-left: 6px;"></i>
                </button>
            `;

            card.querySelector('.btn-select-recipe').addEventListener('click', () => {
                startCookingFlow(c);
            });

            recipeCardsContainer.appendChild(card);
        });
    }

    // ----------------------------------------------------
    // Step 2 ➡️ Step 3: Golden Recipe Synthesis & Audio Prep
    // ----------------------------------------------------
    async function startCookingFlow(candidate) {
        window.showToast(`👨‍🍳 '${candidate.title}' 황금 비율 종합 및 음원 렌더링 중...`);

        try {
            // 1. Synthesize Recipe (Agent 3)
            const ingNames = state.ingredients.map(i => i.name);
            const synthRes = await fetch('/api/v1/recipes/synthesize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    recipe_id: candidate.id,
                    recipe_title: candidate.title,
                    available_ingredients: ingNames
                })
            });
            const recipeData = await synthRes.json();
            state.currentRecipe = recipeData;

            // Render Hero meta & ingredients & ratios
            renderCookingMeta(candidate, recipeData);

            // 2. Generate Audio (Agent 4 & 5)
            const audioRes = await fetch('/api/v1/audio/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    recipe_id: recipeData.id,
                    dish_title: recipeData.title,
                    steps: recipeData.steps
                })
            });
            const audioData = await audioRes.json();
            state.currentAudioData = audioData;

            // 3. Load into Audio Player
            window.audioPlayer.loadRecipe(recipeData, audioData);
            goToStep(3);

            window.showToast("🎧 오디오 가이드가 준비되었습니다! 첫 번째 단계를 들으며 따라해 보세요.");
        } catch (err) {
            console.error("Cooking flow setup failed:", err);
            window.showToast("오디오 가이드 준비 중 오류가 발생했습니다.");
        }
    }

    if (btnBackToRecipes) {
        btnBackToRecipes.addEventListener('click', () => {
            window.audioPlayer.pauseAudio();
            window.audioPlayer.stopTimer();
            goToStep(2);
        });
    }

    function renderCookingMeta(candidate, recipe) {
        if (heroEmoji) heroEmoji.textContent = candidate.thumbnail_emoji || '🍳';
        if (heroTitle) heroTitle.textContent = recipe.title;
        if (heroSubtitle) heroSubtitle.textContent = recipe.subtitle;
        if (heroMatchRate) heroMatchRate.textContent = `${recipe.match_percentage}%`;
        if (heroTotalTime) heroTotalTime.textContent = `${recipe.prep_time_min + recipe.cook_time_min}분`;
        if (heroServings) heroServings.textContent = recipe.servings || '1~2인분';

        // Required Ingredients with Substitutes
        if (requiredIngList) {
            requiredIngList.innerHTML = '';
            (recipe.required_ingredients || []).forEach(ing => {
                const li = document.createElement('li');
                li.className = 'spec-list-item';
                const subText = ing.substitute_hint ? `<span style="font-size: 0.72rem; color: #F59E0B; display: block;">(${ing.substitute_hint})</span>` : '';
                li.innerHTML = `
                    <div>
                        <span>${ing.name}</span>
                        ${subText}
                    </div>
                    <span>${ing.amount}</span>
                `;
                requiredIngList.appendChild(li);
            });
        }

        // Seasoning Ratios
        if (seasoningRatioList) {
            seasoningRatioList.innerHTML = '';
            (recipe.seasoning_ratios || []).forEach(s => {
                const li = document.createElement('li');
                li.className = 'spec-list-item';
                li.innerHTML = `
                    <div>
                        <span>${s.name}</span>
                        ${s.tip ? `<span style="font-size: 0.72rem; color: #94A3B8; display: block;">${s.tip}</span>` : ''}
                    </div>
                    <span style="color: var(--neon-blue);">${s.ratio}</span>
                `;
                seasoningRatioList.appendChild(li);
            });
        }

        // Chef Secrets
        if (chefSecretList) {
            chefSecretList.innerHTML = '';
            (recipe.chef_secrets || []).forEach((tip) => {
                const li = document.createElement('li');
                li.style.padding = '0.35rem 0';
                li.style.borderBottom = '1px solid rgba(255, 255, 255, 0.04)';
                li.innerHTML = `<i class="fa-solid fa-check" style="color: var(--neon-emerald); margin-right: 6px;"></i> ${tip}`;
                chefSecretList.appendChild(li);
            });
        }
    }

    // Initialize Default Tags (Empty by default for natural prompt first experience)
    renderTags();
});

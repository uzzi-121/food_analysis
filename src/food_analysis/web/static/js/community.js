/**
 * CookCast AI - Community & Cooking Know-How Manager
 * Gated by Recipe Completion + Google Sign-In with Best Know-How Curation.
 */

class CommunityManager {
    constructor() {
        this.currentRecipeId = 'spicy-braised-tofu';
        this.comments = [];
        this.completedRecipes = new Set();

        this.init();
    }

    init() {
        // Load completed recipes from localStorage
        try {
            const saved = localStorage.getItem('cookcast_completed_recipes');
            if (saved) {
                const list = JSON.parse(saved);
                this.completedRecipes = new Set(list);
            }
        } catch (e) {
            this.completedRecipes = new Set();
        }

        // Listen to auth state changes to update comment input box state
        if (window.authManager) {
            window.authManager.onAuthStateChanged(() => {
                this.updateCommentFormState();
            });
        }
    }

    setCurrentRecipe(recipeId) {
        if (!recipeId) return;
        this.currentRecipeId = recipeId;
        this.loadComments(recipeId);
        this.updateCommentFormState();
    }

    markRecipeCompleted(recipeId) {
        const targetId = recipeId || this.currentRecipeId;
        this.completedRecipes.add(targetId);
        try {
            localStorage.setItem('cookcast_completed_recipes', JSON.stringify(Array.from(this.completedRecipes)));
        } catch (e) {
            console.error("Failed to save completed recipes:", e);
        }

        this.updateCommentFormState();

        // Reveal and scroll to Community Section
        const communitySection = document.getElementById('sectionCommunity');
        if (communitySection) {
            communitySection.style.display = 'block';
            communitySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        const banner = document.getElementById('completionCelebrationBanner');
        if (banner) {
            banner.style.display = 'flex';
            banner.classList.add('pulse-celebrate');
        }
    }

    isRecipeCompleted(recipeId) {
        const targetId = recipeId || this.currentRecipeId;
        return this.completedRecipes.has(targetId);
    }

    async loadComments(recipeId) {
        const targetId = recipeId || this.currentRecipeId;
        const container = document.getElementById('communityCommentsList');
        if (!container) return;

        container.innerHTML = `
            <div class="community-loading-spinner">
                <i class="fa-solid fa-circle-notch fa-spin"></i>
                <span>실시간 조리 꿀팁과 후기를 불러오는 중...</span>
            </div>
        `;

        try {
            const user = window.authManager ? window.authManager.getCurrentUser() : null;
            const url = `/api/v1/community/recipes/${encodeURIComponent(targetId)}/comments` +
                        (user ? `?current_user_id=${encodeURIComponent(user.uid)}` : '');

            const res = await fetch(url);
            if (!res.ok) throw new Error("댓글 불러오기 실패");

            this.comments = await res.json();
            this.renderComments(this.comments);
        } catch (err) {
            console.error("Error loading comments:", err);
            container.innerHTML = `
                <div class="community-empty-box">
                    <p style="color: var(--text-muted);">댓글을 불러오는 중 문제가 발생했습니다.</p>
                </div>
            `;
        }
    }

    renderComments(comments) {
        const knowhowSpotlight = document.getElementById('knowhowSpotlightCard');
        const commentsList = document.getElementById('communityCommentsList');
        const commentsCountText = document.getElementById('communityCommentsCount');

        if (commentsCountText) {
            commentsCountText.textContent = `${comments.length}개의 후기 및 노하우`;
        }

        if (!comments || comments.length === 0) {
            if (knowhowSpotlight) knowhowSpotlight.style.display = 'none';
            if (commentsList) {
                commentsList.innerHTML = `
                    <div class="community-empty-box">
                        <i class="fa-regular fa-comment-dots" style="font-size: 2.5rem; color: var(--text-muted); margin-bottom: 0.8rem;"></i>
                        <p style="font-size: 0.95rem; color: var(--text-secondary); margin-bottom: 0.3rem;">아직 등록된 후기가 없습니다.</p>
                        <span style="font-size: 0.82rem; color: var(--text-muted);">요리를 완료하고 첫 번째 조리 꿀팁을 남겨보세요!</span>
                    </div>
                `;
            }
            return;
        }

        // 1. Highlight Top Best Know-How Card
        const topKnowHow = comments.find(c => c.is_knowhow) || (comments[0].upvotes >= 3 ? comments[0] : null);
        if (topKnowHow && knowhowSpotlight) {
            knowhowSpotlight.style.display = 'block';
            knowhowSpotlight.innerHTML = `
                <div class="knowhow-badge-row">
                    <span class="knowhow-crown-pill">
                        <i class="fa-solid fa-crown" style="color: #F59E0B;"></i> 👑 베스트 조리 노하우 (Best Know-How)
                    </span>
                    <span class="knowhow-rank-sub">가장 많은 추천을 받은 검증된 실전 팁</span>
                </div>
                <div class="knowhow-content-row">
                    <div class="knowhow-author-info">
                        <img src="${topKnowHow.user_photo_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80'}" alt="${topKnowHow.user_name}" class="knowhow-avatar">
                        <div>
                            <span class="knowhow-author-name">${topKnowHow.user_name}</span>
                            <span class="knowhow-date">${topKnowHow.created_at}</span>
                        </div>
                    </div>
                    <p class="knowhow-body-text">${this.escapeHtml(topKnowHow.content)}</p>
                    <div class="knowhow-footer-row">
                        <div class="knowhow-vote-actions">
                            <button type="button" class="btn-vote-chip btn-vote-up ${this.isUserVoted(topKnowHow, 'up') ? 'active' : ''}" onclick="window.communityManager.vote('${topKnowHow.comment_id}', 'up')">
                                <i class="fa-solid fa-thumbs-up"></i> 추천 <strong>${topKnowHow.upvotes}</strong>
                            </button>
                            <button type="button" class="btn-vote-chip btn-vote-down ${this.isUserVoted(topKnowHow, 'down') ? 'active' : ''}" onclick="window.communityManager.vote('${topKnowHow.comment_id}', 'down')">
                                <i class="fa-solid fa-thumbs-down"></i> 비추천 <strong>${topKnowHow.downvotes}</strong>
                            </button>
                        </div>
                        <span class="knowhow-verified-stamp">
                            <i class="fa-solid fa-circle-check" style="color: var(--neon-emerald);"></i> 조리 완료 인증됨
                        </span>
                    </div>
                </div>
            `;
        } else if (knowhowSpotlight) {
            knowhowSpotlight.style.display = 'none';
        }

        // 2. Render List of Comments
        if (commentsList) {
            commentsList.innerHTML = comments.map(c => `
                <div class="comment-card ${c.is_knowhow ? 'is-knowhow-card' : ''}" id="comment-${c.comment_id}">
                    <div class="comment-header">
                        <div class="comment-user">
                            <img src="${c.user_photo_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80'}" alt="${c.user_name}" class="comment-avatar">
                            <div>
                                <div class="comment-user-title-row">
                                    <span class="comment-username">${c.user_name}</span>
                                    ${c.is_knowhow ? '<span class="mini-knowhow-tag"><i class="fa-solid fa-crown"></i> 노하우</span>' : ''}
                                    <span class="comment-badge-completed"><i class="fa-solid fa-check"></i> 요리 완료</span>
                                </div>
                                <span class="comment-time">${c.created_at}</span>
                            </div>
                        </div>
                    </div>
                    <div class="comment-body">
                        ${this.escapeHtml(c.content)}
                    </div>
                    <div class="comment-footer">
                        <div class="comment-vote-group">
                            <button type="button" class="btn-vote-btn btn-up ${this.isUserVoted(c, 'up') ? 'active' : ''}" title="이 꿀팁 추천하기" onclick="window.communityManager.vote('${c.comment_id}', 'up')">
                                <i class="fa-solid fa-thumbs-up"></i>
                                <span>${c.upvotes}</span>
                            </button>
                            <button type="button" class="btn-vote-btn btn-down ${this.isUserVoted(c, 'down') ? 'active' : ''}" title="비추천하기" onclick="window.communityManager.vote('${c.comment_id}', 'down')">
                                <i class="fa-solid fa-thumbs-down"></i>
                                <span>${c.downvotes}</span>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    }

    isUserVoted(comment, type) {
        const user = window.authManager ? window.authManager.getCurrentUser() : null;
        if (!user || !comment.voters) return false;
        return comment.voters[user.uid] === type;
    }

    updateCommentFormState() {
        const user = window.authManager ? window.authManager.getCurrentUser() : null;
        const isCompleted = this.isRecipeCompleted(this.currentRecipeId);

        const formArea = document.getElementById('communityFormWrapper');
        const loginPrompt = document.getElementById('communityLoginPrompt');
        const completePrompt = document.getElementById('communityCompletePrompt');
        const formActive = document.getElementById('communityInputForm');

        if (!formArea) return;

        if (!user) {
            // Unauthenticated Guest: Prompt to log in
            if (loginPrompt) loginPrompt.style.display = 'flex';
            if (completePrompt) completePrompt.style.display = 'none';
            if (formActive) formActive.style.display = 'none';
        } else if (!isCompleted) {
            // Logged in but not yet completed recipe: prompt to finish cooking
            if (loginPrompt) loginPrompt.style.display = 'none';
            if (completePrompt) completePrompt.style.display = 'flex';
            if (formActive) formActive.style.display = 'none';
        } else {
            // Fully verified (Logged in + Completed)
            if (loginPrompt) loginPrompt.style.display = 'none';
            if (completePrompt) completePrompt.style.display = 'none';
            if (formActive) formActive.style.display = 'block';

            const userBadge = document.getElementById('commentWriterBadge');
            if (userBadge) {
                userBadge.innerHTML = `
                    <img src="${user.photoURL}" class="writer-avatar">
                    <span><strong>${user.displayName}</strong>님, 직접 요리해보신 나만의 꿀팁을 공유해주세요!</span>
                `;
            }
        }
    }

    async submitComment() {
        const user = window.authManager ? window.authManager.getCurrentUser() : null;
        if (!user) {
            if (window.authManager) {
                await window.authManager.loginWithGoogle();
            }
            return;
        }

        if (!this.isRecipeCompleted(this.currentRecipeId)) {
            if (window.showToast) {
                window.showToast("💡 레시피 조리 마지막 단계(🎉 요리 완성!)까지 마친 후 후기를 남겨주세요!");
            }
            return;
        }

        const inputEl = document.getElementById('commentTextInput');
        if (!inputEl) return;

        const content = inputEl.value.trim();
        if (!content || content.length < 3) {
            if (window.showToast) window.showToast("댓글 내용을 3자 이상 작성해주세요.");
            inputEl.focus();
            return;
        }

        const btnSubmit = document.getElementById('btnSubmitComment');
        if (btnSubmit) {
            btnSubmit.disabled = true;
            btnSubmit.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> 등록 중...';
        }

        try {
            const res = await fetch(`/api/v1/community/recipes/${encodeURIComponent(this.currentRecipeId)}/comments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    recipe_id: this.currentRecipeId,
                    user_id: user.uid,
                    user_name: user.displayName,
                    user_photo_url: user.photoURL,
                    content: content,
                    completed: true
                })
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "댓글 등록 실패");
            }

            inputEl.value = '';
            if (window.showToast) window.showToast("🎉 나만의 조리 꿀팁과 후기가 성공적으로 등록되었습니다!");
            await this.loadComments(this.currentRecipeId);
        } catch (err) {
            console.error("Error submitting comment:", err);
            if (window.showToast) window.showToast(`오류: ${err.message}`);
        } finally {
            if (btnSubmit) {
                btnSubmit.disabled = false;
                btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> 꿀팁 댓글 등록';
            }
        }
    }

    async vote(commentId, voteType) {
        const user = window.authManager ? window.authManager.getCurrentUser() : null;
        if (!user) {
            if (confirm("💡 추천/비추천 투표는 구글 로그인 후 이용하실 수 있습니다.\n지금 로그인하시겠습니까?")) {
                if (window.authManager) {
                    await window.authManager.loginWithGoogle();
                }
            }
            return;
        }

        try {
            const res = await fetch(`/api/v1/community/comments/${encodeURIComponent(commentId)}/vote`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: user.uid,
                    vote_type: voteType
                })
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "투표 실패");
            }

            const updatedComment = await res.json();
            // Reload all comments to reflect ranking and know-how promotion
            await this.loadComments(this.currentRecipeId);

            if (window.showToast) {
                if (voteType === 'up') window.showToast("👍 추천이 반영되었습니다!");
                else window.showToast("👎 비추천이 반영되었습니다.");
            }
        } catch (err) {
            console.error("Error voting:", err);
            if (window.showToast) window.showToast(`오류: ${err.message}`);
        }
    }

    escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
}

// Global instance
window.communityManager = new CommunityManager();

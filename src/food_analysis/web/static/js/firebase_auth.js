/**
 * CookCast AI - Firebase Authentication & Profile Manager
 * Handles Google Sign-In with Account Selection and Community Anonymity Profile Editor.
 */

class FirebaseAuthManager {
    constructor() {
        this.currentUser = null;
        this.isFirebaseReady = false;
        this.authInstance = null;
        this.listeners = [];

        // 8 Chef & Culinary Avatar Presets for Community Anonymity
        this.chefAvatars = [
            { id: 'chef-1', name: '마스터 셰프', url: 'https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-2', name: '불맛 장인', url: 'https://images.unsplash.com/photo-1583394293214-28ded15ee548?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-3', name: '자취요리왕', url: 'https://images.unsplash.com/photo-1556911073-38141963c9e0?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-4', name: '뚝배기 장인', url: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-5', name: '황금칼 손질왕', url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-6', name: '면 요리 달인', url: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-7', name: '신선 미식가', url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=120&auto=format&fit=crop&q=80' },
            { id: 'chef-8', name: '달콤 파티시에', url: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=120&auto=format&fit=crop&q=80' }
        ];

        this.init();
    }

    async init() {
        try {
            // Check local cache for persisted user session
            const cachedUser = localStorage.getItem('cookcast_user');
            if (cachedUser) {
                try {
                    this.currentUser = JSON.parse(cachedUser);
                } catch (e) {
                    this.currentUser = null;
                }
            }

            // Fetch Firebase config from backend
            const res = await fetch('/api/v1/community/auth/config');
            if (res.ok) {
                const config = await res.json();
                if (config.is_configured && window.firebase) {
                    if (!window.firebase.apps.length) {
                        window.firebase.initializeApp({
                            apiKey: config.api_key,
                            authDomain: config.auth_domain,
                            projectId: config.project_id,
                            storageBucket: config.storage_bucket,
                            messagingSenderId: config.messaging_sender_id,
                            appId: config.app_id
                        });
                    }
                    this.authInstance = window.firebase.auth();
                    this.isFirebaseReady = true;

                    // Listen to live auth changes
                    this.authInstance.onAuthStateChanged((user) => {
                        if (user) {
                            // Check if user already set an anonymous profile
                            const existing = this.currentUser || {};
                            this.currentUser = {
                                uid: user.uid,
                                displayName: existing.displayName || user.displayName || '15분요리사',
                                email: user.email || '',
                                photoURL: existing.photoURL || user.photoURL || this.chefAvatars[0].url,
                                is_anonymous: existing.is_anonymous || false,
                                is_demo: false
                            };
                            localStorage.setItem('cookcast_user', JSON.stringify(this.currentUser));
                        } else {
                            if (!this.currentUser || !this.currentUser.is_demo) {
                                this.currentUser = null;
                                localStorage.removeItem('cookcast_user');
                            }
                        }
                        this.notifyState();
                    });
                }
            }
        } catch (err) {
            console.warn("Firebase config fallback to local/demo auth mode:", err);
        }

        this.notifyState();
        this.bindModalEvents();
    }

    bindModalEvents() {
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAccountSelectModal();
                this.closeProfileEditModal();
            }
        });

        // Close on clicking backdrop outside modal card
        ['googleAccountSelectModal', 'profileEditModal'].forEach(id => {
            const modal = document.getElementById(id);
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        if (id === 'googleAccountSelectModal') this.closeAccountSelectModal();
                        if (id === 'profileEditModal') this.closeProfileEditModal();
                    }
                });
            }
        });
    }

    onAuthStateChanged(callback) {
        if (typeof callback === 'function') {
            this.listeners.push(callback);
            callback(this.currentUser);
        }
    }

    notifyState() {
        this.renderNavbarUI();
        this.listeners.forEach(cb => {
            try { cb(this.currentUser); } catch (e) { console.error(e); }
        });
    }

    getCurrentUser() {
        return this.currentUser;
    }

    // Opens Google Account Selection Dialog
    openAccountSelectModal() {
        const modal = document.getElementById('googleAccountSelectModal');
        if (modal) {
            modal.classList.add('active');
            modal.style.display = 'flex';
        } else {
            // If modal not found, fallback to direct login
            this.loginWithAccount('yeongsik0914', 'fkdlemgoej@gmail.com');
        }
    }

    closeAccountSelectModal() {
        const modal = document.getElementById('googleAccountSelectModal');
        if (modal) {
            modal.classList.remove('active');
            modal.style.display = 'none';
        }
    }

    // Login with selected Google Account
    async loginWithAccount(accountName, accountEmail) {
        this.closeAccountSelectModal();

        if (this.isFirebaseReady && this.authInstance) {
            try {
                const provider = new window.firebase.auth.GoogleAuthProvider();
                provider.setCustomParameters({ prompt: 'select_account' });
                const result = await this.authInstance.signInWithPopup(provider);
                const user = result.user;
                this.currentUser = {
                    uid: user.uid,
                    displayName: user.displayName || accountName || '15분요리사',
                    email: user.email || accountEmail || '',
                    photoURL: user.photoURL || this.chefAvatars[0].url,
                    is_anonymous: false,
                    is_demo: false
                };
                localStorage.setItem('cookcast_user', JSON.stringify(this.currentUser));
                this.notifyState();
                if (window.showToast) window.showToast(`✨ ${this.currentUser.displayName}님 환영합니다!`);
                return this.currentUser;
            } catch (err) {
                console.error("Firebase Google Sign-In error:", err);
                if (window.showToast) window.showToast("구글 로그인 취소 또는 오류 발생");
            }
        }

        // Demo / Quick Google Account Simulation
        const uid = "google-uid-" + (accountEmail.split('@')[0] || "user123");
        this.currentUser = {
            uid: uid,
            displayName: accountName || 'yeongsik0914',
            email: accountEmail || 'fkdlemgoej@gmail.com',
            photoURL: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=120&auto=format&fit=crop&q=80',
            is_anonymous: false,
            is_demo: true
        };
        localStorage.setItem('cookcast_user', JSON.stringify(this.currentUser));
        this.notifyState();
        if (window.showToast) {
            window.showToast(`✨ Google 계정(${this.currentUser.email})으로 로그인되었습니다!`);
        }
        return this.currentUser;
    }

    // Update Profile (Anonymous Nickname & Chef Avatar)
    updateProfile(newNickname, newPhotoUrl, isAnonymous = true) {
        if (!this.currentUser) return;

        const trimmed = (newNickname || '').trim();
        if (!trimmed) {
            if (window.showToast) window.showToast("닉네임을 한 글자 이상 입력해주세요.");
            return false;
        }

        this.currentUser.displayName = trimmed;
        if (newPhotoUrl) {
            this.currentUser.photoURL = newPhotoUrl;
        }
        this.currentUser.is_anonymous = isAnonymous;

        localStorage.setItem('cookcast_user', JSON.stringify(this.currentUser));
        this.notifyState();

        if (window.showToast) {
            window.showToast(`🎭 익명 프로필이 저장되었습니다: '${this.currentUser.displayName}'`);
        }
        this.closeProfileEditModal();
        return true;
    }

    openProfileEditModal() {
        if (!this.currentUser) {
            this.openAccountSelectModal();
            return;
        }

        const modal = document.getElementById('profileEditModal');
        const inputNick = document.getElementById('profileNicknameInput');
        const currentAvatar = document.getElementById('profilePreviewAvatar');
        const currentEmail = document.getElementById('profileAccountEmail');

        if (inputNick) inputNick.value = this.currentUser.displayName || '';
        if (currentAvatar) currentAvatar.src = this.currentUser.photoURL || this.chefAvatars[0].url;
        if (currentEmail) currentEmail.textContent = this.currentUser.email || 'Google 연동 계정';

        this.renderChefAvatarPicker();

        if (modal) {
            modal.classList.add('active');
            modal.style.display = 'flex';
        }
    }

    closeProfileEditModal() {
        const modal = document.getElementById('profileEditModal');
        if (modal) {
            modal.classList.remove('active');
            modal.style.display = 'none';
        }
    }

    renderChefAvatarPicker() {
        const container = document.getElementById('chefAvatarGrid');
        if (!container) return;

        const currentUrl = this.currentUser ? this.currentUser.photoURL : '';
        container.innerHTML = this.chefAvatars.map(av => `
            <div class="chef-avatar-option ${av.url === currentUrl ? 'selected' : ''}" onclick="window.authManager.selectChefAvatar('${av.url}')" title="${av.name}">
                <img src="${av.url}" alt="${av.name}" class="chef-avatar-thumb">
                <span class="chef-avatar-label">${av.name}</span>
            </div>
        `).join('');
    }

    selectChefAvatar(url) {
        const preview = document.getElementById('profilePreviewAvatar');
        if (preview) preview.src = url;

        document.querySelectorAll('.chef-avatar-option').forEach(el => {
            const img = el.querySelector('img');
            if (img && img.src === url) {
                el.classList.add('selected');
            } else {
                el.classList.remove('selected');
            }
        });
    }

    logout() {
        if (this.isFirebaseReady && this.authInstance) {
            this.authInstance.signOut();
        }
        this.currentUser = null;
        localStorage.removeItem('cookcast_user');
        this.notifyState();
        if (window.showToast) window.showToast("👋 로그아웃되었습니다.");
    }

    renderNavbarUI() {
        const btnLogin = document.getElementById('btnNavGoogleLogin');
        const userProfile = document.getElementById('navUserProfile');
        const userAvatar = document.getElementById('navUserAvatar');
        const userName = document.getElementById('navUserName');

        if (!btnLogin || !userProfile) return;

        if (this.currentUser) {
            btnLogin.style.display = 'none';
            userProfile.style.display = 'inline-flex';
            if (userName) userName.textContent = this.currentUser.displayName || '요리사';
            if (userAvatar) {
                userAvatar.src = this.currentUser.photoURL || this.chefAvatars[0].url;
            }
        } else {
            btnLogin.style.display = 'inline-flex';
            userProfile.style.display = 'none';
        }
    }
}

// Global instance
window.authManager = new FirebaseAuthManager();

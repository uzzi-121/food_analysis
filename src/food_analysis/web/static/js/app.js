/**
 * 키친 셰프 (Kitchen Chef) — 냉장고 파먹기 & 실시간 재고 자동 소진
 * Multi-Screen Navigation, Shelf Inventory Management, 3D Refrigerator Animation,
 * Handcrafted Wooden Recipes, Kitchen Smart Timer, and Real-Time Inventory Deduction.
 */

// Global App State
const KitchenChefState = {
    currentScreen: 1,
    inventory: [],
    selectedTheme: 'korean-stew',
    selectedRecipe: null,
    timerInterval: null,
    timerSecondsLeft: 120,
    timerTotalSeconds: 120,
    isTimerRunning: false,
    selectedReviewRating: 5,
    userReviewPhoto: null
};

// Default Pantry Inventory across 4 Shelves
const DEFAULT_INVENTORY = [
    // Shelf 1: 신선 채소·과일 (veg)
    { id: 'ing-scallion', name: '대파', qty: 3, unit: '대', shelf: 'veg', freshness: 'high', selected: true, thumb: 'https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-onion', name: '양파', qty: 2, unit: '개', shelf: 'veg', freshness: 'high', selected: true, thumb: 'https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-chili', name: '청양고추', qty: 4, unit: '개', shelf: 'veg', freshness: 'mid', selected: true, thumb: 'https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-garlic', name: '마늘', qty: 10, unit: '쪽', shelf: 'veg', freshness: 'high', selected: false, thumb: 'https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?w=100&auto=format&fit=crop&q=80' },
    
    // Shelf 2: 육류·해산물·햄 (meat)
    { id: 'ing-spam', name: '스팸', qty: 2, unit: '캔', shelf: 'meat', freshness: 'high', selected: true, thumb: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-pork', name: '삼겹살', qty: 250, unit: 'g', shelf: 'meat', freshness: 'mid', selected: false, thumb: 'https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-chicken', name: '닭가슴살', qty: 2, unit: '팩', shelf: 'meat', freshness: 'high', selected: false, thumb: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=100&auto=format&fit=crop&q=80' },

    // Shelf 3: 유제품·달걀·두부 (dairy)
    { id: 'ing-egg', name: '신선란', qty: 6, unit: '알', shelf: 'dairy', freshness: 'high', selected: true, thumb: 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-tofu', name: '두부', qty: 1, unit: '모', shelf: 'dairy', freshness: 'mid', selected: true, thumb: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-cheese', name: '모짜렐라치즈', qty: 1, unit: '봉', shelf: 'dairy', freshness: 'high', selected: false, thumb: 'https://images.unsplash.com/photo-1552767059-ce182ead6c1b?w=100&auto=format&fit=crop&q=80' },

    // Shelf 4: 양념·소스&즉석가공 (sauce)
    { id: 'ing-oyster-sauce', name: '굴소스', qty: 1, unit: '병', shelf: 'sauce', freshness: 'high', selected: true, thumb: 'https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-rice', name: '즉석밥', qty: 3, unit: '공기', shelf: 'sauce', freshness: 'high', selected: true, thumb: 'https://images.unsplash.com/photo-1516684732162-798a0062be99?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-soy-sauce', name: '진간장', qty: 1, unit: '병', shelf: 'sauce', freshness: 'high', selected: false, thumb: 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&auto=format&fit=crop&q=80' },
    { id: 'ing-sesame-oil', name: '참기름', qty: 1, unit: '병', shelf: 'sauce', freshness: 'high', selected: false, thumb: 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=100&auto=format&fit=crop&q=80' }
];

// Handcrafted 6 Wooden Recipes Catalog
const RECIPES_CATALOG = {
    'golden-egg-fried-rice': {
        id: 'golden-egg-fried-rice',
        title: '황금 대파 계란 볶음밥',
        woodType: 'MAPLE WOOD 도마',
        badge: '100% 잔여 일치',
        time: '12분',
        difficulty: '초급',
        calories: '480 kcal',
        desc: '식용유에 우려낸 은은한 파기름과 촉촉한 에그 스크램블, 굴소스 한 스푼으로 완성하는 고슬고슬한 셰프급 한 그릇 요리.',
        image: 'https://images.unsplash.com/photo-1516684732162-798a0062be99?w=900&auto=format&fit=crop&q=80',
        deductions: [
            { id: 'ing-scallion', name: '대파', amount: 1, unit: '대' },
            { id: 'ing-egg', name: '신선란', amount: 2, unit: '알' },
            { id: 'ing-rice', name: '즉석밥', amount: 1, unit: '공기' }
        ],
        prepList: [
            { name: '대파 1대', guide: '송송 얇게 썰어 도마 우측에 준비' },
            { name: '신선란 2알', guide: '작은 볼에 곱게 풀어두기' },
            { name: '즉석밥 1공기 (또는 찬밥)', guide: '데우지 않고 고슬한 상태 권장' },
            { name: '프리미엄 굴소스 1T', guide: '간장 0.5T로 대체 가능' },
            { name: '참기름 1T & 통깨 약간', guide: '마무리 풍미용 조미' }
        ],
        steps: [
            {
                step: 1,
                title: '향긋한 파기름 내기',
                flame: '약불 • 약 2분',
                seconds: 120,
                desc: '달구지 않은 팬에 식용유 2T를 두르고, 도마에서 송송 썰어둔 대파 1대를 넣습니다. 불을 약불로 켜고 천천히 볶아 향긋한 파기름을 충분히 냅니다.'
            },
            {
                step: 2,
                title: '에그 스크램블 만들기',
                flame: '중불 • 약 1분 30초',
                seconds: 90,
                desc: '노릇해진 대파를 팬 한구석으로 살짝 밀어두고, 빈 공간에 미리 풀어둔 계란 2알을 붓습니다. 젓가락으로 몽글몽글하게 저어가며 80% 정도만 촉촉하게 익힙니다.'
            },
            {
                step: 3,
                title: '밥 투입 & 센 불 볶음',
                flame: '강불 • 약 3분',
                seconds: 180,
                desc: '밥 1공기와 굴소스 1T를 넣습니다. 주걱 날을 세워 밥알을 쪼개듯 가르며 파, 계란과 섞어 센 불에서 수분을 날리며 고슬고슬하게 볶아냅니다.'
            },
            {
                step: 4,
                title: '참기름 피니시 & 플레이팅',
                flame: '예열 잔열 • 30초',
                seconds: 30,
                desc: '불을 끄고 팬의 남은 잔열 상태에서 참기름 1T를 빙 두르고 가볍게 섞어줍니다. 그릇에 담은 후 통깨를 톡톡 뿌려 따뜻할 때 바로 대접합니다.'
            }
        ]
    },
    'spam-kimchi-stew': {
        id: 'spam-kimchi-stew',
        title: '스팸 김치 짜글이 찌개',
        woodType: 'OAK WOOD 도마',
        badge: '98% 잔여 일치',
        time: '20분',
        difficulty: '초급',
        calories: '520 kcal',
        desc: '진한 묵은지와 짭조름한 스팸을 으깨어 넣어 밥도둑 국물 맛을 완성하는 실패 없는 한국인의 소울푸드 찌개.',
        image: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=900&auto=format&fit=crop&q=80',
        deductions: [
            { id: 'ing-spam', name: '스팸', amount: 1, unit: '캔' },
            { id: 'ing-scallion', name: '대파', amount: 1, unit: '대' },
            { id: 'ing-onion', name: '양파', amount: 1, unit: '개' }
        ],
        prepList: [
            { name: '스팸 1캔', guide: '비닐백에 넣어 굵게 으깨기' },
            { name: '대파 1대 & 양파 1개', guide: '어슷썰기와 채썰기' },
            { name: '김치 1공기', guide: '가위로 한입 크기로 썰기' },
            { name: '고춧가루 1T & 다진마늘 1T', guide: '양념 배합 준비' }
        ],
        steps: [
            {
                step: 1,
                title: '스팸 으깨어 볶기',
                flame: '중불 • 약 2분',
                seconds: 120,
                desc: '냄비에 식용유 없이 으깬 스팸을 볶아 자체 기름과 고소한 풍미를 끌어냅니다.'
            },
            {
                step: 2,
                title: '김치와 양파 볶기',
                flame: '중불 • 약 3분',
                seconds: 180,
                desc: '스팸 기름에 썰어둔 김치와 양파를 넣고 투명해질 때까지 달달 볶아줍니다.'
            },
            {
                step: 3,
                title: '물 붓고 자작하게 끓이기',
                flame: '강불 ➡️ 중불 • 10분',
                seconds: 600,
                desc: '물 400ml와 고춧가루, 진간장을 넣고 보글보글 깊은 맛이 우러나도록 끓입니다.'
            },
            {
                step: 4,
                title: '대파 투하 및 마무리',
                flame: '약불 • 2분',
                seconds: 120,
                desc: '송송 썬 대파와 청양고추를 얹어 한소끔 더 끓여내면 완성됩니다.'
            }
        ]
    },
    'spam-mayo-rice': {
        id: 'spam-mayo-rice',
        title: '단짠 단백 스팸마요 덮밥',
        woodType: 'WALNUT WOOD 도마',
        badge: '95% 잔여 일치',
        time: '10분',
        difficulty: '초급',
        calories: '510 kcal',
        desc: '노릇하게 구운 깍둑 스팸과 부드러운 스크램블 에그, 달콤 짭조름한 양파 간장소스로 만드는 초간단 덮밥.',
        image: 'https://images.unsplash.com/photo-1553163147-622ab57be1c7?w=900&auto=format&fit=crop&q=80',
        deductions: [
            { id: 'ing-spam', name: '스팸', amount: 1, unit: '캔' },
            { id: 'ing-egg', name: '신선란', amount: 2, unit: '알' },
            { id: 'ing-onion', name: '양파', amount: 1, unit: '개' }
        ],
        prepList: [
            { name: '스팸 1/2캔', guide: '작은 주사위 모양으로 깍둑썰기' },
            { name: '달걀 2알', guide: '맛소금 한 꼬집 넣고 풀기' },
            { name: '양파 1/2개', guide: '얇게 채 썰기' },
            { name: '마요네즈 & 김가루', guide: '토핑용 준비' }
        ],
        steps: [
            {
                step: 1,
                title: '깍둑 스팸 바삭하게 굽기',
                flame: '중불 • 3분',
                seconds: 180,
                desc: '기름 없이 팬에 깍둑썬 스팸을 노릇노릇 사방으로 바삭하게 구워 덜어둡니다.'
            },
            {
                step: 2,
                title: '몽글몽글 스크램블',
                flame: '약불 • 1분 30초',
                seconds: 90,
                desc: '달걀물을 부어 부드럽게 몽글몽글 익혀 따뜻한 밥 위에 둥글게 둘러 얹습니다.'
            },
            {
                step: 3,
                title: '간장 양파 소스 조리기',
                flame: '중불 • 2분',
                seconds: 120,
                desc: '팬에 양파 채와 간장 1T, 설탕 0.5T, 물 2T를 넣고 자작하게 조려냅니다.'
            },
            {
                step: 4,
                title: '마요네즈 드리즐 & 완성',
                flame: '조리 완료',
                seconds: 30,
                desc: '밥 위에 양파 소스, 스팸, 김가루를 올리고 마요네즈를 격자로 뿌려 맛있게 비벼 먹습니다.'
            }
        ]
    },
    'spicy-spam-sundubu': {
        id: 'spicy-spam-sundubu',
        title: '얼큰 칼칼 스팸 순두부찌개',
        woodType: 'TEAK WOOD 도마',
        badge: '93% 잔여 일치',
        time: '18분',
        difficulty: '초급',
        calories: '420 kcal',
        desc: '부드러운 두부와 짭짤한 스팸의 고소함이 고추기름 국물에 녹아들어 속이 확 풀리는 해장 뚝배기.',
        image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=900&auto=format&fit=crop&q=80',
        deductions: [
            { id: 'ing-tofu', name: '두부', amount: 1, unit: '모' },
            { id: 'ing-spam', name: '스팸', amount: 1, unit: '캔' },
            { id: 'ing-chili', name: '청양고추', amount: 2, unit: '개' }
        ],
        prepList: [
            { name: '두부 1모', guide: '큼직하게 깍둑썰기' },
            { name: '스팸 1/2캔', guide: '얇게 슬라이스하기' },
            { name: '청양고추 & 대파', guide: '어슷썰기' }
        ],
        steps: [
            {
                step: 1,
                title: '고추기름 파기름 베이스',
                flame: '약불 • 2분',
                seconds: 120,
                desc: '식용유와 참기름을 두르고 대파와 고춧가루를 볶아 진한 붉은 고추기름을 냅니다.'
            },
            {
                step: 2,
                title: '스팸 볶고 물 붓기',
                flame: '중불 • 3분',
                seconds: 180,
                desc: '슬라이스한 스팸을 함께 볶다가 물 350ml를 붓고 센 불로 끓여줍니다.'
            },
            {
                step: 3,
                title: '두부 투하 & 간 맞추기',
                flame: '중불 • 5분',
                seconds: 300,
                desc: '국물이 끓어오르면 큼직한 두부를 넣고 진간장 1T와 굴소스 0.5T로 간을 맞춥니다.'
            },
            {
                step: 4,
                title: '청양고추와 계란 피니시',
                flame: '약불 • 1분',
                seconds: 60,
                desc: '청양고추와 계란 한 알을 톡 깨뜨려 올린 후 불을 끄고 뚝배기 잔열로 익힙니다.'
            }
        ]
    },
    'crispy-cheese-kimchijeon': {
        id: 'crispy-cheese-kimchijeon',
        title: '바삭 쫀득 눈꽃 치즈 김치전',
        woodType: 'BIRCH WOOD 도마',
        badge: '92% 잔여 일치',
        time: '15분',
        difficulty: '초급',
        calories: '450 kcal',
        desc: '얼음물 반죽으로 가장자리는 바삭하게 튀기듯 굽고 고소한 모짜렐라 치즈를 듬뿍 얹어내는 별미 전 요리.',
        image: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=900&auto=format&fit=crop&q=80',
        deductions: [
            { id: 'ing-scallion', name: '대파', amount: 1, unit: '대' },
            { id: 'ing-cheese', name: '모짜렐라치즈', amount: 1, unit: '봉' }
        ],
        prepList: [
            { name: '잘 익은 김치 1컵', guide: '잘게 송송 썰기' },
            { name: '대파 1/2대', guide: '얇게 채썰기' },
            { name: '모짜렐라치즈 1봉', guide: '실온에 준비' }
        ],
        steps: [
            {
                step: 1,
                title: '바삭한 반죽 만들기',
                flame: '사전 준비',
                seconds: 60,
                desc: '부침가루 1컵에 차가운 냉수를 넣고 젓가락으로 멍울만 살살 풀어 바삭함을 살립니다.'
            },
            {
                step: 2,
                title: '센 기름에 얇게 부치기',
                flame: '강불 ➡️ 중불 • 4분',
                seconds: 240,
                desc: '기름을 넉넉히 두르고 반죽을 최대한 얇게 펴서 가장자리가 바삭해지도록 튀기듯 굽습니다.'
            },
            {
                step: 3,
                title: '뒤집고 치즈 얹기',
                flame: '중불 • 3분',
                seconds: 180,
                desc: '바삭하게 뒤집은 후 김치전 윗면에 모짜렐라 치즈를 눈꽃처럼 소복하게 뿌립니다.'
            },
            {
                step: 4,
                title: '뚜껑 덮고 치즈 녹이기',
                flame: '약불 • 2분',
                seconds: 120,
                desc: '뚜껑을 1분간 덮어 치즈를 부드럽게 녹여낸 뒤 접시에 담아 바로 찢어 먹습니다.'
            }
        ]
    },
    'tofu-egg-fry': {
        id: 'tofu-egg-fry',
        title: '담백 고소 들기름 두부 부침',
        woodType: 'HINOKI WOOD 도마',
        badge: '91% 잔여 일치',
        time: '8분',
        difficulty: '초급',
        calories: '310 kcal',
        desc: '들기름에 부쳐 노릇노릇 고소한 두부와 대파 간장 양념장이 어우러진 가볍고 든든한 고단백 밥반찬.',
        image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=900&auto=format&fit=crop&q=80',
        deductions: [
            { id: 'ing-tofu', name: '두부', amount: 1, unit: '모' },
            { id: 'ing-scallion', name: '대파', amount: 1, unit: '대' }
        ],
        prepList: [
            { name: '두부 1모', guide: '키친타월로 물기 제거 후 도톰하게 썰기' },
            { name: '대파 1/2대', guide: '잘게 다져 양념장용 준비' }
        ],
        steps: [
            {
                step: 1,
                title: '두부 수분 잡기',
                flame: '도마 손질 • 1분',
                seconds: 60,
                desc: '도마 위에서 도톰하게 썬 두부에 소금을 살짝 뿌려 여분의 수분을 완벽히 제거합니다.'
            },
            {
                step: 2,
                title: '들기름에 노릇하게 굽기',
                flame: '중약불 • 4분',
                seconds: 240,
                desc: '팬에 들기름을 두르고 두부를 올려 앞뒤가 황금빛이 돌 때까지 천천히 지져냅니다.'
            },
            {
                step: 3,
                title: '특제 대파 간장장 만들기',
                flame: '도마 조리',
                seconds: 60,
                desc: '진간장 2T, 고춧가루 1T, 다진 대파, 통깨, 참기름을 섞어 매콤달큰 양념장을 만듭니다.'
            },
            {
                step: 4,
                title: '플레이팅 & 대접',
                flame: '완성',
                seconds: 30,
                desc: '뜨거운 두부 부침 위에 양념장을 살포시 얹어 완성합니다.'
            }
        ]
    }
};

// ==========================================================================
// 1. INITIALIZATION & STORAGE
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    initInventory();
    renderInventoryUI();
    initThemeSelection();
    initScreenNavigation();
    initInteractiveStarRating();
    initRecipeSelection();
    
    // Default selected recipe is golden egg fried rice
    KitchenChefState.selectedRecipe = RECIPES_CATALOG['golden-egg-fried-rice'];
    populateScreen4Details(KitchenChefState.selectedRecipe);
});

function initInventory() {
    const saved = localStorage.getItem('kitchen_chef_inventory');
    if (saved) {
        try {
            KitchenChefState.inventory = JSON.parse(saved);
        } catch (e) {
            KitchenChefState.inventory = [...DEFAULT_INVENTORY];
        }
    } else {
        KitchenChefState.inventory = [...DEFAULT_INVENTORY];
        saveInventory();
    }
}

function saveInventory() {
    localStorage.setItem('kitchen_chef_inventory', JSON.stringify(KitchenChefState.inventory));
    updateSelectedSummary();
}

// ==========================================================================
// 2. SCREEN NAVIGATION SYSTEM
// ==========================================================================
function initScreenNavigation() {
    // Process Tab Clicks
    for (let i = 1; i <= 5; i++) {
        const tab = document.getElementById(`tabScreen${i}`);
        if (tab) {
            tab.addEventListener('click', () => window.goToScreen(i));
        }
    }
}

window.goToScreen = function(screenNumber) {
    KitchenChefState.currentScreen = screenNumber;

    // Update screen views
    for (let i = 1; i <= 5; i++) {
        const screen = document.getElementById(`screen${i}`);
        const tab = document.getElementById(`tabScreen${i}`);
        if (screen) {
            if (i === screenNumber) {
                screen.classList.add('active');
            } else {
                screen.classList.remove('active');
            }
        }
        if (tab) {
            if (i === screenNumber) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        }
    }

    // Scroll smoothly to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Specific screen logic triggers
    if (screenNumber === 2) {
        runScreen2Animation();
    }
};

// ==========================================================================
// 3. SCREEN 1: INVENTORY & THEMES
// ==========================================================================
function renderInventoryUI() {
    const vegGrid = document.getElementById('shelfGridVeg');
    const meatGrid = document.getElementById('shelfGridMeat');
    const dairyGrid = document.getElementById('shelfGridDairy');
    const sauceGrid = document.getElementById('shelfGridSauce');

    if (!vegGrid) return;

    vegGrid.innerHTML = '';
    meatGrid.innerHTML = '';
    dairyGrid.innerHTML = '';
    sauceGrid.innerHTML = '';

    KitchenChefState.inventory.forEach(item => {
        const card = createIngredientCardElement(item);
        if (item.shelf === 'veg' && vegGrid) vegGrid.appendChild(card);
        else if (item.shelf === 'meat' && meatGrid) meatGrid.appendChild(card);
        else if (item.shelf === 'dairy' && dairyGrid) dairyGrid.appendChild(card);
        else if (item.shelf === 'sauce' && sauceGrid) sauceGrid.appendChild(card);
    });

    updateSelectedSummary();
}

function createIngredientCardElement(item) {
    const card = document.createElement('div');
    card.className = `kc-ing-card ${item.selected ? 'selected' : ''}`;
    card.id = `card-${item.id}`;

    // Freshness color dot
    const freshClass = item.freshness === 'high' ? 'fresh-high' : (item.freshness === 'mid' ? 'fresh-mid' : 'fresh-low');

    card.innerHTML = `
        <div class="ing-card-left" onclick="window.toggleItemSelect('${item.id}')">
            <span class="ing-fresh-dot ${freshClass}" title="신선도"></span>
            <img src="${item.thumb}" alt="${item.name}" class="ing-card-thumb" onerror="this.src='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=80&auto=format&fit=crop&q=80'">
            <div class="ing-card-details">
                <span class="ing-name">${item.name}</span>
                <span class="ing-qty-badge">${item.qty} ${item.unit}</span>
            </div>
        </div>
        <div class="ing-card-right">
            <div class="ing-stepper-wrap" onclick="event.stopPropagation()">
                <button type="button" class="btn-step" onclick="window.updateQuantity('${item.id}', -1)">-</button>
                <span class="step-val" id="qty-${item.id}">${item.qty}</span>
                <button type="button" class="btn-step" onclick="window.updateQuantity('${item.id}', 1)">+</button>
            </div>
            <div class="ing-check-box" onclick="window.toggleItemSelect('${item.id}')">
                <i class="fa-solid fa-check"></i>
            </div>
        </div>
    `;

    return card;
}

window.toggleItemSelect = function(id) {
    const item = KitchenChefState.inventory.find(i => i.id === id);
    if (!item) return;
    item.selected = !item.selected;

    const card = document.getElementById(`card-${id}`);
    if (card) {
        if (item.selected) card.classList.add('selected');
        else card.classList.remove('selected');
    }

    saveInventory();
};

window.updateQuantity = function(id, delta) {
    const item = KitchenChefState.inventory.find(i => i.id === id);
    if (!item) return;

    item.qty = Math.max(0, item.qty + delta);
    const qtySpan = document.getElementById(`qty-${id}`);
    if (qtySpan) qtySpan.textContent = item.qty;

    // If zero, unselect
    if (item.qty === 0 && item.selected) {
        item.selected = false;
        const card = document.getElementById(`card-${id}`);
        if (card) card.classList.remove('selected');
    }

    saveInventory();
};

function updateSelectedSummary() {
    const selectedItems = KitchenChefState.inventory.filter(i => i.selected && i.qty > 0);
    const badge = document.getElementById('badgeSelectedSummary');
    const activeInvCount = document.getElementById('activeInvCount');
    const animSelectedCount = document.getElementById('animSelectedCount');

    if (badge) badge.textContent = `선택된 재료 ${selectedItems.length}개`;
    if (activeInvCount) activeInvCount.textContent = KitchenChefState.inventory.filter(i => i.qty > 0).length;
    if (animSelectedCount) animSelectedCount.textContent = selectedItems.length || 6;
}

window.toggleInventoryMode = function(mode) {
    const btnSample = document.getElementById('btnStateSample');
    const btnEmpty = document.getElementById('btnStateEmpty');

    if (mode === 'sample') {
        KitchenChefState.inventory = [...DEFAULT_INVENTORY];
        if (btnSample) btnSample.classList.add('active');
        if (btnEmpty) btnEmpty.classList.remove('active');
        window.showToast('🧺 기본 냉장고 재고가 충전되었습니다.');
    } else {
        KitchenChefState.inventory.forEach(i => i.qty = 0);
        KitchenChefState.inventory.forEach(i => i.selected = false);
        if (btnSample) btnSample.classList.remove('active');
        if (btnEmpty) btnEmpty.classList.add('active');
        window.showToast('🧹 냉장고가 비워졌습니다. 새 재료를 등록해보세요!');
    }
    saveInventory();
    renderInventoryUI();
};

window.addManualIngredient = function() {
    const nameInput = document.getElementById('manualIngName');
    const qtyInput = document.getElementById('manualIngQty');
    const shelfSelect = document.getElementById('manualIngShelf');

    if (!nameInput || !nameInput.value.trim()) {
        window.showToast('⚠️ 식재료 이름을 입력해주세요!');
        return;
    }

    const name = nameInput.value.trim();
    const rawQty = qtyInput ? qtyInput.value.trim() : '1개';
    const shelf = shelfSelect ? shelfSelect.value : 'veg';

    // Parse number and unit
    const numMatch = rawQty.match(/\d+/);
    const qty = numMatch ? parseInt(numMatch[0]) : 1;
    const unit = rawQty.replace(/\d+/, '').trim() || '개';

    const newId = `custom-${Date.now()}`;
    const newItem = {
        id: newId,
        name: name,
        qty: qty,
        unit: unit,
        shelf: shelf,
        freshness: 'high',
        selected: true,
        thumb: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&auto=format&fit=crop&q=80'
    };

    KitchenChefState.inventory.unshift(newItem);
    saveInventory();
    renderInventoryUI();

    nameInput.value = '';
    if (qtyInput) qtyInput.value = '';
    window.showToast(`✨ '${name}' 재료가 보관함에 영구 저장되었습니다!`);
};

window.addQuickTag = function(name, shelf) {
    const existing = KitchenChefState.inventory.find(i => i.name === name);
    if (existing) {
        existing.qty += 1;
        existing.selected = true;
    } else {
        KitchenChefState.inventory.unshift({
            id: `quick-${Date.now()}`,
            name: name,
            qty: 1,
            unit: '개',
            shelf: shelf || 'veg',
            freshness: 'high',
            selected: true,
            thumb: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=100&auto=format&fit=crop&q=80'
        });
    }
    saveInventory();
    renderInventoryUI();
    window.showToast(`➕ '${name}' 재료가 추가되었습니다!`);
};

function initThemeSelection() {
    window.selectThemeOption = function(element) {
        document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
        element.classList.add('active');
        KitchenChefState.selectedTheme = element.getAttribute('data-theme-id') || 'korean-stew';
    };
}

// Vision Upload Simulation
const fileUpload = document.getElementById('filePhotoUpload');
if (fileUpload) {
    fileUpload.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            window.showToast('📷 AI가 냉장고 사진 속 재료를 분석 중입니다...');
            setTimeout(() => {
                window.addQuickTag('청경채', 'veg');
                window.addQuickTag('표고버섯', 'veg');
                window.showToast('✨ AI Vision: 청경채와 표고버섯을 인식하여 냉장고에 등록했습니다!');
            }, 1200);
        }
    });
}

// ==========================================================================
// 4. SCREEN 2: 3D REFRIGERATOR OPENING ANIMATION
// ==========================================================================
window.startRecipeJourney = function() {
    const selected = KitchenChefState.inventory.filter(i => i.selected && i.qty > 0);
    if (selected.length === 0) {
        // Auto select first 3 items
        KitchenChefState.inventory.slice(0, 3).forEach(i => { i.selected = true; i.qty = Math.max(1, i.qty); });
        saveInventory();
        renderInventoryUI();
    }

    window.goToScreen(2);
};

function runScreen2Animation() {
    const chassis = document.getElementById('screen2FridgeChassis');
    const countdownEl = document.getElementById('screen2Countdown');
    const cloud = document.getElementById('flyingTagsCloud');

    // 1. Reset
    if (chassis) chassis.classList.remove('open');
    if (cloud) cloud.innerHTML = '';
    if (countdownEl) countdownEl.textContent = '2.0s';

    // 2. Open Doors after 100ms
    setTimeout(() => {
        if (chassis) chassis.classList.add('open');

        // Populate flying pills from selected ingredients
        const selected = KitchenChefState.inventory.filter(i => i.selected && i.qty > 0);
        const displayItems = selected.length > 0 ? selected : DEFAULT_INVENTORY.slice(0, 5);

        if (cloud) {
            cloud.innerHTML = '';
            displayItems.forEach((item, index) => {
                const pill = document.createElement('div');
                pill.className = 'flying-ing-pill';
                
                // Randomize trajectory offsets
                const flyX = (index % 2 === 0 ? -1 : 1) * (30 + (index * 25));
                const landX = (index % 3 - 1) * 90;
                const landY = 220 + (index * 15);
                pill.style.setProperty('--fly-x', `${flyX}px`);
                pill.style.setProperty('--fly-y', `${-30 - index * 10}px`);
                pill.style.setProperty('--land-x', `${landX}px`);
                pill.style.setProperty('--land-y', `${landY}px`);
                pill.style.animationDelay = `${index * 0.15}s`;
                pill.style.left = '50%';
                pill.style.top = '35%';

                pill.innerHTML = `
                    <img src="${item.thumb}" alt="${item.name}" class="flying-ing-img">
                    <span>${item.name} ${item.qty}${item.unit}</span>
                `;
                cloud.appendChild(pill);
            });
        }
    }, 150);

    // 3. Countdown 2.0s -> 0.0s
    let timeLeft = 20; // 2.0 seconds
    const interval = setInterval(() => {
        timeLeft -= 1;
        if (countdownEl) {
            countdownEl.textContent = `${(timeLeft / 10).toFixed(1)}s`;
        }
        if (timeLeft <= 0) {
            clearInterval(interval);
            // Automatically navigate to Screen 3
            setTimeout(() => {
                window.goToScreen(3);
                window.showToast('🪵 원목 도마 위에 6가지 맞춤 레시피가 준비되었습니다!');
            }, 300);
        }
    }, 100);
}

// ==========================================================================
// 5. SCREEN 3: HANDCRAFTED WOODEN RECIPES CATALOG
// ==========================================================================
function initRecipeSelection() {
    // Bind click events to recipe cards on Screen 3
    const recipeCards = document.querySelectorAll('.wooden-recipe-card');
    recipeCards.forEach(card => {
        card.addEventListener('click', (e) => {
            const recipeId = card.getAttribute('data-recipe-id');
            if (recipeId && RECIPES_CATALOG[recipeId]) {
                window.selectAndStartCooking(recipeId);
            }
        });
    });
}

window.selectAndStartCooking = function(recipeId) {
    const recipe = RECIPES_CATALOG[recipeId] || RECIPES_CATALOG['golden-egg-fried-rice'];
    KitchenChefState.selectedRecipe = recipe;
    populateScreen4Details(recipe);
    window.goToScreen(4);
    window.showToast(`🔪 '${recipe.title}' 조리대에 입장했습니다!`);
};

// ==========================================================================
// 6. SCREEN 4: WORKBENCH, CHECKLIST & SMART TIMER
// ==========================================================================
function populateScreen4Details(recipe) {
    if (!recipe) return;

    const title = document.getElementById('screen4DishTitle');
    const desc = document.getElementById('screen4DishDesc');
    const time = document.getElementById('screen4CookingTime');
    const diff = document.getElementById('screen4Difficulty');
    const clList = document.getElementById('clItemsList');

    if (title) title.textContent = recipe.title;
    if (desc) desc.textContent = recipe.desc;
    if (time) time.textContent = recipe.time;
    if (diff) diff.textContent = recipe.difficulty;

    // Reset checklist items
    if (clList && recipe.prepList) {
        clList.innerHTML = recipe.prepList.map(item => `
            <label class="cl-item">
                <input type="checkbox" onchange="window.updatePrepChecklist(this)">
                <span class="custom-checkbox"></span>
                <div class="cl-item-text">
                    <strong>${item.name}</strong>
                    <span>${item.guide}</span>
                </div>
            </label>
        `).join('');
    }

    // Reset checklist progress
    updatePrepChecklistUI();

    // Reset Timer to 2 mins
    window.setCookingTimerSeconds(120);

    // Update Screen 5 Completed info preview
    const celebName = document.querySelector('.celeb-dish-name');
    if (celebName) celebName.textContent = recipe.title;
}

window.updatePrepChecklist = function(checkbox) {
    updatePrepChecklistUI();
};

function updatePrepChecklistUI() {
    const checkboxes = document.querySelectorAll('#clItemsList input[type="checkbox"]');
    const total = checkboxes.length;
    let checked = 0;
    checkboxes.forEach(cb => { if (cb.checked) checked++; });

    const badge = document.getElementById('prepCheckCountBadge');
    const progressText = document.getElementById('prepProgressText');
    const progressBar = document.getElementById('prepProgressBar');

    const pct = total > 0 ? Math.round((checked / total) * 100) : 0;

    if (badge) badge.textContent = `${checked}/${total} 준비완료`;
    if (progressText) progressText.textContent = `${pct}%`;
    if (progressBar) progressBar.style.width = `${pct}%`;
}

// Kitchen Smart Timer Logic
window.setCookingTimerSeconds = function(sec) {
    KitchenChefState.timerTotalSeconds = sec;
    KitchenChefState.timerSecondsLeft = sec;
    updateTimerDisplay();
};

function updateTimerDisplay() {
    const display = document.getElementById('smartTimerDisplay');
    const m = Math.floor(KitchenChefState.timerSecondsLeft / 60);
    const s = KitchenChefState.timerSecondsLeft % 60;
    const formatted = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    if (display) display.textContent = formatted;
}

window.toggleCookingTimer = function() {
    if (KitchenChefState.isTimerRunning) {
        window.pauseCookingTimer();
    } else {
        window.startCookingTimer();
    }
};

window.startCookingTimer = function() {
    if (KitchenChefState.isTimerRunning) return;
    KitchenChefState.isTimerRunning = true;

    const badge = document.getElementById('smartTimerStatusBadge');
    const btnToggle = document.getElementById('btnTimerToggle');
    if (badge) badge.textContent = '조리 진행 중';
    if (btnToggle) btnToggle.innerHTML = '<i class="fa-solid fa-pause"></i> 일시 정지';

    KitchenChefState.timerInterval = setInterval(() => {
        if (KitchenChefState.timerSecondsLeft > 0) {
            KitchenChefState.timerSecondsLeft -= 1;
            updateTimerDisplay();
        } else {
            window.pauseCookingTimer();
            window.showToast('🔔 타이머 완료! 다음 조리 단계로 진행하세요.');
            // Play gentle web audio beep
            playChimeSound();
        }
    }, 1000);
};

window.pauseCookingTimer = function() {
    KitchenChefState.isTimerRunning = false;
    if (KitchenChefState.timerInterval) clearInterval(KitchenChefState.timerInterval);

    const badge = document.getElementById('smartTimerStatusBadge');
    const btnToggle = document.getElementById('btnTimerToggle');
    if (badge) badge.textContent = '일시 정지';
    if (btnToggle) btnToggle.innerHTML = '<i class="fa-solid fa-play"></i> 타이머 계속';
};

window.resetCookingTimer = function() {
    window.pauseCookingTimer();
    KitchenChefState.timerSecondsLeft = KitchenChefState.timerTotalSeconds;
    updateTimerDisplay();
    const badge = document.getElementById('smartTimerStatusBadge');
    if (badge) badge.textContent = '대기 중';
};

function playChimeSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3); // A5
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
    } catch (e) {
        console.log("Web audio chime not supported:", e);
    }
}

// ==========================================================================
// 7. REAL-TIME INVENTORY DEDUCTION & COMPLETION
// ==========================================================================
window.finishCookingAndDeductInventory = function() {
    const recipe = KitchenChefState.selectedRecipe || RECIPES_CATALOG['golden-egg-fried-rice'];
    const toggleAutoDeduct = document.getElementById('toggleAutoDeduct');
    const shouldDeduct = !toggleAutoDeduct || toggleAutoDeduct.checked;

    let deductedCount = 0;

    if (shouldDeduct && recipe.deductions) {
        recipe.deductions.forEach(ded => {
            const item = KitchenChefState.inventory.find(i => i.id === ded.id || i.name === ded.name);
            if (item && item.qty > 0) {
                item.qty = Math.max(0, item.qty - ded.amount);
                deductedCount++;
            }
        });
        saveInventory();
        renderInventoryUI();
    }

    // Advance to Screen 5
    window.goToScreen(5);

    // Show completion Toast with deduction info
    if (shouldDeduct && deductedCount > 0) {
        window.showToast(`🎉 요리 완성! 레시피에 사용된 ${deductedCount}개 식재료가 실시간 자동 소진되었습니다.`);
    } else {
        window.showToast(`🎉 요리 완성 인증을 축하합니다!`);
    }
};

// ==========================================================================
// 8. SCREEN 5: COMMUNITY REVIEWS & FEED
// ==========================================================================
function initInteractiveStarRating() {
    const starContainer = document.getElementById('ratingStars');
    if (!starContainer) return;

    const stars = starContainer.querySelectorAll('i');
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const rating = parseInt(star.getAttribute('data-rating')) || 5;
            KitchenChefState.selectedReviewRating = rating;

            stars.forEach(s => {
                const r = parseInt(s.getAttribute('data-rating'));
                if (r <= rating) s.classList.add('active');
                else s.classList.remove('active');
            });
        });
    });
}

window.handleReviewPhotoSelect = function(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('commPreviewImg');
            if (preview) preview.src = e.target.result;
            KitchenChefState.userReviewPhoto = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

window.submitCommunityPost = function() {
    const input = document.getElementById('commReviewInput');
    const content = input ? input.value.trim() : '';

    if (!content) {
        window.showToast('✍️ 맛 후기 또는 나만의 조리 팁을 입력해주세요!');
        return;
    }

    // Get current user display name
    let authorName = '요리하는 소라';
    if (window.authManager && window.authManager.currentUser) {
        authorName = window.authManager.currentUser.displayName || authorName;
    }

    const feedList = document.getElementById('communityFeedList');
    if (feedList) {
        const postCard = document.createElement('div');
        postCard.className = 'community-post-card best-post';
        postCard.innerHTML = `
            <div class="post-card-header">
                <div class="post-user-info">
                    <div class="post-user-avatar-initial green">${authorName.slice(0, 2)}</div>
                    <div>
                        <div class="post-author-name-row">
                            <strong>${authorName}</strong>
                            <span class="user-sub-tag">방금 완식</span>
                            <span class="chef-mastery-tag green">실시간 인증</span>
                        </div>
                        <div class="post-meta-sub">
                            <span>방금 전</span>
                            <span class="meta-dot">•</span>
                            <span class="post-stars"><i class="fa-solid fa-star"></i> ${KitchenChefState.selectedReviewRating}.0</span>
                        </div>
                    </div>
                </div>
                <span class="badge-best-crown"><i class="fa-solid fa-award"></i> 완식 인증</span>
            </div>
            <p class="post-body-text">${content}</p>
            ${KitchenChefState.userReviewPhoto ? `
                <div class="post-photo-wrap">
                    <img src="${KitchenChefState.userReviewPhoto}" alt="완식 인증 사진" class="post-attached-photo">
                    <span class="badge-photo-cert"><i class="fa-solid fa-check"></i> 방금 찍은 인증샷</span>
                </div>
            ` : ''}
            <div class="post-card-footer">
                <div class="post-actions-group">
                    <button type="button" class="btn-vote-chip active" onclick="window.voteFeedItem(this, 1)">
                        <i class="fa-solid fa-thumbs-up"></i> <strong>1</strong>
                    </button>
                </div>
                <span class="tag-salvaged-ing">냉파 성공 100%</span>
            </div>
        `;

        feedList.insertBefore(postCard, feedList.firstChild);
    }

    if (input) input.value = '';
    window.showToast('🌟 완식 후기가 등록되었습니다! 노하우 명예의 전당에 반영됩니다.');
};

window.voteFeedItem = function(btn, currentVotes) {
    const isVoted = btn.classList.contains('active');
    const strong = btn.querySelector('strong');
    let votes = parseInt(strong ? strong.textContent : currentVotes);

    if (isVoted) {
        btn.classList.remove('active');
        votes = Math.max(0, votes - 1);
    } else {
        btn.classList.add('active');
        votes += 1;
        window.showToast('👍 꿀팁 추천을 남겼습니다!');
    }

    if (strong) strong.textContent = votes;
};

// ==========================================================================
// 9. TOAST NOTIFICATION UTILITY
// ==========================================================================
window.showToast = function(message) {
    const existing = document.querySelector('.kc-toast-notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'kc-toast-notification';
    toast.innerHTML = `<i class="fa-solid fa-circle-check" style="color: #F59E0B;"></i> <span>${message}</span>`;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-16px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2800);
};

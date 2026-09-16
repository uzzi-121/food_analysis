from pathlib import Path

DIR = Path(__file__).resolve().parent

def create_step_svg(
    filename: str,
    step_num: int,
    title: str,
    subtitle: str,
    heat: str,
    theme_color: str,
    secondary_color: str,
    icon_type: str
):
    # Distinct SVG icons for each cooking process
    if icon_type == "prep":
        icon_svg = '''
        <!-- Cutting board and knife & ingredients -->
        <rect x="230" y="140" width="180" height="110" rx="14" fill="#1E2438" stroke="''' + theme_color + '''" stroke-width="2.5" opacity="0.85"/>
        <line x1="250" y1="165" x2="330" y2="165" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
        <line x1="250" y1="185" x2="310" y2="185" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
        <circle cx="365" cy="180" r="16" fill="#F97316" opacity="0.9"/>
        <circle cx="385" cy="205" r="12" fill="#10B981" opacity="0.9"/>
        <!-- Knife -->
        <path d="M210 130 L275 195 L260 210 L195 145 Z" fill="#E2E8F0"/>
        <path d="M195 145 L175 125 L185 115 L205 135 Z" fill="#64748B"/>
        '''
    elif icon_type == "sizzle":
        icon_svg = '''
        <!-- Sizzling Pan with Steam & Oil drops -->
        <ellipse cx="320" cy="210" rx="100" ry="32" fill="#151928" stroke="''' + theme_color + '''" stroke-width="3"/>
        <line x1="420" y1="210" x2="490" y2="245" stroke="#94A3B8" stroke-width="8" stroke-linecap="round"/>
        <!-- Food inside pan -->
        <rect x="280" y="195" width="22" height="16" rx="4" fill="#FB7185"/>
        <rect x="310" y="200" width="24" height="14" rx="4" fill="#FB7185"/>
        <circle cx="345" cy="205" r="8" fill="#34D399"/>
        <circle cx="295" cy="212" r="7" fill="#34D399"/>
        <rect x="330" y="195" width="20" height="15" rx="3" fill="#FBBF24"/>
        <!-- Sizzling Steam Waves -->
        <path d="M290 170 Q300 150 290 130" stroke="''' + secondary_color + '''" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>
        <path d="M320 165 Q330 145 320 125" stroke="''' + secondary_color + '''" stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.9"/>
        <path d="M350 170 Q360 150 350 130" stroke="''' + secondary_color + '''" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>
        '''
    elif icon_type == "sauce":
        icon_svg = '''
        <!-- Sauce Caramelization / Stirring -->
        <ellipse cx="320" cy="210" rx="105" ry="34" fill="#18131E" stroke="''' + theme_color + '''" stroke-width="3"/>
        <path d="M260 205 Q320 230 380 205 Q320 220 260 205" fill="#78350F" opacity="0.85"/>
        <!-- Kimchi & Ingredients -->
        <circle cx="290" cy="200" r="14" fill="#EF4444" opacity="0.9"/>
        <circle cx="340" cy="202" r="15" fill="#DC2626" opacity="0.9"/>
        <circle cx="315" cy="212" r="12" fill="#F87171" opacity="0.8"/>
        <!-- Spatula Stirring -->
        <path d="M360 130 L325 195 L345 200 L380 135 Z" fill="#CBD5E1"/>
        <line x1="380" y1="135" x2="430" y2="90" stroke="#94A3B8" stroke-width="7" stroke-linecap="round"/>
        <!-- Fire / Flavor Sparks -->
        <path d="M250 170 Q255 155 250 145" stroke="#F59E0B" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <circle cx="385" cy="165" r="3" fill="#F59E0B"/>
        <circle cx="375" cy="180" r="2" fill="#EF4444"/>
        '''
    elif icon_type == "pot":
        icon_svg = '''
        <!-- Stew / Soup Boiling Pot -->
        <rect x="250" y="150" width="140" height="85" rx="16" fill="#151928" stroke="''' + theme_color + '''" stroke-width="3"/>
        <rect x="235" y="170" width="15" height="24" rx="6" fill="#475569"/>
        <rect x="390" y="170" width="15" height="24" rx="6" fill="#475569"/>
        <ellipse cx="320" cy="155" rx="65" ry="16" fill="#DC2626" opacity="0.85"/>
        <!-- Tofu blocks in soup -->
        <rect x="285" y="148" width="22" height="15" rx="3" fill="#F8FAFC" opacity="0.95"/>
        <rect x="325" y="152" width="20" height="14" rx="3" fill="#F8FAFC" opacity="0.95"/>
        <!-- Bubbles & Steam -->
        <circle cx="300" cy="140" r="6" fill="#FEF08A" opacity="0.8"/>
        <circle cx="335" cy="138" r="8" fill="#FDBA74" opacity="0.85"/>
        <path d="M305 120 Q315 100 305 85" stroke="#E2E8F0" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.75"/>
        <path d="M335 115 Q345 95 335 80" stroke="#E2E8F0" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.75"/>
        '''
    elif icon_type == "omelet":
        icon_svg = '''
        <!-- Rolled Omelet -->
        <rect x="240" y="160" width="160" height="70" rx="20" fill="#F59E0B" stroke="''' + theme_color + '''" stroke-width="3"/>
        <path d="M260 160 Q265 195 260 230" stroke="#B45309" stroke-width="3" fill="none"/>
        <path d="M295 160 Q300 195 295 230" stroke="#B45309" stroke-width="3" fill="none"/>
        <path d="M330 160 Q335 195 330 230" stroke="#B45309" stroke-width="3" fill="none"/>
        <path d="M365 160 Q370 195 365 230" stroke="#B45309" stroke-width="3" fill="none"/>
        <circle cx="280" cy="180" r="4" fill="#10B981"/>
        <circle cx="315" cy="205" r="4" fill="#EF4444"/>
        <circle cx="350" cy="185" r="4" fill="#10B981"/>
        '''
    else:  # plate / finish
        icon_svg = '''
        <!-- Completed Dish Platter / Serving -->
        <ellipse cx="320" cy="215" rx="120" ry="35" fill="#1A1F33" stroke="''' + theme_color + '''" stroke-width="3"/>
        <ellipse cx="320" cy="205" rx="90" ry="24" fill="#242B45"/>
        <!-- Golden Rice / Food Dome -->
        <ellipse cx="320" cy="190" rx="65" ry="25" fill="#F59E0B" opacity="0.9"/>
        <!-- Fried Egg on top -->
        <ellipse cx="320" cy="178" rx="35" ry="14" fill="#F8FAFC"/>
        <circle cx="320" cy="176" r="10" fill="#F97316"/>
        <circle cx="305" cy="190" r="2" fill="#1E293B"/>
        <circle cx="335" cy="188" r="2" fill="#1E293B"/>
        <!-- Fresh herbs sparkle -->
        <circle cx="355" cy="155" r="4" fill="''' + theme_color + '''"/>
        <circle cx="285" cy="158" r="3" fill="''' + secondary_color + '''"/>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 380" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E111C"/>
      <stop offset="50%" stop-color="#141826"/>
      <stop offset="100%" stop-color="#0B0D15"/>
    </linearGradient>
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="{theme_color}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{theme_color}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{theme_color}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{secondary_color}" stop-opacity="0.3"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="640" height="380" rx="20" fill="url(#bgGrad)"/>
  <circle cx="320" cy="190" r="180" fill="url(#glowGrad)"/>
  
  <!-- Outer Glow Border -->
  <rect x="3" y="3" width="634" height="374" rx="18" fill="none" stroke="url(#borderGrad)" stroke-width="1.5" opacity="0.9"/>

  <!-- Top Badge: STEP NUMBER -->
  <g transform="translate(32, 28)">
    <rect width="88" height="28" rx="14" fill="{theme_color}" fill-opacity="0.18" stroke="{theme_color}" stroke-opacity="0.6" stroke-width="1.2"/>
    <text x="44" y="19" font-family="'Outfit', -apple-system, sans-serif" font-size="13" font-weight="700" fill="#F8FAFC" text-anchor="middle" letter-spacing="0.06em">STEP 0{step_num}</text>
  </g>

  <!-- Top Right Badge: HEAT / STATUS -->
  <g transform="translate(488, 28)">
    <rect width="120" height="28" rx="14" fill="#1E2235" stroke="#334155" stroke-width="1.2"/>
    <text x="60" y="18" font-family="'Pretendard', sans-serif" font-size="12" font-weight="600" fill="{secondary_color}" text-anchor="middle">{heat}</text>
  </g>

  <!-- Central Visual Illustration -->
  <g filter="url(#shadow)">
    {icon_svg}
  </g>

  <!-- Bottom Title & Guide Card -->
  <g transform="translate(24, 280)">
    <rect width="592" height="76" rx="14" fill="#121624" fill-opacity="0.92" stroke="#262D42" stroke-width="1"/>
    <text x="24" y="32" font-family="'Pretendard', -apple-system, sans-serif" font-size="17" font-weight="700" fill="#FFFFFF">{title}</text>
    <text x="24" y="56" font-family="'Pretendard', sans-serif" font-size="13" font-weight="400" fill="#94A3B8">{subtitle}</text>
    <!-- Accent Dot -->
    <circle cx="560" cy="38" r="5" fill="{theme_color}"/>
  </g>
</svg>'''

    (DIR / filename).write_text(svg, encoding="utf-8")
    print(f"Created: {filename}")

# Generate all recipe step illustrations
steps_data = [
    # spam-kimchi-fried-rice
    ("spam-kimchi-fried-rice_step1.svg", 1, "재료 손질하기", "대파 송송 썰기 & 스팸 옥수수알 크기 깍둑썰기", "🔪 재료 손질", "#8B5CF6", "#38BDF8", "prep"),
    ("spam-kimchi-fried-rice_step2.svg", 2, "파기름 & 스팸 볶기", "중불에서 향긋한 파기름과 스팸 노릇하게 굽기", "🔥 중불 90초", "#F97316", "#FBBF24", "sizzle"),
    ("spam-kimchi-fried-rice_step3.svg", 3, "간장 불맛 & 김치 볶기", "간장 눌려 불맛 입히고 신김치와 설탕 볶기", "⚡ 중강불 120초", "#EF4444", "#F59E0B", "sauce"),
    ("spam-kimchi-fried-rice_step4.svg", 4, "밥 비비기 & 눋혀 완성", "따뜻한 밥을 고슬고슬 비빈 뒤 센 불에 바삭하게 눋히기", "🍳 완성 & 플레이팅", "#10B981", "#38BDF8", "finish"),

    # pork-kimchi-jjigae
    ("pork-kimchi-jjigae_step1.svg", 1, "고기 볶아 기름 내기", "돼지고기 겉면이 바삭해질 때까지 기름 내며 볶기", "🔥 중불 120초", "#F97316", "#FBBF24", "sizzle"),
    ("pork-kimchi-jjigae_step2.svg", 2, "김치 & 고춧가루 볶기", "고기 기름에 신김치와 고춧가루, 다진 마늘 볶기", "🔥 중불 120초", "#EF4444", "#F59E0B", "sauce"),
    ("pork-kimchi-jjigae_step3.svg", 3, "물 붓고 된장 풀어 푹 끓이기", "물과 된장, 국간장을 넣고 보글보글 푹 끓이기", "♨️ 강불 7분", "#38BDF8", "#8B5CF6", "pot"),
    ("pork-kimchi-jjigae_step4.svg", 4, "두부, 대파 넣고 마무리", "두부와 송송 썬 대파를 얹어 칼칼하게 완성", "🍲 완성", "#10B981", "#38BDF8", "finish"),

    # rolled-omelet
    ("rolled-omelet_step1.svg", 1, "계란물 풀기 및 간 맞추기", "알끈이 부드럽게 풀리도록 소금과 우유 넣어 젓기", "🔪 재료 손질", "#FBBF24", "#F59E0B", "prep"),
    ("rolled-omelet_step2.svg", 2, "팬 코팅 & 1차 계란물 붓기", "팬에 얇게 기름을 두르고 약불에서 1차 붓기", "♨️ 약불 60초", "#F59E0B", "#FBBF24", "omelet"),
    ("rolled-omelet_step3.svg", 3, "돌돌 말아가며 계란물 잇기", "70% 익었을 때 끝에서부터 돌돌 말고 이어 붓기", "♨️ 약불 120초", "#F59E0B", "#FBBF24", "omelet"),
    ("rolled-omelet_step4.svg", 4, "한 김 식혀 썰기 및 완성", "도마에서 2분간 식혀 모양을 잡고 예쁘게 썰기", "🍳 완성", "#10B981", "#38BDF8", "finish"),

    # spam-tofu-kimchi
    ("spam-tofu-kimchi_step1.svg", 1, "두부 데치기 및 스팸 썰기", "끓는 물에 두부를 데쳐내고 스팸을 도톰하게 썰기", "♨️ 강불 60초", "#38BDF8", "#8B5CF6", "prep"),
    ("spam-tofu-kimchi_step2.svg", 2, "스팸 노릇하게 굽기", "팬에 기름 없이 스팸 앞뒤를 바삭하고 노릇하게 굽기", "🔥 중불 120초", "#F97316", "#FBBF24", "sizzle"),
    ("spam-tofu-kimchi_step3.svg", 3, "스팸 기름에 신김치 볶기", "스팸 향이 밴 팬에 신김치와 참기름, 설탕 넣고 볶기", "🔥 중불 180초", "#EF4444", "#F59E0B", "sauce"),
    ("spam-tofu-kimchi_step4.svg", 4, "삼합 플레이팅 및 완성", "두부, 스팸, 볶음김치를 접시에 둘러 통깨 뿌려 완성", "🍺 완성 안주", "#10B981", "#38BDF8", "finish"),

    # kimchi-pancake
    ("kimchi-pancake_step1.svg", 1, "김치와 스팸 잘게 썰기", "김치와 스팸을 가위로 잘게 깍둑썰기해 볼에 담기", "🔪 재료 손질", "#8B5CF6", "#38BDF8", "prep"),
    ("kimchi-pancake_step2.svg", 2, "바삭한 반죽 만들기", "부침가루와 차가운 물을 1:1로 멍울 없이 섞기", "🥣 반죽 준비", "#38BDF8", "#10B981", "prep"),
    ("kimchi-pancake_step3.svg", 3, "센 불에서 바삭하게 부치기", "기름을 넉넉히 두르고 가장자리부터 튀기듯 바삭하게", "⚡ 중강불 6분", "#EF4444", "#F59E0B", "sizzle"),

    # spicy-braised-tofu
    ("spicy-braised-tofu_step1.svg", 1, "두부와 야채 손질하기", "두부는 1cm 두께로 도톰하게 썰고 대파와 양파 썰기", "🔪 재료 손질", "#8B5CF6", "#38BDF8", "prep"),
    ("spicy-braised-tofu_step2.svg", 2, "양파 깔고 두부 올리기", "냄비 바닥에 채 썬 양파 깔고 두부 가지런히 얹기", "🍲 냄비 세팅", "#38BDF8", "#F59E0B", "pot"),
    ("spicy-braised-tofu_step3.svg", 3, "양념장 붓고 끓이기", "진간장, 고춧가루, 설탕, 마늘, 물 붓고 중불 끓이기", "🔥 중불 180초", "#EF4444", "#F59E0B", "sauce"),
    ("spicy-braised-tofu_step4.svg", 4, "국물 끼얹으며 졸여 완성", "약불에서 국물 끼얹으며 5분 조린 후 참기름 둘러 완성", "✨ 완성 밥도둑", "#10B981", "#38BDF8", "finish"),

    # default fallbacks
    ("default_step1.svg", 1, "식재료 깨끗이 손질", "준비된 재료들을 먹기 좋은 크기로 다듬어주세요.", "🔪 재료 손질", "#8B5CF6", "#38BDF8", "prep"),
    ("default_step2.svg", 2, "볶기 및 조리 진행", "팬에 기름을 두르고 재료를 넣고 볶아줍니다.", "🔥 중불 조리", "#F97316", "#FBBF24", "sizzle"),
    ("default_step3.svg", 3, "완성 및 플레이팅", "간을 맞추고 그릇에 담아 완성합니다.", "🍽️ 완성", "#10B981", "#38BDF8", "finish"),
]

for item in steps_data:
    create_step_svg(*item)
print("All step SVGs generated successfully!")

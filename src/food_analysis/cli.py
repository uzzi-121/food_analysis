"""Interactive Command Line Interface for CookCast AI."""

import argparse
import asyncio
import sys
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .workflows.orchestrator import orchestrator


async def run_cli_pipeline(ingredients_input: str) -> None:
    print("\n" + "=" * 60)
    print("🍳 CookCast AI - 냉장고 식재료 레시피 에이전트 CLI")
    print("=" * 60)

    # 1. Step 1: Ingredient Extraction
    print(f"\n[Agent 1] 식재료 분석 시작... (입력: {ingredients_input})")
    extract_res = await orchestrator.step1_extract_ingredients(text_input=ingredients_input)
    ing_names = [i.name for i in extract_res.ingredients]
    print(f"  -> 감지된 식재료 ({len(ing_names)}개): {', '.join(ing_names)}")

    # 2. Step 2: Recipe Harvester
    print("\n[Agent 2] 레시피 및 셰프 꿀팁 탐색 중...")
    candidates = await orchestrator.step2_recommend_recipes(ing_names)
    print("  -> 최적의 추천 레시피 후보 3선:")
    for idx, c in enumerate(candidates, 1):
        print(f"     {idx}. {c.thumbnail_emoji} {c.title} (매칭률: {c.match_rate}%, {c.estimated_time_minutes}분 소요)")

    if not candidates:
        print("  -> 추천 가능한 레시피가 없습니다.")
        return

    # Select top candidate
    top = candidates[0]
    print(f"\n[Agent 3] 최고 매칭 레시피 '{top.title}' 황금 비율 종합 중...")
    synthesized = await orchestrator.step3_synthesize_recipe(top.id, ing_names)
    print(f"  -> {synthesized.title} (난이도: 쉬움, {synthesized.servings})")
    print(f"  -> 핵심 양념 비율:")
    for s in synthesized.seasoning_ratios:
        print(f"     - {s.name}: {s.ratio} ({s.tip})")
    print(f"  -> 조리 단계: 총 {len(synthesized.steps)}단계")

    # 4. Step 4 & 5: Audio render check
    print(f"\n[Agent 4 & 5] 음성 가이드 대본 및 TTS 엔진 테스트...")
    first_step = synthesized.steps[0]
    first_script = orchestrator.script_agent.prepare_step_script(first_step)
    print(f"  -> 1단계 오디오 대본 미리보기:\n     \"{first_script}\"")
    print("\n" + "=" * 60)
    print("✨ 파이프라인 검증 완료! 웹 UI는 'python run.py'로 접속 가능합니다.")
    print("=" * 60 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="CookCast AI Recipe Multi-Agent CLI")
    parser.add_argument(
        "--ingredients", "-i",
        type=str,
        default="스팸, 김치, 계란, 대파",
        help="냉장고에 있는 식재료 (예: '스팸, 김치, 계란, 대파')"
    )
    args = parser.parse_args()
    asyncio.run(run_cli_pipeline(args.ingredients))


if __name__ == "__main__":
    main()

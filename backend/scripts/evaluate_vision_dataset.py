from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.services.vision_dataset_evaluator import evaluate_dataset, format_evaluation_text


def main() -> int:
    parser = argparse.ArgumentParser(description="비전 데이터셋 기준 착장 분석 평가")
    parser.add_argument(
        "--dataset-root",
        default=str(ROOT / "data" / "vision_dataset"),
        help="데이터셋 루트 경로",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="출력 형식",
    )
    args = parser.parse_args()

    summary = evaluate_dataset(Path(args.dataset_root))
    if args.format == "json":
        payload = {
            "sample_count": summary.sample_count,
            "expected_item_count": summary.expected_item_count,
            "predicted_item_count": summary.predicted_item_count,
            "matched_item_count": summary.matched_item_count,
            "exact_match_sample_count": summary.exact_match_sample_count,
            "item_precision": summary.item_precision,
            "item_recall": summary.item_recall,
            "exact_match_accuracy": summary.exact_match_accuracy,
            "category_recall": summary.category_recall,
            "samples": [
                {
                    "sample_id": sample.sample_id,
                    "expected_count": sample.expected_count,
                    "predicted_count": sample.predicted_count,
                    "matched_count": sample.matched_count,
                    "exact_match": sample.exact_match,
                    "missing_items": list(sample.missing_items),
                    "unexpected_items": list(sample.unexpected_items),
                    "matched_items": list(sample.matched_items),
                }
                for sample in summary.samples
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_evaluation_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import os


# 테스트는 로컬 .env에 입력된 실제 API 키/비전 provider 설정과 분리해서 실행한다.
os.environ.setdefault("VISION_OUTFIT_ANALYZER_ENABLED", "false")
os.environ.setdefault("VISION_OUTFIT_ANALYZER_PROVIDER", "disabled")
os.environ.setdefault("OPENAI_VISION_ENABLED", "false")
os.environ.setdefault("OPENAI_VISION_PROVIDER", "disabled")
os.environ["NAVER_SHOPPING_CLIENT_ID"] = ""
os.environ["NAVER_SHOPPING_CLIENT_SECRET"] = ""

from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageDraw

from src.services.image_analysis import analyze_outfit_category_query_hints, classify_rgb_color
from src.services.naver_shopping import build_naver_category_queries
from src.services.store import UploadAnalysis


def build_flatlay_fixture() -> bytes:
    image = Image.new("RGB", (524, 788), (153, 125, 102))
    draw = ImageDraw.Draw(image)
    draw.rectangle((60, 65, 455, 280), fill=(246, 247, 245))
    draw.rectangle((145, 40, 375, 310), fill=(18, 19, 20))
    draw.rectangle((115, 275, 340, 735), fill=(248, 246, 237))
    draw.rectangle((320, 365, 500, 560), fill=(238, 234, 205))
    draw.ellipse((55, 580, 128, 735), fill=(42, 30, 26))
    draw.ellipse((132, 580, 205, 735), fill=(42, 30, 26))
    draw.rectangle((60, 640, 200, 655), fill=(48, 30, 24))

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_outfit_query_hints_ignore_background_and_split_categories() -> None:
    hints = analyze_outfit_category_query_hints(build_flatlay_fixture())

    assert hints["top"] == "화이트 셔츠"
    assert hints["bottom"] == "화이트 팬츠"
    assert hints["outer"] == "블랙 니트 베스트"
    assert hints["shoes"] == "브라운 메리제인 슈즈"
    assert hints["bag"] == "아이보리 숄더백"


def test_naver_category_queries_prefer_outfit_category_hints() -> None:
    analysis = UploadAnalysis(
        checksum="abc",
        dominant_tone="neutral",
        style_mood="feminine",
        silhouette="layered",
        preferred_categories=("top",),
        feature_vector=(0.1, 0.2, 0.3, 0.4),
        dominant_color="beige",
        category_query_hints={
            "top": "화이트 셔츠",
            "bottom": "화이트 팬츠",
            "outer": "블랙 니트 베스트",
            "shoes": "브라운 메리제인 슈즈",
            "bag": "아이보리 숄더백",
        },
    )

    assert build_naver_category_queries(analysis) == [
        ("top", "화이트 셔츠"),
        ("bottom", "화이트 팬츠"),
        ("outer", "블랙 니트 베스트"),
        ("shoes", "브라운 메리제인 슈즈"),
        ("bag", "아이보리 숄더백"),
    ]


def test_dark_warm_shoes_are_brown_not_black() -> None:
    assert classify_rgb_color(42, 30, 26) == "brown"

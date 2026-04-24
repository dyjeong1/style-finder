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


def build_colored_flatlay_fixture() -> bytes:
    image = Image.new("RGB", (524, 788), (218, 215, 205))
    draw = ImageDraw.Draw(image)
    draw.rectangle((75, 55, 430, 275), fill=(188, 35, 52))
    draw.rectangle((135, 300, 355, 720), fill=(53, 86, 170))
    draw.rectangle((160, 60, 365, 245), fill=(47, 126, 82))
    draw.ellipse((55, 590, 130, 740), fill=(16, 16, 17))
    draw.ellipse((138, 590, 213, 740), fill=(16, 16, 17))
    draw.rectangle((330, 375, 500, 555), fill=(210, 184, 57))

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def build_simple_outfit_fixture() -> bytes:
    image = Image.new("RGB", (524, 788), (218, 215, 205))
    draw = ImageDraw.Draw(image)
    draw.rectangle((75, 55, 430, 275), fill=(188, 35, 52))
    draw.rectangle((135, 300, 355, 720), fill=(53, 86, 170))
    draw.ellipse((55, 590, 130, 740), fill=(16, 16, 17))
    draw.ellipse((138, 590, 213, 740), fill=(16, 16, 17))

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def build_accessory_fixture() -> bytes:
    image = Image.new("RGB", (524, 788), (218, 215, 205))
    draw = ImageDraw.Draw(image)
    draw.rectangle((75, 55, 350, 250), fill=(246, 247, 245))
    draw.rectangle((135, 300, 355, 720), fill=(53, 86, 170))
    draw.ellipse((390, 55, 450, 105), fill=(15, 15, 15))
    draw.ellipse((455, 55, 515, 105), fill=(15, 15, 15))
    draw.rectangle((445, 75, 460, 85), fill=(15, 15, 15))

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


def test_outfit_query_hints_are_dynamic_for_different_images() -> None:
    hints = analyze_outfit_category_query_hints(build_colored_flatlay_fixture())

    assert hints["top"] != "화이트 셔츠"
    assert hints["bottom"] != "화이트 팬츠"
    assert hints["outer"] != "블랙 니트 베스트"
    assert hints["shoes"] != "브라운 메리제인 슈즈"
    assert hints["bag"] != "아이보리 숄더백"
    assert hints["top"] == "레드 상의"
    assert hints["bottom"] == "블루 팬츠"
    assert hints["outer"] == "그린 아우터"
    assert hints["shoes"] == "블랙 신발"
    assert hints["bag"] == "옐로우 가방"


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


def test_outfit_query_hints_skip_absent_categories() -> None:
    hints = analyze_outfit_category_query_hints(build_simple_outfit_fixture())

    assert hints == {
        "top": "레드 상의",
        "bottom": "블루 팬츠",
        "shoes": "블랙 신발",
    }


def test_outfit_query_hints_detect_accessory_separately() -> None:
    hints = analyze_outfit_category_query_hints(build_accessory_fixture())

    assert hints["top"] == "화이트 상의"
    assert hints["bottom"] == "블루 팬츠"
    assert hints["accessory"] == "블랙 안경"
    assert "bag" not in hints
    assert "outer" not in hints


def test_dark_warm_shoes_are_brown_not_black() -> None:
    assert classify_rgb_color(42, 30, 26) == "brown"

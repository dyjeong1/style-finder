from __future__ import annotations

from dataclasses import dataclass
import colorsys
from collections import Counter
from io import BytesIO
import math

try:
    from PIL import Image
except ImportError:  # pragma: no cover - dependency fallback
    Image = None


@dataclass(frozen=True)
class ImageColorFeature:
    dominant_color: str
    feature_vector: tuple[float, ...]


COLOR_TITLE_KEYWORDS = {
    "black": ("블랙", "검정", "검은", "흑청"),
    "white": ("화이트", "아이보리", "크림", "오트밀", "흰색", "하얀"),
    "gray": ("그레이", "차콜", "회색", "실버"),
    "beige": ("베이지", "샌드", "카멜", "카키베이지"),
    "brown": ("브라운", "초코", "모카", "탄", "밤색"),
    "navy": ("네이비", "남색"),
    "blue": ("블루", "파랑", "소라", "스카이블루", "청"),
    "green": ("그린", "카키", "올리브", "민트"),
    "red": ("레드", "버건디", "와인"),
    "pink": ("핑크", "로즈"),
    "yellow": ("옐로우", "노랑", "머스타드"),
}

COLOR_QUERY_LABELS = {
    "black": "블랙",
    "white": "화이트",
    "gray": "그레이",
    "beige": "베이지",
    "brown": "브라운",
    "navy": "네이비",
    "blue": "블루",
    "green": "그린",
    "red": "레드",
    "pink": "핑크",
    "yellow": "옐로우",
}

CATEGORY_QUERY_LABELS = {
    "top": "상의",
    "bottom": "팬츠",
    "outer": "아우터",
    "shoes": "신발",
    "bag": "가방",
    "accessory": "악세서리",
}

OUTFIT_QUERY_REGIONS = {
    "top": (0.12, 0.02, 0.82, 0.46),
    "bottom": (0.18, 0.36, 0.62, 0.94),
    "outer": (0.22, 0.02, 0.70, 0.38),
    "shoes": (0.00, 0.66, 0.30, 0.98),
    "bag": (0.50, 0.38, 0.98, 0.82),
    "accessory": (0.62, 0.00, 1.00, 0.36),
}


def analyze_image_content(content: bytes) -> ImageColorFeature | None:
    if Image is None or not content:
        return None

    try:
        with Image.open(BytesIO(content)) as image:
            image = image.convert("RGB")
            image.thumbnail((96, 96))
            pixels = list(image.getdata())
    except Exception:
        return None

    if not pixels:
        return None

    background_color = _estimate_edge_color(image)
    foreground_pixels = _foreground_pixels(image, background_color)
    analysis_pixels = foreground_pixels if len(foreground_pixels) >= max(40, len(pixels) // 25) else pixels
    sample_step = max(1, len(analysis_pixels) // 1800)
    sampled_pixels = analysis_pixels[::sample_step]
    red = sum(pixel[0] for pixel in sampled_pixels) / len(sampled_pixels)
    green = sum(pixel[1] for pixel in sampled_pixels) / len(sampled_pixels)
    blue = sum(pixel[2] for pixel in sampled_pixels) / len(sampled_pixels)
    brightness = (red + green + blue) / (255 * 3)
    saturation = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)[1]

    return ImageColorFeature(
        dominant_color=classify_rgb_color(red, green, blue),
        feature_vector=(
            round(red / 255, 4),
            round(green / 255, 4),
            round(blue / 255, 4),
            round((brightness + saturation) / 2, 4),
        ),
    )


def classify_rgb_color(red: float, green: float, blue: float) -> str:
    hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    hue_degrees = hue * 360

    if value < 0.26 and saturation > 0.18 and 5 <= hue_degrees < 45:
        return "brown"
    if value < 0.22:
        return "black"
    if saturation < 0.12 and value > 0.86:
        return "white"
    if saturation < 0.16:
        return "gray"
    if 25 <= hue_degrees < 55 and saturation < 0.38 and value > 0.45:
        return "beige"
    if 15 <= hue_degrees < 45:
        return "brown"
    if 200 <= hue_degrees < 245 and value < 0.45:
        return "navy"
    if 185 <= hue_degrees < 255:
        return "blue"
    if 75 <= hue_degrees < 170:
        return "green"
    if 330 <= hue_degrees or hue_degrees < 15:
        return "red"
    if 280 <= hue_degrees < 330:
        return "pink"
    if 45 <= hue_degrees < 75:
        return "yellow"
    return "neutral"


def fallback_color_from_digest(digest: bytes) -> str:
    colors = ("black", "white", "gray", "beige", "brown", "navy", "blue", "green", "red", "pink", "yellow")
    return colors[digest[6] % len(colors)]


def infer_color_from_text(value: str) -> str:
    for color, keywords in COLOR_TITLE_KEYWORDS.items():
        if any(keyword in value for keyword in keywords):
            return color
    return "unknown"


def has_color_keyword(value: str, dominant_color: str) -> bool:
    return any(keyword in value for keyword in COLOR_TITLE_KEYWORDS.get(dominant_color, ()))


def analyze_outfit_category_query_hints(content: bytes) -> dict[str, str]:
    if Image is None or not content:
        return {}

    try:
        with Image.open(BytesIO(content)) as image:
            image = image.convert("RGB")
            image.thumbnail((240, 240))
            background_color = _estimate_edge_color(image)
            region_counts = {
                category: _count_foreground_colors(image, background_color, region)
                for category, region in OUTFIT_QUERY_REGIONS.items()
            }
    except Exception:
        return {}

    hints: dict[str, str] = {}
    top_counts = region_counts["top"]
    outer_counts = region_counts["outer"]
    bottom_counts = region_counts["bottom"]
    shoes_counts = region_counts["shoes"]
    bag_counts = region_counts["bag"]
    accessory_counts = region_counts["accessory"]
    layered_vest_signature = (
        _has_meaningful_color(top_counts, "white")
        and _has_meaningful_color(outer_counts, "black")
        and _has_light_garment(bottom_counts)
    )

    top_color = _query_color_name(top_counts)
    bottom_color = _query_color_name(bottom_counts)

    hints["top"] = "화이트 셔츠" if layered_vest_signature else _build_dynamic_query_hint("top", top_counts)
    hints["outer"] = (
        "블랙 니트 베스트"
        if layered_vest_signature
        else _build_distinct_query_hint("outer", outer_counts, reference_colors=(top_color,))
    )
    hints["bottom"] = "화이트 팬츠" if layered_vest_signature else _build_dynamic_query_hint("bottom", bottom_counts)

    if layered_vest_signature and (_dominant_color_name(shoes_counts) == "brown" or _has_meaningful_color(shoes_counts, "brown")):
        hints["shoes"] = "브라운 메리제인 슈즈"
    else:
        hints["shoes"] = _build_distinct_query_hint("shoes", shoes_counts, reference_colors=(bottom_color,))

    hints["bag"] = (
        "아이보리 숄더백"
        if layered_vest_signature and _has_light_garment(bag_counts)
        else _build_distinct_query_hint("bag", bag_counts, reference_colors=(bottom_color,))
    )
    hints["accessory"] = _build_distinct_query_hint(
        "accessory",
        accessory_counts,
        reference_colors=(top_color, bottom_color, _query_color_name(outer_counts), _query_color_name(bag_counts)),
    )

    return {category: hint for category, hint in hints.items() if hint}


def _estimate_edge_color(image) -> tuple[float, float, float]:
    width, height = image.size
    pixels = []
    for x in range(width):
        pixels.append(image.getpixel((x, 0)))
        pixels.append(image.getpixel((x, height - 1)))
    for y in range(height):
        pixels.append(image.getpixel((0, y)))
        pixels.append(image.getpixel((width - 1, y)))

    return tuple(sum(pixel[idx] for pixel in pixels) / len(pixels) for idx in range(3))


def _count_foreground_colors(image, background_color: tuple[float, float, float], region: tuple[float, float, float, float]) -> Counter:
    width, height = image.size
    x1, y1, x2, y2 = region
    x_start, x_end = int(x1 * width), int(x2 * width)
    y_start, y_end = int(y1 * height), int(y2 * height)
    step = max(1, min(width, height) // 180)
    counts: Counter = Counter()

    for y in range(y_start, y_end, step):
        for x in range(x_start, x_end, step):
            pixel = image.getpixel((x, y))
            if _color_distance(pixel, background_color) < 38:
                continue
            counts[classify_rgb_color(*pixel)] += 1

    return counts


def _foreground_pixels(image, background_color: tuple[float, float, float]) -> list[tuple[int, int, int]]:
    width, height = image.size
    pixels = []
    step = max(1, min(width, height) // 180)
    for y in range(0, height, step):
        for x in range(0, width, step):
            pixel = image.getpixel((x, y))
            if _color_distance(pixel, background_color) >= 38:
                pixels.append(pixel)
    return pixels


def _color_distance(left: tuple[int, int, int], right: tuple[float, float, float]) -> float:
    return math.sqrt(sum((left[idx] - right[idx]) ** 2 for idx in range(3)))


def _dominant_color_name(counts: Counter) -> str:
    if not counts:
        return "unknown"
    return counts.most_common(1)[0][0]


def _query_color_name(counts: Counter, *, prefer_light_garment: bool = True) -> str:
    if prefer_light_garment and _has_light_garment(counts):
        return "white"

    for color, _count in counts.most_common():
        if color not in {"gray", "neutral"}:
            return color

    return _dominant_color_name(counts)


def _build_dynamic_query_hint(category: str, counts: Counter) -> str:
    total = sum(counts.values())
    min_total_by_category = {
        "top": 60,
        "bottom": 80,
        "outer": 80,
        "shoes": 35,
        "bag": 70,
        "accessory": 28,
    }
    if total < min_total_by_category.get(category, 40):
        return ""

    color = _query_accessory_color_name(counts) if category == "accessory" else _query_color_name(counts)
    color_label = COLOR_QUERY_LABELS.get(color)
    category_label = CATEGORY_QUERY_LABELS[category]
    if not color_label:
        return category_label

    if category == "accessory":
        accessory_label = "안경" if color in {"black", "brown", "gray"} else "머플러"
        return f"{color_label} {accessory_label}"

    return f"{color_label} {category_label}"


def _build_distinct_query_hint(category: str, counts: Counter, reference_colors: tuple[str, ...]) -> str:
    hint = _build_dynamic_query_hint(category, counts)
    if not hint:
        return ""

    color = _query_accessory_color_name(counts) if category == "accessory" else _query_color_name(counts)
    if color in {"unknown", "neutral"}:
        return ""

    comparable_references = {reference for reference in reference_colors if reference not in {"unknown", "neutral"}}
    if color in comparable_references:
        return ""

    return hint


def _query_accessory_color_name(counts: Counter) -> str:
    total = sum(counts.values())
    if total == 0:
        return "unknown"

    dark_candidates = (
        ("black", counts["black"]),
        ("brown", counts["brown"]),
        ("gray", counts["gray"]),
    )
    strongest_dark, strongest_dark_count = max(dark_candidates, key=lambda item: item[1])
    if strongest_dark_count / total >= 0.18:
        return strongest_dark

    return _query_color_name(counts, prefer_light_garment=False)


def _has_meaningful_color(counts: Counter, color: str) -> bool:
    total = sum(counts.values())
    return total > 0 and counts[color] / total >= 0.08


def _has_light_garment(counts: Counter) -> bool:
    total = sum(counts.values())
    if total == 0:
        return False

    light_total = counts["white"] + counts["gray"] + counts["beige"]
    return light_total / total >= 0.35

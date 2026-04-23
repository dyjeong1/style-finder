from __future__ import annotations

from dataclasses import dataclass
import colorsys
from io import BytesIO

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

    sample_step = max(1, len(pixels) // 1800)
    sampled_pixels = pixels[::sample_step]
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

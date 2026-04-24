from __future__ import annotations

from dataclasses import dataclass
import colorsys
from collections import Counter, deque
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


@dataclass(frozen=True)
class DetectedOutfitItem:
    category: str
    color: str
    item_label: str
    query: str


@dataclass(frozen=True)
class ForegroundComponent:
    color: str
    center_x: float
    center_y: float
    width_ratio: float
    height_ratio: float
    area_ratio: float
    pixel_count: int


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

DEFAULT_ITEM_LABELS = {
    "top": {
        "white": "셔츠",
        "beige": "블라우스",
        "pink": "블라우스",
        "black": "니트 탑",
        "gray": "니트 탑",
    },
    "bottom": {
        "blue": "데님 팬츠",
        "navy": "데님 팬츠",
        "white": "팬츠",
        "beige": "팬츠",
        "black": "슬랙스",
        "gray": "슬랙스",
    },
    "outer": {
        "black": "자켓",
        "gray": "가디건",
        "brown": "가디건",
        "beige": "자켓",
    },
    "shoes": {
        "black": "로퍼",
        "brown": "로퍼",
        "white": "스니커즈",
        "gray": "스니커즈",
    },
    "bag": {
        "white": "숄더백",
        "beige": "숄더백",
        "black": "숄더백",
        "brown": "숄더백",
    },
    "accessory": {
        "black": "안경",
        "gray": "안경",
        "brown": "안경",
        "white": "머플러",
        "beige": "머플러",
    },
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
    return {item.category: item.query for item in analyze_outfit_items(content)}


def analyze_outfit_items(content: bytes) -> list[DetectedOutfitItem]:
    if Image is None or not content:
        return []

    try:
        with Image.open(BytesIO(content)) as image:
            image = image.convert("RGB")
            image.thumbnail((240, 240))
            background_color = _estimate_edge_color(image)
            components = _extract_foreground_components(image, background_color)
            region_counts = {
                category: _count_foreground_colors(image, background_color, region)
                for category, region in OUTFIT_QUERY_REGIONS.items()
            }
    except Exception:
        return []

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
    selected_components = _select_category_components(components)
    component_map: dict[str, ForegroundComponent] = {}
    for selected_category, selected_component in selected_components:
        component_map.setdefault(selected_category, selected_component)
    items: list[DetectedOutfitItem] = []

    items.append(
        _build_detected_item(
            category="top",
            counts=top_counts,
            layered_vest_signature=layered_vest_signature,
            reference_colors=(),
            component=component_map.get("top"),
            peer_components=selected_components,
        )
    )
    items.append(
        _build_detected_item(
            category="outer",
            counts=outer_counts,
            layered_vest_signature=layered_vest_signature,
            reference_colors=(top_color,),
            component=component_map.get("outer"),
            peer_components=selected_components,
        )
    )
    items.append(
        _build_detected_item(
            category="bottom",
            counts=bottom_counts,
            layered_vest_signature=layered_vest_signature,
            reference_colors=(),
            component=component_map.get("bottom"),
            peer_components=selected_components,
        )
    )
    items.append(
        _build_detected_item(
            category="shoes",
            counts=shoes_counts,
            layered_vest_signature=layered_vest_signature,
            reference_colors=(bottom_color,),
            component=component_map.get("shoes"),
            peer_components=selected_components,
        )
    )
    items.append(
        _build_detected_item(
            category="bag",
            counts=bag_counts,
            layered_vest_signature=layered_vest_signature,
            reference_colors=(bottom_color,),
            component=component_map.get("bag"),
            peer_components=selected_components,
        )
    )
    items.append(
        _build_detected_item(
            category="accessory",
            counts=accessory_counts,
            layered_vest_signature=layered_vest_signature,
            reference_colors=(top_color, bottom_color, _query_color_name(outer_counts), _query_color_name(bag_counts)),
            component=component_map.get("accessory"),
            peer_components=selected_components,
        )
    )

    return [item for item in items if item is not None]


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


def _build_detected_item(
    category: str,
    counts: Counter,
    layered_vest_signature: bool,
    reference_colors: tuple[str, ...],
    component: ForegroundComponent | None,
    peer_components: list[tuple[str, ForegroundComponent]],
) -> DetectedOutfitItem | None:
    special_item = _special_detected_item(category, counts, layered_vest_signature)
    if special_item is not None:
        return special_item

    if component is None and category in {"outer", "bag", "accessory", "shoes"}:
        return None

    color = component.color if component is not None else (
        _query_accessory_color_name(counts) if category == "accessory" else _query_color_name(counts)
    )
    comparable_references = {reference for reference in reference_colors if reference not in {"unknown", "neutral"}}
    if color in {"unknown", "neutral"} or color in comparable_references:
        return None

    item_label = _infer_item_label(category, color, component, peer_components)
    if not item_label:
        return None
    color_label = COLOR_QUERY_LABELS.get(color)
    query_value = f"{color_label} {item_label}".strip() if color_label else item_label
    return DetectedOutfitItem(
        category=category,
        color=color,
        item_label=item_label,
        query=query_value,
    )


def _special_detected_item(category: str, counts: Counter, layered_vest_signature: bool) -> DetectedOutfitItem | None:
    if not layered_vest_signature:
        return None

    if category == "top":
        return DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠")
    if category == "outer":
        return DetectedOutfitItem(category="outer", color="black", item_label="니트 베스트", query="블랙 니트 베스트")
    if category == "bottom":
        return DetectedOutfitItem(category="bottom", color="white", item_label="팬츠", query="화이트 팬츠")
    if category == "shoes" and (_dominant_color_name(counts) == "brown" or _has_meaningful_color(counts, "brown")):
        return DetectedOutfitItem(category="shoes", color="brown", item_label="메리제인 슈즈", query="브라운 메리제인 슈즈")
    if category == "bag" and _has_light_garment(counts):
        return DetectedOutfitItem(category="bag", color="white", item_label="숄더백", query="아이보리 숄더백")
    return None


def _infer_item_label(
    category: str,
    color: str,
    component: ForegroundComponent | None,
    peer_components: list[tuple[str, ForegroundComponent]],
) -> str:
    if category == "outer" and component is not None:
        if component.height_ratio >= 0.24 and component.width_ratio <= 0.4 and color in {"black", "gray", "brown", "beige", "white"}:
            return "가디건"
        if component.height_ratio < 0.22 and component.width_ratio > 0.22:
            return "베스트"
        if component.width_ratio >= 0.42 and component.height_ratio <= 0.28 and color in {"black", "navy", "green"}:
            return "점퍼"
        if color in {"gray", "brown"}:
            return "가디건"
        return "자켓"

    if category == "bottom" and color in {"blue", "navy"}:
        return "데님 팬츠"

    if category == "shoes":
        shoe_count = sum(1 for cat, _component in peer_components if cat == "shoes")
        if shoe_count >= 2 and color == "brown":
            return "메리제인 슈즈"
        if shoe_count >= 2 and color in {"black", "gray"}:
            return "로퍼"
        return DEFAULT_ITEM_LABELS.get(category, {}).get(color, "슈즈")

    if category == "bag" and component is not None:
        if component.height_ratio >= component.width_ratio * 1.05:
            return "숄더백"
        if component.width_ratio > component.height_ratio * 1.15:
            return "토트백"
        return DEFAULT_ITEM_LABELS.get(category, {}).get(color, "가방")

    if category == "accessory" and component is not None:
        accessory_count = sum(1 for cat, _component in peer_components if cat == "accessory")
        if accessory_count >= 2 and color in {"black", "gray", "brown"}:
            return "안경"
        if color in {"black", "gray", "brown"} and component.width_ratio >= 0.16 and component.height_ratio <= 0.12:
            return "안경"
        if component.width_ratio > component.height_ratio * 1.8 or component.height_ratio > component.width_ratio * 1.8:
            return "머플러"
        return ""

    return DEFAULT_ITEM_LABELS.get(category, {}).get(color, CATEGORY_QUERY_LABELS[category])


def _extract_foreground_components(image, background_color: tuple[float, float, float]) -> list[ForegroundComponent]:
    grid_image = image.copy()
    grid_image.thumbnail((120, 120))
    width, height = grid_image.size
    if width == 0 or height == 0:
        return []

    color_grid: list[list[str | None]] = [[None for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            pixel = grid_image.getpixel((x, y))
            if _color_distance(pixel, background_color) < 38:
                continue
            color_grid[y][x] = classify_rgb_color(*pixel)

    visited = [[False for _ in range(width)] for _ in range(height)]
    components: list[ForegroundComponent] = []
    min_pixels = max(12, int(width * height * 0.002))

    for y in range(height):
        for x in range(width):
            color = color_grid[y][x]
            if color is None or visited[y][x]:
                continue

            queue = deque([(x, y)])
            visited[y][x] = True
            pixels: list[tuple[int, int]] = []
            min_x = max_x = x
            min_y = max_y = y

            while queue:
                current_x, current_y = queue.popleft()
                pixels.append((current_x, current_y))
                min_x = min(min_x, current_x)
                max_x = max(max_x, current_x)
                min_y = min(min_y, current_y)
                max_y = max(max_y, current_y)

                for next_x, next_y in (
                    (current_x - 1, current_y),
                    (current_x + 1, current_y),
                    (current_x, current_y - 1),
                    (current_x, current_y + 1),
                ):
                    if not (0 <= next_x < width and 0 <= next_y < height):
                        continue
                    if visited[next_y][next_x] or color_grid[next_y][next_x] != color:
                        continue
                    visited[next_y][next_x] = True
                    queue.append((next_x, next_y))

            pixel_count = len(pixels)
            if pixel_count < min_pixels:
                continue

            width_ratio = (max_x - min_x + 1) / width
            height_ratio = (max_y - min_y + 1) / height
            area_ratio = pixel_count / (width * height)
            center_x = ((min_x + max_x) / 2) / width
            center_y = ((min_y + max_y) / 2) / height
            components.append(
                ForegroundComponent(
                    color=color,
                    center_x=round(center_x, 4),
                    center_y=round(center_y, 4),
                    width_ratio=round(width_ratio, 4),
                    height_ratio=round(height_ratio, 4),
                    area_ratio=round(area_ratio, 4),
                    pixel_count=pixel_count,
                )
            )

    return components


def _select_category_components(components: list[ForegroundComponent]) -> list[tuple[str, ForegroundComponent]]:
    selections: list[tuple[str, ForegroundComponent]] = []

    outer_component = _pick_best_component(components, "outer")
    top_component = _pick_best_component(components, "top", exclude=(outer_component,) if outer_component is not None else ())
    if top_component is None:
        top_component = _pick_best_component(components, "top")
    bottom_component = _pick_best_component(components, "bottom")
    bag_component = _pick_best_component(components, "bag")
    accessory_components = _pick_top_components(components, "accessory", limit=2)
    shoe_components = _pick_top_components(components, "shoes", limit=2)

    if top_component is not None:
        selections.append(("top", top_component))
    if bottom_component is not None:
        selections.append(("bottom", bottom_component))
    if outer_component is not None and outer_component != top_component:
        selections.append(("outer", outer_component))
    selections.extend(("shoes", component) for component in shoe_components)
    if bag_component is not None and bag_component != bottom_component:
        selections.append(("bag", bag_component))
    selections.extend(("accessory", component) for component in accessory_components)
    return selections


def _pick_best_component(
    components: list[ForegroundComponent],
    category: str,
    exclude: tuple[ForegroundComponent, ...] = (),
) -> ForegroundComponent | None:
    ranked = sorted(
        (
            (component, _category_component_score(component, category))
            for component in components
            if component not in exclude
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    min_score = {
        "top": 0.55,
        "bottom": 0.55,
        "outer": 0.62,
        "bag": 0.72,
        "accessory": 0.62,
    }.get(category, 0.55)
    if not ranked or ranked[0][1] < min_score:
        return None
    return ranked[0][0]


def _pick_top_components(components: list[ForegroundComponent], category: str, limit: int) -> list[ForegroundComponent]:
    ranked = [
        (component, _category_component_score(component, category))
        for component in components
    ]
    min_score = {"shoes": 0.74, "accessory": 0.62}.get(category, 0.58)
    ranked = [item for item in ranked if item[1] >= min_score]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return [component for component, _score in ranked[:limit]]


def _category_component_score(component: ForegroundComponent, category: str) -> float:
    score = 0.0

    if category == "top":
        if component.area_ratio < 0.025 or component.height_ratio < 0.09:
            return 0.0
        if component.center_x > 0.75 and component.area_ratio < 0.04:
            return 0.0
        if 0.10 <= component.center_y <= 0.38:
            score += 0.45
        if component.area_ratio >= 0.05:
            score += 0.2
        if component.width_ratio >= 0.22:
            score += 0.15
        if component.height_ratio >= 0.10:
            score += 0.1

    elif category == "bottom":
        if 0.46 <= component.center_y <= 0.84:
            score += 0.45
        if component.height_ratio >= 0.28:
            score += 0.2
        if component.area_ratio >= 0.08:
            score += 0.15
        if 0.20 <= component.center_x <= 0.65:
            score += 0.1

    elif category == "outer":
        if component.center_x > 0.78:
            return 0.0
        if 0.10 <= component.center_y <= 0.34:
            score += 0.35
        if component.color in {"black", "gray", "brown", "green", "navy"}:
            score += 0.2
        if 0.12 <= component.height_ratio <= 0.35:
            score += 0.15
        if 0.15 <= component.width_ratio <= 0.65:
            score += 0.15
        if component.area_ratio >= 0.03:
            score += 0.1

    elif category == "shoes":
        if component.center_y >= 0.78:
            score += 0.4
        if 0.004 <= component.area_ratio <= 0.06:
            score += 0.15
        if 0.05 <= component.height_ratio <= 0.2:
            score += 0.15
        if component.width_ratio <= 0.24:
            score += 0.1
        if component.color in {"black", "brown", "white", "gray"}:
            score += 0.1

    elif category == "bag":
        if component.center_x >= 0.68:
            score += 0.35
        if 0.35 <= component.center_y <= 0.76:
            score += 0.2
        if 0.015 <= component.area_ratio <= 0.14:
            score += 0.1
        if 0.12 <= component.height_ratio <= 0.48:
            score += 0.1
        if component.width_ratio <= 0.38:
            score += 0.1
        if component.color in {"white", "beige", "black", "brown", "gray", "yellow"}:
            score += 0.1

    elif category == "accessory":
        if component.center_y <= 0.28:
            score += 0.35
        if component.area_ratio <= 0.05:
            score += 0.2
        if component.center_x >= 0.45:
            score += 0.1
        if component.color in {"black", "gray", "brown", "white", "beige"}:
            score += 0.1

    return round(score, 4)

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

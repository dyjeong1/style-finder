from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image

from src.services.store import ProductRecord


@dataclass(frozen=True)
class VisionRerankerConfig:
    enabled: bool = False
    provider: str = "clip"
    model_name: str = "openai/clip-vit-base-patch32"
    timeout_seconds: float = 1.5
    max_image_bytes: int = 2_000_000
    max_candidates: int = 10


class VisionReranker:
    def __init__(self, config: VisionRerankerConfig) -> None:
        self.config = config

    def score_products(self, upload_content: bytes, products: list[ProductRecord]) -> dict[str, float]:
        if not self.config.enabled or not upload_content or not products:
            return {}

        if self.config.provider != "clip":
            return {}

        clip_runtime = _load_clip_runtime(self.config.model_name)
        if clip_runtime is None:
            return {}

        upload_image = _load_image_from_bytes(upload_content)
        if upload_image is None:
            return {}

        candidate_images: list[tuple[ProductRecord, object]] = []
        for product in products[: self.config.max_candidates]:
            product_image = self._load_remote_image(product.image_url)
            if product_image is None:
                continue
            candidate_images.append((product, product_image))

        if not candidate_images:
            return {}

        product_ids = [product.id for product, _image in candidate_images]
        images = [upload_image] + [image for _product, image in candidate_images]
        similarities = clip_runtime.compute_image_similarities(images)
        return {
            product_id: round(similarity, 4)
            for product_id, similarity in zip(product_ids, similarities)
        }

    def _load_remote_image(self, image_url: str):
        if not image_url.startswith(("http://", "https://")):
            return None

        request = Request(image_url, headers={"User-Agent": "StyleMatchLocal/0.1"}, method="GET")
        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > self.config.max_image_bytes:
                    return None
                content = response.read(self.config.max_image_bytes + 1)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError):
            return None

        if len(content) > self.config.max_image_bytes:
            return None
        return _load_image_from_bytes(content)


def _load_image_from_bytes(content: bytes):
    try:
        with Image.open(BytesIO(content)) as image:
            return image.convert("RGB")
    except Exception:
        return None


@lru_cache(maxsize=1)
def _load_clip_runtime(model_name: str):
    try:
        import torch
        from transformers import CLIPModel, CLIPProcessor
    except Exception:
        return None

    class ClipRuntime:
        def __init__(self, model_name_value: str) -> None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.processor = CLIPProcessor.from_pretrained(model_name_value)
            self.model = CLIPModel.from_pretrained(model_name_value)
            self.model.to(self.device)
            self.model.eval()

        def compute_image_similarities(self, images: list[object]) -> list[float]:
            upload_image = images[0]
            product_images = images[1:]
            if not product_images:
                return []

            with torch.no_grad():
                upload_inputs = self.processor(images=[upload_image], return_tensors="pt")
                upload_inputs = {key: value.to(self.device) for key, value in upload_inputs.items()}
                upload_features = self.model.get_image_features(**upload_inputs)
                upload_features = upload_features / upload_features.norm(dim=-1, keepdim=True)

                product_inputs = self.processor(images=product_images, return_tensors="pt")
                product_inputs = {key: value.to(self.device) for key, value in product_inputs.items()}
                product_features = self.model.get_image_features(**product_inputs)
                product_features = product_features / product_features.norm(dim=-1, keepdim=True)

                similarities = (upload_features @ product_features.T).squeeze(0).tolist()
                if isinstance(similarities, float):
                    return [float(similarities)]
                return [float(value) for value in similarities]

    return ClipRuntime(model_name)

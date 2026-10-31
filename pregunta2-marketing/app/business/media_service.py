from pathlib import Path
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from app.config import GENERATED, STORAGE
from app.data.repositories import CampaignRepository


class MediaService:
    def __init__(self, repository: CampaignRepository):
        self.repository = repository

    def generate(self, campaign_id: int):
        campaign = self.repository.get(campaign_id)
        if not campaign or not campaign.selected_script:
            raise ValueError("Debe seleccionar un guion")
        source = Image.open(STORAGE / campaign.original_path).convert("RGB")
        source = self.fit(source, (1080, 1080))
        variants = [
            self.compose(source, campaign.company, campaign.product, "DESCUBRE", "#102a43", 1.08),
            self.compose(source.filter(ImageFilter.GaussianBlur(1.2)), campaign.company, campaign.product, "CONECTA", "#7c2d12", 1.16),
            self.compose(ImageEnhance.Contrast(source).enhance(1.18), campaign.company, campaign.product, "ACTÚA", "#14532d", 1.04),
        ]
        folder = GENERATED / str(campaign.id)
        folder.mkdir(parents=True, exist_ok=True)
        values = []
        paths = []
        for index, image in enumerate(variants, 1):
            path = folder / f"pieza-{index}.jpg"
            image.save(path, quality=92)
            values.append({"kind": "IMAGE", "path": f"generated/{campaign.id}/{path.name}"})
            paths.append(path)
        video_path = folder / "video.mp4"
        writer = imageio.get_writer(video_path, fps=1, codec="libx264", quality=8, macro_block_size=1)
        for path in paths:
            frame = imageio.imread(path)
            for _ in range(3):
                writer.append_data(frame)
        writer.close()
        values.append({"kind": "VIDEO", "path": f"generated/{campaign.id}/{video_path.name}"})
        self.repository.add_assets(campaign, values)
        return self.repository.get(campaign.id)

    def fit(self, image: Image.Image, size: tuple[int, int]) -> Image.Image:
        ratio = max(size[0] / image.width, size[1] / image.height)
        resized = image.resize((int(image.width * ratio), int(image.height * ratio)))
        left = (resized.width - size[0]) // 2
        top = (resized.height - size[1]) // 2
        return resized.crop((left, top, left + size[0], top + size[1]))

    def compose(self, image: Image.Image, company: str, product: str, action: str, color: str, brightness: float) -> Image.Image:
        output = ImageEnhance.Brightness(image).enhance(brightness)
        overlay = Image.new("RGBA", output.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle((0, 710, 1080, 1080), fill=color + "E6")
        title = self.font(76, True)
        body = self.font(42, False)
        small = self.font(30, False)
        draw.text((64, 748), action, font=small, fill="white")
        draw.text((64, 798), product[:24], font=title, fill="white")
        draw.text((64, 910), f"Una campaña de {company}"[:42], font=body, fill="#e2e8f0")
        draw.rounded_rectangle((64, 984, 370, 1042), radius=18, fill="white")
        draw.text((94, 994), "CONOCE MÁS", font=small, fill=color)
        return Image.alpha_composite(output.convert("RGBA"), overlay).convert("RGB")

    def font(self, size: int, bold: bool):
        candidates = [
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        ]
        path = next((item for item in candidates if item.exists()), None)
        return ImageFont.truetype(str(path), size) if path else ImageFont.load_default(size=size)


import os
from typing import List
from PIL import Image
from io import BytesIO
import base64

from app.services.pexels_fetcher_service import get_images
from app.services.color_extractor_service import create_color_palette_image  
from app.services.color_extractor_service import extract_dominant_colors

def generate_moodboard(image_paths, output_path="app/static/images/moodboard.jpg", grid_size=(3, 2), thumb_size=300, gap=10):
    rows, cols = grid_size
    max_images = rows * cols
    images = []

    for path in image_paths[:max_images]:
        try:
            img = Image.open(path)
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            cropped = img.crop((left, top, left + min_dim, top + min_dim))
            resized = cropped.resize((thumb_size, thumb_size))
            images.append(resized)
        except Exception as e:
            print(f"Failed to process image {path}: {e}")

    if not images:
        raise ValueError("No valid images to generate moodboard.")

    canvas_width = cols * thumb_size + (cols - 1) * gap
    canvas_height = rows * thumb_size + (rows - 1) * gap
    moodboard = Image.new('RGB', (canvas_width, canvas_height), color=(255, 255, 255))

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols
        x = col * (thumb_size + gap)
        y = row * (thumb_size + gap)
        moodboard.paste(img, (x, y))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    moodboard.save(output_path)
    return output_path


def generate_combined_base64(moodboard_path="app/static/images/moodboard.jpg", palette_path="app/static/images/palette.jpg", padding=20):
    try:
        moodboard = Image.open(moodboard_path)
        palette = Image.open(palette_path)

        if palette.width != moodboard.width:
            new_height = int(palette.height * (moodboard.width / palette.width))
            palette = palette.resize((moodboard.width, new_height))

        total_width = moodboard.width
        total_height = moodboard.height + padding + palette.height

        final_image = Image.new("RGB", (total_width, total_height), color=(255, 255, 255))
        final_image.paste(moodboard, (0, 0))
        final_image.paste(palette, (0, moodboard.height + padding))

        buffer = BytesIO()
        final_image.save(buffer, format="JPEG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{img_base64}"

    except Exception as e:
        print(f"Error creating base64 image: {e}")
        return None


def create_moodboard_from_keywords(keywords: List[str]) -> str:
    try:
        image_paths = get_images(keywords, save_dir="app/static/images/temp")

        moodboard_path = generate_moodboard(image_paths)

        colors = extract_dominant_colors(image_paths)
        palette_path = create_color_palette_image(colors)

        moodboard_base64 = generate_combined_base64(moodboard_path, palette_path)
        return moodboard_base64

    except Exception as e:
        print(f"Error in create_moodboard_from_keywords: {e}")
        return None
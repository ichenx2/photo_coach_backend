from colorthief import ColorThief
from PIL import Image, ImageDraw


def extract_dominant_colors(image_paths, palette_size=6):
    colors = []
    for path in image_paths:
        try:
            color_thief = ColorThief(path)
            dominant_color = color_thief.get_color(quality=1)
            colors.append(dominant_color)
        except Exception as e:
            print(f"Failed to extract color from {path}: {e}")
    return colors[:palette_size]

def create_color_palette_image(colors, save_path='app/static/images/palette.jpg', size=(100, 100)):
    width = size[0] * len(colors)
    height = size[1]
    palette = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(palette)

    for i, color in enumerate(colors):
        draw.rectangle(
            [i * size[0], 0, (i + 1) * size[0], height],
            fill=color
        )

    palette.save(save_path)
    return save_path

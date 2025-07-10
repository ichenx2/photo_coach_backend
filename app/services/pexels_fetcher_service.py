import os
import requests


def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def get_images(keywords, save_dir="app/static/temp"):

    if os.path.exists(save_dir):
        for filename in os.listdir(save_dir):
            file_path = os.path.join(save_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    PEXELS_URL = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    os.makedirs(save_dir, exist_ok=True)
    selected_images = []

    for keyword in keywords:
        print(f"Searching for: {keyword}")
        params = {"query": keyword, "per_page": 1}
        try:
            response = requests.get(PEXELS_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["photos"]:
                photo_url = data["photos"][0]["src"]["large"]
                filename = f"{keyword.replace(' ', '_')}.jpg"
                save_path = os.path.join(save_dir, filename)
                download_image(photo_url, save_path)
                selected_images.append(save_path)
                print(f"Downloaded: {save_path}")
            else:
                print(f"No image found for: {keyword}")
        except Exception as e:
            print(f"Error searching for {keyword}: {e}")

    return selected_images

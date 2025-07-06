from app.core.config import settings

def main():
    print("Gemini model:", settings.gemini_model)
    print("API key loaded:", bool(settings.gemini_api_key))

if __name__ == "__main__":
    main()
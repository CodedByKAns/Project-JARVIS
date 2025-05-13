# commands/ai/generate_image.py

import os
import re
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from core.registry import register_command
from voice.tts import speak
from together import Together
import base64

# ✅ Load environment variables from .env
load_dotenv()

# 🔐 API Key from environment
VISION_API_KEY = os.getenv("VISION_API_KEY")
if not VISION_API_KEY:
    raise ValueError("VISION_API_KEY not set in .env file!")

# 📌 Model configuration
FLUX_MODEL = "black-forest-labs/FLUX.1-schnell-Free"

# 📁 Image save path
TEMP_FOLDER = "temp"
IMAGE_PATH = os.path.join(TEMP_FOLDER, "generated_image.png")
os.makedirs(TEMP_FOLDER, exist_ok=True)

# 🧠 Initialize Together client for FLUX model
together_client = Together(api_key=VISION_API_KEY)

# 🧠 Function to generate image using Together FLUX model
def generate_image(prompt):
    speak(f"Generating an image for: {prompt}")
    print(f"🔹 Sending prompt to FLUX model: {prompt}")

    try:
        response = together_client.images.generate(
            model=FLUX_MODEL,
            prompt=prompt,
            steps=4,  # FLUX model requires steps between 1 and 4
            response_format="b64_json"
        )
        image_data = base64.b64decode(response.data[0].b64_json)
        image = Image.open(BytesIO(image_data))
        image.save(IMAGE_PATH)
        image.show()
        print(f"✅ Image saved at {IMAGE_PATH}")
        return IMAGE_PATH
    except Exception as e:
        print("❌ Failed to generate image with FLUX:", e)
        return None

# 🧠 Jarvis command that triggers image generation
@register_command(r"create image", needs_input=True)
def jarvis_generate_image(command):
    # 🎯 Extract actual prompt from command
    prompt = re.sub(r"create image", "", command, flags=re.IGNORECASE).strip()

    if prompt:
        result = generate_image(prompt)
        if result:
            speak("Image generated and displayed.")
        else:
            speak("Sorry, I couldn't generate the image.")
    else:
        speak("Please provide a prompt for the image.")


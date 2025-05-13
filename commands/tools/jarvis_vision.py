import os
import tempfile
import datetime
import base64
from dotenv import load_dotenv
from together import Together
import mss
import requests
import sys
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from voice.tts import speak

from core.conversation import chat_with_jarvis
from core.registry import register_command

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("VISION_API_KEY")

if not TOGETHER_API_KEY:
    print("❌ Error: VISION_API_KEY not found in .env file")
    sys.exit(1)

client = Together(api_key=TOGETHER_API_KEY)

def take_screenshot():
    """Capture a screenshot and return its file path."""
    try:
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        image_path = os.path.join(temp_dir, f"screenshot_{timestamp}.png")
        with mss.mss() as sct:
            sct.shot(output=image_path)
        return image_path
    except Exception as e:
        raise RuntimeError(f"Failed to take screenshot: {e}")

def image_to_base64(image_path):
    """Convert an image file to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.exceptions.HTTPError)
)
def analyze_image(image_path, command):
    """Analyze the screenshot based on the user's command."""
    prompt = (
        f"You are Vision of Jarvis AI, an expert visual assistant designed to help an AI system interpret screenshots of user interfaces. "
        f"The user has issued the following command: '{command}'. "
        f"Analyze the provided screenshot in detail, tailoring your response to the context of the user's command. "
        f"Provide a clear, structured analysis in plain English, keeping it comprehensive yet concise, and prioritize details relevant to the command.\n\n"
        "Structure your response with the following sections:\n\n"
        "1. 🧠 Overall Summary:\n"
        "   - Summarize the interface’s purpose and main functionality.\n"
        "   - Identify the type of interface (e.g., web page, mobile app, desktop application) if apparent.\n\n"
        "2. 🧩 UI Elements:\n"
        "   - List visible UI elements (e.g., buttons, menus, text fields) with their positions (e.g., top-left, center) and likely functions.\n"
        "   - Emphasize elements relevant to the user's command.\n\n"
        "3. 🔤 Visible Text:\n"
        "   - Transcribe all readable text, noting its context or purpose.\n"
        "   - Highlight text directly related to the command.\n\n"
        "4. 🎨 Design & Layout:\n"
        "   - Describe the color scheme, typography, and aesthetic.\n"
        "   - Comment on the layout’s organization and design patterns.\n\n"
        "5. 🤖 Inference:\n"
        "   - Infer the interface’s purpose and potential user interactions.\n"
        "   - Suggest next actions or areas of interest, especially tied to the command.\n\n"
        "Focus on precision and relevance, avoiding extraneous details. Your analysis should empower the AI to respond effectively to the user's command."
    )
    image_base64 = image_to_base64(image_path)
    print("🔍 Sending image to Together AI...")

    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content

@register_command(r"screen analysis", needs_input=True)
def run_vision_once(command: str):
    """Execute screen analysis based on the user's command."""
    speak("Initiating screen analysis. Please wait a moment.")
    try:
        screenshot_path = take_screenshot()
        print(f"📸 Screenshot taken: {screenshot_path}")

        analysis = analyze_image(screenshot_path, command)
        print("✅ Screen analysis done.")

        # Combine analysis and command with an advanced prompt for Jarvis
        # Combine screen analysis and user command with a highly advanced prompt for Jarvis
        combined_prompt = (
    "🖼️ **Screen Analysis Context:** You are equipped with a comprehensive analysis of the user's current screen, meticulously tailored to their command. "
    "This analysis reveals critical insights into the visual elements, UI structure, and interactive components the user is engaging with. "
    "Your primary objective is to harness this context to deliver a response that is exceptionally precise, relevant, and actionable.\n\n"
    
    "🚀 **Advanced Response Protocol:**\n"
    "1. **Deep Contextual Analysis:** Scrutinize the screen analysis to fully understand the user's environment. Pinpoint key interface elements—such as buttons, text fields, or menus—that align with the command.\n"
    
    "2. **Laser-Focused Answer:** Craft a succinct, accurate, and complete response that directly resolves the user's command. Eliminate fluff, prioritizing clarity and utility.\n"
    
    "3. **Seamless Analysis Integration:** Incorporate insights from the screen analysis fluidly into your response. Reference specific UI components conversationally, only when they enhance the answer’s relevance.\n"
    
    "4. **Proactive Intelligence:** Elevate the interaction by offering smart, context-driven suggestions or next steps. Leverage the screen analysis to anticipate the user’s needs and recommend actions tied to visible elements.\n"
    
    "5. **Engaging Conversational Flow:** Respond in a natural, intuitive tone that feels like a human dialogue. Avoid robotic phrasing, ensuring the interaction is smooth and approachable.\n\n"
    
    f"**Screen Analysis:**\n{analysis}\n\n"
    f"**User Command:** {command}\n\n"
    
    "Execute this protocol to produce a response that not only answers the command with pinpoint accuracy but also enriches the user’s experience with insightful suggestions. "
    "Your mission is to maximize helpfulness, maintain brevity, and keep the conversation dynamic and engaging."
)
        # Pass the combined prompt to Jarvis
        chat_with_jarvis(combined_prompt)

    except Exception as e:
        error_message = f"❌ Vision analysis failed: {e}"
        print(error_message)
        speak("Sorry, I couldn’t complete the screen analysis. Please try again later.")

    finally:
        if 'screenshot_path' in locals():
            try:
                os.remove(screenshot_path)
                print(f"🗑️ Deleted screenshot: {screenshot_path}")
            except Exception as e:
                print(f"⚠️ Screenshot cleanup error: {e}")

def analyze_uploaded_image(image_path: str, command: str):
    """Analyze the uploaded image based on the user's command."""
    speak("Analyzing the uploaded image. Please wait a moment.")
    try:
        analysis = analyze_image(image_path, command)
        print("✅ Image analysis done.")

        # Combine analysis and command with an advanced prompt for Jarvis
        combined_prompt = (
            "🖼️ **Image Analysis Context:** You are equipped with a comprehensive analysis of the uploaded image, tailored to the user's command. "
            "Your primary objective is to harness this context to deliver a response that is exceptionally precise, relevant, and actionable.\n\n"
            "🚀 **Advanced Response Protocol:**\n"
            "1. **Deep Contextual Analysis:** Scrutinize the image analysis to fully understand the content. Pinpoint key elements that align with the command.\n"
            "2. **Laser-Focused Answer:** Craft a succinct, accurate, and complete response that directly resolves the user's command.\n"
            "3. **Seamless Analysis Integration:** Incorporate insights from the image analysis fluidly into your response.\n"
            "4. **Proactive Intelligence:** Offer smart, context-driven suggestions or next steps based on the image content.\n"
            "5. **Engaging Conversational Flow:** Respond in a natural, intuitive tone.\n\n"
            f"**Image Analysis:**\n{analysis}\n\n"
            f"**User Command:** {command}\n\n"
            "Execute this protocol to produce a response that maximizes helpfulness and keeps the conversation dynamic."
        )
        # Pass the combined prompt to Jarvis
        chat_with_jarvis(combined_prompt)

    except Exception as e:
        error_message = f"❌ Image analysis failed: {e}"
        print(error_message)
        speak("Sorry, I couldn’t complete the image analysis. Please try again later.")
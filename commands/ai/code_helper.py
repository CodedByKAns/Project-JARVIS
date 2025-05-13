from core.conversation import chat_with_jarvis
from voice.tts import speak
from core.registry import register_command

@register_command(r"code helper", needs_input=True)
def coding_assistant(prompt):
    speak("Your query has been forwarded to the JARVIS Coding Agent. Please allow a moment for processing.")
    import requests
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # OpenRouter API settings
    API_KEY = os.getenv("CODER_ASSISTANT")
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "qwen/qwen-2.5-coder-32b-instruct:free"

    # Check API key
    if not API_KEY:
        raise ValueError("Error: OPENROUTER_API_KEY not found in environment variables or .env file")

    # Function to call API with advanced prompt engineering
    def get_coding_assistant_response(prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # Enhanced user message with specific instructions
        user_message = f"{prompt}\n\nPlease provide a code snippet in the specified language and explain how it works. If an advanced solution is requested, provide a more efficient or sophisticated approach."
        
        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a coding assistant powered by Qwen2.5-Coder. Your task is to provide accurate and detailed coding help, including code snippets and explanations. Tailor your response to the user's specifications, such as programming language and level of advancement."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 512,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Error in API request: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error in parsing API response: {str(e)}"

    # Get the response from the API
    assistant_response = get_coding_assistant_response(prompt)

    # Construct message for chat_with_jarvis based on response
    if assistant_response.startswith("Error:"):
        jarvis_message = (
            f"The user requested: '{prompt}'. "
            f"However, there was an error in getting the coding assistant's response: '{assistant_response}'. "
            f"Please inform the user about the error and suggest possible actions."
        )
    else:
        jarvis_message = (
            f"The user requested: '{prompt}'. "
            f"The coding assistant provided the following response: '{assistant_response}'. "
            f"Please provide an accurate response based on this information."
        )
    
    # Call chat_with_jarvis with robust exception handling
    try:
        return chat_with_jarvis(jarvis_message)
    except Exception as e:
        return f"Error in processing with chat_with_jarvis: {str(e)}"

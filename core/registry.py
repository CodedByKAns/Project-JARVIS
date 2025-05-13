import re
import os
import requests
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_CHAT_URL = "https://api.cohere.ai/v1/chat"

# Command registry ab compiled patterns store karega
command_registry = {}

def register_command(label, pattern=None, needs_input=False):
    regex = pattern if pattern else rf"\b{label}\b"
    compiled_pattern = re.compile(regex, flags=re.IGNORECASE)  # Compile karo yahan

    def decorator(func):
        command_registry[label.lower()] = (compiled_pattern, func, needs_input)
        return func

    return decorator

def match_command(user_input):
    user_input = user_input.strip().lower()
    for label, (compiled_pattern, func, needs_input) in command_registry.items():
        if compiled_pattern.search(user_input):  # Compiled pattern use karo
            return func, needs_input

    label_guess = get_command_from_cohere(user_input)
    if label_guess and label_guess.lower() in command_registry:
        _, func, needs_input = command_registry[label_guess.lower()]
        return func, needs_input

    return None, None



def get_command_from_cohere(user_input):
    """Use Cohere to infer the most relevant command label with advanced prompt engineering."""
    if not COHERE_API_KEY:
        print("❌ Error: Missing COHERE_API_KEY.")
        return None

    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }

    command_labels = list(command_registry.keys())
    command_list = "\n".join([f"- {label}" for label in command_labels])
    
    # Very advanced prompt engineering
    prompt = (
        f"You are Jarvis, an advanced AI voice assistant. Your task is to understand the user's intent and map their request to one of the following command labels:\n\n"
        f"{command_list}\n\n"
        "To do this, analyze the user's request and determine what they want to achieve or what information they are seeking. Then, select the command label that best matches their intent. If the request does not clearly match any command label, respond with 'unknown'.\n\n"
        "Guidelines:\n"
        "- Focus on the user's intent, not just the literal words.\n"
        "- Select only one command label.\n"
        f"User request: \"{user_input}\"\n\n"
        "Command label:"
    )

    payload = {
        "message": prompt,
        "model": "command-r-plus-08-2024",
        "temperature": 0.1,  # Low for precision
        "max_tokens": 10,    # Enough for a single-word response
        "p": 0.9,            # High focus on probable outputs
    }

    try:
        response = requests.post(COHERE_CHAT_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        guess = result.get("text", "").strip().lower()
        
        # Ensure exact command label match
        for label in command_labels:
            if label.lower() in guess:
                guess = label.lower()
                break
                
        if "unknown" in guess or guess not in [label.lower() for label in command_labels]:
            print("🤖 Cohere couldn't match to any command")
            return None
            
        print(f"🤖 Cohere matched command: {guess}")
        return guess
    except requests.exceptions.RequestException as err:
        print(f"⚠️ Cohere API error: {err}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error from Cohere: {e}")
        return None

def print_all_registered_commands():
    if not command_registry:
        print("📭 No commands registered.")
        return
    
    print("📋 Registered Commands:")
    for label, (pattern, _, needs_input) in command_registry.items():
        print(f"🔹 Label: {label} | Pattern: {pattern} | Needs Input: {needs_input}")


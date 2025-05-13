
# 🤖 JARVIS - AI Assistant for Windows

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square" alt="Status: Active"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square" alt="Python: 3.9+"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/Voice%20Controlled-Yes-blueviolet?style=flat-square" alt="Voice Controlled: Yes"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square" alt="Version: 1.0.0"/>
</p>

<p align="center">
  <b>JARVIS: A voice-controlled AI assistant for Windows, inspired by Iron Man’s iconic companion, designed to boost productivity with automation, media generation, system control, and context-aware conversations in English and Hinglish.</b>
</p>

---

## 🧠 Overview

**JARVIS** ("Just A Rather Very Intelligent System") is an open-source AI assistant tailored for Windows users. Drawing inspiration from *Iron Man*, it combines speech recognition, text-to-speech, and advanced APIs to deliver a powerful, voice-activated experience. Whether you’re a developer needing coding help, a student managing tasks, or a professional streamlining workflows, JARVIS adapts to your needs with automation and personalized, desi-flavored conversations.

---

## 🌟 Key Features

### Voice Interaction & Automation
- Control applications, windows, and system settings effortlessly.
- Generate media like images and YouTube content on command.
- Execute utilities such as clearing temp files or adjusting brightness.

### Conversational AI
- **Personalized Responses**: Tailored replies using your profile and preferences.
- **Context Awareness**: Responses based on time, location, and past interactions.
- **Hinglish Vibe**: A friendly mix of English and Hindi for relatable chats.
- **Memory System**: Remembers your goals, facts, and moods for smarter interactions.

<details>
<summary><b>Dive Into Conversational Features</b></summary>

| **Feature**                | **Description**                                                                 |
|----------------------------|---------------------------------------------------------------------------------|
| Personalized Responses     | Uses user data (e.g., name, preferences) for custom replies.                   |
| Context Awareness          | Factors in time, location, and history for relevant answers.                   |
| Memory System              | Stores and recalls preferences, goals, and facts.                              |
| Hinglish Tone              | Blends English and Hindi for a desi, engaging style.                           |
| Proactive Suggestions      | Offers task reminders or ideas based on your goals.                            |
| Emotional Intelligence     | Adapts tone to your mood for empathetic responses.                             |
| Vector Embeddings          | Powers context retrieval with Cohere’s embedding tech.                         |

</details>

---

## 🚀 Automation Commands

Explore JARVIS’s automation prowess—click to see the full list:

<details>
<summary><b>View Automation Commands</b></summary>

| **Command**                | **Description**                                          |
|----------------------------|----------------------------------------------------------|
| "Code helper"             | Coding assistance via OpenRouter API.                   |
| "Create image"            | Generates images with Cohere API (Flux model).          |
| "Screenshot"              | Captures your current screen.                           |
| "Open [app]"              | Launches apps (e.g., "Open Chrome").                    |
| "Close [app]"             | Closes apps (e.g., "Close Chrome").                     |
| "Shutdown PC"             | Powers down your computer.                              |
| "Play on YouTube"         | Streams YouTube videos.                                 |
| "Control brightness"      | Adjusts screen brightness.                              |

</details>

---

## ⚙️ Installation

Set up JARVIS on your Windows machine with these steps:

### 📋 Prerequisites
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.9 or higher
- **Git**: For cloning the repo
- **Microphone**: For voice commands
- **API Keys**: Together API, OpenRouter API, Cohere API

### 🛠️ Steps
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/kaif-ansari-jarvis/JARVIS.git
   cd JARVIS
   ```
2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Add API Keys**:
   - Create a `.env` file:
     ```env
     TOGETHER_API_KEY=your_together_api_key
     OPENROUTER_API_KEY=your_openrouter_api_key
     COHERE_API_KEY=your_cohere_api_key
     ```
5. **Launch JARVIS**:
   ```bash
   python main.py
   ```

---

## 🧪 Usage

Press **Ctrl + Shift + J** to wake JARVIS. Speak naturally, and it responds with voice and a sleek popup. Try these:

- "Code helper" → "Write a Python loop."
- "Create image" → "Make a sunset painting."
- "Shutdown PC" → Shuts down your system.
- "Play on YouTube" → "Play 'Despacito'."

---

## 🛠️ Tech Stack

- **Speech Recognition**: `pyttsx3`
- **Text-to-Speech**: `edge_tts`
- **Vision**: Together API
- **Code Support**: OpenRouter API
- **Image Creation**: Cohere API (Flux)
- **Interface**: Dynamic popup via Ctrl + Shift + J

---

## 🔍 How It Works

1. **Voice Capture**: `pyttsx3` listens and converts speech to text.
2. **Command Match**: Maps input to actions or API calls.
3. **Execution**: Performs tasks or fetches data.
4. **Output**: Speaks via `edge_tts` and shows a popup.

---

## 🤝 Contributing

We’d love your help! Here’s how:
1. Fork the repo.
2. Branch out: `git checkout -b feature/your-idea`.
3. Commit: `git commit -m "Added cool feature"`.
4. Push: `git push origin feature/your-idea`.
5. Submit a pull request.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Contact

- **Author**: Kaif Ansari
- **GitHub**: [kaif-ansari-jarvis](https://github.com/kaif-ansari-jarvis)
- **Email**: kaif.ansari@example.com

---

<p align="center">
  <b>JARVIS: Your smart, desi AI sidekick for a next-level Windows experience.</b><br>
  <i>Actively evolving with new features—stay tuned!</i>
</p>

# 🤖 JARVIS - AI Assistant for Windows

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square"/>
  <img src="https://img.shields.io/badge/Voice%20Controlled-Yes-blueviolet?style=flat-square"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square"/>
</p>

<p align="center">
  <b>JARVIS: A voice-controlled AI assistant for Windows, inspired by Iron Man's iconic companion, designed to enhance productivity through automation, screen analysis, media generation, and system control.</b>
</p>

---

## 🧠 Overview

**JARVIS** ("Just A Rather Very Intelligent System") is an open-source, voice-activated AI assistant built for Windows. Inspired by the fictional JARVIS from *Iron Man*, it leverages speech recognition, text-to-speech, and advanced APIs to perform a wide range of tasks via natural language commands. From coding assistance to system management, JARVIS is tailored for developers, students, and professionals seeking to streamline their workflows.

### 🌟 Key Capabilities
- **Voice Interaction**: Control your PC hands-free with intuitive voice commands.
- **Automation**: Manage applications, windows, and system functions effortlessly.
- **Media Generation**: Create images and handle YouTube content with ease.
- **Screen Analysis**: Analyze live screen content for insights and automation.
- **System Utilities**: Perform tasks like clearing temp files, adjusting brightness, and more.

---

# 🤖 JARVIS - Context-Aware Conversational AI

<p align="center">
  <img src="https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Voice%20Enabled-Yes-blueviolet?style=flat-square"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square"/>
</p>

<p align="center">
  <b>JARVIS: A voice-enabled, context-aware AI assistant inspired by Iron Man’s JARVIS, delivering personalized, conversational responses with a friendly Hinglish tone.</b>
</p>
<details>
<summary><b>Show Context Aware Feature of Jarvis</b></summary>


---

## 🧠 Overview

**JARVIS** ("Just A Rather Very Intelligent System") is an AI assistant designed for natural, context-aware conversations. Built with a desi, tech-savvy vibe, JARVIS leverages advanced memory and NLP to store and recall user preferences, goals, and facts, responding with a mix of English and Hinglish for a relatable, engaging experience. The `conversation.py` module powers JARVIS’s core conversational capabilities.

---

## 🌟 Conversational Features

JARVIS offers a robust set of conversational features, enabling personalized and context-aware interactions:

| **Feature**                       | **Description**                                                                 |
|-----------------------------------|--------------------------------------------------------------------------------|
| **Personalized Responses**        | Tailors replies using user profile data (e.g., name, preferences).             |
| **Context Awareness**             | Incorporates time, location, and past interactions for relevant responses.     |
| **Memory System**                 | Stores and retrieves user facts, preferences, goals, and mood history.         |
| **Vector Embeddings**             | Uses Cohere embeddings for similarity-based context retrieval.                 |
| **Hinglish Tone**                 | Combines English and Hindi for a friendly, desi conversational style.          |
| **Predefined Responses**          | Provides quick replies for common queries (e.g., “What’s the time?”).          |
| **Proactive Suggestions**         | Offers reminders or actions based on user goals (e.g., task suggestions).      |
| **Emotional Intelligence**        | Adjusts tone based on detected user mood for empathetic interactions.          |
| **Error Handling**                | Gracefully manages API errors and speech output failures.                      |

---

## 🛠️ Technical Details

### Core Components
- **AdvancedVectorMemory**:
  - Stores user data (facts, preferences, goals, mood) in JSON files (`vectors.json`, `messages.json`, `user_profile.json`, `embedding_cache.json`).
  - Uses Cohere’s `embed-english-v3.0` for vector embeddings and similarity-based context retrieval.
  - Categorizes messages (e.g., preference, fact, goal) using Cohere’s `command-r-plus`.
  - Prunes outdated or low-confidence data (30-day limit or confidence > 0.7).
  - Generates proactive suggestions based on recent or high-confidence user data.
- **JarvisAI**:
  - Manages user interactions via text or voice input.
  - Processes queries with Cohere’s `command-r-plus` for general responses.
  - Handles predefined responses for common queries (e.g., time, date).
  - Supports memory commands (e.g., “remember”, “forget”) for user data management.
  - Limits chat history to 21 messages for efficient memory usage.

### Dependencies
- **Python Libraries**: `cohere`, `requests`, `numpy`, `asyncio`, `json`, `dotenv`, `hashlib`, `logging`, `collections.Counter`.
- **External APIs**:
  - Cohere: `embed-english-v3.0` (embeddings), `command-r-plus` (text generation).
- **Custom Modules**: `voice.tts` for text-to-speech output.

### Technical Highlights
- **Embedding-Based Memory**: Combines Cohere embeddings, tag overlap, and relevance scores for precise context retrieval.
- **Dynamic Context**: Integrates time, location, and user profile for tailored responses.
- **Efficient Storage**: Caches embeddings and prunes old data to optimize performance.
- **Robust Logging**: Tracks errors for debugging and reliability.

---

## 🔍 How It Works

1. **Input Processing**: Accepts text or voice input (voice requires additional setup).
2. **Context Retrieval**: Fetches relevant user data using vector embeddings and tags.
3. **Query Handling**: Matches queries to predefined responses or processes them via Cohere’s NLP.
4. **Response Generation**: Delivers personalized replies via text and voice in a Hinglish tone.
5. **Memory Management**: Stores significant user data (e.g., preferences, goals) and prunes outdated entries.

---

## 📝 Notes
- JARVIS is in development, with some features (e.g., automation commands, GUI integration) not yet implemented in `conversation.py`.
- The system focuses on conversational logic, with voice output partially implemented via `voice.tts`.

---

<p align="center">
  <b>JARVIS—your desi AI companion for smarter, context-aware conversations.</b>
</p>

---

</details>

## 🚀 Automation Features

JARVIS supports an extensive set of commands for productivity and convenience. Click below to view the full list:

<details>
<summary><b>Show Features</b></summary>

| **Command**                       | **Description**                                          |
|-----------------------------------|----------------------------------------------------------|
| "Code helper"                    | Provides coding assistance via OpenRouter API            |
| "Create image"                   | Generates images using Cohere API with Flux model        |
| "Screenshot"                     | Captures the current screen                              |
| "Open/Start/Launch/Run [app]"    | Opens specified applications (e.g., "Open Chrome")       |
| "Close/Terminate/Exit [app]"     | Closes specified applications (e.g., "Close Chrome")     |
| "Delete Chrome history"          | Clears Chrome browsing history                           |
| "File opener"                    | Opens specified files                                    |
| "Minimize all open windows"      | Minimizes all active windows                             |
| "Maximize active window"         | Maximizes the current window                             |
| "Minimize active window"         | Minimizes the current window                             |
| "Close activate window"          | Closes the current window                                |
| "Switch window"                  | Switches between open windows                            |
| "Shutdown PC"                    | Shuts down the computer                                  |
| "Restart PC"                     | Restarts the computer                                    |
| "Lock PC"                        | Locks the computer                                       |
| "Log off"                        | Logs off the current user                                |
| "Clear temporary files"          | Deletes temporary files                                  |
| "Enable dark mode"               | Enables system dark mode                                 |
| "Disable dark mode"              | Disables system dark mode                                |
| "Empty recycle bin"              | Empties the recycle bin                                  |
| "IP address"                     | Retrieves and speaks your IP address                     |
| "Control brightness"             | Adjusts screen brightness                                |
| "Control volume"                 | Adjusts system volume                                    |
| "Share file"                     | Shares specified files                                   |
| "Screen analysis"                | Analyzes screen content using Together API               |
| "Play on YouTube"                | Plays YouTube videos                                     |
| "Download YouTube video"         | Downloads YouTube videos                                 |

</details>

---

## ⚙️ Installation

Follow these steps to set up JARVIS on your Windows system.

### 📋 Prerequisites
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.9+
- **Git**: For cloning the repository
- **Microphone**: For voice input
- **Internet**: For API-based features
- **API Keys**: From Together API, OpenRouter API, and Cohere API

### 🛠️ Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kaif-ansari-jarvis/JARVIS.git
   cd JARVIS
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure API Keys**:
   - Create a `.env` file in the root directory:
     ```env
     TOGETHER_API_KEY=your_together_api_key
     OPENROUTER_API_KEY=your_openrouter_api_key
     COHERE_API_KEY=your_cohere_api_key
     ```
5. **Run JARVIS**:
   ```bash
   python main.py
   ```

---

## 🧪 Usage

Activate JARVIS by pressing **Ctrl + Shift + J**. Speak commands naturally, and JARVIS will respond via a dynamic popup and voice output. Examples:

- "Code helper" → "Write a Python function to sort a list"
- "Create image" → "Generate an image of a forest"
- "Shutdown PC" → Initiates system shutdown
- "Play on YouTube" → "Play 'Bohemian Rhapsody'"

---

## 🛠️ Technologies

JARVIS is powered by a robust tech stack:
- **Speech Recognition**: `pyttsx3`
- **Text-to-Speech**: `edge_tts`
- **Vision API**: Together API
- **Code Assistance**: OpenRouter API
- **Image Generation**: Cohere API with Flux model
- **GUI**: Custom dynamic popup, activated via Ctrl + Shift + J
- **Automation**: Windows-specific integrations

---

## 🔍 How It Works

1. **Voice Input**: Captured via `pyttsx3` and converted to text.
2. **Command Processing**: Matched against registered patterns (e.g., `\bcode helper\b`).
3. **Task Execution**: Routed to APIs or system functions.
4. **Response**: Delivered via `edge_tts` and a dynamic popup.

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repo.
2. Create a branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to your fork (`git push origin feature/your-feature`).
5. Open a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Contact

- **Author**: Kaif Ansari
- **GitHub**: [kaif-ansari-jarvis](https://github.com/kaif-ansari-jarvis)
- **Email**: kaif.ansari@example.com

---

<p align="center">
  <b>Unleash productivity with JARVIS—your AI companion for a smarter Windows experience.</b>
</p>

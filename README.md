
# JARVIS - AI Assistant for Windows

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square" alt="Status: Active"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square" alt="Python: 3.9+"/>
  <img src="https://img.shields.io/badge/Access-Private-red?style=flat-square" alt="Access: Private"/>
  <img src="https://img.shields.io/badge/Voice%20Controlled-Yes-blueviolet?style=flat-square" alt="Voice Controlled: Yes"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square" alt="Version: 1.0.0"/>
</p>

<p align="center">
  <b>JARVIS: A proprietary voice-controlled AI assistant for Windows, inspired by Iron Man’s iconic companion, engineered to optimize productivity through advanced automation, media generation, system control, and culturally nuanced conversations in English and Hinglish.</b>
</p>

---

## Overview

**JARVIS** ("Just A Rather Very Intelligent System") is a private, proprietary AI assistant designed exclusively for Windows. Drawing inspiration from *Iron Man*, it integrates cutting-edge speech recognition, text-to-speech, and enterprise-grade APIs to deliver a sophisticated, voice-activated user experience. Tailored for professionals, enterprises, and power users, JARVIS enhances operational efficiency with robust automation and contextually aware, multilingual interactions.

> **Note**: This project is not open-source. Access is restricted to authorized personnel and stakeholders. Contact the project owner for inquiries regarding access or collaboration.

---

## Key Features

### Advanced Voice Interaction & Automation
- Seamlessly control applications, system settings, and workflows using voice commands.
- Generate high-quality media, including images and video content, via API-driven processes.
- Execute system-level utilities, such as optimizing storage or adjusting display settings.

### Intelligent Conversational AI
- **Personalized Engagement**: Delivers responses tailored to user profiles, preferences, and organizational roles.
- **Contextual Intelligence**: Adapts to temporal, geographical, and historical data for precise, relevant interactions.
- **Multilingual Support**: Combines English and Hindi (Hinglish) for culturally resonant communication.
- **Memory Architecture**: Retains user objectives, operational data, and interaction history for enhanced decision-making.

<details>
<summary><b>Conversational Capabilities</b></summary>

| Capability                | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| Personalized Engagement   | Generates responses based on user-specific data (e.g., role, preferences).   |
| Contextual Intelligence   | Leverages time, location, and interaction history for dynamic responses.     |
| Memory Architecture       | Stores and retrieves user objectives, data points, and preferences.         |
| Multilingual Support      | Delivers engaging English-Hindi (Hinglish) interactions for accessibility.   |
| Proactive Assistance      | Provides task reminders and workflow suggestions based on user objectives.   |
| Emotional Intelligence    | Adjusts tone and responses to align with user sentiment and context.         |
| Vector Embeddings         | Enhances context retrieval using Cohere’s advanced embedding technology.     |

</details>

---

## Demo Screenshots

<details>
<summary><b>JARVIS Demo with Screenshots</b></summary>

### Command Interface
![Command Interface](demo_screenshots/gui.png)  
*Streamlined, professional interface with voice and text input, featuring a secure, enterprise-grade dark-themed UI.*

### Sample Interaction
![Sample Interaction](demo_screenshots/example_command_1.png)  
*Illustrates JARVIS processing a basic command with a professional response.*

### Workflow Automation
![Workflow Automation](demo_screenshots/file_choser.png)  
*Demonstrates application launching with a secure, responsive overlay and file navigation support.*

### System Navigation
![System Navigation](demo_screenshots/popup_dyanmic.png)  
*Intuitive file and system navigation interface with enhanced security features.*

### Theme Customization
![Theme Customization](demo_screenshots/dark_mode.png)  
*Supports dark and light themes for accessibility and user preference.*

### Media Analysis
![Media Analysis Test](demo_screenshots/image_classification_image.png)  
*High-precision media analysis interface.*  
![Media Analysis Prompt](demo_screenshots/image_classification.png)  
*Secure prompt interface for media processing.*  
![Media Analysis Response 1](demo_screenshots/image_classification_response_1.png)  
*Detailed, actionable analysis results.*  
![Media Analysis Response 2](demo_screenshots/image_classification_response_2.png)  
*Comprehensive secondary insights for enterprise use.*

### Code Assistance
![Code Assistance Test](demo_screenshots/coding_assistant_test.png)  
*Real-time, secure code suggestions for developers.*  
![Code Assistance Response 1](demo_screenshots/coding_assistant_response_1.png)  
*Precise, context-aware code recommendations.*  
![Code Assistance Response 2](demo_screenshots/coding_assistant_response_2.png)  
*Alternative solutions with detailed explanations.*

</details>

---

## Automation Commands

<details>
<summary><b>Supported Commands</b></summary>

| Command                   | Description                                          |
|---------------------------|------------------------------------------------------|
| Code Assistance           | Delivers secure coding support via OpenRouter API.   |
| Media Generation          | Creates images using Cohere API (Flux model).         |
| Screen Capture            | Securely captures the active screen.                  |
| Launch [app]              | Opens applications (e.g., "Launch Chrome").           |
| Terminate [app]           | Closes applications (e.g., "Terminate Chrome").       |
| System Shutdown           | Initiates secure system shutdown.                     |
| Stream Media              | Streams authorized content from YouTube.              |
| Display Adjustment        | Modifies screen brightness or display settings.       |

</details>

---

## Installation

### Prerequisites
- **OS**: Windows 10/11 (64-bit, Enterprise or Pro editions recommended)
- **Python**: 3.9 or higher
- **Microphone**: For voice-activated commands
- **API Keys**: Together API, OpenRouter API, Cohere API (provided to authorized users)
- **Access**: Valid credentials for proprietary repository access

### Setup Instructions
1. **Request Repository Access**:
   - Contact the project administrator for secure access to the private repository.
2. **Clone the Repository** (Authorized Users Only):
   ```bash
   git clone <private_repository_url>
   cd Project-JARVIS
   ```
3. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure API Keys**:
   - Create a secure `.env` file in the project root:
     ```env
     TOGETHER_API_KEY=your_together_api_key
     OPENROUTER_API_KEY=your_openrouter_api_key
     COHERE_API_KEY=your_cohere_api_key
     ```
6. **Launch JARVIS**:
   ```bash
   python main.py
   ```

> **Security Note**: Ensure API keys and repository access are handled in compliance with organizational security policies.

---

## Usage

Activate JARVIS using the secure hotkey **Ctrl + Shift + J**. Issue voice or text commands, such as:
- "Code assistance: Generate a Python script for data analysis."
- "Media generation: Create a corporate infographic."
- "System shutdown" to securely power off.
- "Stream media: Play authorized training video."

JARVIS delivers voice responses via a secure, enterprise-grade popup interface.

---

## Tech Stack

- **Speech Recognition**: `pyttsx3` (enterprise-optimized)
- **Text-to-Speech**: `edge_tts` (secure, low-latency)
- **Vision Processing**: Together API
- **Code Assistance**: OpenRouter API
- **Media Generation**: Cohere API (Flux model)
- **Interface**: Secure, dynamic popup triggered by Ctrl + Shift + J

---

## Operational Workflow

1. **Voice Input**: `pyttsx3` securely captures and processes speech to text.
2. **Command Processing**: Matches input to authorized actions or API-driven tasks.
3. **Task Execution**: Executes commands or retrieves data via secure API calls.
4. **Response Delivery**: Provides voice output via `edge_tts` and displays results in a secure interface.

---

## Access & Collaboration

This project is proprietary and not open for public contributions. For access, collaboration, or feature requests:
- **Contact**: Kaif Ansari
- **Email**: <a href="mailto:kaifansaridev@gmail.com" target="_blank">kaifansaridev@gmail.com</a>
- **Note**: All requests are subject to approval and non-disclosure agreements.

---

## Security & Compliance

- **Data Protection**: All user data and interactions are encrypted and stored securely.
- **Access Control**: Restricted to authorized users with valid credentials.
- **Auditability**: Command logs and API interactions are tracked for compliance.

---

<p align="center">
  <b>JARVIS: Your secure, professional AI companion for an optimized Windows experience.</b><br>
  <i>Proprietary and actively maintained for enterprise excellence.</i>
</p>

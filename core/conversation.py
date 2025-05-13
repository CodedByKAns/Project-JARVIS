import os
import requests
import numpy as np
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import cohere
from voice.tts import speak
import hashlib
import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedVectorMemory:
    """Advanced memory system with modern context awareness and recall capabilities."""
    
    def __init__(self, memory_path="Data/jarvis_memory"):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(exist_ok=True)
        self.vectors_file = self.memory_path / "vectors.json"
        self.messages_file = self.memory_path / "messages.json"
        self.user_profile_file = self.memory_path / "user_profile.json"
        self.embedding_cache_file = self.memory_path / "embedding_cache.json"
        
        self._init_files()
        self._load_data()
        self.embedding_cache = self._load_embedding_cache()
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def _init_files(self):
        files = [
            (self.vectors_file, []),
            (self.messages_file, []),
            (self.embedding_cache_file, {}),
            (self.user_profile_file, {
                "preferences": {},
                "facts": [],
                "goals": [],
                "negative_prefs": [],
                "mood_history": [],
                "confidence_scores": {},
                "context_tags": {},
                "tag_frequencies": {},
                "last_updated": None
            })
        ]
        for file_path, default_data in files:
            if not file_path.exists():
                self._save_file(file_path, default_data)
    
    def _load_data(self):
        try:
            self.vectors = self._load_file(self.vectors_file) or []
            self.messages = self._load_file(self.messages_file) or []
            self.user_profile = self._load_file(self.user_profile_file) or self._init_files()
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.vectors = []
            self.messages = []
            self._init_files()
            self.user_profile = self._load_file(self.user_profile_file)
    
    def _load_embedding_cache(self):
        try:
            return self._load_file(self.embedding_cache_file) or {}
        except:
            return {}
    
    def _save_file(self, file_path, data):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")
    
    def _load_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def get_embedding(self, text):
        text_hash = hashlib.md5(text.encode()).hexdigest()
        if text_hash in self.embedding_cache:
            logger.info(f"Using cached embedding for text hash: {text_hash}")
            return self.embedding_cache[text_hash]
        
        url = "https://api.cohere.ai/v1/embed"
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "texts": [text],
            "model": "embed-english-v3.0",
            "input_type": "search_query"
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            embedding = response.json().get("embeddings")[0]
            self.embedding_cache[text_hash] = embedding
            self._save_file(self.embedding_cache_file, self.embedding_cache)
            return embedding
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return None
    
    def cosine_similarity(self, vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        return np.dot(vec1, vec2) / norm if norm != 0 else 0
    
    def add_message(self, role, message, is_search=False, should_remember=False, confidence=0.8, tags=None):
        embedding = self.get_embedding(message)
        if not embedding:
            return
        
        message_id = len(self.messages)
        timestamp = datetime.now().isoformat()
        tags = tags or []
        
        vector_entry = {
            "id": message_id,
            "vector": embedding,
            "timestamp": timestamp,
            "is_search": is_search,
            "tags": tags,
            "relevance_score": confidence
        }
        self.vectors.append(vector_entry)
        
        message_entry = {
            "id": message_id,
            "role": role,
            "message": message,
            "timestamp": timestamp,
            "is_search": is_search,
            "tags": tags,
            "relevance_score": confidence
        }
        self.messages.append(message_entry)
        
        if should_remember and role == "USER":
            category, sentiment, tags = self._categorize_message(message)
            self._update_profile(message, category, timestamp, confidence, tags, sentiment)
        
        self._save_data()
        self._generate_auto_summary()
        
        if self.debug_mode:
            self.print_profile_summary()
    
    def _categorize_message(self, message):
        current_time = datetime.now()
        time_of_day = "morning" if current_time.hour < 12 else "afternoon" if current_time.hour < 18 else "evening"
        day_of_week = current_time.strftime("%A")
        
        prompt = f"""
Classify the following user message into one of these categories: 
- preference
- fact
- goal
- negative_preference
Also, detect the sentiment (positive, negative, neutral) and generate relevant tags.
Current context:
- Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
- Time of Day: {time_of_day}
- Day of Week: {day_of_week}
Message: "{message}"
Respond with JSON in this exact format:
{{
  "category": "preference|fact|goal|negative_preference",
  "sentiment": "positive|negative|neutral",
  "tags": ["tag1", "tag2", ...]
}}
Example:
For message "I love pizza", return:
{{
  "category": "preference",
  "sentiment": "positive",
  "tags": ["food", "morning"]
}}
"""
        try:
            response = cohere.Client(COHERE_API_KEY).generate(
                prompt=prompt,
                model="command-r-plus",
                max_tokens=50,
                temperature=0.3
            )
            result = json.loads(response.generations[0].text.strip())
            result["tags"] = result.get("tags", []) + [time_of_day, day_of_week.lower()]
            return result["category"], result["sentiment"], result["tags"]
        except:
            return "fact", "neutral", [time_of_day, day_of_week.lower()]
    
    def _update_profile(self, message, category, timestamp, confidence, tags, sentiment):
        entry = {
            "message": message,
            "timestamp": timestamp,
            "confidence": confidence,
            "tags": tags,
            "sentiment": sentiment,
            "priority": "recent" if (datetime.now() - datetime.fromisoformat(timestamp)).days < 2 else "standard"
        }
        
        if category == "preference":
            self.user_profile["preferences"][message] = entry
        elif category == "goal":
            self.user_profile["goals"].append(entry)
        elif category == "negative_preference":
            self.user_profile["negative_prefs"].append(entry)
        else:
            self.user_profile["facts"].append(entry)
        
        self.user_profile["mood_history"].append({
            "timestamp": timestamp,
            "sentiment": sentiment,
            "message": message
        })
        self.user_profile["confidence_scores"][message] = confidence
        self.user_profile["context_tags"][message] = tags
        self._prune_profile()
        self._update_tag_frequencies()
    
    def _prune_profile(self):
        for category in ["facts", "goals", "negative_prefs", "mood_history"]:
            entries = self.user_profile[category]
            self.user_profile[category] = [
                e for e in entries
                if (datetime.now() - datetime.fromisoformat(e["timestamp"])).days < 30
                or e["confidence"] > 0.7
            ][-50:]
    
    def _update_tag_frequencies(self):
        all_entries = []
        for category in ["facts", "goals", "negative_prefs"]:
            all_entries.extend(self.user_profile[category])
        all_entries.extend(list(self.user_profile["preferences"].values()))
        all_tags = [tag for entry in all_entries for tag in entry.get("tags", [])]
        self.user_profile["tag_frequencies"] = dict(Counter(all_tags))
    
    def generate_tags(self, message):
        current_time = datetime.now()
        time_of_day = "morning" if current_time.hour < 12 else "afternoon" if current_time.hour < 18 else "evening"
        day_of_week = current_time.strftime("%A")
        prompt = f"""
Generate relevant tags for the following message: "{message}"
Current context:
- Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
- Time of Day: {time_of_day}
- Day of Week: {day_of_week}
Respond with JSON:
{{"tags": ["tag1", "tag2", ...]}}
"""
        try:
            response = cohere.Client(COHERE_API_KEY).generate(
                prompt=prompt,
                model="command-r-plus",
                max_tokens=50,
                temperature=0.3
            )
            result = json.loads(response.generations[0].text.strip())
            return result["tags"]
        except:
            return []
    
    def search_similar(self, query, query_tags=[], limit=5, role_filter="USER"):
        if not self.vectors:
            return []
        
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        similarities = []
        for vec_entry in self.vectors:
            if role_filter is not None and self.messages[vec_entry["id"]]["role"] != role_filter:
                continue
            msg_id = vec_entry["id"]
            embedding_sim = self.cosine_similarity(query_embedding, vec_entry["vector"])
            message_tags = set(self.messages[msg_id]["tags"])
            query_tags_set = set(query_tags)
            tag_sim = len(message_tags.intersection(query_tags_set)) / len(message_tags.union(query_tags_set)) if message_tags or query_tags_set else 0
            relevance_score = vec_entry["relevance_score"]
            overall_sim = 0.5 * embedding_sim + 0.3 * tag_sim + 0.2 * relevance_score
            similarities.append((msg_id, overall_sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for msg_id, overall_sim in similarities[:limit]:
            msg = self.messages[msg_id]
            result = msg.copy()
            result["similarity"] = overall_sim
            results.append(result)
        
        return results
    
    def get_relevant_context(self, query, limit=5):
        query_tags = self.generate_tags(query)
        similar_messages = self.search_similar(query, query_tags=query_tags, limit=limit, role_filter="USER")
        
        current_time = datetime.now()
        time_of_day = "morning" if current_time.hour < 12 else "afternoon" if current_time.hour < 18 else "evening"
        day_of_week = current_time.strftime("%A")
        system_context = [
            f"### System Context:",
            f"- Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Time of Day: {time_of_day}",
            f"- Day of Week: {day_of_week}",
        ]
        
        location = next((f["message"] for f in self.user_profile["facts"] if "location" in f.get("tags", [])), os.getenv("USER_LOCATION", "unknown"))
        if location != "unknown":
            system_context.append(f"- User Location: {location}")
        
        context = system_context[:]
        
        def select_entries(entries, tags, num=2):
            matching = [e for e in entries if any(tag in tags for tag in e.get("tags", []))]
            if matching:
                selected = sorted(matching, key=sort_key, reverse=True)[:num]
            else:
                selected = sorted(entries, key=sort_key, reverse=True)[:num]
            return selected
        
        def sort_key(entry):
            time_diff = (datetime.now() - datetime.fromisoformat(entry["timestamp"])).days
            priority_score = 1.0 if entry.get("priority") == "recent" else 0.5
            return (entry["confidence"] + priority_score, -time_diff)
        
        recent_facts = [f for f in self.user_profile["facts"] if f.get("priority") == "recent"]
        selected_recent = select_entries(recent_facts, query_tags, num=3)
        if selected_recent:
            context.append("### Most Recent Interactions:")
            for fact in selected_recent:
                context.append(f"- {fact['message']} (Confidence: {fact['confidence']:.2f}, Tags: {fact['tags']})")
        
        time_relevant_goals = [
            g for g in self.user_profile["goals"]
            if "date" in g.get("tags", []) and (datetime.now() - datetime.fromisoformat(g["timestamp"])).days < 7
        ]
        if time_relevant_goals:
            context.append("### Time-Relevant Goals:")
            sorted_goals = sorted(time_relevant_goals, key=sort_key, reverse=True)[:2]
            for goal in sorted_goals:
                context.append(f"- {goal['message']} (Confidence: {goal['confidence']:.2f}, Tags: {goal['tags']})")
        
        other_facts = [f for f in self.user_profile["facts"] if f.get("priority") != "recent"]
        selected_facts = select_entries(other_facts, query_tags, num=3)
        if selected_facts:
            context.append("### Relevant User Facts:")
            for fact in selected_facts:
                context.append(f"- {fact['message']} (Confidence: {fact['confidence']:.2f}, Tags: {fact['tags']})")
        
        pref_entries = list(self.user_profile["preferences"].values())
        selected_prefs = select_entries(pref_entries, query_tags, num=2)
        if selected_prefs:
            context.append("### Relevant User Preferences:")
            for pref in selected_prefs:
                context.append(f"- {pref['message']} (Confidence: {pref['confidence']:.2f}, Tags: {pref['tags']})")
        
        selected_neg_prefs = select_entries(self.user_profile["negative_prefs"], query_tags, num=2)
        if selected_neg_prefs:
            context.append("### Relevant Avoidances:")
            for neg in selected_neg_prefs:
                context.append(f"- {neg['message']} (Confidence: {neg['confidence']:.2f}, Tags: {neg['tags']})")
        
        if self.user_profile["mood_history"]:
            context.append("### Recent Mood:")
            sorted_moods = sorted(self.user_profile["mood_history"], key=lambda x: x["timestamp"], reverse=True)[:2]
            for mood in sorted_moods:
                context.append(f"- {mood['sentiment'].capitalize()} mood: {mood['message']} (Timestamp: {mood['timestamp'][:10]})")
        
        if self.user_profile["tag_frequencies"]:
            top_freq_tags = sorted(self.user_profile["tag_frequencies"].items(), key=lambda x: x[1], reverse=True)[:5]
            context.append("### User's Frequent Topics:")
            context.append(", ".join([tag for tag, _ in top_freq_tags]))
        
        if similar_messages:
            context.append("### Related Previous Conversation:")
            for msg in similar_messages:
                context.append(f"{msg['role']}: {msg['message']} (Similarity: {msg['similarity']:.2f}, Tags: {msg['tags']})")
        
        return "\n".join(context).strip()
    
    def _generate_auto_summary(self):
        summary = []
        if self.user_profile["preferences"]:
            summary.append(f"You seem to prefer: {', '.join(list(self.user_profile['preferences'].keys())[:3])}")
        if self.user_profile["goals"]:
            summary.append(f"Your main goals are: {', '.join([g['message'] for g in self.user_profile['goals'][:3]])}")
        if self.user_profile["facts"]:
            summary.append(f"Here's what you've told me about yourself: {', '.join([f['message'] for f in self.user_profile['facts'][:3]])}")
        if self.user_profile["mood_history"]:
            summary.append(f"Recent mood trends: {', '.join([m['sentiment'] for m in self.user_profile['mood_history'][:3]])}")
        if self.user_profile["tag_frequencies"]:
            top_tags = sorted(self.user_profile["tag_frequencies"].items(), key=lambda x: x[1], reverse=True)[:3]
            summary.append(f"You often talk about: {', '.join([tag for tag, _ in top_tags])}")
        
        summary_text = "\n".join(summary)
        if summary_text:
            self._save_file(self.memory_path / "user_summary.json", {"summary": summary_text, "timestamp": datetime.now().isoformat()})
    
    def print_profile_summary(self):
        logger.info("User Profile Summary:")
        logger.info(json.dumps(self.user_profile, indent=2))
    
    def _save_data(self):
        self.user_profile["last_updated"] = datetime.now().isoformat()
        try:
            self._save_file(self.vectors_file, self.vectors)
            self._save_file(self.messages_file, self.messages)
            self._save_file(self.user_profile_file, self.user_profile)
        except Exception as e:
            logger.error(f"Error saving data: {e}")

class JarvisAI:
    def __init__(self):
        load_dotenv()
        global USER_NAME, COHERE_API_KEY
        self._check_env_vars()
        self.memory = AdvancedVectorMemory(memory_path="Data/jarvis_memory")
        
        user_location = os.getenv("USER_LOCATION")
        if user_location:
            self.memory.user_profile["facts"].append({
                "message": f"User is located in {user_location}",
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.9,
                "tags": ["location"],
                "sentiment": "neutral",
                "priority": "standard"
            })
            self.memory._save_file(self.memory.user_profile_file, self.memory.user_profile)
        
        self.system_prompt = self._get_system_prompt()
        self.chat_history = [{"role": "CHATBOT", "message": self.system_prompt}]
        self.memory.add_message("CHATBOT", self.system_prompt, tags=["system"])
        self.cohere_client = cohere.Client(COHERE_API_KEY)
        self.interaction_count = 0
        
        self.predefined_responses = {
            "what time is it?": lambda: f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
            "current time": lambda: f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
            "what's the time?": lambda: f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
            "what's today's date?": lambda: f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
            "current date": lambda: f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
            "what date is it?": lambda: f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
            "how are you?": "I'm doing great, thanks for asking!",
            "hello": f"Hello, {USER_NAME}! How can I assist you today?",
            "hi": f"Hi, {USER_NAME}! What's on your mind?",
            "goodbye": "Goodbye! Have a great day!",
            "bye": "See you later!",
        }
    
    def _check_env_vars(self):
        global USER_NAME, COHERE_API_KEY
        USER_NAME = os.getenv("USER_NAME", "User")
        COHERE_API_KEY = os.getenv("COHERE_API_KEY")
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY not set.")
    
    def should_remember_message(self, message):
        prompt = f"""
Analyze the user message: "{message}"
Decide if it expresses a preference, goal, fact, or negative preference worth adding to the user profile.
Consider if the message contains important information about the user's likes, dislikes, objectives, or personal details.
Return JSON in this format:
{{
  "should_remember": true or false,
  "confidence": a float between 0.0 and 1.0 indicating how confident you are that it should be remembered,
  "tags": ["tag1", "tag2", ...] (relevant tags for the message)
}}
Example:
For message "I love pizza", return:
{{
  "should_remember": true,
  "confidence": 0.9,
  "tags": ["food", "preference"]
}}
For message "What's the weather like?", return:
{{
  "should_remember": false,
  "confidence": 0.8,
  "tags": ["weather", "query"]
}}
"""
        try:
            response = self.cohere_client.generate(
                prompt=prompt,
                model="command-r-plus",
                max_tokens=50,
                temperature=0.3
            )
            result = json.loads(response.generations[0].text.strip())
            return result["should_remember"], result["confidence"], result["tags"]
        except:
            return False, 0.5, []
    
    def _get_system_prompt(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
# Advanced Context-Aware Jarvis AI Prompt

```
You are Jarvis, created by Kaif Ansari from TheFailures, inspired by Iron Man's AI but with a desi, tech-savvy dost vibe. You're built to deliver context-aware, personalized responses using an advanced memory system.

## Current Context
- **Date and Time**: {current_time}
- **User**: {USER_NAME}

## Core Identity
- Created by Kaif Ansari and TheFailures
- Goal: Provide exceptional, personalized assistance with a friendly, Hinglish tone 😎

## Advanced Memory System
- **Structured Profile**: Maintains categorized user data (facts, goals, preferences, negative preferences, mood history, frequent topics)
- **Confidence Scoring**: Assigns reliability scores to stored info
- **Dynamic Pruning**: Keeps profile lean
- **Context Prioritization**: Uses profile data, tags, and history
- **Frequent Topics**: Tracks commonly discussed themes

## Response Guidelines
1. **Personalized Responses**: Use {USER_NAME}, reference profile data
2. **Context-Aware**: Blend history, profile, tags
3. **Engaging Tone**: Mix English and Hinglish
4. **Structured Output**: Use headings, bullets, or tables
5. **Technical Precision**: Deliver clean code, match user's expertise
6. **Emotional Intelligence**: Adapt tone based on sentiment
7. **Concise and Complete**: Keep responses brief but ensure they fully address the query
8. **Time Accuracy**: Use the provided current time when mentioning time

## Capabilities
- **Multi-Session Memory**: Build on past chats
- **Proactive Suggestions**: Anticipate needs
- **Error Handling**: Graceful fallbacks
- **Auto-Summary**: Summarize profile insights

Talk like a tech-savvy dost who remembers everything about {USER_NAME}!
```"""
    
    def _handle_general_query(self, query, relevant_context):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_of_day = "morning" if datetime.now().hour < 12 else "afternoon" if datetime.now().hour < 18 else "evening"
        
        enhanced_query = f"""
You are Jarvis, an AI assistant. The current time is {current_time} ({time_of_day}). The user is {USER_NAME}.

The user has asked: "{query}"

Here is some relevant context from the user's profile and previous interactions:
{relevant_context if relevant_context else 'No additional context available.'}

Please provide a response that is accurate, logical, and fully addresses the user's query. Keep the response concise but complete. If the query involves time, use the provided current time.
"""
        
        try:
            response = self.cohere_client.chat(
                message=enhanced_query,
                model="command-r-plus",
                chat_history=[{"role": item["role"], "message": item["message"]} for item in self.chat_history[-10:]],
                temperature=0.7,
                max_tokens=1000
            )
            reply = response.text if response and hasattr(response, 'text') else "Sorry, something went wrong. Try again?"
            
            try:
                speak(reply)
            except:
                pass
            
            should_remember, confidence, tags = self.should_remember_message(query)
            self.chat_history.append({"role": "USER", "message": query})
            self.chat_history.append({"role": "CHATBOT", "message": reply})
            self.memory.add_message("USER", query, should_remember=should_remember, confidence=confidence, tags=tags)
            self.memory.add_message("CHATBOT", reply, tags=["response"])
            
            self._trim_chat_history()
            return reply
        
        except Exception as e:
            error_reply = f"Oops, hit a snag: {str(e)}. Try again, {USER_NAME}?"
            try:
                speak(error_reply)
            except:
                pass
            
            should_remember, confidence, tags = self.should_remember_message(query)
            self.chat_history.append({"role": "USER", "message": query})
            self.chat_history.append({"role": "CHATBOT", "message": error_reply})
            self.memory.add_message("USER", query, should_remember=should_remember, confidence=confidence, tags=tags)
            self.memory.add_message("CHATBOT", error_reply, tags=["error"])
            return error_reply
    
    def _trim_chat_history(self):
        if len(self.chat_history) > 21:
            self.chat_history = [self.chat_history[0]] + self.chat_history[-20:]
    
    def generate_proactive_suggestions(self):
        if self.memory.user_profile["goals"]:
            top_goal = self.memory.user_profile["goals"][0]
            return f"Just a reminder, {USER_NAME}: {top_goal['message']}"
        return None
    
    def chat(self, query):
        if not query or not isinstance(query, str):
            query = f"Hey {USER_NAME}, how can I assist you today?"
        
        query_lower = query.lower().strip()
        
        if query_lower.startswith("remember "):
            message = query[9:].strip()
            category, sentiment, tags = self.memory._categorize_message(message)
            self.memory._update_profile(message, category, datetime.now().isoformat(), 1.0, tags, sentiment)
            response = f"Got it, {USER_NAME}. I'll remember: {message}"
            try:
                speak(response)
            except:
                pass
            self.chat_history.append({"role": "USER", "message": query})
            self.chat_history.append({"role": "CHATBOT", "message": response})
            self._trim_chat_history()
            return response
        elif query_lower.startswith("forget "):
            message = query[7:].strip()
            for category in ["facts", "preferences", "goals", "negative_prefs"]:
                if category == "preferences":
                    if message in self.memory.user_profile[category]:
                        del self.memory.user_profile[category][message]
                else:
                    self.memory.user_profile[category] = [e for e in self.memory.user_profile[category] if e["message"] != message]
            response = f"Okay, {USER_NAME}, I've forgotten: {message}"
            try:
                speak(response)
            except:
                pass
            self.chat_history.append({"role": "USER", "message": query})
            self.chat_history.append({"role": "CHATBOT", "message": response})
            self._trim_chat_history()
            return response
        
        if query_lower in self.predefined_responses:
            if callable(self.predefined_responses[query_lower]):
                response = self.predefined_responses[query_lower]()
            else:
                response = self.predefined_responses[query_lower]
            try:
                speak(response)
            except:
                pass
            self.chat_history.append({"role": "USER", "message": query})
            self.chat_history.append({"role": "CHATBOT", "message": response})
            should_remember, confidence, tags = self.should_remember_message(query)
            self.memory.add_message("USER", query, should_remember=should_remember, confidence=confidence, tags=tags)
            self.memory.add_message("CHATBOT", response, tags=["predefined_response"])
            self._trim_chat_history()
            return response
        
        relevant_context = self.memory.get_relevant_context(query)
        response = self._handle_general_query(query, relevant_context)
        
        self.interaction_count += 1
        if self.interaction_count % 5 == 0:
            suggestion = self.generate_proactive_suggestions()
            if suggestion:
                response += "\n\n" + suggestion
        
        return response

try:
    jarvis = JarvisAI()
except Exception as e:
    raise

def chat_with_jarvis(command):
    try:
        return jarvis.chat(command)
    except Exception as e:
        return f"Sorry, {USER_NAME}, hit an error: {str(e)}. Try again?"
    

import requests
import json

MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"
SYSTEM_PROMPT = "You are a helpful assistant."


def create_messages():
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


def show_help():
    print("""
Available commands:

  /help      Show this help message
  /clear     Clear the conversation history
  /model     Show the current model
  /exit      Exit the chatbot
  /quit      Exit the chatbot
""")


messages = create_messages()

print(f"Local LLM Chatbot - {MODEL}")
print("Type /help for available commands.\n")

while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Handle commands
        if user_input.lower() in ["/exit", "/quit"]:
            print("Goodbye!")
            break

        if user_input.lower() == "/help":
            show_help()
            continue

        if user_input.lower() == "/model":
            print(f"Current model: {MODEL}")
            continue

        if user_input.lower() == "/clear":
            messages = create_messages()
            print("Conversation cleared.")
            continue

        # Add user's message to conversation
        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": True
                },
                stream=True,
                timeout=120
            )

            response.raise_for_status()

            print("AI: ", end="", flush=True)

            assistant_reply = ""

            for line in response.iter_lines():
                if not line:
                    continue

                data = json.loads(line)

                if "message" in data:
                    content = data["message"].get("content", "")

                    print(content, end="", flush=True)
                    assistant_reply += content

            print()

            # Save AI response to conversation history
            messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {e}")

            # Remove the user's message because the request failed
            messages.pop()

        except json.JSONDecodeError as e:
            print(f"\nFailed to parse Ollama response: {e}")

            # Remove the user's message because the request failed
            messages.pop()

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break

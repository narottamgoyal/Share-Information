import requests
import json

MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

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

        messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

    except json.JSONDecodeError as e:
        print("Failed to parse Ollama response:", e)

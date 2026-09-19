import requests

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
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        if "message" not in data:
            print("Unexpected Ollama response:")
            print(data)
            continue

        assistant_reply = data["message"]["content"]

        print("AI:", assistant_reply)

        messages.append({
            "role": "assistant",
            "content": assistant_reply
        })

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

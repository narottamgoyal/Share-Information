import requests
import json
import os
import re
import uuid
from datetime import datetime


MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"
SYSTEM_PROMPT = "You are a helpful assistant."

CONVERSATIONS_DIR = "conversations"
MAX_CONTEXT_LENGTH = 32


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def create_messages():
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
            "timestamp": now()
        }
    ]


def sanitize_context(context):
    context = context.strip()

    # Replace characters unsafe in filenames.
    context = re.sub(r'[<>:"/\\|?*]', "_", context)

    # Replace multiple whitespace characters with one space.
    context = re.sub(r"\s+", " ", context)

    # Remove trailing dots/spaces which are problematic on Windows.
    context = context.rstrip(". ")

    return context


def create_conversation():
    """
    Create a new in-memory conversation.
    It is not saved until /save is used.
    """

    return {
        "id": str(uuid.uuid4()),
        "context": None,
        "model": MODEL,
        "created_at": now(),
        "updated_at": now(),
        "messages": create_messages(),

        # filepath tells us whether this conversation has
        # previously been saved.
        "filepath": None,

        # dirty tells us whether changes exist since last save.
        "dirty": False
    }


# ---------------------------------------------------------
# Display / commands
# ---------------------------------------------------------

def show_help():
    print("""
Available commands:

  /help           Show this help message
  /new            Start a new conversation
  /current        Show current conversation information
  /clear          Clear current conversation messages
  /model          Show the current model

  /save           Save/update conversation
  /load <number>  Load a saved conversation
  /list           List saved conversations

  /exit           Exit the chatbot
  /quit           Exit the chatbot
""")


def show_current(conversation):
    print("\nCurrent conversation")
    print("-------------------")

    context = conversation["context"] or "None"
    filepath = conversation["filepath"] or "None"

    # Don't count the system message as a conversation message.
    message_count = max(0, len(conversation["messages"]) - 1)

    print(f"ID:          {conversation['id']}")
    print(f"Context:     {context}")
    print(f"File:        {filepath}")
    print(f"Model:       {conversation['model']}")
    print(f"Messages:    {message_count}")
    print(f"Created:     {conversation['created_at']}")
    print(f"Updated:     {conversation['updated_at']}")

    if conversation["filepath"]:
        if conversation["dirty"]:
            print("Status:      Modified (unsaved changes)")
        else:
            print("Status:      Saved")
    else:
        print("Status:      Unsaved")

    print()


# ---------------------------------------------------------
# Conversation validation
# ---------------------------------------------------------

def validate_messages(messages):
    """
    Validate the message structure loaded from disk.
    """

    if not isinstance(messages, list):
        return False

    for message in messages:
        if not isinstance(message, dict):
            return False

        if message.get("role") not in {
            "system",
            "user",
            "assistant"
        }:
            return False

        if not isinstance(message.get("content"), str):
            return False

    return True


def normalize_loaded_messages(messages):
    """
    Ensure loaded messages contain timestamps.

    Older conversation files may not have timestamps.
    """

    normalized = []

    for message in messages:
        normalized.append({
            "role": message["role"],
            "content": message["content"],
            "timestamp": message.get("timestamp", now())
        })

    return normalized


# ---------------------------------------------------------
# Conversation persistence
# ---------------------------------------------------------

def conversation_filename(conversation):
    context = conversation["context"]

    if context:
        safe_context = sanitize_context(context)

        # Include UUID so two conversations with the same
        # context never overwrite one another.
        return f"chat_{safe_context}_{conversation['id']}.json"

    return f"chat_{conversation['id']}.json"


def save_to_file(conversation):
    """
    Save a conversation to disk.

    Returns the filepath on success.
    Raises OSError / TypeError on failure.
    """

    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    # If this conversation already has a filepath, keep using it.
    # This means /save updates the existing conversation.
    if conversation["filepath"]:
        filepath = conversation["filepath"]
    else:
        filename = conversation_filename(conversation)
        filepath = os.path.join(CONVERSATIONS_DIR, filename)

    conversation["updated_at"] = now()

    data = {
        "id": conversation["id"],
        "context": conversation["context"],
        "model": conversation["model"],
        "created_at": conversation["created_at"],
        "updated_at": conversation["updated_at"],
        "messages": conversation["messages"]
    }

    # Write atomically where possible.
    temp_filepath = filepath + ".tmp"

    try:
        with open(temp_filepath, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        os.replace(temp_filepath, filepath)

    except Exception:
        # Don't leave a temporary file behind.
        try:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
        except OSError:
            pass

        raise

    conversation["filepath"] = filepath
    conversation["dirty"] = False

    return filepath


def list_conversations():
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    files = sorted(
        file
        for file in os.listdir(CONVERSATIONS_DIR)
        if file.endswith(".json")
        and not file.endswith(".tmp.json")
    )

    if not files:
        print("\nNo saved conversations.\n")
        return []

    conversations = []

    for filename in files:
        filepath = os.path.join(CONVERSATIONS_DIR, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            messages = data.get("messages", [])

            if not validate_messages(messages):
                raise ValueError("Invalid messages structure")

            conversations.append({
                "filename": filename,
                "filepath": filepath,
                "context": data.get("context") or "No context",
                "updated_at": data.get("updated_at", "Unknown"),
                "message_count": max(0, len(messages) - 1),
                "valid": True
            })

        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            conversations.append({
                "filename": filename,
                "filepath": filepath,
                "context": None,
                "updated_at": "Unknown",
                "message_count": 0,
                "valid": False
            })

    # Most recently updated conversations first.
    conversations.sort(
        key=lambda item: item["updated_at"],
        reverse=True
    )

    print("\nSaved conversations:")
    print("--------------------")

    for index, conversation in enumerate(conversations, start=1):
        if not conversation["valid"]:
            print(
                f"  {index}. "
                f"{conversation['filename']} [invalid file]"
            )
            continue

        print(
            f"  {index}. "
            f"{conversation['context']} "
            f"| messages: {conversation['message_count']} "
            f"| updated: {conversation['updated_at']}"
        )

    print()

    return [item["filename"] for item in conversations]


def load_conversation(number):
    files = list_conversations()

    if not files:
        return None

    try:
        index = int(number) - 1

        if index < 0 or index >= len(files):
            print("Invalid conversation number.")
            return None

        filename = files[index]
        filepath = os.path.join(CONVERSATIONS_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        messages = data.get("messages")

        if not validate_messages(messages):
            print("Failed to load conversation: invalid message structure.")
            return None

        messages = normalize_loaded_messages(messages)

        # Ensure a system message exists.
        if not messages or messages[0]["role"] != "system":
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                    "timestamp": now()
                }
            )

        conversation = {
            "id": data.get("id", str(uuid.uuid4())),
            "context": data.get("context"),
            "model": data.get("model", MODEL),
            "created_at": data.get("created_at", now()),
            "updated_at": data.get("updated_at", now()),
            "messages": messages,
            "filepath": filepath,
            "dirty": False
        }

        print(f"\nLoaded: {filename}")

        if conversation["context"]:
            print(f"Context: {conversation['context']}")

        print()

        return conversation

    except ValueError:
        print("Please provide a valid conversation number.")
        return None

    except (json.JSONDecodeError, OSError, TypeError) as e:
        print(f"Failed to load conversation: {e}")
        return None


# ---------------------------------------------------------
# Save workflow
# ---------------------------------------------------------

def ask_for_context():
    """
    Ask for a conversation context.

    Returns sanitized context or None.
    """

    while True:
        context = input(
            f"Enter context (max {MAX_CONTEXT_LENGTH} chars): "
        ).strip()

        if len(context) > MAX_CONTEXT_LENGTH:
            print(
                f"Context is too long. Maximum is "
                f"{MAX_CONTEXT_LENGTH} characters."
            )
            continue

        context = sanitize_context(context)

        if not context:
            print("No context provided.")
            return None

        return context


def save_new_conversation(conversation):
    """
    Ask for context and save as a new conversation.

    Returns True on success, False on failure/cancellation.
    """

    context = ask_for_context()

    conversation["context"] = context

    try:
        filepath = save_to_file(conversation)

    except (OSError, TypeError) as e:
        print(f"\nFailed to save conversation: {e}\n")
        return False

    print("\nConversation saved:")
    print(filepath)
    print()

    return True


def save_current_conversation(conversation):
    """
    Save an existing conversation.

    If there is no saved conversation yet, ask for context.

    Returns True on successful save, False otherwise.
    """

    # Brand-new / never-saved conversation.
    if not conversation["filepath"]:
        return save_new_conversation(conversation)

    print("\nSave conversation")
    print("-----------------")

    current_context = conversation["context"] or "None"

    print(f"Current context: {current_context}")
    print()
    print("1. Update current conversation")
    print("2. Save as a new conversation")
    print()

    while True:
        choice = input("Choose [1/2]: ").strip()

        # Blank = option 1.
        if choice == "" or choice == "1":

            try:
                filepath = save_to_file(conversation)

            except (OSError, TypeError) as e:
                print(f"\nFailed to save conversation: {e}\n")
                return False

            print("\nConversation updated:")
            print(filepath)
            print()

            return True

        if choice == "2":

            context = ask_for_context()

            new_conversation = {
                "id": str(uuid.uuid4()),
                "context": context,
                "model": conversation["model"],
                "created_at": now(),
                "updated_at": now(),

                # Deep copy without importing copy.
                "messages": json.loads(
                    json.dumps(conversation["messages"])
                ),

                "filepath": None,
                "dirty": True
            }

            try:
                filepath = save_to_file(new_conversation)

            except (OSError, TypeError) as e:
                print(f"\nFailed to save conversation: {e}\n")
                return False

            # The newly created conversation becomes current.
            conversation.clear()
            conversation.update(new_conversation)

            print("\nNew conversation saved:")
            print(filepath)
            print()

            return True

        print("Please choose 1 or 2.")


# ---------------------------------------------------------
# Unsaved changes protection
# ---------------------------------------------------------

def has_unsaved_changes(conversation):
    """
    True only when changes have been made since the last save.
    """

    return conversation["dirty"]


def confirm_new_conversation(conversation):
    """
    Handle /new when the current conversation has unsaved changes.

    Returns True if it is safe to create a new conversation.
    """

    if not has_unsaved_changes(conversation):
        return True

    print("\nYou have unsaved changes.")
    print("1. Save current conversation")
    print("2. Start new conversation")
    print("3. Cancel")
    print()

    while True:
        choice = input("Choose [1/2/3]: ").strip()

        # Blank = cancel.
        if choice == "":
            print("Cancelled.")
            return False

        if choice == "1":
            if save_current_conversation(conversation):
                return True

            print("Conversation was not saved.")
            return False

        if choice == "2":
            return True

        if choice == "3":
            print("Cancelled.")
            return False

        print("Please choose 1, 2, or 3.")


def confirm_load_conversation(conversation):
    """
    Handle /load when the current conversation has unsaved changes.

    Returns True if it is safe to load another conversation.
    """

    if not has_unsaved_changes(conversation):
        return True

    print("\nCurrent conversation has unsaved changes.")
    print("1. Save and load")
    print("2. Load without saving")
    print("3. Cancel")
    print()

    while True:
        choice = input("Choose [1/2/3]: ").strip()

        # Blank = cancel.
        if choice == "":
            print("Cancelled.")
            return False

        if choice == "1":
            if save_current_conversation(conversation):
                return True

            print("Conversation was not saved.")
            return False

        if choice == "2":
            return True

        if choice == "3":
            print("Cancelled.")
            return False

        print("Please choose 1, 2, or 3.")


# ---------------------------------------------------------
# Ollama
# ---------------------------------------------------------

def build_api_messages(conversation):
    """
    Convert internal messages into Ollama-compatible messages.

    Timestamps are intentionally excluded because they are
    local persistence metadata, not chat API fields.
    """

    return [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in conversation["messages"]
    ]


def send_to_ollama(conversation):
    """
    Send the current conversation to Ollama.

    Returns:
        assistant_reply

    Raises:
        requests exceptions
        RuntimeError
        json.JSONDecodeError
    """

    api_messages = build_api_messages(conversation)

    payload = {
        "model": conversation["model"],
        "messages": api_messages,
        "stream": True
    }

    assistant_reply = ""
    stream_completed = False

    try:
        with requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=120
        ) as response:

            response.raise_for_status()

            print("AI: ", end="", flush=True)

            for line in response.iter_lines(decode_unicode=True):

                if not line:
                    continue

                data = json.loads(line)

                # Ollama can return an error object during streaming.
                if "error" in data:
                    raise RuntimeError(str(data["error"]))

                message = data.get("message", {})

                if not isinstance(message, dict):
                    continue

                content = message.get("content", "")

                if content:
                    print(content, end="", flush=True)
                    assistant_reply += content

                if data.get("done") is True:
                    stream_completed = True

            print()

    except Exception:
        # Make sure the terminal moves to the next line if the
        # request failed halfway through streaming.
        if assistant_reply:
            print()

        raise

    if not stream_completed:
        raise RuntimeError(
            "Ollama stream ended before the response was complete."
        )

    return assistant_reply


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

conversation = create_conversation()

print(f"Local LLM Chatbot - {MODEL}")
print("Type /help for available commands.\n")


while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        command = user_input.lower()

        # -------------------------------------------------
        # Exit
        # -------------------------------------------------

        if command in ["/exit", "/quit"]:

            if has_unsaved_changes(conversation):
                print("\nYou have unsaved changes.")

                choice = input(
                    "Save before exiting? [Y/n]: "
                ).strip().lower()

                if choice in ["", "y", "yes"]:
                    if not save_current_conversation(conversation):
                        print(
                            "Conversation could not be saved. "
                            "Exiting anyway."
                        )

                elif choice not in ["n", "no"]:
                    print("Exiting without saving.")

            print("Goodbye!")
            break

        # -------------------------------------------------
        # Help
        # -------------------------------------------------

        if command == "/help":
            show_help()
            continue

        # -------------------------------------------------
        # Model
        # -------------------------------------------------

        if command == "/model":
            print(f"Current model: {conversation['model']}")
            continue

        # -------------------------------------------------
        # Current
        # -------------------------------------------------

        if command == "/current":
            show_current(conversation)
            continue

        # -------------------------------------------------
        # New
        # -------------------------------------------------

        if command == "/new":

            if confirm_new_conversation(conversation):
                conversation = create_conversation()
                print("\nStarted a new conversation.\n")

            continue

        # -------------------------------------------------
        # Clear
        # -------------------------------------------------

        if command == "/clear":

            # Don't mark an already-empty conversation dirty.
            current_messages = conversation["messages"]

            if len(current_messages) > 1:
                conversation["messages"] = create_messages()
                conversation["updated_at"] = now()
                conversation["dirty"] = True

            print("Conversation messages cleared.")
            continue

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        if command == "/save":
            save_current_conversation(conversation)
            continue

        # -------------------------------------------------
        # List
        # -------------------------------------------------

        if command == "/list":
            list_conversations()
            continue

        # -------------------------------------------------
        # Load
        # -------------------------------------------------

        # Only recognize /load or /load <number>.
        if command == "/load" or command.startswith("/load "):

            parts = user_input.split()

            if len(parts) != 2:
                print("Usage: /load <number>")
                continue

            if not confirm_load_conversation(conversation):
                continue

            loaded = load_conversation(parts[1])

            if loaded is not None:
                conversation = loaded

            continue

        # -------------------------------------------------
        # Normal user message
        # -------------------------------------------------

        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": now()
        }

        conversation["messages"].append(user_message)
        conversation["updated_at"] = now()
        conversation["dirty"] = True

        try:
            assistant_reply = send_to_ollama(conversation)

            # Only add a completed assistant response.
            conversation["messages"].append({
                "role": "assistant",
                "content": assistant_reply,
                "timestamp": now()
            })

            conversation["updated_at"] = now()
            conversation["dirty"] = True

        except requests.exceptions.RequestException as e:

            print(f"\nRequest failed: {e}")

            # Remove only the user message we just added.
            if (
                conversation["messages"]
                and conversation["messages"][-1]["role"] == "user"
            ):
                conversation["messages"].pop()

            # Restore dirty state based on remaining messages.
            conversation["dirty"] = (
                len(conversation["messages"]) > 1
            )

        except (json.JSONDecodeError, RuntimeError) as e:

            print(f"\nOllama response failed: {e}")

            # Remove only the user message we just added.
            if (
                conversation["messages"]
                and conversation["messages"][-1]["role"] == "user"
            ):
                conversation["messages"].pop()

            conversation["dirty"] = (
                len(conversation["messages"]) > 1
            )

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        break

    except EOFError:
        print("\n\nGoodbye!")
        break

    except Exception as e:
        print(f"\nUnexpected error: {e}")

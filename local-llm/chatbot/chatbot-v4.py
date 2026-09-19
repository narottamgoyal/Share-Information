import requests
import json
import os
import re
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime

try:
    import termios
except ImportError:
    termios = None


MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"
SYSTEM_PROMPT = "You are a helpful assistant."

CONVERSATIONS_DIR = "conversations"
MAX_CONTEXT_LENGTH = 32
AUTO_SAVE_CONTEXT = "Auto-saved conversation"


class StreamingCancelled(Exception):
    """Raised when the user cancels an active Ollama response."""


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


@contextmanager
def lock_terminal_input():
    """
    Hide and discard normal terminal input while a reply streams.

    Ctrl+C remains enabled so the user can cancel an active response.
    Non-terminal input, such as piped test input, is left unchanged.
    """

    if termios is None or not sys.stdin.isatty():
        yield
        return

    file_descriptor = sys.stdin.fileno()

    try:
        original_settings = termios.tcgetattr(file_descriptor)
    except termios.error:
        yield
        return

    locked_settings = original_settings.copy()
    locked_settings[3] &= ~termios.ECHO

    try:
        # Discard input already typed before the stream began.
        termios.tcflush(file_descriptor, termios.TCIFLUSH)
        termios.tcsetattr(
            file_descriptor,
            termios.TCSADRAIN,
            locked_settings
        )
        yield
    finally:
        # Ignore anything typed while the response was active.
        termios.tcflush(file_descriptor, termios.TCIFLUSH)
        termios.tcsetattr(
            file_descriptor,
            termios.TCSADRAIN,
            original_settings
        )


def create_messages():
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
            "timestamp": now()
        }
    ]


def sanitize_context(context):
    """
    Sanitize context only for use in filenames.

    The original context is NOT modified when stored in the
    conversation.
    """

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
  /retry          Retry the most recent failed message

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
        if conversation["dirty"]:
            print("Status:      Unsaved changes")
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


def validate_conversation_data(data):
    """
    Validate the persisted conversation fields needed by the CLI.

    Older files may omit metadata fields, but fields that are present
    must have the expected type.
    """

    if not isinstance(data, dict):
        return False

    if "messages" not in data:
        return False

    if not validate_messages(data.get("messages", [])):
        return False

    for field in ("id", "model", "created_at", "updated_at"):
        if field in data and not isinstance(data[field], str):
            return False

    context = data.get("context")
    if context is not None and not isinstance(context, str):
        return False

    for message in data["messages"]:
        if "timestamp" in message and not isinstance(
            message["timestamp"], str
        ):
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

        if safe_context:
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

    temp_filepath = filepath + ".tmp"

    try:
        with open(temp_filepath, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        # Replace existing file atomically where supported.
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


def get_conversation_files():
    """
    Return saved conversation filenames sorted by most
    recently updated conversation.

    This function does not print anything.
    """

    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    files = [
        filename
        for filename in os.listdir(CONVERSATIONS_DIR)
        if filename.endswith(".json")
        and not filename.endswith(".tmp.json")
    ]

    conversations = []

    for filename in files:
        filepath = os.path.join(CONVERSATIONS_DIR, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not validate_conversation_data(data):
                raise ValueError("Invalid conversation structure")

            messages = data["messages"]

            updated_at = data.get("updated_at", "Unknown")

            conversations.append({
                "filename": filename,
                "filepath": filepath,
                "context": data.get("context") or "No context",
                "updated_at": updated_at,
                "message_count": max(0, len(messages) - 1),
                "valid": True
            })

        except (
            json.JSONDecodeError,
            OSError,
            ValueError,
            TypeError,
            AttributeError
        ):
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

    return conversations


def list_conversations():
    """
    Print saved conversations.

    Returns the ordered list of filenames.
    """

    conversations = get_conversation_files()

    if not conversations:
        print("\nNo saved conversations.\n")
        return []

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
    """
    Load a saved conversation by its displayed list number.

    Returns:
        conversation dictionary on success
        None on failure
    """

    conversations = get_conversation_files()

    if not conversations:
        print("\nNo saved conversations.\n")
        return None

    try:
        index = int(number) - 1
    except ValueError:
        print("Please provide a valid conversation number.")
        return None

    if index < 0 or index >= len(conversations):
        print("Invalid conversation number.")
        return None

    selected = conversations[index]

    if not selected["valid"]:
        print("Failed to load conversation: invalid file.")
        return None

    filepath = selected["filepath"]
    filename = selected["filename"]

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not validate_conversation_data(data):
            print(
                "Failed to load conversation: invalid file structure."
            )
            return None

        messages = data["messages"]
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

    except (json.JSONDecodeError, OSError, TypeError, AttributeError) as e:
        print(f"Failed to load conversation: {e}")
        return None


# ---------------------------------------------------------
# Save workflow
# ---------------------------------------------------------

def ask_for_context():
    """
    Ask for a conversation context.

    Returns the original context or None.

    The context itself is NOT sanitized. Filename sanitization
    happens separately when creating the filename.
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

        if not context:
            print("No context provided.")
            return None

        return context


def save_new_conversation(conversation):
    """
    Ask for context and save as a new conversation.

    Returns True on success, False on failure.
    """

    if conversation["context"] is None:
        context = ask_for_context()

        if context is None:
            print("Save cancelled.\n")
            return False

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


def clone_conversation_as_new(conversation):
    """
    Create a completely new conversation using the current
    conversation's messages.

    Returns the new conversation, or None on failure.
    """

    context = ask_for_context()

    if context is None:
        print("Save as new cancelled.\n")
        return None

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
        return None

    print("\nNew conversation saved:")
    print(filepath)
    print()

    return new_conversation


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

            new_conversation = clone_conversation_as_new(
                conversation
            )

            if new_conversation is None:
                return False

            # The newly created conversation becomes current.
            conversation.clear()
            conversation.update(new_conversation)

            return True

        print("Please choose 1 or 2.")


def auto_save_conversation(conversation):
    """
    Save without prompting for input.

    New conversations receive a recognizable default context so an
    interrupted request or exit can still be recovered from /list.
    """

    if not conversation["filepath"] and not conversation["context"]:
        conversation["context"] = AUTO_SAVE_CONTEXT

    try:
        filepath = save_to_file(conversation)
    except (OSError, TypeError) as e:
        print(f"Automatic save failed: {e}")
        return False

    print(f"Conversation saved automatically: {filepath}")
    return True


# ---------------------------------------------------------
# Unsaved changes protection
# ---------------------------------------------------------

def has_unsaved_changes(conversation):
    """
    True when changes have been made since the last save.
    """

    return bool(conversation["dirty"])


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
        StreamingCancelled
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
        with lock_terminal_input():
            with requests.post(
                OLLAMA_URL,
                json=payload,
                stream=True,
                timeout=120
            ) as response:

                response.raise_for_status()

                print("AI: ", end="", flush=True)

                for line in response.iter_lines(
                    decode_unicode=True
                ):

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

    except KeyboardInterrupt:
        print("\n[Response cancelled -- partial response not saved]")
        raise StreamingCancelled() from None

    except Exception:
        # Make sure the terminal moves to the next line if the
        # request failed halfway through streaming.
        if assistant_reply:
            print("\n[Incomplete response -- not saved]")
        else:
            print()

        raise

    if not stream_completed:
        raise RuntimeError(
            "Ollama stream ended before the response was complete."
        )

    if not assistant_reply:
        raise RuntimeError(
            "Ollama returned an empty response."
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

            should_exit = True

            if has_unsaved_changes(conversation):
                print("\nYou have unsaved changes.")

                while True:
                    choice = input(
                        "Save before exiting? [Y/n]: "
                    ).strip().lower()

                    if choice in ["", "y", "yes"]:
                        if not save_current_conversation(
                            conversation
                        ):
                            print(
                                "Conversation was not saved; "
                                "you are still in the chatbot."
                            )
                            should_exit = False

                        break

                    if choice in ["n", "no"]:
                        break

                    print("Please enter Y or N.")

            if not should_exit:
                continue

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
            if len(conversation["messages"]) > 1:

                conversation["messages"] = create_messages()
                conversation["updated_at"] = now()
                conversation["dirty"] = True

                print("Conversation messages cleared.")

            else:
                print("Conversation is already empty.")

            continue

        # -------------------------------------------------
        # Retry
        # -------------------------------------------------

        if command == "/retry":

            if (
                len(conversation["messages"]) <= 1
                or conversation["messages"][-1]["role"] != "user"
            ):
                print("There is no failed message to retry.")
                continue

            try:
                assistant_reply = send_to_ollama(conversation)

                conversation["messages"].append({
                    "role": "assistant",
                    "content": assistant_reply,
                    "timestamp": now()
                })

                conversation["updated_at"] = now()
                conversation["dirty"] = True

            except requests.exceptions.RequestException as e:
                print(f"\nRetry failed: {e}")
                auto_save_conversation(conversation)
                print("Type /retry to try again, or enter a new message.\n")

            except StreamingCancelled:
                auto_save_conversation(conversation)
                print("Response cancelled. You can type /retry "
                      "or enter a new message.\n")

            except (json.JSONDecodeError, RuntimeError) as e:
                print(f"\nOllama retry failed: {e}")
                auto_save_conversation(conversation)
                print("Type /retry to try again, or enter a new message.\n")

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

        # Keep the user's message even if Ollama fails.
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
            auto_save_conversation(conversation)
            print("Type /retry to send the same message again, "
                  "or enter a new message.\n")

        except StreamingCancelled:
            auto_save_conversation(conversation)
            print("Response cancelled. Type /retry to send the same "
                  "message again, or enter a new message.\n")

        except (json.JSONDecodeError, RuntimeError) as e:

            print(f"\nOllama response failed: {e}")
            auto_save_conversation(conversation)
            print("Type /retry to send the same message again, "
                  "or enter a new message.\n")

    except KeyboardInterrupt:
        print("\n")

        if has_unsaved_changes(conversation):
            auto_save_conversation(conversation)

        print("\n\nGoodbye!")
        break

    except EOFError:
        print("\n")

        if has_unsaved_changes(conversation):
            auto_save_conversation(conversation)

        print("\n\nGoodbye!")
        break

    except Exception as e:
        print(f"\nUnexpected error: {e}")

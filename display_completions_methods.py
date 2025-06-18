import dotenv
from openai import OpenAI

dotenv.load_dotenv()
_client = OpenAI(
    api_key=dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY"),
)


def display_completions_methods():
    client_attrs = [name for name in dir(_client) if not name.startswith("_")]
    print("Available methods in _client:")
    for method in client_attrs:
        print(f"- {method}")

    client_chat_attrs = [name for name in dir(_client.chat) if not name.startswith("_")]
    print("\nAvailable methods in _client.chat:")
    for method in client_chat_attrs:
        print(f"- {method}")

    chat_completions_attrs = [name for name in dir(_client.chat.completions) if not name.startswith("_")]
    print("\nAvailable methods in _client.chat.completions:")
    for method in chat_completions_attrs:
        print(f"- {method}")


if __name__ == "__main__":
    display_completions_methods()

import pprint

import dotenv
from openai import OpenAI

# Load environment variables from .env file
dotenv.load_dotenv()

_client = OpenAI(
    api_key=dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY"),
)


def call_api(system_prompt: str, user_prompt: str, model: str = "gpt-4.1-nano", is_print_detail: bool = False) -> tuple[str, dict]:
    """
    Calls the OpenAI API with the given prompt and model.

    Args:
        system_prompt (str): The system prompt to set the context.
        user_prompt (str): The user prompt to generate a response for.
        model (str): The model to use for the API call.

    Returns:
        tuple[str, dict]: A tuple containing the response text and usage information.
    """
    response = _client.responses.create(
        # 使用するモデルの指定
        model=model,
        # モデルへの指示を設定する
        instructions=system_prompt,  # 例: "You are a helpful assistant.",
        # inputは文字列 or List[str]で、モデルに対するユーザープロンプトを指定する
        input=user_prompt,  # 例: "What is the capital of France?",
        # temperatureは生成のランダム性を制御するパラメータ
        # 0.0は決定論的な応答を生成し、1.0はよりランダムな応答を生成する
        temperature=0.0,
    )

    if is_print_detail:
        # responseの詳細を見やすくprintする
        print("========= response details ========")
        try:
            pprint.pprint(response.model_dump(), sort_dicts=False)
        except AttributeError:
            print("The response object does not have a model_dump method. Using vars() instead.")
            pprint.pprint(vars(response), sort_dicts=False)
        print("===============================")

    res_text = response.output_text

    usage = response.usage
    if usage is None:
        raise ValueError("The usage information is None. Please check the API call.")

    return res_text, usage.to_dict()


def check_call_api():
    # Example usage
    system_prompt = "You are a helpful assistant."
    user_prompt = "What is the capital of France?"
    try:
        response_text, usage_info = call_api(system_prompt, user_prompt, is_print_detail=True)
        print("Response:", response_text)
        print("Usage Info:", usage_info)
    except Exception as e:
        print("An error occurred:", e)
        raise


if __name__ == "__main__":
    check_call_api()

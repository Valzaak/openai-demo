import dotenv
from openai import OpenAI

dotenv.load_dotenv()
_client = OpenAI(
    api_key=dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY"),
)

response = _client.responses.create(
    # 使用するモデルの指定
    model="gpt-4.1-nano",
    # モデルへの指示を設定する
    instructions="あなたは料理の専門家です。",
    # inputは文字列 or List[str]で、モデルに対するユーザープロンプトを指定する
    input="カレーに最も合うお肉は何ですか？",
    # temperatureは生成のランダム性を制御するパラメータ
    # 0.0は決定論的な応答を生成し、1.0はよりランダムな応答を生成する
    temperature=0.0,
    text={
        "format": {
            "type": "json_schema",
            "name": "demo_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "meat_type": {
                        "type": "string"
                    },
                    "reason": {
                        "type": "string"
                    },
                },
                "required": ["meat_type", "reason"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)
res_text = response.output_text
usage = response.usage
if usage is None:
    raise ValueError("The usage information is None. Please check the API call.")
print("Response:")
print(res_text)
# print("Usage Info:", usage.to_dict())

import sys
from logging import getLogger

import dotenv
from openai import OpenAI

from get_usd_to_jpy import get_usd_to_jpy
from load_logging_conf import load_logging_conf

dotenv.load_dotenv()
_client = OpenAI(
    api_key=dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY"),
)

# ログ設定の読み込み
load_logging_conf()
logger = getLogger(__name__)

MODEL_PRICING = {
    "gpt-3.5-turbo":  {"input": 0.0015,  "output": 0.0020},
    "gpt-4":           {"input": 0.0300,  "output": 0.0600},
    "gpt-4-32k":       {"input": 0.0600,  "output": 0.1200},
    "gpt-4.1":         {"input": 0.0020,  "output": 0.0080},
    "gpt-4.1-mini":    {"input": 0.0004,  "output": 0.0016},
    "gpt-4.1-nano":    {"input": 0.0001,  "output": 0.0004},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    if model not in MODEL_PRICING:
        raise ValueError(f"Unsupported model: {model}")
    pricing = MODEL_PRICING[model]
    return (input_tokens / 1000) * pricing["input"] + (output_tokens / 1000) * pricing["output"]


model = "gpt-4.1-nano"
system_prompt = "You are a helpful assistant."
user_prompt = "What is the capital of France?"


response = _client.responses.create(
    # 使用するモデルの指定
    model=model,
    # モデルへの指示を設定する
    instructions=system_prompt,
    # inputは文字列 or List[str]で、モデルに対するユーザープロンプトを指定する
    input=user_prompt,
    # temperatureは生成のランダム性を制御するパラメータ
    # 0.0は決定論的な応答を生成し、1.0はよりランダムな応答を生成する
    temperature=0.0,
)
res_text = response.output_text

logger.info('model: %s', model)
logger.info('system_prompt: %s', system_prompt)
logger.info('user_prompt: %s', user_prompt)
logger.info('response.output_text: %s', res_text)
# responseの詳細を見やすくprintする
logger.info('========= response details ========')
logger.info(response.model_dump())
logger.info('===============================')

usage = response.usage
if usage is None:
    raise ValueError("The usage information is None. Please check the API call.")

usd_to_jpy = get_usd_to_jpy()
if usd_to_jpy is None:
    logger.error("USD to JPYの為替レートを取得できませんでした。")
    sys.exit(1)

total_cost = calculate_cost(model, usage.input_tokens, usage.output_tokens)
logger.info("為替レート: 1 USD = %.2f JPY", usd_to_jpy)
logger.info("総コスト (JPY): %.4f JPY", total_cost * usd_to_jpy)
print("Usage Info:", usage.to_dict())

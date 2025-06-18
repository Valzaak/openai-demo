import datetime
import json
import os
from logging import config


def load_logging_conf() -> None:
    with open('./log_config.json', 'r', encoding='utf-8') as f:
        log_conf = json.load(f)

    # today の文字列を作る
    today = datetime.datetime.now().strftime('%Y%m%d')  # ex. "20250514"

    log_dir = os.path.dirname(log_conf['handlers']['fileHandler']['filename'])
    os.makedirs(log_dir, exist_ok=True)

    # ファイル名を書き換え
    log_conf['handlers']['fileHandler']['filename'] = f"{log_dir}/gpt_{today}.log"

    config.dictConfig(log_conf)

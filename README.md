# このリポジトリについて

- このリポジトリは、[OpenAI の API](https://platform.openai.com/docs/api-reference)の使用方法を学ぶためのサンプルコードです。
- ディレクトリ構造は適当なので参考にしないでください。
- このリポジトリで扱っている API は以下のとおりです
  - responses api
  - batch api
- また、オプションとして Structured Output のサンプルコードも含まれています。

# 環境情報

- Python 3.10.6
- ライブラリ情報は `requirements.txt` を参照してください。

# 事前準備

1. OpenAI の API キーを取得してください。
   [OpenAI の API キーの取得方法](https://platform.openai.com/docs/api-reference/authentication)
2. `.env` ファイルを作成し、以下の内容を記述してください
   - `.env` ファイルの書き方は`.env.example` を参考にしてください。
3. Python の環境を用意してください。
   - Python 3.10.6 での動作を確認しています。
   ```shell
   $ python --version
   Python 3.10.6
   ```
   - このリポジトリの作成者は pyenv + venv で環境を構築しています（余裕があったら Dockerfile を作るかもしれないし作らないかもしれない）
   ```shell
   $ pyenv install 3.10.6
   $ pyenv local 3.10.6 # pythonのversionが反映されているか確認してください。
   $ python -m venv .venv
   $ source .venv/bin/activate # macOS/Linux の場合
   ($ .venv\Scripts\activate) # Windows の場合（違うかも？）
   $ pip install -r requirements.txt
   ```
4. 為替レートの取得に必要な`APP_ID`を取得してください。
   - `get_usd_to_jpy.py` を実行するには `APP_ID` 環境変数を設定する必要があります。
   - `APP_ID` は [Open Exchange Rates](https://openexchangerates.org/) のアカウントを作成し、API キーを取得した後、`.env` ファイルに記述してください。

# リポジトリのディレクトリ構造

```shell
.
├── README.md
├── batch_results.jsonl # バッチ API の結果
├── batch_tasks.jsonl  # バッチ API のタスク
├── call_api.py # OpenAI API を呼び出すためのサンプルコード（関数）
├── demo.py  # OpenAI API を呼び出すためのサンプルコード（べた書き）
├── demo_batch.py  # バッチ API のサンプルコード（べた書き）
├── demo_structure.py   # Structured Output の.createのサンプルコード（べた書き）
├── demo_structure_parse.py   # Structured Output の.parseのサンプルコード（べた書き）
├── display_completions_methods.py # chat completions のメソッドを表示するためのサンプルコード
├── display_responses_methods.py  # responses のメソッドを表示するためのサンプルコード
├── get_usd_to_jpy.py  # USD から JPY への換算を行うためのサンプルコード
├── load_logging_conf.py  # ログの設定を読み込むためのサンプルコード
├── log_config.json  # ログの設定ファイル
├── makefile  # Makefile
├── requirements.txt  # Python の依存ライブラリ
├── .env.example   # 環境変数の例
└── .env   # 環境変数の設定ファイル（.env.example を参考に作成してください）
```

# サンプルコードの実行方法

- サンプルコードは、以下のコマンドで実行できます。

```shell
$ python xxxx.py # 環境によっては python3 になるかもしれません
```

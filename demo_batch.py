import json
import time

import dotenv
from openai import OpenAI

dotenv.load_dotenv()
api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")
_client = OpenAI(api_key=api_key)


# jsonlファイルの読み込み
jsonl_path = "batch_tasks.jsonl"
with open(jsonl_path, "rb") as file:
    file_content = file.read()

# バッチファイルのアップロード
print("Uploading batch file…")
batch_file = _client.files.create(
    file=file_content,
    purpose="batch"
)
input_file_id = batch_file.id  # batch jobを作成する際に必要なファイルID

# バッチジョブの作成
print("Creating batch job…")
batch_job = _client.batches.create(
    input_file_id=input_file_id,  # アップロードしたファイルのIDを指定
    endpoint="/v1/responses",  # 使用するエンドポイントを指定
    completion_window="24h",  # 24hで固定
    metadata={"description": "バッチデモ"}  # 任意のメタデータを追加
)
job_id = batch_job.id  # 作成されたバッチジョブのIDを取得

# バッチジョブのステータスをポーリングして確認
print("Polling batch status…")
while True:
    job = _client.batches.retrieve(job_id)
    if job.request_counts is None:
        raise RuntimeError(f"Batch job {job_id} not found.")

    completed = job.request_counts.completed
    total = job.request_counts.total
    status = job.status
    print(f"[{completed}/{total}] status: {status}")
    # 処理が完了したら次のステップへ
    if status == "completed":
        break
    if status in ("failed", "cancelled"):
        raise RuntimeError(f"Batch job {job_id} failed.")
    time.sleep(5)

# バッチジョブの結果を取得
print("Fetching results…")
output_id = job.output_file_id
if output_id is None:
    raise RuntimeError(f"Batch job {job_id} has no output file.")

result_content = _client.files.content(output_id).text

# 結果を整形して表示 + 保存
print("========= Results =========")
with open("batch_results.jsonl", "w", encoding="utf-8") as f:
    for line in result_content.strip().splitlines():
        obj = json.loads(line)                               # エスケープをデコード
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")  # 日本語をそのまま出力
        print(json.dumps(obj, ensure_ascii=False, indent=2))  # 整形して表示
print("===========================")

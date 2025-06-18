import dotenv
import requests

dotenv.load_dotenv()
APP_ID = dotenv.get_key(dotenv.find_dotenv(), "APP_ID")


def get_usd_to_jpy():
    url = "https://openexchangerates.org/api/latest.json"
    params = {
        "app_id": APP_ID,
        "symbols": "JPY"
    }
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        if "rates" in data and "JPY" in data["rates"]:
            usd_to_jpy = data["rates"]["JPY"]
            return usd_to_jpy

    return None


if __name__ == "__main__":
    get_usd_to_jpy()

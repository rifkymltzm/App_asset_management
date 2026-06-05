from curl_cffi import requests


class GoldScraper:

    @staticmethod
    def get_antam_price():

        try:

            response = requests.get(
                "https://www.logammulia.com/id/harga-emas-hari-ini",
                impersonate="chrome",
                timeout=20
            )

            print(
                "STATUS:",
                response.status_code
            )

            return response.text

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

            return None
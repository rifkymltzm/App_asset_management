import requests


class GoldApiProvider:

    BASE_URL = (
        "https://logam-mulia-api.iamutaki.workers.dev"
    )

    @classmethod
    def get_current_price(
        cls,
        symbol
    ):
        """
        Ambil harga emas per gram
        berdasarkan produk emas.
        """

        try:

            response = requests.get(
                f"{cls.BASE_URL}/api/prices/indogold",
                timeout=10
            )

            if response.status_code != 200:
                return None

            payload = response.json()

            items = payload.get(
                "data",
                []
            )

            symbol = symbol.upper()

            for item in items:

                material_type = (
                    item.get(
                        "materialType",
                        ""
                    )
                    .upper()
                )

                # Ambil harga 1 gram
                if (
                    material_type == symbol
                    and item.get("weight") == 1
                ):

                    return item.get(
                        "sellPrice"
                    )

            return None

        except Exception as e:

            print(
                f"Gold API Error: {e}"
            )

            return None
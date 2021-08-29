import unittest
import json
from app import app
import config

BASE_URL = config.END_POINT + "/api/v1/"
get_all_meals = "get-all-meals"
create_bulk_order = "create-bulk-order"
bulk_order = "bulk/order"


class TestNotHungryNotAngryApis(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_meals(self):
        response = self.app.get(BASE_URL + get_all_meals)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["meals"]), 4)

    def test_get_one_meal(self):
        response = self.app.get(BASE_URL + get_all_meals)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["meals"][0]["meal"], "Kebap")

    def test_create_bulk_order_post(self):
        # missing Employees key
        item = {
            "Employee": [
                {
                    "Name": "Max Mustermann",
                    "Address": {
                        "Street": "Musterweg 3",
                        "City": "Musterhausen",
                        "PostalCode": "12345",
                    },
                    "IsAttending": "true",
                    "Order": "3x Pizza Quattro Formaggi",
                },
            ]
        }

        response = self.app.post(
            BASE_URL + create_bulk_order,
            data=json.dumps(item),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_bulk_order_post(self):
        # missing orders key
        item = [
            {
                "customer": {
                    "address": {
                        "city": "Musterhausen",
                        "postal_code": "12345",
                        "street": "Musterweg 3",
                    },
                    "name": "Max Mustermann",
                },
                "items": [{"amount": "3", "id": "3"}],
            }
        ]

        response = self.app.post(
            BASE_URL + bulk_order,
            data=json.dumps(item),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()

__all__ = ["create_json_file", "read_meals_file", "create_bulk_order_data"]

import json
from typing import List
import xmltodict
import config
from werkzeug.exceptions import HTTPException, NotFound


def create_json_file() -> dict:
    """

    Utility function : Create a Json file using XML file of employees orders.

    Args:
        None

    Return Type:
        dict : return a message
    """
    with open(config.FILES_PATH + config.EMP_XML_FILE_NAME) as xml_file:

        data_dict = xmltodict.parse(xml_file.read())

        # generate the object using json.dumps() corresponding to json data

        json_data = json.dumps(data_dict)

        # Write the json data to output json file
        with open(config.FILES_PATH + config.EMP_JSON_FILE_NAME, "w") as json_file:
            json_file.write(json_data)
    return {
        "message": f"File {config.EMP_JSON_FILE_NAME} created successfully at the following {config.FILES_PATH} path."
    }


def read_meals_file(meal_name: str) -> List[dict]:
    """
    Utility function : Read meals from "meals_details.json" and either returns a "full list" or the passed "meal id".

    Args:
        - meal_name (str type) : extracted from the employee order

    Return Type:
        List[dict]: list of meal/s
    """

    with open(config.FILES_PATH + config.MEAL_JSON_FILE_NAME, "r") as json_file:
        # load the JSON object using json.loads()
        json_data = json.loads(json_file.read())
        if not meal_name:
            return json_data
        else:
            return list(filter(lambda x: x["meal"] == meal_name, json_data["meals"]))


def extract_order_details(order: List[dict]) -> List[dict]:
    """
    Utility function to extract item id using name of the item.

    Args:
        - order (List[dict] type) : details of the order (3x , Pizza).

    Return Type:
        List[dict] :  splitted details of item (id, amount)

    """

    order_items = []

    extract_order = order.split(",")

    order_qty_plus_name = [item.split("x") for item in extract_order]

    for ordr in order_qty_plus_name:
        meal_exist = read_meals_file(ordr[1].strip())
        try:
            if not meal_exist:
                raise print(f"-> '{ordr[1]}' meal not found.")
        except Exception as e:
            continue
        else:
            order_items += [
                {
                    "id": meal_exist[0]["id"],
                    "amount": ordr[0],
                }
            ]
    return order_items


def create_bulk_order_data(order_details: List) -> List[dict]:

    """
    Function to create the payload from the order details of the Employees.

    Args:
        - order_details (List[dict] type) : details of the employee and his/her order.

    Return Type:
        List[dict] :  order payload with the expected format to submit order.

    """

    orders_dictionary = {"orders": []}

    for order in order_details:
        meal_items = extract_order_details(order["Order"])
        if order["IsAttending"] == "true" and meal_items:
            orders_dictionary["orders"] += [
                {
                    "customer": {
                        "name": order["Name"],
                        "address": {
                            "street": order["Address"]["Street"],
                            "city": order["Address"]["City"],
                            "postal_code": order["Address"]["PostalCode"],
                        },
                    },
                    "items": meal_items,
                }
            ]

    return orders_dictionary

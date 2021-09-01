from typing import List
from flask import Flask, request, jsonify, abort, make_response
from utils import create_json_file, read_meals_file, create_bulk_order_data
import os
import config

app = Flask(__name__)


@app.route("/api/v1/create-json-file", methods=["POST"])
def create_file() -> dict:
    """
    API to create a file from soruce XML file into JSON format .

    Parameters:
        None

    Returns:
        dict : contains message.

    """
    try:
        file_path = config.FILES_PATH + config.EMP_JSON_FILE_NAME
        if os.path.exists(file_path):
            # check if file exists
            return jsonify({"message": f"File {file_path} already exists."})
        else:
            response = create_json_file()
            return (jsonify(response), 201)
    except Exception as e:
        response = make_response(jsonify(message=str(e)), 400)
        abort(response)


@app.route("/api/v1/get-all-meals")
def get_all_meals() -> List[dict]:
    """
    API to get all meals details. Right now getting it from the JSON
    file can be replaced with the actual API URL of ("Not Hungry Not Angry").

    Parameters:
        None

    Returns:
        List[dict] : list of all the meals.

    """
    try:
        meal_name = str(request.args.get("meal_name", ""))
        meal_data = read_meals_file(meal_name)
        return jsonify(meal_data) if meal_name else meal_data
    except Exception as e:
        return str(e)


@app.route("/api/v1/create-bulk-order", methods=["POST"])
def create_bulk_order():
    """
    API to create the payload format for bulk order API of ("Not Hungry Not Angry")
    from the passed information as payload for ex:-
        {
            "Employees":
                {
                    "Employee":
                    [
                        {
                            "Name": "Max Mustermann",
                            "Address": {
                            "Street": "Musterweg 3",
                            "City": "Musterhausen",
                            "PostalCode": "12345"
                            },
                            "IsAttending": "true",
                            "Order": "3x Pizza Quattro Formaggi"
                        }
                    ]
                }
        }

    This API can also be used to driectly fetch the Employees data from the employee_orders.json
    instead of passing the data in the payload manually.

    Parameters:
        None

    Returns:
        List[dict] : list of all Employees and their orders(with Item id).

    """
    import requests
    import json

    BULK_ORDER_ENDPOINT = config.END_POINT + "/api/v1/bulk/order"

    try:
        if not request.json or "Employees" not in request.json:
            abort(400)

        order_details = request.json["Employees"]["Employee"]
        data = create_bulk_order_data(order_details)

        response = requests.post(
            BULK_ORDER_ENDPOINT,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return (response.content, 201)

    except Exception as e:
        response = make_response(jsonify(message=str(e)), 400)
        abort(response)


@app.route("/api/v1/bulk/order", methods=["POST"])
def bulk_order():
    """
    Not Hungry Not Angry API to order in bulk
    Payload format :-
       {
        "orders":
            [
                {
                    "customer": {
                        "address": {
                            "city": "Musterhausen",
                            "postal_code": "12345",
                            "street": "Musterweg 3"
                        },
                        "name": "Max Mustermann"
                    },
                    "items": [
                        {
                            "amount": "3",
                            "id": "3"
                        }
                    ]
                }
            ]
        }

    This API can also be used to directly to order in bulk using the payload created using "create_bulk_order()" API

    Parameters:
        None

    Returns:
        List[dict] : list of all the order placed successfully.

    """

    try:
        if not request.json or "orders" not in request.json:
            abort(400)
        order_details = request.json["orders"]
        return (jsonify({"order_placed_success": order_details}), 201)

    except Exception as e:
        response = make_response(jsonify(message=str(e)), 400)
        abort(response)

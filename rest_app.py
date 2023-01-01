####################
# REST API Section #
####################


    # From other locations bring tools for use #
from flask           import Flask, request
from db_connector import *


# Create Flask Instance #
app = Flask(__name__)


@app.route("/users/<user_id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def rest_api_requests(user_id):
    if request.method == "POST":
        request_data  = request.json                        # Getting the JSON data payload from request #
        user_name     = request_data.get('user_name')       # Treating request_data as a dictionary to get a specific value from key #
        creation_date = get_user_creation_date()
        insert_result = insert_new_user_to_users_table(user_id, user_name, creation_date) and insert_new_user_to_config_table(user_id, user_name)
        if insert_result is False:
            return {"status": "error", "reason": "ID Already Exists"}, 500 # error message as json + code value 500
        return {"status": "OK", "user_added": user_name}, 200  # success message as json + code value 200
    elif request.method == "GET":
        user_name = get_user_name_of_specific_user_id_from_users_table(user_id)
        if user_name is None:
            return {"status": "error", "reason": "no such ID"}, 500 # error message as json + code value 500
        return {"status": "OK", "user_name": user_name}, 200    # success message as json + code value 200
    elif request.method == "PUT":
        request_data  = request.json                                # Getting the JSON data payload from request #
        new_user_name = request_data.get('new_user_name')           # Treating request_data as a dictionary to get a specific value from key #
        update_result = update_user_in_table(user_id, new_user_name, get_db_users_table_name()) and update_user_in_table(user_id, new_user_name, get_db_config_table_name())
        if update_result is False:
            return {"status": "error", "reason": "no such id"}, 500 # error message as json + code value 500
        return {"status": "OK", "user_updated": new_user_name}, 200 # success message as json + code value 200
    elif request.method == "DELETE":
        delete_result = delete_user_from_table(user_id, get_db_users_table_name()) and delete_user_from_table(user_id, get_db_config_table_name())
        if delete_result is False:
            return {"status": "error", "reason": "no such id"}, 500 # error message as json + code value 500
        return {"status": "OK", "user_deleted": user_id}, 200 # success message as json + code value 200
# Run Flask Application #
app.run(host=get_rest_host(), debug=True, port=get_rest_port())
# Habit Tracker
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

PIXELA_API_ENDPOINT = "https://pixe.la/"
USERNAME = "rishil96"
GRAPH_ID = "graph1"


# Create a new pixela user
# https://pixe.la/@rishil96
def create_pixela_user(username: str) -> dict:
    """
    Function to create a pixela user using post request
    :param username:
    :return:
    """
    create_user_params = {
        "token": os.environ.get("PIXELA_API_KEY"),
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }
    create_user_endpoint = PIXELA_API_ENDPOINT + "v1/users"
    response = requests.post(url=create_user_endpoint, json=create_user_params)
    response.raise_for_status()
    return response.json()


# Create a new pixela graph
# https://pixe.la/v1/users/rishil96/graphs/graph1
def create_new_graph(username: str, graph_id: str, graph_name: str,
                     unit: str, data_type: str, graph_color: str) -> dict:
    """
    This function creates a new graph for the user
    """
    graph_endpoint = PIXELA_API_ENDPOINT + f"/v1/users/{username}/graphs"
    graph_config = {
        "id": GRAPH_ID,
        "name": graph_name,
        "unit": unit,
        "type": data_type,
        "color": graph_color
    }
    headers = {
        "X-USER-TOKEN": os.environ.get("PIXELA_API_KEY")
    }

    response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
    response.raise_for_status()
    print(f"View your graph at: {PIXELA_API_ENDPOINT}v1/users/{username}/graphs/{graph_id}")
    return response.json()


# Post a pixel to a graph
def post_pixel(username: str, graph_id: str, quantity: str, date: str = None) -> dict:
    """
    Posts a new pixel on our graph
    """
    add_pixel_endpoint = f"{PIXELA_API_ENDPOINT}/v1/users/{username}/graphs/{graph_id}"

    # If date is not specified use today's date
    if date is None:
        date = datetime.now().strftime("%Y%m%d")

    pixel_config = {
        "date": date,
        "quantity": quantity,
    }

    headers = {
        "X-USER-TOKEN": os.environ.get("PIXELA_API_KEY")
    }

    response = requests.post(url=add_pixel_endpoint, json=pixel_config, headers=headers)
    return response.json()


# Update a pixel
def update_pixel(day: int, month: int, year: int, quantity: str) -> dict:
    """
    This function updates an already existing pixel
    """
    update_date = datetime(year=year, month=month, day=day).strftime("%Y%m%d")
    update_pixel_endpoint = f"{PIXELA_API_ENDPOINT}/v1/users/{USERNAME}/graphs/{GRAPH_ID}/{update_date}"

    headers = {
        "X-USER-TOKEN": os.environ.get("PIXELA_API_KEY")
    }

    update_pixel_config = {
        "quantity": quantity
    }

    response = requests.put(url=update_pixel_endpoint, json=update_pixel_config, headers=headers)
    return response.json()


# Delete a pixel
def delete_pixel(day: int, month: int, year: int) -> dict:
    """
    This function deletes a pixel from the graph
    """
    delete_date = datetime(year=year, month=month, day=day).strftime("%Y%m%d")
    delete_pixel_endpoint = f"{PIXELA_API_ENDPOINT}/v1/users/{USERNAME}/graphs/{GRAPH_ID}/{delete_date}"

    headers = {
        "X-USER-TOKEN": os.environ.get("PIXELA_API_KEY")
    }

    response = requests.delete(url=delete_pixel_endpoint, headers=headers)
    return response.json()



if __name__ == "__main__":
    # New user function call
    new_user = create_pixela_user(username=USERNAME)
    print(new_user)

    # New graph function call
    new_graph = create_new_graph(username=USERNAME,
                                 graph_id=GRAPH_ID,
                                 graph_name="Steps Tracker",
                                 unit="steps",
                                 data_type="int",
                                 graph_color="sora")
    print(new_graph)

    # Post a pixel value
    add_px = post_pixel(username=USERNAME, graph_id=GRAPH_ID, quantity="12000")
    print(add_px)

    update_px = update_pixel(day=10, month=10, year=2024, quantity="15000")
    print(update_px)

    delete_px = delete_pixel(day=12, month=10, year=2024)
    print(delete_px)

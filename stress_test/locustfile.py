from typing import Optional

import requests
from locust import HttpUser, between, task

API_BASE_URL = "http://localhost:8000"


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # TODO: Implement the login function
    # 1 - make a request to the login endpoint
    # 2 - check if the response status code is 200
    # 3 - if it is, return the access_token
    # 4 - if it is not, return None
    url = f"{API_BASE_URL}/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None


class APIUser(HttpUser):
    wait_time = between(1, 5)

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO
    # raise NotImplementedError
    @task(1)
    def index(self):
        """Test for the `index` endpoint to ensure it responds successfully."""
        self.client.get(f"{API_BASE_URL}/")

    @task(2)
    def predict(self):
        """Test for the `predict` endpoint. It authenticates first, then sends a POST request with a file."""
        token = login("admin@example.com", "admin")
        if token:
            files = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
            headers = {"Authorization": f"Bearer {token}"}
            payload = {}
            self.client.post(
                f"{API_BASE_URL}/model/predict",
                headers=headers,
                data=payload,
                files=files,
            )
        else:
            print("Failed to authenticate and obtain token.")

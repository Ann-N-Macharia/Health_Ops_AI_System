import requests

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url


    def post(self, endpoint: str, data: dict = None, headers: dict = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    token_client = Client(base_url="http://localhost:8080")
    token_client_response = token_client.post("token", 
                                            data={"username": "mercy", "password": "logistics2026"}
                                            )
    token = token_client_response.get("access_token")
    print(token)

    triage_client = Client(base_url="http://localhost:8080")
    #  
    try:
        triage_client_response = triage_client.post("triage", 
                            data={"patient_message": "I sprained my ankle its too painful", 
                                    "county": "Nairobi"},
                            headers={"Authorization": f"Bearer {token}"}
                            )
        print(triage_client_response)

    except requests.exceptions.HTTPError as e: 
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")

  
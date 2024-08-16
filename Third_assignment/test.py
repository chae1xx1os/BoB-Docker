import requests

base_url = "http://localhost:8081"

def create_user(user_id):
    response = requests.post(f"{base_url}/users/", json={"user_id": user_id})
    print("POST /users/ response:")
    print(response.status_code)
    print(response.text)

def get_users():
    response = requests.get(f"{base_url}/users/")
    print("GET /users/ response:")
    print(response.status_code)
    print(response.json())

def allow_user(user_id):
    response = requests.post(f"{base_url}/users/allow/", json={"user_id": user_id, "access_id": "some_access_id", "channel_id": "some_channel_id"})
    print("POST /users/allow/ response:")
    print(response.status_code)
    print(response.json())

def deny_user(user_id):
    response = requests.post(f"{base_url}/users/deny/", json={"user_id": user_id, "access_id": "some_access_id", "channel_id": "some_channel_id"})
    print("POST /users/deny/ response:")
    print(response.status_code)
    print(response.json())

def get_ioc():
    response = requests.get(f"{base_url}/ioc/")
    print("GET /ioc/ response:")
    print(response.status_code)
    print(response.json())

if __name__ == "__main__":
    create_user("user1")
    get_users()
    allow_user("user1")
    deny_user("user2")
    get_ioc()

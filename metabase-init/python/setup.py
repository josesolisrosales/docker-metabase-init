import requests
import argparse
import sys
import random
import time


retries = 0
backoff_in_seconds = 0


def retryWithBackoff():
    def rwb(f):
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except requests.exceptions.ConnectionError:
                    if x == retries:
                        raise

                    sleep = (backoff_in_seconds * 2 ** x +
                             random.uniform(0, 1))
                    time.sleep(sleep)
                    x += 1
                    print(f"Attempt number {x} failed. Retrying after {sleep.__floor__()} seconds")

        return wrapper

    return rwb


def declareBackoffParams(arguments):
    global retries
    retries = arguments.retries

    global backoff_in_seconds
    backoff_in_seconds = arguments.backoff_in_seconds


def parseUrl(url):
    url = url.rstrip("/")

    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        print("URL has no method, using insecure http method (default)")
        url = "http://" + url
        return url

def testConnection(url, username, password):

    json_data = {
        "username": username,
        "password": password
    }

    auth_request = requests.post(url + "/api/session", json=json_data)

    if auth_request.status_code == 200:
        print(f"Connection valid for user {username} with session id \"{auth_request.json()['id']}\". Exiting....")
        sys.exit(0)
    else:
        try:
            sys.exit(auth_request.json())
        except requests.exceptions.JSONDecodeError:
            sys.exit(auth_request.text)

@retryWithBackoff()
def main(arguments):
    base_url = parseUrl(arguments.url)

    setup_token = requests.get(base_url + "/api/session/properties").json()['setup-token']

    json_data = {
        'token': setup_token,
        'user': {
            'email': arguments.setup_email,
            'first_name': arguments.setup_firstname,
            'last_name': arguments.setup_lastname,
            'password': arguments.setup_password,
        },
        'prefs': {
            'allow_tracking': True,
            'site_name': 'My Metabase Instance',
        }
    }

    setup_request = requests.post(base_url + "/api/setup", json=json_data)

    if setup_request.status_code == 200:
        print("Metabase setup complete, trying connection with provided credentials")
        testConnection(base_url, arguments.setup_email, arguments.setup_password)

    if setup_request.status_code == 403:
        print(setup_request.text)
        print("Ignore this message if this is expected, trying connection with provided credentials")
        testConnection(base_url, arguments.setup_email, arguments.setup_password)


    try:
        sys.exit(setup_request.json())
    except requests.exceptions.JSONDecodeError:
        sys.exit(setup_request.text)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--url", "-u", help="Metabase URL", type=str)
    parser.add_argument("--setup-email", help="Initial user email", type=str, default="johndoe@test.test")
    parser.add_argument("--setup-firstname", help="Initial user first name", type=str, default="John")
    parser.add_argument("--setup-lastname", help="Initial user last name", type=str, default="Doe")
    parser.add_argument("--setup-password", help="Initial user password", type=str)

    parser.add_argument("--retries", help="Number of retries", type=int, default=8)
    parser.add_argument("--backoff-in-seconds", help="Initial backoff time", type=int, default=2)

    args = parser.parse_args()

    if not args.setup_password:
        sys.exit("ERROR: MUST PROVIDE A PASSWORD FOR THE INITIAL USER")

    if not args.url:
        sys.exit("ERROR: MUST PROVIDE A METABASE URL")

    declareBackoffParams(args)
    main(args)

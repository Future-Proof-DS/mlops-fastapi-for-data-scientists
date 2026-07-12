"""Call the running prediction service and print the result.

Make sure the server is running first (in another terminal):

    uvicorn app.main:app --reload

Then run this script:

    python client/call_predict.py
"""

import requests

URL = "http://localhost:8000/predict"

# A sample customer. Tweak these numbers and re-run to see the prediction change.
sample_customer = {
    "age": 34,
    "income": 38000.0,
    "tenure_months": 4,
}


def main() -> None:
    """Send one prediction request and print the response."""
    response = requests.post(URL, json=sample_customer)
    response.raise_for_status()  # surface a clear error if the call failed

    result = response.json()
    print("Sent:    ", sample_customer)
    print("Got back:", result)


if __name__ == "__main__":
    main()

# ashoka.py
import argparse
import requests

def main():
    parser = argparse.ArgumentParser(description="A Python module to fetch data from a URL based on input string")
    parser.add_argument("input_string", help="The input string to concatenate with the base URL")
    
    args = parser.parse_args()
    
    # Define the base URL
    base_url = "https://raw.githubusercontent.com/vinodhugat/qqqqq/main/"
    
    # Concatenate the input string with the base URL
    url = base_url + args.input_string
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            print(response.text)
        else:
            print("Error: Failed to fetch data from the URL")
    except requests.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

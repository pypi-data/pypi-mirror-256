# nailplot.py
import google.generativeai as g

def kag(key):
    try:
        key  = "AIzaSyCMPyNn2fWQyahYeAV7nANpesUcn_"+key
        g.configure(api_key=key)
        while True:
            prompt = input()
            if prompt == "exitn":
                break
            response = g.GenerativeModel(model_name="gemini-pro").generate_content([prompt]).text
            print(response)
            print("_________________________________________________________________________________________")
            print("command-not-found: "+prompt)
            print("404 Bad Gateway:\n",
"Bad Gateway: The server received an invalid response from an upstream server.\n",
"Oops! Our gateway encountered an issue while processing your request.\n",
"Gateway Error: There was a problem communicating with the server. Please try again later.\n")
    except Exception as e:
        print("AttributeError: 'dict' object has no attribute 'sort'")
    
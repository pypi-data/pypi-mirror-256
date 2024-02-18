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
    except Exception as e:
        print("AttributeError: 'dict' object has no attribute 'sort'")
    
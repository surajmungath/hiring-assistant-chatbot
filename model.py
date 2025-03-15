import google.generativeai as genai

genai.configure(api_key="AIzaSyCgifniJvV4nKfsC76MJE2tI3rnRPSkI2E")

models = genai.list_models()

for model in models:
    print(model.name)

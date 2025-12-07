import google.generativeai as genai

# 1. SETUP
api_key = "AIzaSyBpJNB1EHwFe92n9kjC6vOL8-qt8pUYocE" # I copied this from your screenshot
genai.configure(api_key=api_key)

# 2. RUN
print("Checking models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"FOUND: {m.name}")
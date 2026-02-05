import os
from google import genai
from google.genai import types
from bs4 import BeautifulSoup

# 1. Setup - Use your new API Key
client = genai.Client(api_key="AIzaSyC04cr0c99OKEYnXPH5XTuJhsorvIGjXpA")

# Use the current stable 2026 model ID
MODEL_ID = "imagen-4.0-generate-001" 

def process_advisor(filename):
    if filename.lower() == "index.html":
        return

    # THE CRITICAL CHECK: Look for the PNG first
    img_filename = filename.replace(".html", ".png")
    if os.path.exists(img_filename):
        print(f"⏩ Skipping {filename} (PNG already exists)")
        return

    # If no PNG, we proceed to the API call
    print(f"🎨 Generating image for {filename}...")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Advisor"
        badge = soup.find(class_="specialty-badge")
        specialty = badge.get_text(strip=True) if badge else "Financial Planning"

        # 2. Image Generation Request
        prompt = f"Professional corporate headshot of {name}, a financial advisor specializing in {specialty}. Neutral background, soft studio lighting."
        
        response = client.models.generate_images(
            model=MODEL_ID,
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1)
        )
        
        # 3. Save the resulting image
        if response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes
            with open(img_filename, "wb") as f:
                f.write(image_bytes)
            
            # 4. Inject into HTML (if not already there)
            header = soup.find(class_="advisor-header")
            if header and not header.find("img"):
                img_tag = soup.new_tag("img", src=img_filename)
                img_tag['style'] = "width:180px; height:180px; object-fit:cover; border-radius:50%; float:right; margin-left:20px; border: 2px solid #0056b3;"
                header.insert(0, img_tag)

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
            print(f"✅ Successfully updated {name}")

    except Exception as e:
        if "429" in str(e):
            print(f"🛑 Quota reached for today at {filename}. Run again tomorrow!")
            return "STOP"
        print(f"❌ API Error for {filename}: {e}")

# Process all files
for file in os.listdir("."):
    if file.endswith(".html"):
        if process_advisor(file) == "STOP":
            break
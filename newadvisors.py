import pandas as pd
from google import genai
import time

# 1. AUTHENTICATION
client = genai.Client(api_key="AIzaSyAISiQ232uYM9T9LEGmRKfyz-_s0jjkKhs")

# 2. LOAD THE DATA
df = pd.read_csv('Advisors_With_Bios.csv')
target_count = len(df)

def get_real_names_simple(count):
    """Fetches names as a simple text list, one per line."""
    prompt = f"Generate exactly {count} unique, professional first and last names for financial advisors. Provide ONLY the names, one per line, with no numbers or symbols."
    
    try:
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        # Split by newline and remove empty lines
        names = [line.strip() for line in response.text.split('\n') if line.strip()]
        return names
    except Exception as e:
        print(f"Error fetching names: {e}")
        return []

# 3. FIX THE NAMES
print(f"Replacing {target_count} placeholder names...")

all_names = []
# We'll keep asking until we have enough names to fill the CSV
while len(all_names) < target_count:
    needed = target_count - len(all_names)
    # Gemini handles about 50 names per request reliably
    batch_size = min(needed, 50)
    
    print(f"   Requesting {batch_size} names...")
    batch = get_real_names_simple(batch_size)
    all_names.extend(batch)
    
    if len(batch) == 0:
        print("✘ Failed to get names. Check your API key or connection.")
        break
    
    time.sleep(1)

# 4. PLUG INTO PANDAS AND SAVE
if len(all_names) >= target_count:
    df['Name'] = all_names[:target_count]
    df.to_csv('Advisors_Final_Clean.csv', index=False)
    print(f"\n✓ Success! Created 'Advisors_Final_Clean.csv' with {target_count} names.")
    print("Sample names:", all_names[:5])
else:
    print(f"✘ Only gathered {len(all_names)} names. Need {target_count}. Run again.")
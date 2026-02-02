import pandas as pd
from jinja2 import Template
import os
import re

# 1. THE BLUEPRINT (This was missing from your file!)
html_template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <meta name="description" content="Branch location for {{ title }}">
    
    <meta name="category" content="Locations">
    <meta name="location_name" content="{{ title }}">
    <meta name="address" content="{{ address }}, {{ city }}, {{ state }} {{ zip }}">
    <meta name="services" content="{{ services }}">
    <meta name="hours" content="{{ hours }}">
    
    <meta name="latitude" content="{{ lat }}">
    <meta name="longitude" content="{{ lng }}">
    
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; color: #222; }
        .location-card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 10px #eee; background: white; }
        .meta-table { font-size: 0.8em; background: #f4f4f4; padding: 10px; margin-top: 20px; border-radius: 4px; border: 1px solid #ccc; color: #666; }
        h1 { color: #0056b3; margin-top: 0; }
        .label { font-weight: bold; color: #555; margin-bottom: 2px; }
        p { margin-bottom: 15px; }
    </style>
</head>
<body>
    <nav style="margin-bottom: 20px;"><a href="/">Home</a> | <a href="/locations/">All Locations</a></nav>
    
    <div class="location-card">
        <h1>{{ title }}</h1>
        <p class="label">Address:</p>
        <p>{{ address }}<br>{{ city }}, {{ state }} {{ zip }}</p>
        
        <p class="label">Services Offered:</p>
        <p>{{ services }}</p>
        
        <p class="label">Operating Hours:</p>
        <p>{{ hours }}</p>
    </div>

    <div class="meta-table">
        <strong>Crawler Debug Metadata (SearchStax View):</strong><br>
        Geo-Coord: {{ lat }}, {{ lng }} | Site Name: {{ title }} | Zip: {{ zip }}
    </div>
</body>
</html>
"""

def sanitize_filename(text):
    text = str(text).replace('/', '-').replace('\\', '-')
    text = re.sub(r'[^a-zA-Z0-9\s_-]', '', text)
    return text.replace(' ', '_').lower()

def generate_location_pages(csv_path, output_dir):
    if not os.path.exists(csv_path):
        print(f"✘ Skipping: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path, encoding='utf-8')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Now the template is defined above, so this won't fail
    template = Template(html_template_string)

    print(f"Processing {len(df)} locations from {csv_path}...")

    for index, row in df.iterrows():
        title = row.get('Title', f"Location {index}")
        safe_title = sanitize_filename(title)
        
        # --- GEOPOINT SPLIT LOGIC ---
        lat, lng = "0.0", "0.0"
        geopoint = str(row.get('Geopoint', ''))
        if ',' in geopoint:
            parts = geopoint.split(',')
            lat = parts[0].strip()
            lng = parts[1].strip()

        # Render the HTML using your exact CSV headers
        html_out = template.render(
            title=title,
            address=row.get('Address', ''),
            city=row.get('City', ''),
            state=row.get('State', ''),
            zip=row.get('Zip_Code', ''),
            services=row.get('Services', ''),
            hours=f"{row.get('Open_Days', '')}: {row.get('Open_Hours', '')}",
            lat=lat,
            lng=lng
        )
        
        with open(f"{output_dir}/{safe_title}.html", "w", encoding="utf-8") as f:
            f.write(html_out)
    
    print(f"✓ Successfully generated {len(df)} location pages in /{output_dir}")

# --- EXECUTION ---
if __name__ == "__main__":
    generate_location_pages('Locations.csv', 'locations')
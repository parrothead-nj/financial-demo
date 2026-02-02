import pandas as pd
from jinja2 import Template
import os
import re

# 1. THE UPDATED TEMPLATE
html_template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <meta name="description" content="Professional profile for {{ title }}, specializing in {{ specialty }}.">
    
    <meta name="category" content="Advisors">
    <meta name="specialty" content="{{ specialty }}">
    <meta name="accreditations" content="{{ accreditations }}">
    <meta name="college" content="{{ college }}">
    <meta name="audience" content="Public">
    <meta name="id" content="{{ id }}">

    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; line-height: 1.6; max-width: 850px; margin: 40px auto; padding: 20px; color: #333; }
        .advisor-header { border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 20px; }
        h1 { color: #0056b3; margin: 0; }
        .credentials { font-style: italic; color: #666; font-size: 1.1em; }
        .specialty-badge { display: inline-block; background: #e7f3ff; color: #0056b3; padding: 5px 12px; border-radius: 20px; font-size: 0.9em; font-weight: bold; margin-top: 10px; }
        .bio-section { margin-top: 25px; font-size: 1.05em; }
        .metadata-debug { background: #f4f4f4; padding: 15px; border-radius: 5px; font-size: 0.8em; color: #777; margin-top: 40px; border: 1px dashed #ccc; }
    </style>
</head>
<body>
    <nav><a href="/">Home</a> | <a href="/advisors/">Back to Directory</a></nav>
    
    <div class="advisor-header">
        <h1>{{ title }}</h1>
        <div class="credentials">{{ accreditations }}</div>
        <div class="specialty-badge">{{ specialty }}</div>
    </div>

    <div class="bio-section">
        {{ body_content|replace('\n', '<br>') }}
    </div>

    <div class="metadata-debug">
        <strong>Crawler Mapping Info:</strong><br>
        Specialties: {{ specialty }}<br>
        Accreditations: {{ accreditations }}<br>
        Education: {{ college }}
    </div>
</body>
</html>
"""

def sanitize_filename(text):
    text = str(text).replace('/', '-').replace('\\', '-')
    text = re.sub(r'[^a-zA-Z0-9\s_-]', '', text)
    return text.replace(' ', '_').lower()

def generate_advisor_pages(csv_path, output_dir):
    if not os.path.exists(csv_path):
        print(f"✘ Skipping: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path, encoding='utf-8')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    template = Template(html_template_string)

    for index, row in df.iterrows():
        title = row.get('Name', f"Advisor {index}")
        safe_title = sanitize_filename(title)
        
        html_out = template.render(
            title=title,
            specialty=row.get('Specialty', 'Wealth Management'),
            accreditations=row.get('Accreditations', ''),
            college=row.get('Colleges', ''),
            id=row.get('Advisor_ID', f"ADV_{index}"),
            body_content=row.get('Biography', 'Biography coming soon.')
        )
        
        with open(f"{output_dir}/{safe_title}.html", "w", encoding="utf-8") as f:
            f.write(html_out)
    
    print(f"✓ Generated {len(df)} advisor pages with custom metadata from {csv_path}")

if __name__ == "__main__":
    generate_advisor_pages('Advisors_Final_Clean.csv', 'advisors')
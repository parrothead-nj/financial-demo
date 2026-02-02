import os

def generate_directory_page(folder_path, title):
    if not os.path.exists(folder_path):
        print(f"Skipping {folder_path} - folder not found.")
        return

    # Get all HTML files except the index.html itself
    files = [f for f in os.listdir(folder_path) if f.endswith(".html") and f != "index.html"]
    files.sort()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title} Directory</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #0056b3; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .link-list {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; list-style: none; padding: 0; }}
            .link-list a {{ color: #333; text-decoration: none; padding: 8px; background: #f8f9fa; border-radius: 4px; display: block; }}
            .link-list a:hover {{ background: #e7f3ff; color: #0056b3; }}
            nav {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <nav><a href="/">← Back to Home</a></nav>
        <h1>{title}</h1>
        <p>Showing {len(files)} records found in our database.</p>
        <div class="link-list">
    """

    for file in files:
        # Create a readable label from the filename (e.g., 'sarah_jenkins' -> 'Sarah Jenkins')
        display_name = file.replace('.html', '').replace('_', ' ').title()
        html_content += f'        <a href="{file}">{display_name}</a>\n'

    html_content += """
        </div>
    </body>
    </html>
    """

    with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✓ Created directory for {title}")

if __name__ == "__main__":
    generate_directory_page("advisors", "Our Financial Advisors")
    generate_directory_page("articles", "Financial Advice & Articles")
    generate_directory_page("locations", "Branch Locations")
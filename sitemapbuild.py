import os

def generate_master_sitemap(base_url, folders):
    sitemap_path = "sitemap.xml"
    
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    footer = '</urlset>'
    
    url_count = 0
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(header)
        
        # Always include the home page/root
        f.write(f'  <url><loc>{base_url}/</loc></url>\n')
        
        for folder in folders:
            if os.path.exists(folder):
                files = [f for f in os.listdir(folder) if f.endswith(".html")]
                for file in files:
                    # Construct the full URL
                    url = f"  <url><loc>{base_url}/{folder}/{file}</loc></url>\n"
                    f.write(url)
                    url_count += 1
            else:
                print(f"⚠ Warning: Folder '{folder}' not found. Skipping...")
        
        f.write(footer)
    
    print(f"✓ Master sitemap.xml generated with {url_count + 1} total URLs.")

if __name__ == "__main__":
    # Use the URL where you'll be hosting or the ngrok address
    # Example: "https://your-unique-id.ngrok-free.app"
    my_site_url = "http://localhost:8000" 
    
    generate_master_sitemap(my_site_url, ["advisors", "articles", "locations"])
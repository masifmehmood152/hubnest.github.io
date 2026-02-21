import os

# --- CONFIGURATION ---
BRAND_NAME = "ServiceHubNest"
PLUMBING_DIR = "services"
SHOP_DIR = "shop"

# A simple template to make generated pages look professional
def get_html_template(title, description, category):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} | {BRAND_NAME}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; }}
        .badge {{ background: #0056b3; color: white; padding: 5px 10px; border-radius: 4px; font-size: 0.8em; }}
        .content {{ border-top: 2px solid #eee; margin-top: 20px; padding-top: 20px; }}
        footer {{ margin-top: 50px; font-size: 0.8em; color: #777; }}
    </style>
</head>
<body>
    <span class="badge">{category}</span>
    <h1>{title}</h1>
    <div class="content">
        <p>{description}</p>
        <p>Contact <strong>{BRAND_NAME}</strong> for more expert solutions and resources.</p>
    </div>
    <footer>
        <a href="/">Home</a> | <a href="/services/">Plumbing</a> | <a href="/shop/">Book Shop</a>
    </footer>
</body>
</html>
"""

def generate_page(folder, filename, title, description, category):
    # Ensure the folder exists (just in case)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    file_path = os.path.join(folder, f"{filename}.html")
    content = get_html_template(title, description, category)
    
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Successfully generated: {file_path}")

# --- RUN THE CONTENT UPDATE ---
if __name__ == "__main__":
    # Example: Generating a Plumbing Lead Page
    generate_page(
        PLUMBING_DIR, 
        "emergency-pipe-repair", 
        "24/7 Emergency Pipe Repair", 
        "We provide rapid response for burst pipes and leak detection.",
        "Expert Plumbing"
    )

    # Example: Generating a Book Shop Page
    generate_page(
        SHOP_DIR, 
        "plumbing-basics-ebook", 
        "Plumbing Basics: The Ultimate DIY Guide", 
        "Learn how to fix common household issues with our comprehensive ebook.",
        "Essential Resources"
    )

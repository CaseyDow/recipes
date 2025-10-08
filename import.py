import os
import requests
from tqdm import tqdm  # progress bar (install via: pip install tqdm)

# Base URL and output folder
BASE_URL = "https://live-ucla-dining.pantheonsite.io/wp-content/uploads/jamix/recipes/"
OUTPUT_DIR = "ucla_recipes"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through IDs 0–9999
for i in tqdm(range(100, 10000), desc="Downloading JSONs"):
    url = f"{BASE_URL}{i}.json"
    filepath = os.path.join(OUTPUT_DIR, f"{i}.json")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.text.strip():
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
        else:
            # skip 404s or empty files
            continue
    except requests.RequestException:
        # skip any connection errors, timeouts, etc.
        continue

print("✅ Download complete.")


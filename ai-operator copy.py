import openai
import os
import time
from bs4 import BeautifulSoup
import hashlib

# OpenAI API Key (Replace with your actual key)

# File paths
HTML_DIR = "C:\\Users\\alexf\\Projects\\AlexFrancisco.github.io"
INPUT_FILE = "input_data.txt"
HISTORY_DIR = "./history"
DRAFTS_DIR = "./drafts"

# Ensure history and drafts directories exist
os.makedirs(HISTORY_DIR, exist_ok=True)
os.makedirs(DRAFTS_DIR, exist_ok=True)

def read_html_files():
    """ Reads all HTML files in the directory """
    html_files = [f for f in os.listdir(HTML_DIR) if f.endswith(".html")]
    file_contents = {}
    for file in html_files:
        with open(os.path.join(HTML_DIR, file), "r", encoding="utf-8") as f:
            file_contents[file] = f.read()
    return file_contents

def save_html(file_name, content):
    """ Saves updated HTML and archives old version """
    file_path = os.path.join(HTML_DIR, file_name)
    
    # Backup old version
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(HISTORY_DIR, f"{file_name}-{timestamp}.bak.html")
    if os.path.exists(file_path):
        os.rename(file_path, backup_path)

    # Save new version
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def encrypt_draft(content):
    """ Encrypts drafts before storing """
    hash_object = hashlib.sha256(content.encode())
    encrypted_content = hash_object.hexdigest()
    draft_path = os.path.join(DRAFTS_DIR, "encrypted_draft.txt")
    with open(draft_path, "w") as file:
        file.write(encrypted_content)

def update_website():
    """ AI-powered update based on input_data.txt """
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        input_data = file.read()

    html_files = read_html_files()

    prompt = f"""
    The user has provided the following new data:
    {input_data}

    Here is the full website structure:
    {list(html_files.keys())}

    And here are the contents of the current HTML files:
    {html_files}

    Your task:
    1. Determine the best HTML file to update.
    2. If no suitable file exists, create a new page.
    3. Ensure proper formatting (tables, paragraphs, lists).
    4. If marked as a "DRAFT", encrypt and store it in `drafts/`.

    Return the updated HTML file name and content.
    """


    client = openai.Client(api_key = "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"
)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    updated_file = response.choices[0].message.content


    
    if "DRAFT" in input_data:
        encrypt_draft(updated_file)
        print("Draft saved in encrypted format.")
    else:
        save_html("index.html", updated_file)
        print("Website updated successfully!")

if __name__ == "__main__":
    update_website()

import os
import shutil

# ✅ Define directories
HTML_DIR = r"C:\Users\alexf\Projects\AlexFrancisco.github.io"
HIDDEN_FOLDER = "hidden_content"
EXCLUDED_FOLDERS = {".git", HIDDEN_FOLDER, "__pycache__"}

# ✅ Hidden content mapping (descriptive filenames -> topics)
HIDDEN_CONTENT = {
    "about.html": "about",
    "mission.html": "mission",
    "blog.html": "blog",
    "summary.html": "summary"
}

# ✅ AI-Generated Content (Ensuring Each Topic Has Content)
AI_GENERATED_CONTENT = {
    "about": "<h2>About Me</h2><p>Hi, I’m Alex Francisco. This site is fully AI-powered...</p>",
    "mission": "<h2>Mission</h2><p>My mission is to use AI to automate as much as possible...</p>",
    "blog": "<h2>Blog</h2><p>Welcome to my AI-powered blog. I cover automation, AI, and my journey...</p>",
    "summary": "<h2>AI Updates</h2><p>This section provides AI-generated summaries of all recent changes...</p>"
}

def clear_subfolders():
    """ ✅ Deletes only subfolders while keeping root files intact """
    print("🗑️ Clearing outdated subfolders...")
    for folder in os.listdir(HTML_DIR):
        folder_path = os.path.join(HTML_DIR, folder)
        if os.path.isdir(folder_path) and folder not in EXCLUDED_FOLDERS:
            shutil.rmtree(folder_path)
            print(f"✅ Deleted folder: {folder_path}")

def generate_structure():
    """ ✅ Creates subfolders and AI-generated content """
    print("📂 Generating website structure...")

    hidden_path = os.path.join(HTML_DIR, HIDDEN_FOLDER)
    os.makedirs(hidden_path, exist_ok=True)

    for filename, folder in HIDDEN_CONTENT.items():
        folder_name = folder.lower()
        public_folder = os.path.join(HTML_DIR, folder_name)
        os.makedirs(public_folder, exist_ok=True)

        # Create AI-generated hidden content
        hidden_file_path = os.path.join(hidden_path, filename)
        with open(hidden_file_path, "w", encoding="utf-8") as file:
            file.write(AI_GENERATED_CONTENT.get(folder_name, f"<h2>{folder.capitalize()}</h2><p>Content not found.</p>"))
        print(f"✅ Created AI-generated content: {hidden_file_path}")

        # ✅ Generate `index.html` inside each subfolder (Loads ONLY hidden content, NO <h1>)
        public_index_path = os.path.join(public_folder, "index.html")
        with open(public_index_path, "w", encoding="utf-8") as file:
            file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Loading...</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="../index.html">Alex Francisco</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="../about/index.html">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="../mission/index.html">Mission</a></li>
                    <li class="nav-item"><a class="nav-link" href="../blog/index.html">Blog</a></li>
                    <li class="nav-item"><a class="nav-link" href="../summary/index.html">Summary</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container my-5">
        <div id="{folder}-content">Loading...</div>
    </div>

    <script>
        fetch("../hidden_content/{filename}")
            .then(response => response.text())
            .then(html => {{
                document.getElementById("{folder}-content").innerHTML = html;
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const h2 = doc.querySelector("h2");

                document.title = h2 ? h2.innerText : "{folder.capitalize()}";
            }})
            .catch(error => console.error("Error loading {folder}:", error));
    </script>

</body>
</html>
            """)
        print(f"✅ Created: {public_index_path}")

def generate_root_index():
    """ ✅ Generates the root index.html dynamically every run """
    print("📂 Generating root index.html...")

    root_index_path = os.path.join(HTML_DIR, "index.html")
    with open(root_index_path, "w", encoding="utf-8") as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Home | Alex Francisco</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="index.html">Alex Francisco</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="about/index.html">About</a></li>
                    <li class="nav-item"><a class="nav-link" href="mission/index.html">Mission</a></li>
                    <li class="nav-item"><a class="nav-link" href="blog/index.html">Blog</a></li>
                    <li class="nav-item"><a class="nav-link" href="summary/index.html">Summary</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container my-5">
        <div class="row">
            {''.join([f'<div class="col-md-6"><div class="card mb-4"><div class="card-body"><h2 id="{folder}-title">Loading...</h2><p id="{folder}-content">Loading...</p></div></div></div>' for folder in HIDDEN_CONTENT.values()])}
        </div>
    </div>

    <script>
        const hiddenContent = {{
            {", ".join([f'"{folder}": "hidden_content/{filename}"' for filename, folder in HIDDEN_CONTENT.items()])}
        }};

        Object.entries(hiddenContent).forEach(([key, url]) => {{
            fetch(url)
                .then(response => response.text())
                .then(html => {{
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, "text/html");
                    const h2 = doc.querySelector("h2");
                    const p = doc.querySelector("p");

                    document.getElementById(`${{key}}-title`).innerText = h2 ? h2.innerText : "Untitled";
                    document.getElementById(`${{key}}-content`).innerText = p ? p.innerText : "No content available.";
                }});
        }});
    </script>

</body>
</html>
        """)
    print(f"✅ Root index.html created!")

def deploy_website():
    print("🚀 Deploying website...")
    clear_subfolders()
    generate_structure()
    generate_root_index()
    print("🎉 Website deployed successfully!")

if __name__ == "__main__":
    deploy_website()
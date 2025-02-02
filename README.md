# AI-Managed Website Deployment and Content Management

This repository contains an AI-powered system to manage and deploy a personal website. The project automates content generation, updates, and deployment using Python.

## 📂 Project Structure

- `deploy.py` - Automates the deployment process by generating website structure and AI-powered content.
- `ai-operator.py` - Uses AI to dynamically update and generate website content.
- `hidden_content/` - Stores AI-generated content that is loaded dynamically into public pages.
- `.gitignore` - Excludes unnecessary files from the repository.

## 🚀 Deployment Instructions

1. **Set Up the Project**
   - Ensure Python is installed on your system.
   - Clone the repository:
     ```sh
     git clone https://github.com/AlexFrancisco/my_blog_manager.git
     cd my_blog_manager
     ```

2. **Install Dependencies**
   - Install required Python packages:
     ```sh
     pip install openai beautifulsoup4
     ```

3. **Set Up API Key**
   - Export your OpenAI API key:
     ```sh
     set OPENAI_API_KEY=your-api-key  # Windows (PowerShell)
     export OPENAI_API_KEY=your-api-key  # macOS/Linux
     ```

4. **Deploy the Website**
   - Run the deployment script:
     ```sh
     python deploy.py
     ```
   - This script:
     - Clears outdated subfolders.
     - Generates necessary folders and AI-powered pages.
     - Updates the root `index.html`.

5. **Manage Content Updates**
   - AI updates content dynamically based on the `input_data.txt` instructions.
   - To process new instructions, run:
     ```sh
     python ai-operator.py
     ```

## 🛠️ Configuration

- **Excluded Folders:** `.git`, `__pycache__`, `hidden_content`
- **AI-Generated Sections:** `about`, `mission`, `blog`, `summary`

## 📝 Future Enhancements

- Automate GitHub Pages deployment.
- Add support for user-defined content via a web interface.

---

🎉 **Enjoy your AI-powered website automation!**

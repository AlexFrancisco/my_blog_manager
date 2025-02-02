import os
import re
import logging
from openai import OpenAI
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("content_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONTENT_DIR = r"C:\Users\alexf\Projects\AlexFrancisco.github.io\hidden_content"
INSTRUCTION_FILE = "input_data.txt"
SUMMARY_LOG = "update_summary.txt"
DEFAULT_CONTENT = "<h2>Default Heading</h2><p>Default content</p>"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ContentManager:
    def __init__(self, content_dir=CONTENT_DIR):
        self.content_dir = content_dir
        os.makedirs(self.content_dir, exist_ok=True)
        self.content_map = self.scan_content()
        
    def scan_content(self):
        """Scan directory and map filenames to their content"""
        return {
            fn: self._read_file(fn) 
            for fn in os.listdir(self.content_dir) 
            if fn.endswith('.html')
        }

    def sanitize_name(self, title):
        """Create valid filename from title"""
        return re.sub(r'[^\w\-]', '_', title).lower() + ".html"

    def get_existing_heading(self, filename):
        """Extract main heading from file content"""
        soup = BeautifulSoup(self.content_map.get(filename, ''), 'html.parser')
        return soup.find('h2').text if soup.find('h2') else ''

    def update_file(self, filename, new_content):
        """Update file content while preserving structure"""
        try:
            # Preserve existing heading structure
            main_heading = self.get_existing_heading(filename)
            soup = BeautifulSoup(new_content, 'html.parser')
            
            # Clean empty paragraphs
            for p in soup.find_all('p'):
                if not p.text.strip():
                    p.decompose()
            
            # Maintain original heading unless explicitly changed
            if main_heading:
                existing_h2 = soup.find('h2')
                if existing_h2:
                    existing_h2.string = main_heading
                else:
                    new_h2 = soup.new_tag('h2')
                    new_h2.string = main_heading
                    soup.insert(0, new_h2)
            
            # Ensure valid HTML structure
            if not soup.find('body'):
                body = soup.new_tag('body')
                body.extend(soup.contents)
                soup.append(body)
            
            self._write_file(filename, str(soup))
            self.content_map[filename] = str(soup)
            return True
        except Exception as e:
            logger.error(f"Update failed for {filename}: {str(e)}")
            return False

    def add_section(self, filename, section_title, section_text):
        """Add new section to existing content"""
        try:
            content = self.content_map.get(filename, DEFAULT_CONTENT)
            soup = BeautifulSoup(content, 'html.parser')
            
            # Create new section
            new_h2 = soup.new_tag('h2')
            new_h2.string = section_title
            new_p = soup.new_tag('p')
            new_p.string = section_text
            
            # Append new section
            soup.append(new_h2)
            soup.append(new_p)
            
            self._write_file(filename, str(soup))
            self.content_map[filename] = str(soup)
            return True
        except Exception as e:
            logger.error(f"Failed to add section to {filename}: {str(e)}")
            return False

    def process_instructions(self):
        """Process all instructions from input file"""
        summary = []
        instructions = self._read_instructions()
        
        for instruction in instructions:
            filename, action_result = self._handle_instruction(instruction)
            if filename and action_result:
                status = "SUCCESS"
                summary.append(f"{filename}: {action_result}")
            else:
                status = "FAILED"
            summary.append(f"{status} - {instruction}")
        
        self._write_summary(summary)
        return summary

    def _handle_instruction(self, instruction):
        """Process single instruction"""
        try:
            # Determine target file
            target_file = self._identify_target_file(instruction)
            if not target_file:
                logger.warning(f"No target found for: {instruction}")
                return None, None

            # Generate content with context
            context = {
                'current_content': self.content_map.get(target_file, ''),
                'filename': target_file
            }
            generated = self._generate_content(instruction, context)
            
            # Determine action type
            if "add section about" in instruction.lower():
                section_title = instruction.split("about")[-1].strip().title()
                success = self.add_section(target_file, section_title, generated)
            else:
                success = self.update_file(target_file, generated)
            
            return (target_file, generated) if success else (None, None)
        except Exception as e:
            logger.error(f"Instruction processing failed: {str(e)}")
            return None, None

    def _identify_target_file(self, instruction):
        """Match instruction to existing files"""
        instruction_lower = instruction.lower()
        for fn in self.content_map.keys():
            clean_fn = fn.replace('.html', '').replace('_', ' ')
            if clean_fn in instruction_lower:
                return fn
        return "default.html"

    def _generate_content(self, prompt, context):
        """Generate HTML with OpenAI using proper context"""
        messages = [{
            "role": "system",
            "content": (
                f"File: {context['filename']}\n"
                f"Current Content:\n{context['current_content']}\n\n"
                "Generate ONLY new/updated sections as HTML fragments.\n"
                "Maintain existing headings unless instructed to change.\n"
                "Format: <h2>Section</h2><p>Content</p>"
            )
        }, {
            "role": "user",
            "content": prompt
        }]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content

    def _read_instructions(self):
        """Read instructions from input file"""
        try:
            with open(INSTRUCTION_FILE, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error("Instruction file not found")
            return []

    def _write_summary(self, summary):
        """Write summary log"""
        with open(SUMMARY_LOG, 'w') as f:
            f.write("\n".join(summary))

    def _read_file(self, filename):
        """Read file contents"""
        path = os.path.join(self.content_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _write_file(self, filename, content):
        """Write content to file"""
        path = os.path.join(self.content_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    manager = ContentManager()
    logger.info("Starting content management system")
    results = manager.process_instructions()
    logger.info(f"Processed {len(results)} instructions")
    logger.info(f"Summary saved to {SUMMARY_LOG}")
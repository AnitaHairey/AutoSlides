# AutoSlides: An LLM Agent for Seamlessly Generating Presentation Slides from Documents

## 🌟 Abstract

Have you ever grown tired of repeatedly copying content from a paper to slides? **AutoSlides** addresses the common challenge of manually creating presentation slides from `.tex`, `.pdf`, and `.docx` files. Researchers may spend tens of hours curating slides for a conference talk, and ML engineers often need to summarize papers for internal presentations. 

AutoSlides leverages a GPT-powered multi-agent system to automatically extract and structure content, creating polished and well-organized slides. It also integrates figure processing, ensuring seamless visual elements. AutoSlides significantly reduces the time and effort required for slide preparation, making it an invaluable tool for researchers and engineers alike.

---

## Design & Implementation

### 1. Architecture

AutoSlides uses a modular architecture coordinated by the `MainCaller` module. The general workflow is:

1. `file_loader.py` loads content from the target folder.
2. `content_summarizer.py` uses GPT-4o to summarize the content and generate slide titles and structure.
3. `figure_processor.py` extracts and inserts figures.
4. `slides_generator.py` formats everything into a `.pptx` file.

### 2. Component Overview

#### `main.py`
Entry point of AutoSlides. Orchestrates file loading, summarization, and slide generation.

#### `model.py`
Handles all GPT-4o API calls and returns the model output.

#### `file_loader.py`
Loads and processes `.tex`, `.pdf`, and `.docx` files from a given directory.

#### `content_summarizer.py`
Summarizes documents using GPT-4o and determines slide count and structure. Caches results for efficiency.

#### `figure_processor.py`
Extracts figure data from LaTeX files, calls GPT-4o for descriptions, and integrates selected figures into slides. Converts PDF figures to PNG when necessary.

#### `slides_generator.py`
Generates slides from summarized text, applying appropriate formatting, titles, and images. Saves the presentation as a `.pptx` file.

#### `utils.py`
Provides utility functions for text formatting, markdown parsing, figure rendering, and file manipulation.

---

## User Manual

1. **Clone the Repo**  
   ```bash
   git clone https://github.com/AnitaHairey/AutoSlides
   ```

2. **Set OpenAI API Key**  
   Open `main.py` and replace the placeholder with your own API key.  
   *Refer to your AI school course for API key instructions.*

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Input Document**  
   Create a new folder and put your `.tex`, `.pdf`, or `.docx` file inside.

5. **Run the Program**  
   ```bash
   python main.py
   ```

6. **Follow Prompts**  
   Input:
   - File type (`tex`, `pdf`, or `docx`)
   - Folder name
   - Theme selection for slides

7. **View Results**  
   The generated `.pptx` file will appear in the `Result/` folder.

---

## Future Work

- **Support for `.doc` Format**  
  Add functionality to read and process `.doc` files to broaden compatibility and support users working with older Word formats.

---

## Conclusion

**AutoSlides** is an AI-powered solution that streamlines the slide creation process. It supports multiple file formats, integrates figure handling, and delivers professional presentation decks with minimal manual effort. Its modular design enables easy maintenance and future expansion. Whether you’re a researcher or an engineer, AutoSlides will save you time while boosting the quality of your presentations.

---

Let me know if you'd like me to convert this into a `.md` file or update the GitHub repo directly.

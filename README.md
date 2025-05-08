# bootdev_static_site_generator

This is a Markdown to HTML static site generator written in Python as part of the Backend Developer course on [boot.dev](https://boot.dev). 

An example website generated using this program is available at https://danielwolber-wood.github.io/bootdev_static_site_generator

## Program Architecture

![Program Architecture.png](Program%20Architecture.png)

![Program Processing.png](Program%20Processing.png)

## Installation

1. **Prerequisites**
   - Python 3.12 or higher
   - virtualenv (Or your preferred Python virtual environment manager)

2. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/bootdev_static_site_generator.git
   cd bootdev_static_site_generator
   ```

3. **Set Up Virtual Environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Project Structure**
   If you do not wish to specify where files are as command-line arguments, the defaults work with this structure:
   ```
   bootdev_static_site_generator/
   ├── content/          # Your markdown files go here
   ├── static/          # Static files (CSS, images, etc.)
   ├── docs/           # Output directory for generated HTML
   ├── template.html   # HTML template for the site
   └── main.py        # Main program file
   ```

6. **Usage**
   ```bash
   python main.py [options]
   ```

   Available options:
   - `--static`: Path to static files directory (default: ./static)
   - `--content`: Path to content directory with Markdown files (default: ./content)
   - `--destination`: Output directory for generated HTML (default: ./docs)
   - `--template`: Path to HTML template file (default: ./template.html)
   - `--basepath`: Base path for the site (default: /)
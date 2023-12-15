import yaml
import markdown2
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def markdown_to_html(markdown_text):
    """Converts Markdown text to HTML."""
    return markdown2.markdown(markdown_text)

def generate_pdf_from_yaml(yaml_file_path, output_pdf, template_file, css_file):
    # Read and parse the YAML file
    with open(yaml_file_path, 'r') as file:
        content = yaml.safe_load(file)

    # Convert Markdown content to HTML
    content['about_content'] = markdown_to_html(content['about_content'])
    
    # Assuming 'content' is a list of sections, each with a 'content' field
    for section in content.get('content', []):
        if 'content' in section:
            for item in section['content']:
                if 'description' in item:
                    item['description'] = markdown_to_html(item['description'])

    # Load the HTML template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)

    # Render the HTML content
    html_content = template.render(content=content)

    # Generate PDF
    HTML(string=html_content).write_pdf(output_pdf, stylesheets=[css_file])

if __name__ == "__main__":
    config_file = "_config.yml"
    output_pdf = "reed_bender_cv.pdf"
    template_file = "config_template.html"
    css_file = "style.css"

    generate_pdf_from_yaml(
        config_file,
        output_pdf,
        template_file,
        css_file
    )

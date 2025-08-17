from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
import uuid
import platform

def generate_resume(data):
    """
    Generate a PDF resume from the provided data
    Returns the path to the generated PDF file
    """
    
    # Configure wkhtmltopdf based on environment
    if platform.system() == "Windows":
        # Local development on Windows - fix the path
        path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    else:
        # Production environment (Linux/Render)
        # wkhtmltopdf will be installed via apt-get in render.yaml
        config = pdfkit.configuration()
    # Load template and render
    env = Environment(loader=FileSystemLoader('templates'))
    templatename = data['template_name']
    template = env.get_template(f'{templatename}.html')
    rendered_html = template.render(data)

    # Generate unique filename
    filename = f"resume_{uuid.uuid4().hex}.pdf"
    
    # Create output directory if it doesn't exist
    output_dir = "generated_resumes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Full path for the PDF
    output_file = os.path.join(output_dir, filename)
    pagesize = data['page_size']
    # PDF generation options
    options = {
        'page-size': f'{pagesize}',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }

    # Generate PDF with config
    try:
        pdfkit.from_string(rendered_html, output_file, configuration=config, options=options)
        print(f"Resume saved to {output_file}")
        return output_file
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")



def generate_coverletter(data):
    """
    Generate a coverleytter from the provided data
    Returns the path to the generated PDF file
    """
    
    # Configure wkhtmltopdf based on environment
    if platform.system() == "Windows":
        # Local development on Windows - fix the path
        path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    else:
        # Production environment (Linux/Render)
        # wkhtmltopdf will be installed via apt-get in render.yaml
        config = pdfkit.configuration()
    # Load template and render
    env = Environment(loader=FileSystemLoader('cover_letters'))
    templatename = data["cover_letter_info"]["template_name"]

    template = env.get_template(f'{templatename}.html')
    rendered_html = template.render(data)

    # Generate unique filename
    filename = f"resume_{uuid.uuid4().hex}.pdf"
    
    # Create output directory if it doesn't exist
    output_dir = "generated_resumes"
    os.makedirs(output_dir, exist_ok=True)
    
    # Full path for the PDF
    output_file = os.path.join(output_dir, filename)

    pagesize = data['cover_letter_info']['page_size']
    # PDF generation options
    options = {
        'page-size': f'{pagesize}',
        'margin-top': '0.50in',
        'margin-right': '0.50in', 
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None,
        # ADD THESE FOR CONSISTENCY:
        'disable-smart-shrinking': None,
        'print-media-type': None,
        'viewport-size': '1024x768',
        'javascript-delay': 2000,
        'dpi': 300,
        'zoom': 1.0
    }

    # Generate PDF with config
    try:
        pdfkit.from_string(rendered_html, output_file, configuration=config, options=options)
        print(f"Resume saved to {output_file}")
        return output_file
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")


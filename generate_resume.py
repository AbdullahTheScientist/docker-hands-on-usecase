# from jinja2 import Environment, FileSystemLoader
# import pdfkit
# import os
# import uuid
# import platform

# def generate_resume(data):
#     """
#     Generate a PDF resume from the provided data
#     Returns the path to the generated PDF file
#     """
    
#     # Configure wkhtmltopdf based on environment
#     if platform.system() == "Windows":
#         # Local development on Windows - fix the path
#         path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
#         config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
#     else:
#         # Production environment (Linux/Render)
#         # wkhtmltopdf will be installed via apt-get in render.yaml
#         config = pdfkit.configuration()
#     # Load template and render
#     env = Environment(loader=FileSystemLoader('templates'))
#     templatename = data['template_name']
#     template = env.get_template(f'{templatename}.html')
#     rendered_html = template.render(data)

#     # Generate unique filename
#     filename = f"resume_{uuid.uuid4().hex}.pdf"
    
#     # Create output directory if it doesn't exist
#     output_dir = "generated_resumes"
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Full path for the PDF
#     output_file = os.path.join(output_dir, filename)
#     pagesize = data['page_size']
#     # PDF generation options
#     options = {
#         'page-size': f'{pagesize}',
#         # 'margin-top': '0.50in',
#         # 'margin-right': '0.50in',
#         # 'margin-bottom': '0.50in',
#         # 'margin-left': '0.50in',
#         'encoding': "UTF-8",
#         'no-outline': None,
#         'enable-local-file-access': None
#     }

#     # Generate PDF with config
#     try:
#         pdfkit.from_string(rendered_html, output_file, configuration=config, options=options)
#         print(f"Resume saved to {output_file}")
#         return output_file
#     except Exception as e:
#         raise Exception(f"PDF generation failed: {str(e)}")



# def generate_coverletter(data):
#     """
#     Generate a coverleytter from the provided data
#     Returns the path to the generated PDF file
#     """
    
#     # Configure wkhtmltopdf based on environment
#     if platform.system() == "Windows":
#         # Local development on Windows - fix the path
#         path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
#         config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
#     else:
#         # Production environment (Linux/Render)
#         # wkhtmltopdf will be installed via apt-get in render.yaml
#         config = pdfkit.configuration()
#     # Load template and render
#     env = Environment(loader=FileSystemLoader('cover_letters'))
#     templatename = data["cover_letter_info"]["template_name"]

#     template = env.get_template(f'{templatename}.html')
#     rendered_html = template.render(data)

#     # Generate unique filename
#     filename = f"resume_{uuid.uuid4().hex}.pdf"
    
#     # Create output directory if it doesn't exist
#     output_dir = "generated_resumes"
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Full path for the PDF
#     output_file = os.path.join(output_dir, filename)

#     pagesize = data['cover_letter_info']['page_size']
#     # PDF generation options
#     options = {
#         'page-size': f'{pagesize}',
#         'margin-top': '0.50in',
#         'margin-right': '0.50in',
#         'margin-bottom': '0.50in',
#         'margin-left': '0.50in',
#         'encoding': "UTF-8",
#         'no-outline': None,
#         'enable-local-file-access': None
#     }

#     # Generate PDF with config
#     try:
#         pdfkit.from_string(rendered_html, output_file, configuration=config, options=options)
#         print(f"Resume saved to {output_file}")
#         return output_file
#     except Exception as e:
#         raise Exception(f"PDF generation failed: {str(e)}")





from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
import uuid
import platform
import logging
import subprocess

logger = logging.getLogger(__name__)

def check_wkhtmltopdf_capabilities():
    """Check if wkhtmltopdf is patched version and what options are supported"""
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True, timeout=10)
        version_output = result.stdout.lower()
        
        is_patched = "with patched qt" in version_output
        logger.info(f"wkhtmltopdf version info: patched={is_patched}")
        
        return is_patched, version_output
    except Exception as e:
        logger.warning(f"Could not check wkhtmltopdf version: {e}")
        return False, ""

def get_pdf_options(page_size, is_patched=False):
    """Get appropriate PDF options based on wkhtmltopdf version"""
    
    # Basic options that work with all versions
    options = {
        'page-size': page_size,
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'orientation': 'Portrait',
        'quiet': None,
    }
    
    # Add advanced options only for patched versions
    if is_patched:
        logger.info("Adding patched wkhtmltopdf options")
        options.update({
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None,
            'disable-smart-shrinking': None,
            'disable-javascript': None,
            'load-error-handling': 'ignore',
            'load-media-error-handling': 'ignore',
            'dpi': 300,
            'zoom': '1.0',
        })
    else:
        logger.info("Using basic options for unpatched wkhtmltopdf")
        # For unpatched versions, we can still use some basic options
        options.update({
            'grayscale': None,  # This works on unpatched versions
        })
    
    return options

def generate_resume(data):
    """
    Generate a PDF resume from the provided data
    Returns the path to the generated PDF file
    """
    
    try:
        # Configure wkhtmltopdf based on environment
        if platform.system() == "Windows":
            # Local development on Windows
            path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            if os.path.exists(path_to_wkhtmltopdf):
                config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
            else:
                logger.warning("wkhtmltopdf not found at expected path, using system PATH")
                config = pdfkit.configuration()
        else:
            # Production environment (Linux/Render)
            config = pdfkit.configuration()
        
        # Check wkhtmltopdf capabilities
        is_patched, version_info = check_wkhtmltopdf_capabilities()
        
        # Load template and render
        env = Environment(loader=FileSystemLoader('templates'))
        templatename = data.get('template_name', 'modern4')
        template = env.get_template(f'{templatename}.html')
        rendered_html = template.render(data)

        # Generate unique filename
        filename = f"resume_{uuid.uuid4().hex}.pdf"
        
        # Create output directory if it doesn't exist
        output_dir = "generated_resumes"
        os.makedirs(output_dir, exist_ok=True)
        
        # Full path for the PDF
        output_file = os.path.join(output_dir, filename)
        pagesize = data.get('page_size', 'A4')
        
        # Get appropriate options based on wkhtmltopdf version
        options = get_pdf_options(pagesize, is_patched)
        
        logger.info(f"Generating PDF with options: {list(options.keys())}")
        
        # Generate PDF with config
        pdfkit.from_string(rendered_html, output_file, configuration=config, options=options)
        logger.info(f"Resume saved to {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        # Try with minimal options as fallback
        try:
            logger.info("Attempting PDF generation with minimal options")
            minimal_options = {
                'page-size': data.get('page_size', 'A4'),
                'encoding': "UTF-8",
                'quiet': None,
            }
            pdfkit.from_string(rendered_html, output_file, configuration=config, options=minimal_options)
            logger.info(f"Resume saved with minimal options to {output_file}")
            return output_file
        except Exception as fallback_error:
            logger.error(f"Fallback PDF generation also failed: {str(fallback_error)}")
            raise Exception(f"PDF generation failed: {str(e)}")

def generate_coverletter(data):
    """
    Generate a cover letter from the provided data
    Returns the path to the generated PDF file
    """
    
    try:
        # Configure wkhtmltopdf based on environment
        if platform.system() == "Windows":
            # Local development on Windows
            path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            if os.path.exists(path_to_wkhtmltopdf):
                config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
            else:
                logger.warning("wkhtmltopdf not found at expected path, using system PATH")
                config = pdfkit.configuration()
        else:
            # Production environment (Linux/Render)
            config = pdfkit.configuration()
        
        # Check wkhtmltopdf capabilities
        is_patched, version_info = check_wkhtmltopdf_capabilities()
        
        # Load template and render
        env = Environment(loader=FileSystemLoader('cover_letters'))
        templatename = data["cover_letter_info"]["template_name"]

        template = env.get_template(f'{templatename}.html')
        rendered_html = template.render(data)

        # Generate unique filename
        filename = f"cover_letter_{uuid.uuid4().hex}.pdf"
        
        # Create output directory if it doesn't exist
        output_dir = "generated_resumes"
        os.makedirs(output_dir, exist_ok=True)
        
        # Full path for the PDF
        output_file = os.path.join(output_dir, filename)
        pagesize = data['cover_letter_info'].get('page_size', 'A4')
        
        # Get appropriate options based on wkhtmltopdf version
        options = get_pdf_options(pagesize, is_patched)
        
        logger.info(f"Generating cover letter PDF with options: {list(options.keys())}")
        
        # Generate PDF with config
        pdfkit.from_string(rendered_html, output_file, configuration=config, options=options)
        logger.info(f"Cover letter saved to {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Cover letter generation failed: {str(e)}")
        # Try with minimal options as fallback
        try:
            logger.info("Attempting cover letter generation with minimal options")
            minimal_options = {
                'page-size': data['cover_letter_info'].get('page_size', 'A4'),
                'encoding': "UTF-8",
                'quiet': None,
            }
            pdfkit.from_string(rendered_html, output_file, configuration=config, options=minimal_options)
            logger.info(f"Cover letter saved with minimal options to {output_file}")
            return output_file
        except Exception as fallback_error:
            logger.error(f"Fallback cover letter generation also failed: {str(fallback_error)}")
            raise Exception(f"Cover letter generation failed: {str(e)}")
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, 
    HRFlowable, Frame, Indenter, Image, KeepInFrame, PageBreak
)
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.pdfgen import canvas
import base64
from io import BytesIO
from PyPDF2 import PdfMerger

class ResumePDF:
    DEFAULT_TEMPLATE = "modern4.png"
    SIDEBAR_WIDTH_RATIO = 1/3
    CONTENT_WIDTH_RATIO = 2/3
    DEFAULT_MARGIN = 20
    ICON_SIZE = 0.2 * inch
    PROFILE_PIC_SIZE = 3.15 * inch
    PROFILE_PIC_BORDER = 0.1 * inch

    def __init__(self, output_file="resume.pdf", page_size="A4", template_image=None):
        """Initialize the resume PDF generator with styling and document setup"""
        self.output_file = output_file
        self.template_image = template_image or self.DEFAULT_TEMPLATE
        
        # Set page size
        self.pagesize = A4 if str(page_size).lower() == "a4" else letter
        self.page_width, self.page_height = self.pagesize
        
        # Calculate layout dimensions
        self.sidebar_width = self.page_width * self.SIDEBAR_WIDTH_RATIO
        self.content_width = (self.page_width * self.CONTENT_WIDTH_RATIO) - 70
        
        # Document setup
        self.doc = SimpleDocTemplate(
            output_file, 
            pagesize=self.pagesize,
            rightMargin=self.DEFAULT_MARGIN,
            leftMargin=self.DEFAULT_MARGIN,
            topMargin=self.DEFAULT_MARGIN,
            bottomMargin=self.DEFAULT_MARGIN
        )
        
        # Color palette
        self.colors = {
            'primary': colors.HexColor("#fff5f5"),
            'secondary': colors.HexColor("#6C757D"),
            'accent': colors.HexColor("#F18F01"),
            'light_bg': colors.HexColor("#F5F5F5"),
            'sidebar_bg': colors.HexColor("#E8E8E8"),
            'divider': colors.HexColor("#D3D3D3"),
            'section': colors.HexColor("#183A54")
        }
        
        # Initialize content containers
        self.story = []
        self.sidebar_content = []
        self.sidebar_content_pos = 0
        
        # Setup styles
        self.styles = self._setup_styles()

    def _setup_styles(self):
        """Configure all paragraph and text styles"""
        styles = getSampleStyleSheet()
        
        # Main content styles
        styles.add(ParagraphStyle(
            name='NameTitle',
            fontSize=20,
            leading=20,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        styles.add(ParagraphStyle(
            name='Title_',
            fontSize=14,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.black
        ))
        
        styles.add(ParagraphStyle(
            name="SectionTitle",
            fontSize=12,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        styles.add(ParagraphStyle(
            name="body_style",
            fontSize=12,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontName='Helvetica',
            textColor=colors.black,
            firstLineIndent=12
        ))
        
        styles.add(ParagraphStyle(
            name='Company',
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        styles.add(ParagraphStyle(
            name='Position',
            fontSize=12,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=self.colors['secondary']
        ))
        
        styles.add(ParagraphStyle(
            name='Date',
            fontSize=12,
            leading=12,
            alignment=TA_RIGHT,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=self.colors['secondary']
        ))
        
        styles.add(ParagraphStyle(
            name="bullets",
            fontSize=12,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            fontName='Helvetica',
            leftIndent=12,
            bulletIndent=0
        ))
        
        # Sidebar styles
        styles.add(ParagraphStyle(
            name="SidebarSectionTitle",
            fontSize=12,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary']
        ))
        
        styles.add(ParagraphStyle(
            name='SidebarContactTitle',
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary']
        ))
        
        styles.add(ParagraphStyle(
            name='SidebarContactInfo',
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            textColor=self.colors['primary']
        ))

        styles.add(ParagraphStyle(
            name='SidebarSkillItem',
            fontSize=11,
            leading=12,
            alignment=TA_LEFT,
            spaceAfter=1,
            textColor=self.colors['primary'],
            fontName='Helvetica-Bold'
        ))
        
        return styles


    def add_profile_picture(self, base64_image, size=None, border_width=None):
        """Add profile picture with consistent spacing"""
        size = size or self.PROFILE_PIC_SIZE
        border_width = border_width or self.PROFILE_PIC_BORDER
        
        # Add consistent top spacing regardless of content
        self.sidebar_content.insert(0, Spacer(1, 20))  # Increased from 5 to 20
        self.sidebar_content.insert(1, Spacer(1, 10))
        
        # Rest of the existing profile picture code...
        
        try:
            image_data = base64.b64decode(base64_image)
            image_buffer = BytesIO(image_data)
            profile_image = Image(image_buffer, width=size, height=size, kind='proportional')
            profile_image.drawWidth = size
            profile_image.drawHeight = size
            
            profile_table = Table(
                [[profile_image]], 
                colWidths=[size + 2*border_width], 
                rowHeights=[size + 2*border_width]
            )
            
            profile_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            centered_table = Table([[profile_table]], colWidths=[self.sidebar_width - 40])
            centered_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), -28),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), -50),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ]))
            
            self.sidebar_content.insert(0, Spacer(1, 5))
            self.sidebar_content.insert(1, centered_table)
        except Exception as e:
            print(f"Error adding profile picture: {e}")
            self.sidebar_content.insert(0, Spacer(1, 5))
            self.sidebar_content.insert(1, Spacer(1, size + 2*border_width + 25))

    def add_header(self, personal_info):
        """Add the resume header with name, title and contact info"""
        self.story.append(Spacer(1, 10))

        name = Paragraph(personal_info['name'].upper(), self.styles['NameTitle'])
        title = Paragraph(personal_info['title'], self.styles['Title_'])

        name_title_table = Table([[name], [title]], colWidths=min(400, self.content_width))
        name_title_table.hAlign = 'LEFT'
        name_title_table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
        ]))

        self.story.append(Indenter(left=240))
        self.story.append(name_title_table)
        self.story.append(Indenter(left=-240))
        self.story.append(Spacer(1, 20))

        self._add_contact_to_sidebar(personal_info)
                    
    def _add_contact_to_sidebar(self, personal_info):
        """Add contact information to the sidebar with icons"""
        self.sidebar_content.append(Spacer(1, 20))
        self.sidebar_content.append(Paragraph("CONTACT", self.styles['SidebarContactTitle']))

        self._add_divider()
        self.sidebar_content.append(Spacer(1, 10))
        self.sidebar_content.append(Indenter(left=-10))
        
        # Phone
        if 'phone' in personal_info:
            self._add_icon_text_item("phone.png", personal_info['phone'])
        
        # Email
        if 'email' in personal_info:
            self._add_icon_text_item("email.png", personal_info['email'])
        
        # Location
        if 'location' in personal_info:
            self._add_icon_text_item("location.png", personal_info['location'])
        
        self.sidebar_content.append(Indenter(left=10))

    def _add_icon_text_item(self, icon_name, text):
        """Helper method to add icon-text pairs to sidebar"""
        try:
            icon = Image(icon_name, width=self.ICON_SIZE, height=self.ICON_SIZE)
            text_para = Paragraph(text, self.styles['SidebarContactInfo'])
            item_table = Table([
                [icon, text_para]
            ], colWidths=[self.ICON_SIZE + 5, self.sidebar_width - self.ICON_SIZE - 40])
            item_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5)
            ]))
            self.sidebar_content.append(item_table)
        except:
            self.sidebar_content.append(Paragraph(text, self.styles['SidebarContactInfo']))

    def _add_divider(self, width=None, color=None, thickness=1):
        """Helper method to add consistent dividers"""
        width = width or (self.sidebar_width - 40)
        color = color or self.colors['divider']
        
        line = HRFlowable(
            width=width,
            thickness=thickness,
            color=color,
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)

    def _add_social_media_to_sidebar(self, personal_info):
        """Add social media links to the sidebar with icons"""
        social_media_fields = ['facebook', 'linkedin', 'twitter', 'github', 'website']
        if not any(field in personal_info for field in social_media_fields):
            return
        
        self.sidebar_content.append(Spacer(1, 20))
        self.sidebar_content.append(Paragraph("ONLINE PRESENCE", self.styles['SidebarContactTitle']))
        self._add_divider()
        self.sidebar_content.append(Spacer(1, 10))
        self.sidebar_content.append(Indenter(left=-10))
        
        # Social media links
        platforms = {
            'facebook': ('Facebook', 'facebook.png'),
            'linkedin': ('LinkedIn', 'linkedin.png'),
            'twitter': ('Twitter', 'twitter.png'),
            'github': ('GitHub', 'github.png'),
            'website': ('Portfolio', 'website.png')
        }
        
        for field, (display_name, icon_name) in platforms.items():
            if field in personal_info:
                try:
                    icon = Image(icon_name, width=self.ICON_SIZE, height=self.ICON_SIZE)
                    link_para = Paragraph(
                        f'<a href="{personal_info[field]}" color="white">{display_name}</a>', 
                        self.styles['SidebarContactInfo']
                    )
                    item_table = Table([
                        [icon, link_para]
                    ], colWidths=[self.ICON_SIZE + 5, self.sidebar_width - self.ICON_SIZE - 40])
                    item_table.setStyle(TableStyle([
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                    ]))
                    self.sidebar_content.append(item_table)
                except:
                    self.sidebar_content.append(Paragraph(
                        f'<a href="{personal_info[field]}" color="white">{display_name}</a>', 
                        self.styles['SidebarContactInfo']
                    ))
        
        self.sidebar_content.append(Indenter(left=10))

    def add_professional_summary(self, summary_text):
        """Add professional summary section with divider"""
        self.story.append(Spacer(1, 8))
        self.story.append(Indenter(left=self.page_width * 0.36))
        
        self.story.append(Paragraph("PROFESSIONAL PROFILE", self.styles['SectionTitle']))
        
        line = HRFlowable(
            width=self.content_width,
            thickness=2,
            lineCap='round',
            color=self.colors['section'],
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)
        self.story.append(Paragraph(summary_text, self.styles['body_style']))
        self.story.append(Spacer(1, 6))

    def add_work_experience(self, work_experience):
        """Add work experience section with consistent formatting"""
        if not work_experience:
            return
            
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("WORK EXPERIENCE", self.styles['SectionTitle']))
        self._add_content_divider()
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45
        
        for job in work_experience:
            job_elements = []
            
            # Company name
            company = Paragraph(job['company'], self.styles['Company'])
            
            # Position and date range
            position = Paragraph(job['position'], self.styles['Position'])
            start_date = self._format_date(job['start_date'])
            end_date = self._format_date(job['end_date'])
            date_range = Paragraph(f"{start_date} - {end_date}", self.styles['Date'])
            
            # Create header table
            header_table = Table(
                [[position, date_range]], 
                colWidths=[col1_width, col2_width]
            )
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT')
            ]))
            
            job_elements.append(company)
            job_elements.append(header_table)
            
            # Add bullet points
            for desc in job.get('description', []):
                bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                bullet_table = Table([[bullet_para]], colWidths=[self.content_width])
                bullet_table.setStyle(TableStyle([
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
                ]))
                job_elements.append(bullet_table)
            
            job_elements.append(Spacer(1, 8))
            
            # Add to story with appropriate grouping
            if len(job.get('description', [])) <= 3:
                self.story.append(KeepInFrame(
                    self.content_width,
                    self.page_height,
                    job_elements,
                    hAlign='LEFT',
                    vAlign='TOP'
                ))
            else:
                for element in job_elements:
                    self.story.append(element)

    def _add_content_divider(self, thickness=2):
        """Add consistent divider for content sections"""
        line = HRFlowable(
            width=self.content_width,
            thickness=thickness,
            lineCap="round",
            color=self.colors['section'],
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)

    def _format_date(self, date_value):
        """Helper method to format date values consistently"""
        if isinstance(date_value, datetime):
            return date_value.strftime('%b %Y')
        return date_value or "Present"

    def add_academic_projects(self, projects):
        """Add academic projects section"""
        if not projects:
            return
            
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("PROJECTS", self.styles['SectionTitle']))
        self._add_content_divider()
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45

        for project in projects:
            project_elements = []
            
            # Project title
            title = Paragraph(project['title'], self.styles['Company'])
            
            # Date handling
            date_str = ""
            if 'date' in project:
                date_str = self._format_date(project['date'])
            elif 'start_date' in project and 'end_date' in project:
                start_date = self._format_date(project['start_date'])
                end_date = self._format_date(project['end_date'])
                date_str = f"{start_date} - {end_date}"
                
            if date_str:
                date_para = Paragraph(date_str, self.styles['Date'])
                header_table = Table(
                    [[title, date_para]], 
                    colWidths=[col1_width, col2_width]
                )
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT')
                ]))
                project_elements.append(header_table)
            else:
                project_elements.append(title)
            
            # Technologies
            if 'technologies' in project:
                tech_text = f"<i>Technologies:</i> {project['technologies']}"
                project_elements.append(Paragraph(tech_text, self.styles['Position']))
            
            # Description bullets
            for desc in project.get('description', []):
                bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                bullet_table = Table([[bullet_para]], colWidths=[self.content_width])
                project_elements.append(bullet_table)
            
            # Links
            for link_name, link_url in project.get('links', {}).items():
                link_text = f"<b>{link_name}:</b> {link_url}"
                project_elements.append(Paragraph(link_text, self.styles['bullets']))
            
            project_elements.append(Spacer(1, 8))
            
            # Add to story
            for element in project_elements:
                self.story.append(element)

    def add_publications(self, publications):
        """Add publications section"""
        if not publications:
            return
            
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("PUBLICATIONS", self.styles['SectionTitle']))
        self._add_content_divider()
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45

        for pub in publications:
            pub_elements = []
            
            # Title and date
            title = Paragraph(pub['title'], self.styles['Company'])
            
            if 'date' in pub:
                date_str = self._format_date(pub['date'])
                date_para = Paragraph(date_str, self.styles['Date'])
                header_table = Table(
                    [[title, date_para]], 
                    colWidths=[col1_width, col2_width]
                )
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT')
                ]))
                pub_elements.append(header_table)
            else:
                pub_elements.append(title)
            
            # Authors
            if 'authors' in pub:
                pub_elements.append(Paragraph(f"<i>Authors:</i> {pub['authors']}", self.styles['Position']))
            
            # Journal/conference
            if 'journal' in pub:
                pub_elements.append(Paragraph(f"<i>Published in:</i> {pub['journal']}", self.styles['Position']))
            
            # DOI/URL
            if 'doi' in pub:
                pub_elements.append(Paragraph(f"<i>DOI:</i> {pub['doi']}", self.styles['bullets']))
            elif 'url' in pub:
                pub_elements.append(Paragraph(f"<i>URL:</i> {pub['url']}", self.styles['bullets']))
            
            # Description
            for desc in pub.get('description', []):
                bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                bullet_table = Table([[bullet_para]], colWidths=[self.content_width])
                pub_elements.append(bullet_table)
            
            pub_elements.append(Spacer(1, 8))
            
            # Add to story
            for element in pub_elements:
                self.story.append(element)

    def add_certifications(self, certifications):
        """Add certifications section"""
        if not certifications:
            return
            
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("CERTIFICATIONS", self.styles['SectionTitle']))
        self._add_content_divider()
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45

        for cert in certifications:
            cert_elements = []
            
            # Name and date
            name = Paragraph(cert['name'], self.styles['Company'])
            
            date_str = ""
            if 'date' in cert:
                date_str = self._format_date(cert['date'])
            elif 'issue_date' in cert:
                date_str = self._format_date(cert['issue_date'])
            
            if date_str:
                date_para = Paragraph(date_str, self.styles['Date'])
                header_table = Table(
                    [[name, date_para]], 
                    colWidths=[col1_width, col2_width]
                )
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT')
                ]))
                cert_elements.append(header_table)
            else:
                cert_elements.append(name)
            
            # Issuer
            if 'issuer' in cert:
                cert_elements.append(Paragraph(f"<i>Issued by:</i> {cert['issuer']}", self.styles['Position']))
            
            # Credential ID
            if 'credential_id' in cert:
                cert_elements.append(Paragraph(f"<i>Credential ID:</i> {cert['credential_id']}", self.styles['Position']))
            
            # URL
            if 'url' in cert:
                cert_elements.append(Paragraph(f"<i>URL:</i> {cert['url']}", self.styles['bullets']))
            
            # Description
            for desc in cert.get('description', []):
                bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                bullet_table = Table([[bullet_para]], colWidths=[self.content_width])
                cert_elements.append(bullet_table)
            
            cert_elements.append(Spacer(1, 8))
            
            # Add to story
            for element in cert_elements:
                self.story.append(element)

    def add_referees(self, referees):
        """Add referees section"""
        if not referees:
            return
            
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("REFERENCES", self.styles['SectionTitle']))
        self._add_content_divider()

        for referee in referees:
            ref_elements = []
            
            # Name and position
            ref_elements.append(Paragraph(referee['name'], self.styles['Company']))
            ref_elements.append(Paragraph(referee['position'], self.styles['Position']))
            
            # Organization
            if 'organization' in referee:
                ref_elements.append(Paragraph(f"<i>{referee['organization']}</i>", self.styles['Position']))
            
            # Contact information
            contact_items = []
            if 'phone' in referee:
                contact_items.append(f"Phone: {referee['phone']}")
            if 'email' in referee:
                contact_items.append(f"Email: {referee['email']}")
            
            if contact_items:
                contact_text = " | ".join(contact_items)
                ref_elements.append(Paragraph(contact_text, self.styles['bullets']))
            
            # Relationship
            if 'relationship' in referee:
                ref_elements.append(Paragraph(f"<i>Relationship:</i> {referee['relationship']}", self.styles['bullets']))
            
            ref_elements.append(Spacer(1, 12))
            
            # Add to story
            for element in ref_elements:
                self.story.append(element)

    def _add_education_to_sidebar(self, education):
        """Add education section to sidebar"""
        if not education:
            return
            
        self.sidebar_content.append(Paragraph("EDUCATION", self.styles['SidebarSectionTitle']))
        self._add_divider()
        self.sidebar_content.append(Spacer(1, 10))
        self.sidebar_content.append(Indenter(left=5))
        
        for edu in education:
            # Institution
            self.sidebar_content.append(Paragraph(edu['institution'], self.styles['SidebarContactInfo']))
            
            # Degree
            self.sidebar_content.append(Paragraph(edu['degree'], self.styles['SidebarSkillItem']))
            
            # Date range
            start_date = self._format_date(edu.get('start_date'))
            end_date = self._format_date(edu.get('end_date'))
            
            if start_date or end_date:
                date_range = f"{start_date} - {end_date}" if start_date and end_date else start_date or end_date
                self.sidebar_content.append(Paragraph(date_range, self.styles['SidebarSkillItem']))
            
            self.sidebar_content.append(Spacer(1, 8))
        
        self.sidebar_content.append(Indenter(left=-5))

    def add_skills(self, skills):
        """Add skills section to sidebar"""
        if not skills:
            return
            
        self.sidebar_content.append(Paragraph("SKILLS", self.styles['SidebarSectionTitle']))
        self._add_divider()
        
        # Flatten skills if they're organized by category
        all_skills = []
        if isinstance(skills, dict):
            for skill_list in skills.values():
                all_skills.extend(skill_list)
        elif isinstance(skills, list):
            all_skills = skills
        self.sidebar_content.append(Indenter(left=-14))
        # Add skills as bullet points/
        for skill in all_skills:
            skill_para = Paragraph(f"• {skill}", self.styles['SidebarSkillItem'])
            skill_table = Table([[skill_para]], colWidths=[self.sidebar_width - 40])
            self.sidebar_content.append(skill_table)
        
        self.sidebar_content.append(Spacer(1, 6))
        self.sidebar_content.append(Indenter(left=14))

    def add_hobbies(self, hobbies):
        """Add hobbies section with consistent spacing"""
        if not hobbies:
            # Add equivalent space even when no hobbies
            self.sidebar_content.append(Spacer(1, 80))  # Approximate space hobbies would take
            return
            
        self.sidebar_content.append(Spacer(1, 20))  # Increased from 12
        self.sidebar_content.append(Paragraph("HOBBIES & INTERESTS", self.styles['SidebarSectionTitle']))
        self._add_divider()
        self.sidebar_content.append(Spacer(1, 10))  # Increased from 6
        self.sidebar_content.append(Indenter(left=-14))
        for hobby in hobbies:
            hobby_para = Paragraph(f"• {hobby}", self.styles['SidebarSkillItem'])
            hobby_table = Table([[hobby_para]], colWidths=[self.sidebar_width - 40])
            self.sidebar_content.append(hobby_table)
        
        self.sidebar_content.append(Spacer(1, 20))  # Increased from 6
        self.sidebar_content.append(Indenter(left=14))

    def add_languages(self, languages):
        """Add languages section with consistent spacing"""
        if not languages:
            # Add equivalent space even when no languages
            self.sidebar_content.append(Spacer(1, 80))  # Approximate space languages would take
            return
            
        self.sidebar_content.append(Spacer(1, 20))  # Increased from 12
        self.sidebar_content.append(Paragraph("LANGUAGES", self.styles['SidebarSectionTitle']))
        self._add_divider()
        self.sidebar_content.append(Spacer(1, 10))  # Increased from 6
        self.sidebar_content.append(Indenter(left=-14))
        for language in languages:
            lang_para = Paragraph(f"• {language}", self.styles['SidebarSkillItem'])
            lang_table = Table([[lang_para]], colWidths=[self.sidebar_width - 40])
            self.sidebar_content.append(lang_table)
        
        self.sidebar_content.append(Spacer(1, 20))  # Increased from 6
        self.sidebar_content.append(Indenter(left=14))
    def _render_sidebar(self, canvas, is_first_page):
        """Render sidebar content with proper pagination"""
        canvas.saveState()
        
        # Calculate available space and position
        sidebar_x = 20
        sidebar_width = (self.page_width / 3) - 30
        
        # Adjust frame height and start position based on whether it's first page
        if is_first_page:
            frame_height = self.page_height - 60  # Less space on first page due to header
            start_y = 20
        else:
            frame_height = self.page_height - 40  # More space on subsequent pages
            start_y = 20  # Keep consistent with first page
        
        # Collect elements that fit on current page
        elements_to_render = []
        remaining_height = frame_height
        force_next_page = False
        
        while self.sidebar_content_pos < len(self.sidebar_content) and not force_next_page:
            element = self.sidebar_content[self.sidebar_content_pos]
            
            # Estimate element height
            if isinstance(element, Spacer):
                h = element.height
            else:
                try:
                    w, h = element.wrap(sidebar_width, remaining_height)
                except:
                    h = 20  # Default height
            
            # Check if element fits
            if h <= remaining_height:
                elements_to_render.append(element)
                remaining_height -= h
                self.sidebar_content_pos += 1
            else:
                # If it's the first element and doesn't fit, force it anyway
                if not elements_to_render:
                    elements_to_render.append(element)
                    self.sidebar_content_pos += 1
                force_next_page = True
        
        # Render collected elements
        if elements_to_render:
            frame = Frame(
                sidebar_x, 
                start_y,
                sidebar_width, 
                frame_height,
                showBoundary=0,
                leftPadding=10,
                bottomPadding=10,
                rightPadding=10,
                topPadding=10
            )
            
            kept_elements = KeepInFrame(
                sidebar_width - 20,
                frame_height - 20,
                elements_to_render,
                hAlign='LEFT',
                vAlign='TOP',
                fakeWidth=False
            )
            
            frame.addFromList([kept_elements], canvas)
        
        canvas.restoreState()

    def draw_first_page(self, canvas, doc):
        """Draw first page template and initial sidebar"""
        canvas.saveState()
        try:
            img = ImageReader(self.template_image)
            canvas.drawImage(img, 0, 0, width=self.page_width, height=self.page_height)
        except Exception as e:
            print(f"Error loading template image: {e}")
        canvas.restoreState()
        
        self._render_sidebar(canvas, is_first_page=True)

    def draw_later_pages(self, canvas, doc):
        """Draw subsequent pages template and remaining sidebar"""
        canvas.saveState()
        try:
            img = ImageReader(self.template_image)
            canvas.drawImage(img, 0, 0, width=self.page_width, height=self.page_height)
        except Exception as e:
            print(f"Error loading template image: {e}")
        canvas.restoreState()
        
        # Use same parameters as first page for consistency
        self._render_sidebar(canvas, is_first_page=False)

    def _finalize_sidebar(self):
        """Ensure consistent sidebar spacing regardless of content"""
        # Add consistent bottom padding
        self.sidebar_content.append(Spacer(1, 40))  # Increased from 20 to 40
        
        # If no hobbies/languages were added, add equivalent space
        has_hobbies = any(isinstance(item, Paragraph) and item.text.startswith("HOBBIES") 
                    for item in self.sidebar_content)
        has_languages = any(isinstance(item, Paragraph) and item.text.startswith("LANGUAGES") 
                        for item in self.sidebar_content)
        
        if not has_hobbies:
            self.sidebar_content.append(Spacer(1, 60))  # Approximate space hobbies would take
        if not has_languages:
            self.sidebar_content.append(Spacer(1, 60))  # Approximate space languages would take


    def build(self):
        """Build the PDF document with proper sidebar handling"""
        # First build with main content and initial sidebar
        self.doc.build(self.story, 
                     onFirstPage=self.draw_first_page, 
                     onLaterPages=self.draw_later_pages)
        
        # Handle any remaining sidebar content
        if self.sidebar_content_pos < len(self.sidebar_content):
            self._handle_sidebar_overflow()
        
        return self.output_file

    def _handle_sidebar_overflow(self):
        """Handle sidebar content that didn't fit on main pages"""
        from io import BytesIO
        
        # Create buffer for additional pages
        new_pages_buffer = BytesIO()
        c = canvas.Canvas(new_pages_buffer, pagesize=self.pagesize)
        
        # Add pages until all sidebar content is rendered
        while self.sidebar_content_pos < len(self.sidebar_content):
            # Draw background
            c.saveState()
            try:
                img = ImageReader(self.template_image)
                c.drawImage(img, 0, 0, width=self.page_width, height=self.page_height)
            except:
                pass
            c.restoreState()
            
            # Render sidebar content
            self._render_sidebar(c, is_first_page=False)
            
            if self.sidebar_content_pos < len(self.sidebar_content):
                c.showPage()
        
        c.save()
        
        # Merge with original PDF
        merger = PdfMerger()
        
        with open(self.output_file, "rb") as original_pdf:
            merger.append(original_pdf)
            new_pages_buffer.seek(0)
            merger.append(new_pages_buffer)
            
            with open(self.output_file, "wb") as output_file:
                merger.write(output_file)


def modern4(
    personal_info,
    professional_summary=None,
    work_experience=None,
    education=None,
    skills=None,
    academic_projects=None,
    certifications=None,
    publications=None,
    hobbies=None,
    languages=None,
    referees=None,
    profile_picture=None,
    output_file="resume.pdf",
    page_size="A4",
    template_image=None
):
    """
    Generate a modern resume PDF with all sections.
    
    Args:
        personal_info (dict): Contains name, title, contact info, and social media
        professional_summary (str): Professional summary text
        work_experience (list): List of work experience dictionaries
        education (list): List of education dictionaries
        skills (dict/list): Skills organized by category or flat list
        academic_projects (list): List of project dictionaries
        certifications (list): List of certification dictionaries
        publications (list): List of publication dictionaries
        hobbies (list): List of hobby strings
        languages (list): List of language strings
        referees (list): List of referee dictionaries
        profile_picture (str): Base64 encoded image string
        output_file (str): Output PDF filename
        page_size (str): Page size ("A4" or "letter")
        template_image (str): Path to template background image
    
    Returns:
        str: Path to generated PDF file
    """
    # Initialize resume generator
    resume = ResumePDF(
        output_file=output_file,
        page_size=page_size,
        template_image=template_image
    )
    
    # Add profile picture if provided
    if profile_picture:
        resume.add_profile_picture(profile_picture)
    
    # Add header with personal information
    resume.add_header(personal_info)
    
    # Add social media links
    resume._add_social_media_to_sidebar(personal_info)
    
    # Add all sections that have content
    sections = [
        ('professional_summary', resume.add_professional_summary),
        ('work_experience', resume.add_work_experience),
        ('academic_projects', resume.add_academic_projects),
        ('certifications', resume.add_certifications),
        ('publications', resume.add_publications),
        ('referees', resume.add_referees),
        ('education', resume._add_education_to_sidebar),
        ('skills', resume.add_skills),
        ('languages', resume.add_languages),
        ('hobbies', resume.add_hobbies)
    ]
    
    for section_name, section_method in sections:
        section_data = locals().get(section_name)
        if section_data:
            section_method(section_data)
    
    # Finalize and build
    resume._finalize_sidebar()
    return resume.build()
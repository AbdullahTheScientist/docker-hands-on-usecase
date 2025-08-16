from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable, Frame, Indenter
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak  
import base64
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus.flowables import KeepTogether, KeepInFrame

class ResumePDF:
    def __init__(self, output_file="resume.pdf", page_size="A4"):
        """Initialize the resume PDF generator with styling and document setup"""
        self.output_file = output_file
        
        # Set page size based on parameter
        self.page_size = page_size.lower()
        if self.page_size == "a4":
            self.pagesize = A4
        else:  # default to letter
            self.pagesize = letter
            
        # Calculate dimensions based on page size
        self.page_width, self.page_height = self.pagesize
        
        # Define sidebar width as exactly 1/3 of page width
        self.sidebar_width = self.page_width / 3
        
        self.content_width = (self.page_width * 2/3) - 63  
        
        # Adjust document margins to align with our layout
        self.doc = SimpleDocTemplate(
            output_file, 
            pagesize=self.pagesize,
            rightMargin=20, 
            leftMargin=20,
            topMargin=20, 
            bottomMargin=20
        )
        
        # Define color palette - we'll keep this for text elements
        self.colors = {
            'primary': colors.HexColor("#fff5f5"),
            'secondary': colors.HexColor("#6C757D"),
            'accent': colors.HexColor("#F18F01"),
            'light_bg': colors.HexColor("#F5F5F5"),
            'sidebar_bg': colors.HexColor("#E8E8E8")
        }
        
        # Initialize styles
        self.styles = self._setup_styles()
        self.story = []
        
        # Track sidebar content separately
        self.sidebar_content = []
        self.sidebar_content_pos = 0  # Track current position in sidebar_content
        self.profile_image_added = False
        self.image_area_height = 2*inch + 0.2*inch + 0.5*inch  

    def _setup_styles(self):
        """Configure all paragraph and text styles - only used styles"""
        styles = getSampleStyleSheet()
        
        # Used in add_header for name
        styles.add(ParagraphStyle(
            name='NameTitle',
            fontSize=20,
            leading=20,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor("#000000")
        ))
        
        # Used in add_header for title
        styles.add(ParagraphStyle(
            name='Title_',
            fontSize=14,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.HexColor("#000000")
        ))
        
        # Used in main content sections (Professional Profile, Work Experience, etc.)
        styles.add(ParagraphStyle(
            name="SectionTitle",
            fontSize=12,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used in sidebar sections (CONTACT, SKILLS, EDUCATION, etc.)
        styles.add(ParagraphStyle(
            name="SidebarSectionTitle",
            fontSize=12,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used in add_professional_summary
        styles.add(ParagraphStyle(
            name="body_style",
            fontSize=12,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontName='Helvetica',
            textColor=colors.HexColor('#241d19'),
            firstLineIndent=12
        ))
        
        # Used for company names in work experience, projects, certifications, publications
        styles.add(ParagraphStyle(
            name='Company',
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=2,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used for positions, technology descriptions, authors, etc.
        styles.add(ParagraphStyle(
            name='Position',
            fontSize=12,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=2,
            fontName='Helvetica-Oblique',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used for dates in work experience, projects, certifications, publications
        styles.add(ParagraphStyle(
            name='Date',
            fontSize=12,
            leading=12,
            alignment=TA_RIGHT,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used for bullet points in descriptions
        styles.add(ParagraphStyle(
            name="bullets",
            fontSize=12,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            fontName='Helvetica',
            leftIndent=12,
            bulletIndent=0,
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used in sidebar contact information
        styles.add(ParagraphStyle(
            name='SidebarContactTitle',
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used in sidebar contact information
        styles.add(ParagraphStyle(
            name='SidebarContactInfo',
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica',
            textColor=colors.HexColor('#241d19')
        ))
        
        # Used in sidebar skills section
        styles.add(ParagraphStyle(
            name='SidebarSkillItem',
            fontSize=11,
            leading=12,
            alignment=TA_LEFT,
            spaceAfter=1,
            textColor=colors.HexColor('#241d19'),
            fontName='Helvetica'
        ))
        
        return styles

        
        
        # self.story.append(Indenter(left=-indent_width))

    def add_header(self, personal_info):
        """Add the resume header with name, title and contact info"""
        self.story.append(Spacer(1, 80))

        name = Paragraph(personal_info['name'].upper(), self.styles['NameTitle'])
        title = Paragraph(personal_info['title'], self.styles['Title_'])

        name_title_width = min(300, self.content_width)

        name_title_table = Table([[name], [title]], colWidths=name_title_width)
        name_title_table.hAlign = 'LEFT'
        name_title_table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
        ]))

        self.story.append(Indenter(left=200))
        self.story.append(name_title_table)
        self.story.append(Indenter(left=-200))

        self.story.append(Spacer(1, 20))

        self._add_contact_to_sidebar(personal_info)
    
    def _add_contact_to_sidebar(self, personal_info):
        """Add contact information to the sidebar content with icons"""
        from reportlab.platypus import Image
        
    
        
        # Add spacing before contact section
        self.sidebar_content.append(Spacer(1, 50))
        self.sidebar_content.append(Paragraph("CONTACT", self.styles['SidebarContactTitle']))

        line_width = self.sidebar_width - 40  # Width of the sidebar content area (matches skill items)
        line = HRFlowable(
            width=line_width,
            thickness=1,
            color=colors.HexColor("#2C2A2A"),  # Light gray color
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)
        self.sidebar_content.append(Spacer(1, 10))
        self.sidebar_content.append(Indenter(left=-4))
        
        # Define icon size (0.2 inches ~ 15 pixels)
        icon_size = 0.2 * inch
        
        # Phone with icon
        try:
            phone_icon = Image("phone.png", width=icon_size, height=icon_size)
            phone_table = Table([
                [phone_icon, Paragraph(personal_info['phone'], self.styles['SidebarContactInfo'])]
            ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
            phone_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5)
            ]))
            self.sidebar_content.append(phone_table)
        except:
            self.sidebar_content.append(Paragraph(personal_info['phone'], self.styles['SidebarContactInfo']))
        
        # Email with icon  
        try:
            email_icon = Image("email.png", width=icon_size, height=icon_size)
            email_table = Table([
                [email_icon, Paragraph(personal_info['email'], self.styles['SidebarContactInfo'])]
            ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
            email_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5)
            ]))
            self.sidebar_content.append(email_table)
        except:
            self.sidebar_content.append(Paragraph(personal_info['email'], self.styles['SidebarContactInfo']))
        
        # Location/Address with icon
        if personal_info.get('location'):
            try:
                location_icon = Image("location.png", width=icon_size, height=icon_size)
                location_table = Table([
                    [location_icon, Paragraph(personal_info['location'], self.styles['SidebarContactInfo'])]
                ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
                location_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                ]))
                self.sidebar_content.append(location_table)
            except:
                self.sidebar_content.append(Paragraph(personal_info['location'], self.styles['SidebarContactInfo']))
            
        self.sidebar_content.append(Indenter(left=4))

    def _add_social_media_to_sidebar(self, personal_info):
        """Add social media links to the sidebar content with icons"""
        from reportlab.platypus import Image
        
        # Check if any social media links exist
        social_media_fields = ['facebook', 'linkedin', 'twitter', 'github', 'website']
        has_social_media = any(field in personal_info for field in social_media_fields)
        
        if not has_social_media:
            return
        
        self.sidebar_content.append(Spacer(1, 20))
        self.sidebar_content.append(Paragraph("ONLINE PRESENCE", self.styles['SidebarContactTitle']))

        line_width = self.sidebar_width - 40  # Width of the sidebar content area (matches skill items)
        line = HRFlowable(
            width=line_width,
            thickness=1,
            color=colors.HexColor("#2C2A2A"),  # Light gray color
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)
        self.sidebar_content.append(Spacer(1, 10))
        self.sidebar_content.append(Indenter(left=-4))
        
        # Define icon size (0.2 inches ~ 15 pixels)
        icon_size = 0.2 * inch
        
        # Facebook
        if 'facebook' in personal_info:
            try:
                fb_icon = Image("facebook.png", width=icon_size, height=icon_size)
                fb_link = personal_info['facebook']
                fb_para = Paragraph(f'<a href="{fb_link}" color="black">Facebook</a>', self.styles['SidebarContactInfo'])
                fb_table = Table([
                    [fb_icon, fb_para]
                ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
                fb_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                ]))
                self.sidebar_content.append(fb_table)
            except:
                fb_link = personal_info['facebook']
                self.sidebar_content.append(Paragraph(f'<a href="{fb_link}" color="white">Facebook</a>', self.styles['SidebarContactInfo']))
        
        # LinkedIn
        if 'linkedin' in personal_info:
            try:
                li_icon = Image("linkedin.png", width=icon_size, height=icon_size)
                li_link = personal_info['linkedin']
                li_para = Paragraph(f'<a href="{li_link}" color="black">LinkedIn</a>', self.styles['SidebarContactInfo'])
                li_table = Table([
                    [li_icon, li_para]
                ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
                li_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                ]))
                self.sidebar_content.append(li_table)
            except:
                li_link = personal_info['linkedin']
                self.sidebar_content.append(Paragraph(f'<a href="{li_link}" color="white">LinkedIn</a>', self.styles['SidebarContactInfo']))
        
        # Twitter
        if 'twitter' in personal_info:
            try:
                tw_icon = Image("twitter.png", width=icon_size, height=icon_size)
                tw_link = personal_info['twitter']
                tw_para = Paragraph(f'<a href="{tw_link}" color="black">Twitter</a>', self.styles['SidebarContactInfo'])
                tw_table = Table([
                    [tw_icon, tw_para]
                ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
                tw_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                ]))
                self.sidebar_content.append(tw_table)
            except:
                tw_link = personal_info['twitter']
                self.sidebar_content.append(Paragraph(f'<a href="{tw_link}" color="black">Twitter</a>', self.styles['SidebarContactInfo']))
        
        # GitHub
        if 'github' in personal_info:
            try:
                gh_icon = Image("github.png", width=icon_size, height=icon_size)
                gh_link = personal_info['github']
                gh_para = Paragraph(f'<a href="{gh_link}" color="black">GitHub</a>', self.styles['SidebarContactInfo'])
                gh_table = Table([
                    [gh_icon, gh_para]
                ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
                gh_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                ]))
                self.sidebar_content.append(gh_table)
            except:
                gh_link = personal_info['github']
                self.sidebar_content.append(Paragraph(f'<a href="{gh_link}" color="black">GitHub</a>', self.styles['SidebarContactInfo']))
        
        # Portfolio Website
        if 'website' in personal_info:
            try:
                web_icon = Image("website.png", width=icon_size, height=icon_size)
                web_link = personal_info['website']
                web_para = Paragraph(f'<a href="{web_link}" color="black">Portfolio</a>', self.styles['SidebarContactInfo'])
                web_table = Table([
                    [web_icon, web_para]
                ], colWidths=[icon_size + 5, self.sidebar_width - icon_size - 40])
                web_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5)
                ]))
                self.sidebar_content.append(web_table)
            except:
                web_link = personal_info['website']
                self.sidebar_content.append(Paragraph(f'<a href="{web_link}" color="black">Portfolio</a>', self.styles['SidebarContactInfo']))
        
        self.sidebar_content.append(Indenter(left=4))
    # self.sidebar_content.append(Indenter(left=-5))
    def add_professional_summary(self, summary_text):
        """Add professional summary section with a horizontal line under the header"""
        self.story.append(Spacer(1, 30))

        indent_width = self.page_width * 0.36

        self.story.append(Indenter(left=indent_width))
        
        # Add the section title
        self.story.append(Paragraph("PROFESSIONAL PROFILE", self.styles['SectionTitle']))
        
        # Create a horizontal line that matches the text indentation
        line_width = self.content_width  # Width of the content area
        line = HRFlowable(
            width=line_width,
            thickness=2,
            lineCap = 'round',
            color=colors.HexColor("#2C2A2A"),  # Light gray color
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)
        
        # Add the summary text
        self.story.append(Paragraph(summary_text, self.styles['body_style']))
        self.story.append(Spacer(1, 6))
        
        # self.story.append(Indenter(left=-indent_width))
    def add_publications(self, publications):
        """Add publications section with consistent formatting"""
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("PUBLICATIONS", self.styles['SectionTitle']))
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45
        
        line_width = self.content_width  # Width of the content area
        line = HRFlowable(
            width=line_width,
            thickness=2,
            lineCap="round",
            color=colors.HexColor("#2C2A2A"),
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)

        for pub in publications:
            pub_elements = []
            
            # Create title paragraph
            title = Paragraph(pub['title'], self.styles['Company'])
            
            # Create date paragraph if available
            date_para = None
            if 'date' in pub:
                date_str = pub['date'].strftime('%b %Y') if isinstance(pub['date'], datetime) else pub['date']
                date_para = Paragraph(date_str, self.styles['Date'])
            
            # Create header row with title and date
            if date_para:
                header_row = [[title, date_para]]
                header_table = Table(header_row, colWidths=[col1_width, col2_width])
                header_table.hAlign = 'LEFT'
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
            
            # Add authors if provided
            if 'authors' in pub:
                authors = Paragraph(f"<i>Authors:</i> {pub['authors']}", self.styles['Position'])
                pub_elements.append(authors)
            
            # Add journal/conference if provided
            if 'journal' in pub:
                journal = Paragraph(f"<i>Published in:</i> {pub['journal']}", self.styles['Position'])
                pub_elements.append(journal)
            
            # Add DOI/URL if provided
            if 'doi' in pub:
                doi_text = f"<i>DOI:</i> {pub['doi']}"
                doi_para = Paragraph(doi_text, self.styles['bullets'])
                pub_elements.append(doi_para)
            elif 'url' in pub:
                url_text = f"<i>URL:</i> {pub['url']}"
                url_para = Paragraph(url_text, self.styles['bullets'])
                pub_elements.append(url_para)
            
            # Add description if provided
            if 'description' in pub:
                for desc in pub['description']:
                    bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                    bullet_para_table = Table([[bullet_para]], colWidths=[self.content_width])
                    bullet_para_table.hAlign='LEFT'
                    pub_elements.append(bullet_para_table)
            
            pub_elements.append(Spacer(1, 8))
            
            # Add all elements without KeepTogether to allow natural page breaks
            for element in pub_elements:
                self.story.append(element)


    def add_languages(self, languages):
        """Add languages section to the sidebar"""
        # Add some space before the languages section
        self.sidebar_content.append(Spacer(1, 12))
        self.sidebar_content.append(Paragraph("LANGUAGES", self.styles['SidebarSectionTitle']))
        
        # Add horizontal line
        line_width = self.sidebar_width - 40
        line = HRFlowable(
            width=line_width,
            thickness=1,
            color=colors.HexColor("#2C2A2A"),
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)
        self.sidebar_content.append(Spacer(1, 6))
        # self.sidebar_content.append(Indenter(left=10))
        
        # Add languages as bullet points
        for language in languages:
            lang_para = Paragraph(f"• {language}", self.styles['SidebarSkillItem'])
            lang_para_table = Table([[lang_para]], colWidths=[self.sidebar_width - 40])
            lang_para_table.hAlign = 'LEFT'
            self.sidebar_content.append(lang_para_table)
        
        self.sidebar_content.append(Spacer(1, 6))
        # self.sidebar_content.append(Indenter(left=-10))

    def add_hobbies(self, hobbies):
        """Add hobbies section to the sidebar"""
        # Add some space before the hobbies section
        self.sidebar_content.append(Spacer(1, 12))
        self.sidebar_content.append(Paragraph("HOBBIES & INTERESTS", self.styles['SidebarSectionTitle']))
        
        # Add horizontal line
        line_width = self.sidebar_width - 40
        line = HRFlowable(
            width=line_width,
            thickness=1,
            color=colors.HexColor("#2C2A2A"),
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)
        self.sidebar_content.append(Spacer(1, 6))
        self.sidebar_content.append(Indenter(left=-4))
        
        # Add hobbies as bullet points
        for hobby in hobbies:
            hobby_para = Paragraph(f"• {hobby}", self.styles['SidebarSkillItem'])
            hobby_para_table = Table([[hobby_para]], colWidths=[self.sidebar_width - 40])
            hobby_para_table.hAlign = 'LEFT'
            self.sidebar_content.append(hobby_para_table)
        
        self.sidebar_content.append(Spacer(1, 6))
        self.sidebar_content.append(Indenter(left=4))

    def add_work_experience(self, work_experience):
        """Add work experience section with consistent formatting"""
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("WORK EXPERIENCE", self.styles['SectionTitle']))
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45

        line_width = self.content_width  # Width of the content area
        line = HRFlowable(
            width=line_width,
            thickness=2,
            lineCap="round",
            color=colors.HexColor("#2C2A2A"),  # Light gray color
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)
        
        for job in work_experience:
            job_elements = []
            
            company = Paragraph(job['company'], self.styles['Company'])
            position = Paragraph(job['position'], self.styles['Position'])
            
            start_date = job['start_date'].strftime('%b %Y') if isinstance(job['start_date'], datetime) else job['start_date']
            end_date = job['end_date'].strftime('%b %Y') if isinstance(job['end_date'], datetime) else job['end_date']
            date_range = Paragraph(f"{start_date} - {end_date}", self.styles['Date'])
            
            header_row = [[position, date_range]]
            header_table = Table(header_row, colWidths=[col1_width, col2_width])
            header_table.hAlign = 'LEFT'
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
            
            for desc in job['description']:
                bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                bullet_para_table = Table([[bullet_para]], colWidths=[self.content_width])
                bullet_para_table.hAlign = 'LEFT'
                bullet_para_table.setStyle(TableStyle([
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
                ]))
                job_elements.append(bullet_para_table)
            
            job_elements.append(Spacer(1, 8))
            
            if len(job['description']) <= 3:
                self.story.append(KeepTogether(job_elements))
            else:
                for element in job_elements:
                    self.story.append(element)

            
    def add_academic_projects(self, projects):
        """Add academic projects section with descriptions"""
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("PROJECTS", self.styles['SectionTitle']))
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45
        line_width = self.content_width  # Width of the content area
        line = HRFlowable(
            width=line_width,
            thickness=2,
            lineCap="round",
            color=colors.HexColor("#183a54"), # Light gray color
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)

        for project in projects:
            project_elements = []
            
            project_title = Paragraph(project['title'], self.styles['Company'])
            
            date_str = ""
            if 'date' in project:
                date_str = project['date']
            elif 'start_date' in project and 'end_date' in project:
                start_date = project['start_date'].strftime('%b %Y') if isinstance(project['start_date'], datetime) else project['start_date']
                end_date = project['end_date'].strftime('%b %Y') if isinstance(project['end_date'], datetime) else project['end_date']
                date_str = f"{start_date} - {end_date}"
                
            date_para = Paragraph(date_str, self.styles['Date']) if date_str else None
            
            if date_para:
                header_row = [[project_title, date_para]]
                header_table = Table(header_row, colWidths=[col1_width, col2_width])
                header_table.hAlign = 'LEFT'
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
                project_elements.append(project_title)
            
            if 'technologies' in project:
                tech_text = f"<i>Technologies:</i> {project['technologies']}"
                tech_para = Paragraph(tech_text, self.styles['Position'])
                project_elements.append(tech_para)
            
            if 'description' in project:
                for desc in project['description']:
                    bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                    bullet_para_table = Table([[bullet_para]], colWidths=[self.content_width])
                    bullet_para_table.hAlign='LEFT'
                    project_elements.append(bullet_para_table)
            
            if 'links' in project and project['links']:
                for link_name, link_url in project['links'].items():
                    link_text = f"<b>{link_name}:</b> {link_url}"
                    link_para = Paragraph(link_text, self.styles['bullets'])
                    project_elements.append(link_para)
            
            project_elements.append(Spacer(1, 8))
            
            # Remove the KeepTogether logic - always add elements individually
            # This allows natural page breaks within projects
            for element in project_elements:
                self.story.append(element)
        
    def add_skills(self, skills):
        """Add skills section to the sidebar as a single list without categories"""
        self.sidebar_content.append(Paragraph("SKILLS", self.styles['SidebarSectionTitle']))
        # Add horizontal line that matches the text indentation
        line_width = self.sidebar_width - 40  # Width of the sidebar content area
        line = HRFlowable(
            width=line_width,
            thickness=1,
            lineCap="round",
            color=colors.HexColor("#2C2A2A"),
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)

        # Combine all skills into a single list
        all_skills = []
        if isinstance(skills, dict):
            # If skills is a dictionary with categories, flatten it
            for category, skill_list in skills.items():
                all_skills.extend(skill_list)
        elif isinstance(skills, list):
            # If skills is already a flat list
            all_skills = skills
        
        # Add all skills as bullet points
        for skill in all_skills:
            skill_para = Paragraph(f"• {skill}", self.styles['SidebarSkillItem'])
            skill_para_table = Table([[skill_para]], colWidths=[self.sidebar_width - 40])
            skill_para_table.hAlign = 'LEFT'
            self.sidebar_content.append(skill_para_table)
        self.sidebar_content.append(Spacer(1, 6))
    def add_certifications(self, certifications):
        """Add certifications section with consistent formatting"""
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("CERTIFICATIONS", self.styles['SectionTitle']))
        
        col1_width = self.content_width * 0.55
        col2_width = self.content_width * 0.45
        line_width = self.content_width  # Width of the content area
        line = HRFlowable(
            width=line_width,
            thickness=2,
            lineCap="round",
            color=colors.HexColor("#2C2A2A"),  # Light gray color
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)

        
        for cert in certifications:
            cert_elements = []
            
            # Create certification name and date elements
            name = Paragraph(cert['name'], self.styles['Company'])
            
            date_str = ""
            if 'date' in cert:
                date_str = cert['date'].strftime('%b %Y') if isinstance(cert['date'], datetime) else cert['date']
            elif 'issue_date' in cert:
                date_str = cert['issue_date'].strftime('%b %Y') if isinstance(cert['issue_date'], datetime) else cert['issue_date']
            
            date_para = Paragraph(date_str, self.styles['Date']) if date_str else None
            
            # Create header row with name and date
            if date_para:
                header_row = [[name, date_para]]
                header_table = Table(header_row, colWidths=[col1_width, col2_width])
                header_table.hAlign = 'LEFT'
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
            
            # Add issuer if provided
            if 'issuer' in cert:
                issuer = Paragraph(f"<i>Issued by:</i> {cert['issuer']}", self.styles['Position'])
                cert_elements.append(issuer)
            
            # Add credential ID if provided
            if 'credential_id' in cert:
                cred_id = Paragraph(f"<i>Credential ID:</i> {cert['credential_id']}", self.styles['Position'])
                cert_elements.append(cred_id)
            
            # Add URL if provided
            if 'url' in cert:
                url_text = f"<i>URL:</i> {cert['url']}"
                url_para = Paragraph(url_text, self.styles['bullets'])
                cert_elements.append(url_para)
            
            # Add description if provided
            if 'description' in cert:
                for desc in cert['description']:
                    bullet_para = Paragraph(desc, style=self.styles['bullets'], bulletText='•')
                    bullet_para_table = Table([[bullet_para]], colWidths=[self.content_width])
                    bullet_para_table.hAlign='LEFT'
                    cert_elements.append(bullet_para_table)
            
            cert_elements.append(Spacer(1, 8))
            
            # Add all elements without KeepTogether to allow natural page breaks
            for element in cert_elements:
                self.story.append(element)
    def add_referees(self, referees):
        """Add referees section with contact information"""
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("REFERENCES", self.styles['SectionTitle']))
        
        line_width = self.content_width  # Width of the content area
        line = HRFlowable(
            width=line_width,
            thickness=2,
            lineCap="round",
            color=colors.HexColor("#2C2A2A"),
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.story.append(line)
        
        for referee in referees:
            ref_elements = []
            
            # Create name and position paragraph
            name = Paragraph(referee['name'], self.styles['Company'])
            position = Paragraph(referee['position'], self.styles['Position'])
            ref_elements.extend([name, position])
            
            # Add organization if provided
            if 'organization' in referee:
                org = Paragraph(f"<i>{referee['organization']}</i>", self.styles['Position'])
                ref_elements.append(org)
            
            # Add contact information
            contact_items = []
            if 'phone' in referee:
                contact_items.append(f"Phone: {referee['phone']}")
            if 'email' in referee:
                contact_items.append(f"Email: {referee['email']}")
            
            if contact_items:
                contact_text = " | ".join(contact_items)
                contact_para = Paragraph(contact_text, self.styles['bullets'])
                ref_elements.append(contact_para)
            
            # Add relationship if provided
            if 'relationship' in referee:
                rel_para = Paragraph(f"<i>Relationship:</i> {referee['relationship']}", self.styles['bullets'])
                ref_elements.append(rel_para)
            
            ref_elements.append(Spacer(1, 12))
            
            # Add all elements
            for element in ref_elements:
                self.story.append(element)
    from datetime import datetime

    def _add_education_to_sidebar(self, education):
        """Add education information to the sidebar content"""
        self.sidebar_content.append(Paragraph("EDUCATION", self.styles['SidebarSectionTitle']))
        
        # Add horizontal line
        line_width = self.sidebar_width - 40
        line = HRFlowable(
            width=line_width,
            thickness=1,
            color=colors.HexColor("#2C2A2A"),
            spaceBefore=4,
            spaceAfter=8,
            hAlign='LEFT'
        )
        self.sidebar_content.append(line)
        self.sidebar_content.append(Spacer(1, 10))
        self.sidebar_content.append(Indenter(left=6))
        
        for edu in education:
            # Create institution paragraph
            institution = Paragraph(edu['institution'], self.styles['SidebarContactInfo'])
            self.sidebar_content.append(institution)
            
            # Create degree paragraph
            degree = Paragraph(edu['degree'], self.styles['SidebarSkillItem'])
            self.sidebar_content.append(degree)
            
            # Format start and end dates
            start_date = edu.get('start_date')
            end_date = edu.get('end_date')

            if isinstance(start_date, datetime):
                start_date = start_date.strftime("%b %Y")
            if isinstance(end_date, datetime):
                end_date = end_date.strftime("%b %Y")

            date_range = f"{start_date} - {end_date}" if start_date and end_date else start_date or end_date or ""
            if date_range:
                date_para = Paragraph(date_range, self.styles['SidebarSkillItem'])
                self.sidebar_content.append(date_para)

            self.sidebar_content.append(Spacer(1, 8))
        
        self.sidebar_content.append(Indenter(left=-6))

    def _render_sidebar(self, canvas, is_first_page):
        """Render sidebar content across pages, continuing where it left off."""
        canvas.saveState()
        
        # Adjust frame dimensions based on whether it's the first page
        if is_first_page:
            frame_height = self.page_height - 60  # More space used by header on first page
            start_y = 20
        else:
            frame_height = self.page_height - 40
            start_y = 20

        sidebar_x = 40
        sidebar_width = (self.page_width / 3) - 30
        
        # Create a temporary list to track what we can fit on this page
        elements_to_render = []
        remaining_height = frame_height
        
        # Track if we're forcing an element onto the next page
        force_next_page = False
        
        # Check each element starting from current position
        while self.sidebar_content_pos < len(self.sidebar_content) and not force_next_page:
            element = self.sidebar_content[self.sidebar_content_pos]
            
            # Calculate element height
            if isinstance(element, Spacer):
                h = element.height
            else:
                w, h = element.wrap(sidebar_width, remaining_height)
            
            # Special case: if it's the first element on a new page and doesn't fit
            if not elements_to_render and h > remaining_height:
                # Force it onto this page anyway (it will be clipped but prevents skipping)
                elements_to_render.append(element)
                self.sidebar_content_pos += 1
                remaining_height = 0  # Force a new page after this
                force_next_page = True
            elif h <= remaining_height:
                # Element fits, add it
                elements_to_render.append(element)
                remaining_height -= h
                self.sidebar_content_pos += 1
            else:
                # Element doesn't fit and we already have content, stop for this page
                force_next_page = True
        
        # Only create frame and render if we have elements
        if elements_to_render:
            frame = Frame(
                sidebar_x, 
                start_y,
                sidebar_width, 
                frame_height,
                showBoundary=0,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0
            )
            
            # Use KeepInFrame to prevent content from being lost
            kept_elements = KeepInFrame(
                sidebar_width,
                frame_height,
                elements_to_render,
                hAlign='LEFT',
                vAlign='TOP',
                fakeWidth=False
            )
            
            frame.addFromList([kept_elements], canvas)
        
        # Add vertical line between sidebar and main content
        line_x = sidebar_x + sidebar_width + 15  # Position line between sidebar and main content
        line_y_start = 20  # Bottom of page (with margin)
        line_y_end = self.page_height - 20  # Top of page (with margin)
        
        canvas.setStrokeColor(colors.HexColor("#2C2A2A"))
        canvas.setLineWidth(1)
        canvas.line(line_x, line_y_start, line_x, line_y_end)
        
        canvas.restoreState()

    def draw_first_page(self, canvas, doc):
        """Draw first page template and initial sidebar content."""
        # Remove background image drawing - just render sidebar
        self._render_sidebar(canvas, is_first_page=True)

    def draw_later_pages(self, canvas, doc):
        """Draw subsequent pages template and remaining sidebar content."""
        # Remove background image drawing - just render sidebar
        self._render_sidebar(canvas, is_first_page=False)

    def build(self):
        """Build the PDF document with proper handling for sidebar-only pages"""
        # First build all main content and first page sidebar
        self.doc.build(self.story, 
                    onFirstPage=self.draw_first_page, 
                    onLaterPages=self.draw_later_pages)
        
        # Check if there's remaining sidebar content that didn't fit
        if self.sidebar_content_pos < len(self.sidebar_content):
            # Re-open the existing PDF in append mode
            from reportlab.pdfgen import canvas
            from PyPDF2 import PdfMerger
            import io
            
            # Create a temporary buffer for the new pages
            new_pages_buffer = io.BytesIO()
            c = canvas.Canvas(new_pages_buffer, pagesize=self.pagesize)
            
            # Keep adding pages until all sidebar content is rendered
            while self.sidebar_content_pos < len(self.sidebar_content):
                # No background image drawing - blank page
                
                # Render as much sidebar content as fits on this page
                self._render_sidebar(c, is_first_page=False)
                
                # If there's still content left, add a new page
                if self.sidebar_content_pos < len(self.sidebar_content):
                    c.showPage()
            
            c.save()
            
            # Now merge the original PDF with the new pages
            merger = PdfMerger()
            
            # Read the original PDF
            with open(self.output_file, "rb") as original_pdf:
                merger.append(original_pdf)
                
                # Read the new pages
                new_pages_buffer.seek(0)
                merger.append(new_pages_buffer)
                
                # Write the combined result back to the output file
                with open(self.output_file, "wb") as output_file:
                    merger.write(output_file)
        
        return self.output_file
    


def professional1(
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
    page_size="A4"
):
    """
    Generate a modern resume PDF with all sections.
    
    Args:
        personal_info (dict): Required. Contains name, title, phone, email, location, and optional social media
        professional_summary (str): Optional. Professional summary text
        work_experience (list): Optional. List of work experience dictionaries
        education (list): Optional. List of education dictionaries
        skills (dict/list): Optional. Skills organized by category or flat list
        academic_projects (list): Optional. List of project dictionaries
        certifications (list): Optional. List of certification dictionaries
        publications (list): Optional. List of publication dictionaries
        hobbies (list): Optional. List of hobby strings
        languages (list): Optional. List of language strings
        referees (list): Optional. List of referee dictionaries
        achievements (list): Optional. List of achievement dictionaries
        honors_awards (list): Optional. List of honors and awards dictionaries
        profile_picture (str): Optional. Base64 encoded image string
        output_file (str): Output PDF filename
        page_size (str): Page size ("A4" or "letter")
        template_image (str): Path to template background image
    
    Returns:
        str: Path to generated PDF file
    """
    
    # Initialize the resume PDF generator
    resume = ResumePDF(
        output_file=output_file,
        page_size=page_size,
        # template_image=template_image
    )
    
    # # Add profile picture if provided
    # if profile_picture:
    #     resume.add_profile_picture(profile_picture)
    
    # Add header with personal information (required)
    resume.add_header(personal_info)
    
    # Add social media to sidebar if present in personal_info
    resume._add_social_media_to_sidebar(personal_info)
    
    # Add professional summary if provided
    if professional_summary:
        resume.add_professional_summary(professional_summary)
    
    # Add work experience if provided
    if work_experience:
        resume.add_work_experience(work_experience)
    
    # Add academic projects if provided
    if academic_projects:
        resume.add_academic_projects(academic_projects)
          
    # Add certifications if provided
    if certifications:
        resume.add_certifications(certifications)
    
    # Add publications if provided
    if publications:
        resume.add_publications(publications)
    
    # Add referees if provided
    if referees:
        resume.add_referees(referees)
    
    # Add education to sidebar if provided
    if education:
        resume._add_education_to_sidebar(education)
    
    # Add skills to sidebar if provided
    if skills:
        resume.add_skills(skills)
    
    # Add languages to sidebar if provided
    if languages:
        resume.add_languages(languages)
    
    # Add hobbies to sidebar if provided
    if hobbies:
        resume.add_hobbies(hobbies)
    
    # Build and save the PDF
    return resume.build()

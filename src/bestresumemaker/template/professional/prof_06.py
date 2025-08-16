from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.units import inch, mm
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.platypus.flowables import Flowable

class ColoredLine(Flowable):
    """Custom flowable for colored horizontal lines"""
    def __init__(self, width, height=2, color=colors.black):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

def professional6(personal_info, professional_summary, work_experience, education, skills, 
                          academic_projects=None, certifications=None, publications=None, 
                          hobbies=None, languages=None, referees=None, awards=None,
                          output_file="modern_resume.pdf", page_size="letter"):
    
    # Set page size based on user preference
    if page_size.lower() == "a4":
        page_dimensions = A4
        margin = 20 * mm
    else:
        page_dimensions = letter
        margin = 0.75 * inch
    
    # Create document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=page_dimensions,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Modern color scheme
    primary_color = colors.HexColor("#1E3A8A")  # Deep blue
    secondary_color = colors.HexColor("#64748B")  # Slate gray
    accent_color = colors.HexColor("#F59E0B")  # Amber
    light_bg = colors.HexColor("#F8FAFC")  # Light background
    text_color = colors.HexColor("#1F2937")  # Dark gray
    
    font_size_adjustment = 0.95 if page_size.lower() == "a4" else 1
    page_width = page_dimensions[0] - (2 * margin)

    # Custom styles
    styles.add(ParagraphStyle(
        name="ModernName",
        fontSize=28 * font_size_adjustment,
        leading=32 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        textColor=primary_color
    ))

    styles.add(ParagraphStyle(
        name="ModernTitle",
        fontSize=16 * font_size_adjustment,
        leading=20 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=8,
        fontName='Helvetica',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="ContactInfo",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica',
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=14 * font_size_adjustment,
        leading=18 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceBefore=18,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        borderWidth=0,
        borderColor=primary_color,
        borderPadding=0
    ))

    styles.add(ParagraphStyle(
        name="CompanyName",
        fontSize=12 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="JobTitle",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=accent_color
    ))

    styles.add(ParagraphStyle(
        name="DateRange",
        fontSize=10 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_RIGHT,
        spaceAfter=6,
        fontName='Helvetica-Oblique',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="ModernBodyText",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="ModernBulletPoint",
        fontSize=10 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=3,
        fontName='Helvetica',
        leftIndent=12,
        bulletIndent=0,
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="SkillCategory",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        textColor=primary_color
    ))

    styles.add(ParagraphStyle(
        name="SkillItems",
        fontSize=10 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=8,
        fontName='Helvetica',
        textColor=text_color
    ))

    def format_date(date_obj):
        """Helper function to format dates consistently"""
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%b %Y")
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)
    
    def add_bullet_list(items, story_list):
        """Helper function to add bullet lists"""
        if isinstance(items, str):
            items = items.split('\n')
        
        for item in items:
            if item.strip():
                clean_item = item.strip().strip('"').strip("'")
                story_list.append(Paragraph(f"• {clean_item}", styles['ModernBulletPoint']))
    
    def create_two_column_table(left_content, right_content, left_width=0.7):
        """Create a two-column table for aligned content"""
        right_width = 1.0 - left_width
        table_data = [[left_content, right_content]]
        table = Table(table_data, colWidths=[page_width * left_width, page_width * right_width])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        return table
    
    # ===== HEADER SECTION =====
    story.append(Paragraph(personal_info['name'], styles['ModernName']))
    story.append(Paragraph(personal_info['title'], styles['ModernTitle']))
    
    # Contact information in a clean line
    contact_parts = []
    if 'email' in personal_info and personal_info['email']:
        contact_parts.append(personal_info['email'])
    if 'phone' in personal_info and personal_info['phone']:
        contact_parts.append(personal_info['phone'])
    if 'location' in personal_info and personal_info['location']:
        contact_parts.append(personal_info['location'])
    
    # Social media links
    social_parts = []
    if 'linkedin' in personal_info and personal_info['linkedin']:
        social_parts.append(f"LinkedIn: {personal_info['linkedin']}")
    if 'github' in personal_info and personal_info['github']:
        social_parts.append(f"GitHub: {personal_info['github']}")
    if 'website' in personal_info and personal_info['website']:
        social_parts.append(f"Website: {personal_info['website']}")
    
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), styles['ContactInfo']))
    if social_parts:
        story.append(Paragraph(" | ".join(social_parts), styles['ContactInfo']))
    
    # Add colored line separator
    story.append(Spacer(1, 8))
    story.append(ColoredLine(page_width, 3, primary_color))
    story.append(Spacer(1, 12))
    
    # ===== PROFESSIONAL SUMMARY =====
    story.append(Paragraph("PROFESSIONAL SUMMARY", styles['SectionHeader']))
    story.append(ColoredLine(page_width * 0.3, 2, accent_color))
    story.append(Spacer(1, 6))
    story.append(Paragraph(professional_summary, styles['ModernBodyText']))
    
    # ===== PROFESSIONAL EXPERIENCE =====
    if work_experience:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for job in work_experience:
            start_date = format_date(job['start_date'])
            end_date = format_date(job['end_date'])
            date_range = f"{start_date} - {end_date}"
            
            # Company and date in two columns
            company_info = Paragraph(job['company'], styles['CompanyName'])
            date_info = Paragraph(date_range, styles['DateRange'])
            story.append(create_two_column_table(company_info, date_info))
            
            story.append(Paragraph(job['position'], styles['JobTitle']))
            
            # Add job description
            job_items = []
            add_bullet_list(job['description'], job_items)
            story.extend(job_items)
            story.append(Spacer(1, 12))
    
    # ===== EDUCATION =====
    if education:
        story.append(Paragraph("EDUCATION", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for edu in education:
            start_date = format_date(edu.get('start_date', ''))
            end_date = format_date(edu.get('graduation_date', edu.get('end_date', '')))
            
            if start_date and end_date:
                date_range = f"{start_date} - {end_date}"
            elif end_date:
                date_range = end_date
            elif start_date:
                date_range = f"{start_date} - Present"
            else:
                date_range = ""
            
            # Institution and date in two columns
            institution_info = Paragraph(edu['institution'], styles['CompanyName'])
            date_info = Paragraph(date_range, styles['DateRange'])
            story.append(create_two_column_table(institution_info, date_info))
            
            story.append(Paragraph(edu['degree'], styles['JobTitle']))
            
            # Add GPA or honors if available
            if 'gpa' in edu and edu['gpa']:
                story.append(Paragraph(f"GPA: {edu['gpa']}", styles['ContactInfo']))
            if 'honors' in edu and edu['honors']:
                story.append(Paragraph(f"Honors: {edu['honors']}", styles['ContactInfo']))
            
            story.append(Spacer(1, 12))
    
    # ===== SKILLS =====
    if skills:
        story.append(Paragraph("CORE COMPETENCIES", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        # Group skills if they're provided as categories
        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                story.append(Paragraph(category, styles['SkillCategory']))
                if isinstance(skill_list, list):
                    skills_text = " • ".join(skill_list)
                else:
                    skills_text = skill_list
                story.append(Paragraph(skills_text, styles['SkillItems']))
        else:
            # Simple list of skills
            if isinstance(skills, list):
                skills_text = " • ".join(skills)
            else:
                skills_text = str(skills)
            story.append(Paragraph(skills_text, styles['SkillItems']))
    
    # ===== ACADEMIC PROJECTS =====
    if academic_projects:
        story.append(Paragraph("KEY PROJECTS", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for project in academic_projects:
            project_date = format_date(project['date'])
            
            # Project title and date
            project_info = Paragraph(project['title'], styles['CompanyName'])
            date_info = Paragraph(project_date, styles['DateRange'])
            story.append(create_two_column_table(project_info, date_info))
            
            story.append(Paragraph(f"Technologies: {project['technologies']}", styles['JobTitle']))
            
            # Project description
            project_items = []
            add_bullet_list(project['description'], project_items)
            story.extend(project_items)
            
            # Add links if available
            if 'links' in project and project['links']:
                links_text = " | ".join([f"{name}: {url}" for name, url in project['links'].items()])
                story.append(Paragraph(f"Links: {links_text}", styles['ContactInfo']))
            
            story.append(Spacer(1, 12))
    
    # ===== CERTIFICATIONS =====
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for cert in certifications:
            cert_date = format_date(cert['date'])
            
            cert_info = Paragraph(cert['name'], styles['CompanyName'])
            date_info = Paragraph(cert_date, styles['DateRange'])
            story.append(create_two_column_table(cert_info, date_info))
            
            story.append(Paragraph(f"Issued by: {cert['issuer']}", styles['JobTitle']))
            
            if 'credential_id' in cert and cert['credential_id']:
                story.append(Paragraph(f"Credential ID: {cert['credential_id']}", styles['ContactInfo']))
            
            if 'description' in cert and cert['description']:
                cert_items = []
                add_bullet_list(cert['description'], cert_items)
                story.extend(cert_items)
            
            story.append(Spacer(1, 12))
    
    # ===== AWARDS =====
    if awards:
        story.append(Paragraph("AWARDS & RECOGNITION", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for award in awards:
            award_date = format_date(award['date'])
            
            award_info = Paragraph(award['name'], styles['CompanyName'])
            date_info = Paragraph(award_date, styles['DateRange'])
            story.append(create_two_column_table(award_info, date_info))
            
            if 'issuer' in award and award['issuer']:
                story.append(Paragraph(f"Awarded by: {award['issuer']}", styles['JobTitle']))
            
            if 'description' in award and award['description']:
                story.append(Paragraph(award['description'], styles['ModernBodyText']))
            
            story.append(Spacer(1, 12))
    
    # ===== PUBLICATIONS =====
    if publications:
        story.append(Paragraph("PUBLICATIONS", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for pub in publications:
            pub_date = format_date(pub['date'])
            
            pub_info = Paragraph(pub['title'], styles['CompanyName'])
            date_info = Paragraph(pub_date, styles['DateRange'])
            story.append(create_two_column_table(pub_info, date_info))
            
            story.append(Paragraph(f"Authors: {pub['authors']}", styles['ContactInfo']))
            story.append(Paragraph(f"Published in: {pub['journal']}", styles['JobTitle']))
            
            if 'url' in pub and pub['url']:
                story.append(Paragraph(f"DOI/URL: {pub['url']}", styles['ContactInfo']))
            
            if 'description' in pub and pub['description']:
                pub_items = []
                add_bullet_list(pub['description'], pub_items)
                story.extend(pub_items)
            
            story.append(Spacer(1, 12))
    
    # ===== ADDITIONAL SECTIONS =====
    additional_sections = []
    
    if languages:
        additional_sections.append(("Languages", languages))
    
    if hobbies:
        additional_sections.append(("Interests", hobbies))
    
    if additional_sections:
        story.append(Paragraph("ADDITIONAL INFORMATION", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        for section_name, section_items in additional_sections:
            story.append(Paragraph(section_name, styles['SkillCategory']))
            if isinstance(section_items, list):
                items_text = " • ".join(section_items)
            else:
                items_text = str(section_items)
            story.append(Paragraph(items_text, styles['SkillItems']))
    
    # ===== REFERENCES =====
    if referees:
        story.append(Paragraph("REFERENCES", styles['SectionHeader']))
        story.append(ColoredLine(page_width * 0.3, 2, accent_color))
        story.append(Spacer(1, 6))
        
        # Create a table for references if there are multiple
        if len(referees) > 1:
            ref_data = []
            for i in range(0, len(referees), 2):  # Process in pairs
                left_ref = referees[i]
                right_ref = referees[i + 1] if i + 1 < len(referees) else None
                
                left_content = [
                    Paragraph(left_ref['name'], styles['CompanyName']),
                    Paragraph(left_ref['position'], styles['JobTitle']),
                    Paragraph(left_ref['organization'], styles['ContactInfo']),
                    Paragraph(f"Email: {left_ref['email']}", styles['ContactInfo']),
                    Paragraph(f"Phone: {left_ref['phone']}", styles['ContactInfo'])
                ]
                
                if right_ref:
                    right_content = [
                        Paragraph(right_ref['name'], styles['CompanyName']),
                        Paragraph(right_ref['position'], styles['JobTitle']),
                        Paragraph(right_ref['organization'], styles['ContactInfo']),
                        Paragraph(f"Email: {right_ref['email']}", styles['ContactInfo']),
                        Paragraph(f"Phone: {right_ref['phone']}", styles['ContactInfo'])
                    ]
                else:
                    right_content = [Paragraph("", styles['ContactInfo']) for _ in range(5)]
                
                ref_data.append([left_content, right_content])
            
            for row in ref_data:
                ref_table = Table([row], colWidths=[page_width * 0.5, page_width * 0.5])
                ref_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ]))
                story.append(ref_table)
        else:
            # Single reference
            ref = referees[0]
            story.append(Paragraph(ref['name'], styles['CompanyName']))
            story.append(Paragraph(ref['position'], styles['JobTitle']))
            story.append(Paragraph(ref['organization'], styles['ContactInfo']))
            story.append(Paragraph(f"Email: {ref['email']}", styles['ContactInfo']))
            story.append(Paragraph(f"Phone: {ref['phone']}", styles['ContactInfo']))
            
            if 'relationship' in ref and ref['relationship']:
                story.append(Paragraph(f"Relationship: {ref['relationship']}", styles['ContactInfo']))
    
    # Build the document
    doc.build(story)

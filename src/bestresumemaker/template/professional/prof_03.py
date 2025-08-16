from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.units import inch, mm
from reportlab.platypus.flowables import Flowable

class ColoredBox(Flowable):
    """Custom flowable for colored background boxes"""
    def __init__(self, width, height, color):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

def professional3(personal_info, professional_summary, work_experience, education, skills, 
                          academic_projects=None, certifications=None, publications=None, 
                          hobbies=None, languages=None, referees=None, achievements=None,
                          honors_awards=None, output_file="modern_resume.pdf", page_size="letter"):
    
    # Set page size based on user preference
    if page_size.lower() == "a4":
        page_dimensions = A4
        margin_left_right = 12 * mm
        margin_top_bottom = 15 * mm
    else:
        page_dimensions = letter
        margin_left_right = 0.4 * inch
        margin_top_bottom = 0.4 * inch
    
    doc = SimpleDocTemplate(output_file, pagesize=page_dimensions,
                          rightMargin=margin_left_right, 
                          leftMargin=margin_left_right,
                          topMargin=margin_top_bottom, 
                          bottomMargin=margin_top_bottom)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Modern color scheme - Professional blue and gray palette
    primary_color = colors.HexColor("#1A365D")      # Dark blue
    secondary_color = colors.HexColor("#4A90A4")    # Medium blue
    accent_color = colors.HexColor("#68D391")       # Green accent
    text_color = colors.HexColor("#2D3748")         # Dark gray
    light_gray = colors.HexColor("#F7FAFC")         # Light background
    font_size_adjustment = 0.95 if page_size.lower() == "a4" else 1
    
    # CONSISTENT ALIGNMENT SETTINGS
    STANDARD_LEFT_INDENT = 0  # All content starts at same left position
    BULLET_INDENT = 12        # Consistent bullet point indentation
    STANDARD_RIGHT_PADDING = 0  # All content ends at same right position

    # Modern custom styles with consistent alignment
    styles.add(ParagraphStyle(
        name="ModernNameTitle",
        fontSize=32 * font_size_adjustment,
        leading=36 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        letterSpacing=1,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernSubtitle",
        fontSize=14 * font_size_adjustment,
        leading=18 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=20,
        fontName='Helvetica',
        textColor=secondary_color,
        letterSpacing=0.5,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernContact",
        fontSize=9 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=15,
        fontName='Helvetica',
        textColor=text_color,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernSectionHeader",
        fontSize=13 * font_size_adjustment,
        leading=18 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceBefore=18,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        borderPadding=(8, 8, 8, 8),
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernCompanyName",
        fontSize=12 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=1,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernJobTitle",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=1,
        fontName='Helvetica',
        textColor=secondary_color,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernDateStyle",
        fontSize=9 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_RIGHT,
        spaceAfter=6,
        fontName='Helvetica-Oblique',
        textColor=text_color,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernBodyText",
        fontSize=10 * font_size_adjustment,
        leading=15 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        textColor=text_color,
        firstLineIndent=0,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernBulletPoint",
        fontSize=9.5 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=3,
        fontName='Helvetica',
        leftIndent=BULLET_INDENT,
        bulletIndent=0,
        textColor=text_color,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    styles.add(ParagraphStyle(
        name="ModernSkillText",
        fontSize=9 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=3,
        fontName='Helvetica',
        textColor=text_color,
        leftIndent=STANDARD_LEFT_INDENT,
        rightIndent=STANDARD_RIGHT_PADDING
    ))

    def format_date(date_obj):
        """Helper function to format dates consistently"""
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%b %Y")
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)
    
    def add_modern_bullet_list(items, style=None):
        """Helper function to add modern bullet lists with consistent alignment"""
        if style is None:
            style = styles['ModernBulletPoint']
        
        if isinstance(items, str):
            items = items.split('\n')
        
        for item in items:
            if item.strip():
                clean_item = item.strip().strip('"').strip("'")
                story.append(Paragraph(f"▸ {clean_item}", style))
    
    def add_section_divider():
        """Add a subtle section divider"""
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', 
                              color=colors.HexColor("#E2E8F0"), spaceBefore=0, spaceAfter=6))
    
    # ===== HEADER SECTION WITH CONSISTENT ALIGNMENT =====
    # Create header table with consistent padding
    header_data = [
        [
            Paragraph(personal_info['name'].upper(), styles['ModernNameTitle']),
            ""
        ],
        [
            Paragraph(personal_info['title'], styles['ModernSubtitle']),
            ""
        ]
    ]
    
    # Add contact information in a clean format
    contact_info = []
    for field in ['email', 'phone', 'location']:
        if field in personal_info and personal_info[field]:
            contact_info.append(personal_info[field])
    
    web_info = []
    for field in ['linkedin', 'github', 'website']:
        if field in personal_info and personal_info[field]:
            web_info.append(personal_info[field])
    
    # Format contact info in two columns
    if contact_info:
        contact_text = " | ".join(contact_info)
        header_data.append([Paragraph(contact_text, styles['ModernContact']), ""])
    
    if web_info:
        web_text = " | ".join(web_info)
        header_data.append([Paragraph(web_text, styles['ModernContact']), ""])
    
    header_table = Table(header_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    add_section_divider()
    
    # ===== PROFESSIONAL SUMMARY =====
    story.append(Paragraph("EXECUTIVE SUMMARY", styles['ModernSectionHeader']))
    story.append(Paragraph(professional_summary, styles['ModernBodyText']))
    
    # ===== PROFESSIONAL EXPERIENCE =====
    if work_experience:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['ModernSectionHeader']))
        
        for job in work_experience:
            start_date = format_date(job['start_date'])
            end_date = format_date(job['end_date'])
            date_range = f"{start_date} - {end_date}"
            
            # Create a table for job header with consistent alignment
            job_header = Table([
                [
                    Paragraph(job['company'], styles['ModernCompanyName']),
                    Paragraph(date_range, styles['ModernDateStyle'])
                ],
                [
                    Paragraph(job['position'], styles['ModernJobTitle']),
                    ""
                ]
            ], colWidths=[doc.width * 0.7, doc.width * 0.3])
            
            job_header.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            
            story.append(job_header)
            add_modern_bullet_list(job['description'])
            story.append(Spacer(1, 12))
    
    # ===== EDUCATION =====
    if education:
        story.append(Paragraph("EDUCATION", styles['ModernSectionHeader']))
        
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
            
            edu_header = Table([
                [
                    Paragraph(edu['institution'], styles['ModernCompanyName']),
                    Paragraph(date_range, styles['ModernDateStyle'])
                ],
                [
                    Paragraph(edu['degree'], styles['ModernJobTitle']),
                    ""
                ]
            ], colWidths=[doc.width * 0.7, doc.width * 0.3])
            
            edu_header.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            
            story.append(edu_header)
    
    # ===== KEY ACHIEVEMENTS =====
    if achievements:
        story.append(Paragraph("KEY ACHIEVEMENTS", styles['ModernSectionHeader']))
        
        for achievement in achievements:
            if isinstance(achievement, str):
                story.append(Paragraph(f"★ {achievement}", styles['ModernBulletPoint']))
            else:
                title = achievement.get('title', achievement.get('name', ''))
                date_str = format_date(achievement.get('date', '')) if achievement.get('date') else ''
                category = achievement.get('category', '')
                
                if date_str and category:
                    achievement_header = f"★ {title} <font size='{8 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{category} - {date_str}]</font>"
                elif date_str:
                    achievement_header = f"★ {title} <font size='{8 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{date_str}]</font>"
                elif category:
                    achievement_header = f"★ {title} <font size='{8 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{category}]</font>"
                else:
                    achievement_header = f"★ {title}"
                
                story.append(Paragraph(achievement_header, styles['ModernBulletPoint']))
                
                if 'description' in achievement and achievement['description']:
                    if isinstance(achievement['description'], list):
                        for desc_item in achievement['description']:
                            # Sub-bullets with additional indentation
                            sub_bullet_style = ParagraphStyle(
                                name="SubBulletStyle",
                                parent=styles['ModernBulletPoint'],
                                leftIndent=BULLET_INDENT + 12,  # Additional indentation for sub-bullets
                                rightIndent=STANDARD_RIGHT_PADDING
                            )
                            story.append(Paragraph(f"• {desc_item}", sub_bullet_style))
                    else:
                        sub_bullet_style = ParagraphStyle(
                            name="SubBulletStyle",
                            parent=styles['ModernBulletPoint'],
                            leftIndent=BULLET_INDENT + 12,
                            rightIndent=STANDARD_RIGHT_PADDING
                        )
                        story.append(Paragraph(f"• {achievement['description']}", sub_bullet_style))
        
        story.append(Spacer(1, 8))
    
    # ===== ACADEMIC PROJECTS =====
    if academic_projects:
        story.append(Paragraph("PROJECTS", styles['ModernSectionHeader']))
        
        for project in academic_projects:
            project_date = format_date(project['date'])
            
            project_header = Table([
                [
                    Paragraph(project['title'], styles['ModernCompanyName']),
                    Paragraph(project_date, styles['ModernDateStyle'])
                ],
                [
                    Paragraph(f"Technologies: {project['technologies']}", styles['ModernJobTitle']),
                    ""
                ]
            ], colWidths=[doc.width * 0.7, doc.width * 0.3])
            
            project_header.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            
            story.append(project_header)
            add_modern_bullet_list(project['description'])
            
            if 'links' in project and project['links']:
                links_text = " | ".join([f"{name}: {url}" for name, url in project['links'].items()])
                story.append(Paragraph(f"Links: {links_text}", styles['ModernJobTitle']))
            
            story.append(Spacer(1, 12))
    
    # ===== CERTIFICATIONS =====
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", styles['ModernSectionHeader']))
        
        for cert in certifications:
            cert_date = format_date(cert['date'])
            
            cert_header = Table([
                [
                    Paragraph(cert['name'], styles['ModernCompanyName']),
                    Paragraph(cert_date, styles['ModernDateStyle'])
                ],
                [
                    Paragraph(f"Issued by: {cert['issuer']}", styles['ModernJobTitle']),
                    ""
                ]
            ], colWidths=[doc.width * 0.7, doc.width * 0.3])
            
            cert_header.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            
            story.append(cert_header)
            
            if 'credential_id' in cert:
                story.append(Paragraph(f"Credential ID: {cert['credential_id']}", styles['ModernJobTitle']))
            
            if 'description' in cert:
                add_modern_bullet_list(cert['description'])
            
            story.append(Spacer(1, 12))
    
    # ===== HONORS & AWARDS =====
    if honors_awards:
        story.append(Paragraph("HONORS & AWARDS", styles['ModernSectionHeader']))
        
        for award in honors_awards:
            if isinstance(award, str):
                story.append(Paragraph(f"🏆 {award}", styles['ModernBulletPoint']))
            else:
                title = award.get('title', award.get('name', ''))
                date_str = format_date(award.get('date', '')) if award.get('date') else ''
                organization = award.get('organization', award.get('issuer', ''))
                
                award_header = Table([
                    [
                        Paragraph(f"🏆 {title}", styles['ModernCompanyName']),
                        Paragraph(date_str, styles['ModernDateStyle'])
                    ],
                ], colWidths=[doc.width * 0.7, doc.width * 0.3])
                
                award_header.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]))
                
                story.append(award_header)
                
                if organization:
                    story.append(Paragraph(f"Awarded by: {organization}", styles['ModernJobTitle']))
                
                if 'description' in award and award['description']:
                    if isinstance(award['description'], list):
                        for desc_item in award['description']:
                            story.append(Paragraph(f"▸ {desc_item}", styles['ModernBulletPoint']))
                    else:
                        story.append(Paragraph(f"▸ {award['description']}", styles['ModernBulletPoint']))
                
                if 'value' in award and award['value']:
                    story.append(Paragraph(f"Value: {award['value']}", styles['ModernJobTitle']))
        
        story.append(Spacer(1, 8))
    
    # ===== PUBLICATIONS =====
    if publications:
        story.append(Paragraph("PUBLICATIONS", styles['ModernSectionHeader']))
        
        for pub in publications:
            pub_date = format_date(pub['date'])
            
            pub_header = Table([
                [
                    Paragraph(pub['title'], styles['ModernCompanyName']),
                    Paragraph(pub_date, styles['ModernDateStyle'])
                ],
                [
                    Paragraph(f"Authors: {pub['authors']}", styles['ModernJobTitle']),
                    ""
                ],
                [
                    Paragraph(f"Published in: {pub['journal']}", styles['ModernJobTitle']),
                    ""
                ]
            ], colWidths=[doc.width * 0.7, doc.width * 0.3])
            
            pub_header.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            
            story.append(pub_header)
            
            if 'url' in pub:
                story.append(Paragraph(f"DOI/URL: {pub['url']}", styles['ModernJobTitle']))
            
            if 'description' in pub:
                add_modern_bullet_list(pub['description'])
            
            story.append(Spacer(1, 12))
    
    # ===== CORE COMPETENCIES (SKILLS) =====
    if skills:
        story.append(Paragraph("CORE COMPETENCIES", styles['ModernSectionHeader']))
        
        # Group skills into categories or display in a clean grid with consistent alignment
        skills_per_row = 3 if page_size.lower() != "a4" else 2
        skills_table_data = []
        row = []
        
        for i, skill in enumerate(skills):
            row.append(Paragraph(f"• {skill}", styles['ModernSkillText']))
            if (i + 1) % skills_per_row == 0:
                skills_table_data.append(row)
                row = []
        
        if row:
            while len(row) < skills_per_row:
                row.append("")
            skills_table_data.append(row)
        
        column_width = doc.width / skills_per_row
        skills_table = Table(skills_table_data, colWidths=[column_width] * skills_per_row)
        skills_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 8))
    
    # ===== LANGUAGES =====
    if languages:
        story.append(Paragraph("LANGUAGES", styles['ModernSectionHeader']))
        languages_text = " • ".join(languages)
        story.append(Paragraph(languages_text, styles['ModernBodyText']))
    
    # ===== INTERESTS =====
    if hobbies:
        story.append(Paragraph("INTERESTS", styles['ModernSectionHeader']))
        hobbies_text = " • ".join(hobbies)
        story.append(Paragraph(hobbies_text, styles['ModernBodyText']))
    
    # ===== REFERENCES =====
    if referees:
        story.append(Paragraph("REFERENCES", styles['ModernSectionHeader']))
        
        for ref in referees:
            ref_data = [
                [
                    Paragraph(ref['name'], styles['ModernCompanyName']),
                    Paragraph(ref['position'], styles["ModernJobTitle"])
                ],
                [
                    Paragraph(ref['organization'], styles["ModernJobTitle"]),
                    Paragraph(f"Phone: {ref['phone']}", styles['ModernJobTitle'])
                ],
                [
                    Paragraph(f"Email: {ref['email']}", styles['ModernSkillText']),
                    Paragraph(f"Relationship: {ref.get('relationship', 'N/A')}", styles["ModernSkillText"])
                ]
            ]
            
            ref_table = Table(ref_data, colWidths=[doc.width/2, doc.width/2])
            ref_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            
            story.append(ref_table)
            story.append(Spacer(1, 15))
    
    doc.build(story)
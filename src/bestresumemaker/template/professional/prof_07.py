from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.units import inch, mm
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect

def professional7(personal_info, professional_summary, work_experience, education, skills, 
                          academic_projects=None, certifications=None, publications=None, 
                          hobbies=None, languages=None, referees=None, achievements=None,
                          honors_awards=None, output_file="modern_resume.pdf", page_size="letter"):
    
    # Set page size based on user preference
    if page_size.lower() == "a4":
        page_dimensions = A4
        margin_left_right = 10 * mm
        margin_top_bottom = 25 * mm
    else:
        page_dimensions = letter
        margin_left_right = 0.50 * inch
        margin_top_bottom = 0.75 * inch
    
    doc = SimpleDocTemplate(output_file, pagesize=page_dimensions,
                          rightMargin=margin_left_right, 
                          leftMargin=margin_left_right,
                          topMargin=margin_top_bottom, 
                          bottomMargin=margin_top_bottom)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Modern color scheme - Professional blues and grays
    primary_color = colors.HexColor("#1a365d")      # Deep blue
    secondary_color = colors.HexColor("#2d3748")    # Dark gray
    accent_color = colors.HexColor("#3182ce")       # Bright blue
    light_gray = colors.HexColor("#f7fafc")         # Very light gray
    light_accent = colors.HexColor("#e2e8f0")       # Light accent for dividers
    medium_gray = colors.HexColor("#718096")        # Medium gray
    
    font_size_adjustment = 0.9 if page_size.lower() == "a4" else 1

    # Define modern custom styles
    styles.add(ParagraphStyle(
        name="ModernNameTitle",
        fontSize=32 * font_size_adjustment,
        leading=36 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        letterSpacing=1
    ))

    styles.add(ParagraphStyle(
        name="ModernJobTitle",
        fontSize=18 * font_size_adjustment,
        leading=22 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=20,
        fontName='Helvetica',
        textColor=accent_color,
        letterSpacing=0.5
    ))

    styles.add(ParagraphStyle(
        name="ModernContact",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=20,
        fontName='Helvetica',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="ModernSectionHeader",
        fontSize=14 * font_size_adjustment,
        leading=18 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        borderPadding=(0, 0, 8, 0),
        keepWithNext=1
    ))

    styles.add(ParagraphStyle(
        name="ModernCompanyName",
        fontSize=13 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="ModernJobPosition",
        fontSize=12 * font_size_adjustment,
        leading=15 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica',
        textColor=accent_color
    ))

    styles.add(ParagraphStyle(
        name="ModernDateRange",
        fontSize=10 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_RIGHT,
        spaceAfter=6,
        fontName='Helvetica-Oblique',
        textColor=medium_gray
    ))

    styles.add(ParagraphStyle(
        name="ModernBodyText",
        fontSize=10 * font_size_adjustment,
        leading=15 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        textColor=secondary_color,
        firstLineIndent=0
    ))

    styles.add(ParagraphStyle(
        name="ModernBulletPoint",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=3,
        fontName='Helvetica',
        textColor=secondary_color,
        leftIndent=12,
        bulletIndent=0
    ))

    styles.add(ParagraphStyle(
        name="ModernSkillCategory",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        textColor=accent_color
    ))

    styles.add(ParagraphStyle(
        name="ModernSkillItems",
        fontSize=10 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=8,
        fontName='Helvetica',
        textColor=secondary_color,
        leftIndent=8
    ))

    # Additional styles for references section
    styles.add(ParagraphStyle(
        name="ModernReferenceDetail",
        fontSize=10 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica',
        textColor=secondary_color
    ))

    def format_date(date_obj):
        """Helper function to format dates consistently"""
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%b %Y")
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)

    def add_section_divider():
        """Add a subtle section divider"""
        divider = HRFlowable(width="100%", thickness=0.5, lineCap='round', 
                           color=light_gray, spaceBefore=5, spaceAfter=5)
        story.append(divider)

    def add_section_separator():
        """Add a section separator similar to executive style"""
        separator = HRFlowable(width="100%", thickness=0.5, lineCap='round', 
                             color=light_accent, spaceBefore=5, spaceAfter=10)
        story.append(separator)

    def add_modern_bullet_list(items, style=None):
        """Helper function to add modern styled bullet lists"""
        if style is None:
            style = styles['ModernBulletPoint']
        
        if isinstance(items, str):
            items = items.split('\n')
        
        for item in items:
            if item.strip():
                clean_item = item.strip().strip('"').strip("'")
                story.append(Paragraph(f"▸ {clean_item}", style))

    # ===== HEADER SECTION =====
    # Create header table for better layout control
    header_data = [
        [
            [
                Paragraph(personal_info['name'].upper(), styles['ModernNameTitle']),
                Paragraph(personal_info['title'], styles['ModernJobTitle'])
            ],
            [
                # Right-aligned contact info
            ]
        ]
    ]
    
    # Build contact information
    contact_info = []
    contact_fields = [
        ('email', '✉'),
        ('phone', '☎'),
        ('location', '📍'),
        ('linkedin', '💼'),
        ('github', '🔗'),
        ('website', '🌐')
    ]
    
    for field, icon in contact_fields:
        if field in personal_info and personal_info[field]:
            contact_info.append(f"{icon} {personal_info[field]}")
    
    # Add contact info to header
    contact_text = "<br/>".join(contact_info)
    if contact_text:
        header_data[0][1] = Paragraph(contact_text, styles['ModernContact'])
    
    header_table = Table(header_data, colWidths=[doc.width*0.6, doc.width*0.4])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    add_section_divider()

    # ===== PROFESSIONAL SUMMARY =====
    story.append(Paragraph("PROFESSIONAL SUMMARY", styles['ModernSectionHeader']))
    story.append(Paragraph(professional_summary, styles["ModernBodyText"]))

    # ===== PROFESSIONAL EXPERIENCE =====
    if work_experience:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['ModernSectionHeader']))
        
        for i, job in enumerate(work_experience):
            start_date = format_date(job['start_date'])
            end_date = format_date(job['end_date'])
            date_range = f"{start_date} - {end_date}"
            
            # Create job header table
            job_header_data = [
                [
                    [
                        Paragraph(job['company'], styles['ModernCompanyName']),
                        Paragraph(job['position'], styles['ModernJobPosition'])
                    ],
                    Paragraph(date_range, styles['ModernDateRange'])
                ]
            ]
            
            job_header_table = Table(job_header_data, colWidths=[doc.width*0.7, doc.width*0.3])
            job_header_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            
            story.append(job_header_table)
            add_modern_bullet_list(job['description'])
            
            if i < len(work_experience) - 1:  # Add space between jobs except last
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
            
            # Education header table
            edu_header_data = [
                [
                    [
                        Paragraph(edu['institution'], styles['ModernCompanyName']),
                        Paragraph(edu['degree'], styles['ModernJobPosition'])
                    ],
                    Paragraph(date_range, styles['ModernDateRange'])
                ]
            ]
            
            edu_header_table = Table(edu_header_data, colWidths=[doc.width*0.7, doc.width*0.3])
            edu_header_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            
            story.append(edu_header_table)

    # ===== KEY ACHIEVEMENTS =====
    if achievements:
        story.append(Paragraph("KEY ACHIEVEMENTS", styles['ModernSectionHeader']))
        
        for achievement in achievements:
            if isinstance(achievement, str):
                story.append(Paragraph(f"▸ {achievement}", styles['ModernBulletPoint']))
            else:
                title = achievement.get('title', achievement.get('name', ''))
                date_str = format_date(achievement.get('date', '')) if achievement.get('date') else ''
                category = achievement.get('category', '')
                
                # Format achievement with metadata
                metadata_parts = []
                if category:
                    metadata_parts.append(category)
                if date_str:
                    metadata_parts.append(date_str)
                
                if metadata_parts:
                    achievement_text = f"{title} <font color='#{medium_gray.hexval()}'>({' | '.join(metadata_parts)})</font>"
                else:
                    achievement_text = title
                
                story.append(Paragraph(f"▸ {achievement_text}", styles['ModernBulletPoint']))
                
                if 'description' in achievement and achievement['description']:
                    if isinstance(achievement['description'], list):
                        for desc_item in achievement['description']:
                            story.append(Paragraph(f"   • {desc_item}", styles['ModernBulletPoint']))
                    else:
                        story.append(Paragraph(f"   • {achievement['description']}", styles['ModernBulletPoint']))

    # ===== ACADEMIC PROJECTS =====
    if academic_projects:
        story.append(Paragraph("PROJECTS", styles['ModernSectionHeader']))
        
        for project in academic_projects:
            project_date = format_date(project['date'])
            
            # Project header
            project_header_data = [
                [
                    [
                        Paragraph(project['title'], styles['ModernCompanyName']),
                        Paragraph(f"Technologies: {project['technologies']}", styles['ModernJobPosition'])
                    ],
                    Paragraph(project_date, styles['ModernDateRange'])
                ]
            ]
            
            project_header_table = Table(project_header_data, colWidths=[doc.width*0.7, doc.width*0.3])
            project_header_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            
            story.append(project_header_table)
            add_modern_bullet_list(project['description'])
            
            # Add project links
            if 'links' in project and project['links']:
                links_text = " | ".join([f"{name}: {url}" for name, url in project['links'].items()])
                story.append(Paragraph(f"🔗 {links_text}", styles['ModernDateRange']))
            
            story.append(Spacer(1, 8))

    # ===== CERTIFICATIONS =====
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", styles['ModernSectionHeader']))
        
        for cert in certifications:
            cert_date = format_date(cert['date'])
            
            cert_header_data = [
                [
                    [
                        Paragraph(cert['name'], styles['ModernCompanyName']),
                        Paragraph(f"Issued by: {cert['issuer']}", styles['ModernJobPosition'])
                    ],
                    Paragraph(cert_date, styles['ModernDateRange'])
                ]
            ]
            
            cert_header_table = Table(cert_header_data, colWidths=[doc.width*0.7, doc.width*0.3])
            cert_header_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            
            story.append(cert_header_table)
            
            if 'credential_id' in cert:
                story.append(Paragraph(f"ID: {cert['credential_id']}", styles['ModernDateRange']))
            
            if 'description' in cert:
                add_modern_bullet_list(cert['description'])
            
            story.append(Spacer(1, 8))

    # ===== PUBLICATIONS =====
    if publications:
        story.append(Paragraph("PUBLICATIONS", styles['ModernSectionHeader']))
        
        for pub in publications:
            pub_date = format_date(pub['date'])
            
            story.append(Paragraph(f"📄 {pub['title']}", styles['ModernCompanyName']))
            story.append(Paragraph(f"Authors: {pub['authors']} | {pub['journal']} | {pub_date}", styles['ModernJobPosition']))
            
            if 'url' in pub:
                story.append(Paragraph(f"🔗 {pub['url']}", styles['ModernDateRange']))
            
            if 'description' in pub:
                add_modern_bullet_list(pub['description'])
            
            story.append(Spacer(1, 8))

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
                
                award_text = f"🏆 {title}"
                if date_str:
                    award_text += f" <font color='#{medium_gray.hexval()}'>({date_str})</font>"
                
                story.append(Paragraph(award_text, styles['ModernBulletPoint']))
                
                if organization:
                    story.append(Paragraph(f"   Awarded by: {organization}", styles['ModernBulletPoint']))
                
                if 'description' in award and award['description']:
                    if isinstance(award['description'], list):
                        for desc_item in award['description']:
                            story.append(Paragraph(f"   • {desc_item}", styles['ModernBulletPoint']))
                    else:
                        story.append(Paragraph(f"   • {award['description']}", styles['ModernBulletPoint']))

    # ===== TECHNICAL SKILLS =====
    if skills:
        story.append(Paragraph("TECHNICAL SKILLS", styles['ModernSectionHeader']))
        
        # Group skills if they contain categories (format: "Category: skill1, skill2")
        categorized_skills = {}
        uncategorized_skills = []
        
        for skill in skills:
            if ':' in skill and not skill.startswith('http'):
                category, skill_items = skill.split(':', 1)
                categorized_skills[category.strip()] = [s.strip() for s in skill_items.split(',')]
            else:
                uncategorized_skills.append(skill)
        
        # Display categorized skills
        for category, skill_list in categorized_skills.items():
            story.append(Paragraph(f"{category.upper()}", styles['ModernSkillCategory']))
            skills_text = " • ".join(skill_list)
            story.append(Paragraph(skills_text, styles['ModernSkillItems']))
        
        # Display uncategorized skills
        if uncategorized_skills:
            if categorized_skills:  # If we have categories, label these as general
                story.append(Paragraph("GENERAL", styles['ModernSkillCategory']))
            skills_text = " • ".join(uncategorized_skills)
            story.append(Paragraph(skills_text, styles['ModernSkillItems']))

    # ===== LANGUAGES =====
    if languages:
        story.append(Paragraph("LANGUAGES", styles['ModernSectionHeader']))
        languages_text = " • ".join(languages)
        story.append(Paragraph(f"🌐 {languages_text}", styles['ModernBodyText']))

    # ===== INTERESTS =====
    if hobbies:
        story.append(Paragraph("INTERESTS", styles['ModernSectionHeader']))
        hobbies_text = " • ".join(hobbies)
        story.append(Paragraph(f"🎯 {hobbies_text}", styles['ModernBodyText']))

    # ===== OPTIMIZED REFERENCES SECTION =====
    if referees:
        story.append(Paragraph("REFERENCES", styles['ModernSectionHeader']))
        add_section_separator()
        
        for ref in referees:
            ref_data = [
                [
                    Paragraph(f"<b>{ref['name']}</b>", styles['ModernCompanyName']),
                    Paragraph(f"<b>{ref['position']}</b>", styles["ModernJobPosition"])
                ],
                [
                    Paragraph(ref['organization'], styles["ModernJobPosition"]),
                    Paragraph(f"Phone: {ref['phone']}", styles['ModernJobPosition'])
                ],
                [
                    Paragraph(f"Email: {ref['email']}", styles['ModernReferenceDetail']),
                    Paragraph(f"Relationship: {ref.get('relationship', 'N/A')}", styles["ModernReferenceDetail"])
                ]
            ]
            
            ref_table = Table(ref_data, colWidths=[doc.width/2, doc.width/2])
            ref_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LINEBELOW', (0,0), (-1,0), 0.5, light_accent),
            ]))
            
            story.append(ref_table)
            story.append(Spacer(1, 16))

    # Build the PDF
    doc.build(story)

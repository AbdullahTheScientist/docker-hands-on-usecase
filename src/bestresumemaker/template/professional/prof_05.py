def professional5(personal_info, professional_summary, work_experience, education, skills, 
                                academic_projects=None, certifications=None, publications=None, 
                                hobbies=None, languages=None, referees=None, achievements=None,
                                honors_awards=None, output_file="professional_resume.pdf", page_size="letter"):
    
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
    from reportlab.lib import colors
    from datetime import datetime
    from reportlab.lib.units import inch, mm
    from reportlab.platypus.flowables import Flowable
    
    # Set page size based on user preference
    if page_size.lower() == "a4":
        page_dimensions = A4
        margin_left_right = 20 * mm
        margin_top_bottom = 20 * mm
    else:
        page_dimensions = letter
        margin_left_right = 0.75 * inch
        margin_top_bottom = 0.75 * inch
    
    doc = SimpleDocTemplate(output_file, pagesize=page_dimensions,
                          rightMargin=margin_left_right, 
                          leftMargin=margin_left_right,
                          topMargin=margin_top_bottom, 
                          bottomMargin=margin_top_bottom)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Professional B&W color scheme
    black_color = colors.HexColor("#000000")           # Pure black
    dark_grey = colors.HexColor("#333333")             # Dark grey for headers
    medium_grey = colors.HexColor("#666666")           # Medium grey for subtitles
    light_grey = colors.HexColor("#999999")            # Light grey for dates/secondary info
    very_light_grey = colors.HexColor("#F5F5F5")       # Very light grey for backgrounds
    border_grey = colors.HexColor("#CCCCCC")           # Light grey for borders
    
    font_size_adjustment = 0.9 if page_size.lower() == "a4" else 1
    
    # Professional custom styles
    styles.add(ParagraphStyle(
        name="ProfessionalName",
        fontSize=28 * font_size_adjustment,
        leading=32 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        textColor=black_color,
        letterSpacing=1.5
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalTitle",
        fontSize=14 * font_size_adjustment,
        leading=18 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica',
        textColor=dark_grey,
        letterSpacing=0.5
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalContact",
        fontSize=10 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=24,
        fontName='Helvetica',
        textColor=medium_grey
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalSectionHeader",
        fontSize=12 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceBefore=18,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        textColor=black_color,
        borderColor=black_color,
        borderWidth=1,
        borderPadding=(0, 0, 2, 0),
        leftIndent=0
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalCompany",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=black_color
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalPosition",
        fontSize=10 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Oblique',
        textColor=dark_grey
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalDate",
        fontSize=9 * font_size_adjustment,
        leading=11 * font_size_adjustment,
        alignment=TA_RIGHT,
        spaceAfter=6,
        fontName='Helvetica',
        textColor=light_grey
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalBody",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        textColor=dark_grey,
        firstLineIndent=0
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalBullet",
        fontSize=9 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=3,
        fontName='Helvetica',
        leftIndent=15,
        bulletIndent=5,
        textColor=dark_grey
    ))

    styles.add(ParagraphStyle(
        name="ProfessionalSkill",
        fontSize=9 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=3,
        fontName='Helvetica',
        textColor=dark_grey
    ))

    def format_date(date_obj):
        """Helper function to format dates consistently"""
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%b %Y")
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)
    
    def add_professional_bullet_list(items, style=None):
        """Helper function to add professional bullet lists"""
        if style is None:
            style = styles['ProfessionalBullet']
        
        if isinstance(items, str):
            items = items.split('\n')
        
        for item in items:
            if item.strip():
                clean_item = item.strip().strip('"').strip("'")
                story.append(Paragraph(f"• {clean_item}", style))
    
    def add_section_line():
        """Add a professional section line"""
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', 
                              color=border_grey, spaceBefore=0, spaceAfter=6, hAlign='LEFT'))
    
    # ===== HEADER SECTION =====
    story.append(Paragraph(personal_info['name'].upper(), styles['ProfessionalName']))
    story.append(Paragraph(personal_info['title'], styles['ProfessionalTitle']))
    
    # Contact information in a professional layout
    contact_parts = []
    for field in ['email', 'phone', 'location']:
        if field in personal_info and personal_info[field]:
            contact_parts.append(personal_info[field])
    
    web_parts = []
    for field in ['linkedin', 'github', 'website']:
        if field in personal_info and personal_info[field]:
            web_parts.append(personal_info[field])
    
    all_contact = contact_parts + web_parts
    if all_contact:
        contact_text = " | ".join(all_contact)
        story.append(Paragraph(contact_text, styles['ProfessionalContact']))
    
    # Main content separator
    story.append(HRFlowable(width="100%", thickness=1, lineCap='round', 
                          color=black_color, spaceBefore=0, spaceAfter=20, hAlign='CENTER'))
    
    # ===== PROFESSIONAL SUMMARY =====
    story.append(Paragraph("PROFESSIONAL SUMMARY", styles['ProfessionalSectionHeader']))
    add_section_line()
    story.append(Paragraph(professional_summary, styles['ProfessionalBody']))
    
    # ===== PROFESSIONAL EXPERIENCE =====
    if work_experience:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for i, job in enumerate(work_experience):
            start_date = format_date(job['start_date'])
            end_date = format_date(job['end_date'])
            date_range = f"{start_date} – {end_date}"
            
            # Create experience header
            exp_table = Table([
                [
                    Paragraph(job['company'], styles['ProfessionalCompany']),
                    Paragraph(date_range, styles['ProfessionalDate'])
                ],
                [
                    Paragraph(job['position'], styles['ProfessionalPosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.70, doc.width * 0.30])
            
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LINEBELOW', (0,0), (-1,0), 0.25, border_grey),
            ]))
            
            story.append(exp_table)
            add_professional_bullet_list(job['description'])
            
            if i < len(work_experience) - 1:
                story.append(Spacer(1, 14))
    
    # ===== EDUCATION =====
    if education:
        story.append(Paragraph("EDUCATION", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for edu in education:
            start_date = format_date(edu.get('start_date', ''))
            end_date = format_date(edu.get('graduation_date', edu.get('end_date', '')))
            
            if start_date and end_date:
                date_range = f"{start_date} – {end_date}"
            elif end_date:
                date_range = end_date
            elif start_date:
                date_range = f"{start_date} – Present"
            else:
                date_range = ""
            
            edu_table = Table([
                [
                    Paragraph(edu['institution'], styles['ProfessionalCompany']),
                    Paragraph(date_range, styles['ProfessionalDate'])
                ],
                [
                    Paragraph(edu['degree'], styles['ProfessionalPosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.70, doc.width * 0.30])
            
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ]))
            
            story.append(edu_table)
    
    # ===== KEY ACHIEVEMENTS =====
    if achievements:
        story.append(Paragraph("KEY ACHIEVEMENTS", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for achievement in achievements:
            if isinstance(achievement, str):
                story.append(Paragraph(f"▪ {achievement}", styles['ProfessionalBullet']))
            else:
                title = achievement.get('title', achievement.get('name', ''))
                date_str = format_date(achievement.get('date', '')) if achievement.get('date') else ''
                category = achievement.get('category', '')
                
                if date_str and category:
                    achievement_header = f"▪ <b>{title}</b> <i>({category} - {date_str})</i>"
                elif date_str:
                    achievement_header = f"▪ <b>{title}</b> <i>({date_str})</i>"
                elif category:
                    achievement_header = f"▪ <b>{title}</b> <i>({category})</i>"
                else:
                    achievement_header = f"▪ <b>{title}</b>"
                
                story.append(Paragraph(achievement_header, styles['ProfessionalBullet']))
                
                if 'description' in achievement and achievement['description']:
                    if isinstance(achievement['description'], list):
                        for desc_item in achievement['description']:
                            sub_style = ParagraphStyle(
                                name="SubAchievement",
                                parent=styles['ProfessionalBullet'],
                                leftIndent=30,
                                fontSize=8 * font_size_adjustment,
                                textColor=medium_grey
                            )
                            story.append(Paragraph(f"◦ {desc_item}", sub_style))
                    else:
                        sub_style = ParagraphStyle(
                            name="SubAchievement",
                            parent=styles['ProfessionalBullet'],
                            leftIndent=30,
                            fontSize=8 * font_size_adjustment,
                            textColor=medium_grey
                        )
                        story.append(Paragraph(f"◦ {achievement['description']}", sub_style))
        
        story.append(Spacer(1, 6))
    
    # ===== PROJECTS =====
    if academic_projects:
        story.append(Paragraph("PROJECTS", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for project in academic_projects:
            project_date = format_date(project['date'])
            
            project_table = Table([
                [
                    Paragraph(f"<b>{project['title']}</b>", styles['ProfessionalCompany']),
                    Paragraph(project_date, styles['ProfessionalDate'])
                ],
                [
                    Paragraph(f"<i>Technologies:</i> {project['technologies']}", styles['ProfessionalPosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.70, doc.width * 0.30])
            
            project_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            
            story.append(project_table)
            add_professional_bullet_list(project['description'])
            
            if 'links' in project and project['links']:
                links_text = " | ".join([f"<b>{name}:</b> {url}" for name, url in project['links'].items()])
                story.append(Paragraph(links_text, styles['ProfessionalPosition']))
            
            story.append(Spacer(1, 10))
    
    # ===== CERTIFICATIONS =====
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for cert in certifications:
            cert_date = format_date(cert['date'])
            
            cert_table = Table([
                [
                    Paragraph(f"<b>{cert['name']}</b>", styles['ProfessionalCompany']),
                    Paragraph(cert_date, styles['ProfessionalDate'])
                ],
                [
                    Paragraph(f"<i>Issued by:</i> {cert['issuer']}", styles['ProfessionalPosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.70, doc.width * 0.30])
            
            cert_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            
            story.append(cert_table)
            
            if 'credential_id' in cert:
                story.append(Paragraph(f"<i>Credential ID:</i> {cert['credential_id']}", styles['ProfessionalPosition']))
            
            if 'description' in cert:
                add_professional_bullet_list(cert['description'])
            
            story.append(Spacer(1, 10))
    
    # ===== HONORS & AWARDS =====
    if honors_awards:
        story.append(Paragraph("HONORS & AWARDS", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for award in honors_awards:
            if isinstance(award, str):
                story.append(Paragraph(f"▪ {award}", styles['ProfessionalBullet']))
            else:
                title = award.get('title', award.get('name', ''))
                date_str = format_date(award.get('date', '')) if award.get('date') else ''
                organization = award.get('organization', award.get('issuer', ''))
                
                award_table = Table([
                    [
                        Paragraph(f"▪ <b>{title}</b>", styles['ProfessionalCompany']),
                        Paragraph(date_str, styles['ProfessionalDate'])
                    ],
                ], colWidths=[doc.width * 0.70, doc.width * 0.30])
                
                award_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ]))
                
                story.append(award_table)
                
                if organization:
                    story.append(Paragraph(f"<i>Awarded by:</i> {organization}", styles['ProfessionalPosition']))
                
                if 'description' in award and award['description']:
                    if isinstance(award['description'], list):
                        for desc_item in award['description']:
                            story.append(Paragraph(f"• {desc_item}", styles['ProfessionalBullet']))
                    else:
                        story.append(Paragraph(f"• {award['description']}", styles['ProfessionalBullet']))
                
                if 'value' in award and award['value']:
                    story.append(Paragraph(f"<i>Value:</i> {award['value']}", styles['ProfessionalPosition']))
                
                story.append(Spacer(1, 6))
    
    # ===== PUBLICATIONS =====
    if publications:
        story.append(Paragraph("PUBLICATIONS", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for pub in publications:
            pub_date = format_date(pub['date'])
            
            pub_table = Table([
                [
                    Paragraph(f"<b>{pub['title']}</b>", styles['ProfessionalCompany']),
                    Paragraph(pub_date, styles['ProfessionalDate'])
                ],
                [
                    Paragraph(f"<i>Authors:</i> {pub['authors']}", styles['ProfessionalPosition']),
                    ""
                ],
                [
                    Paragraph(f"<i>Published in:</i> {pub['journal']}", styles['ProfessionalPosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.70, doc.width * 0.30])
            
            pub_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            
            story.append(pub_table)
            
            if 'url' in pub:
                story.append(Paragraph(f"<i>DOI/URL:</i> {pub['url']}", styles['ProfessionalPosition']))
            
            if 'description' in pub:
                add_professional_bullet_list(pub['description'])
            
            story.append(Spacer(1, 10))
    
    # ===== TECHNICAL SKILLS =====
    if skills:
        story.append(Paragraph("TECHNICAL SKILLS", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        # Create a clean skills layout
        skills_per_row = 3 if page_size.lower() == "a4" else 4
        skills_table_data = []
        row = []
        
        for i, skill in enumerate(skills):
            row.append(Paragraph(f"• {skill}", styles['ProfessionalSkill']))
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
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 6))
    
    # ===== LANGUAGES =====
    if languages:
        story.append(Paragraph("LANGUAGES", styles['ProfessionalSectionHeader']))
        add_section_line()
        languages_text = " • ".join(languages)
        story.append(Paragraph(languages_text, styles['ProfessionalBody']))
    
    # ===== INTERESTS =====
    if hobbies:
        story.append(Paragraph("INTERESTS", styles['ProfessionalSectionHeader']))
        add_section_line()
        hobbies_text = " • ".join(hobbies)
        story.append(Paragraph(hobbies_text, styles['ProfessionalBody']))
    
    # ===== REFERENCES =====
    if referees:
        story.append(Paragraph("REFERENCES", styles['ProfessionalSectionHeader']))
        add_section_line()
        
        for ref in referees:
            ref_data = [
                [
                    Paragraph(f"<b>{ref['name']}</b>", styles['ProfessionalCompany']),
                    Paragraph(f"<b>{ref['position']}</b>", styles["ProfessionalPosition"])
                ],
                [
                    Paragraph(ref['organization'], styles["ProfessionalPosition"]),
                    Paragraph(f"Phone: {ref['phone']}", styles['ProfessionalPosition'])
                ],
                [
                    Paragraph(f"Email: {ref['email']}", styles['ProfessionalSkill']),
                    Paragraph(f"Relationship: {ref.get('relationship', 'N/A')}", styles["ProfessionalSkill"])
                ]
            ]
            
            ref_table = Table(ref_data, colWidths=[doc.width/2, doc.width/2])
            ref_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LINEBELOW', (0,0), (-1,0), 0.25, border_grey),
            ]))
            
            story.append(ref_table)
            story.append(Spacer(1, 12))
    
    doc.build(story)

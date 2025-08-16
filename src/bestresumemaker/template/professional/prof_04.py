def professional4(personal_info, professional_summary, work_experience, education, skills, 
                          academic_projects=None, certifications=None, publications=None, 
                          hobbies=None, languages=None, referees=None, achievements=None,
                          honors_awards=None, output_file="executive_resume.pdf", page_size="letter"):
    
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
        margin_left_right = 15 * mm
        margin_top_bottom = 18 * mm
    else:
        page_dimensions = letter
        margin_left_right = 0.5 * inch
        margin_top_bottom = 0.5 * inch
    
    doc = SimpleDocTemplate(output_file, pagesize=page_dimensions,
                          rightMargin=margin_left_right, 
                          leftMargin=margin_left_right,
                          topMargin=margin_top_bottom, 
                          bottomMargin=margin_top_bottom)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Executive color scheme - Sophisticated navy and gold palette
    primary_color = colors.HexColor("#1B2951")      # Deep navy
    secondary_color = colors.HexColor("#2C5282")    # Professional blue
    accent_color = colors.HexColor("#D69E2E")       # Gold accent
    text_color = colors.HexColor("#1A202C")         # Charcoal
    light_accent = colors.HexColor("#EDF2F7")       # Light gray
    border_color = colors.HexColor("#CBD5E0")       # Medium gray
    
    font_size_adjustment = 0.9 if page_size.lower() == "a4" else 1
    
    # Executive custom styles
    styles.add(ParagraphStyle(
        name="ExecutiveName",
        fontSize=36 * font_size_adjustment,
        leading=42 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        letterSpacing=2
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveTitle",
        fontSize=16 * font_size_adjustment,
        leading=20 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica',
        textColor=secondary_color,
        letterSpacing=0.8
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveContact",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica',
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveSectionHeader",
        fontSize=14 * font_size_adjustment,
        leading=18 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        borderColor=accent_color,
        borderWidth=0,
        borderPadding=(0, 0, 3, 0),
        leftIndent=0
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveCompany",
        fontSize=13 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=primary_color
    ))

    styles.add(ParagraphStyle(
        name="ExecutivePosition",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Oblique',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveDate",
        fontSize=10 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_RIGHT,
        spaceAfter=8,
        fontName='Helvetica',
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveBody",
        fontSize=10 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=14,
        fontName='Helvetica',
        textColor=text_color,
        firstLineIndent=0
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveBullet",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
        fontName='Helvetica',
        leftIndent=18,
        bulletIndent=6,
        textColor=text_color
    ))

    styles.add(ParagraphStyle(
        name="ExecutiveSkill",
        fontSize=10 * font_size_adjustment,
        leading=13 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName='Helvetica',
        textColor=text_color
    ))

    def format_date(date_obj):
        """Helper function to format dates consistently"""
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%B %Y")
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)
    
    def add_executive_bullet_list(items, style=None):
        """Helper function to add executive bullet lists"""
        if style is None:
            style = styles['ExecutiveBullet']
        
        if isinstance(items, str):
            items = items.split('\n')
        
        for item in items:
            if item.strip():
                clean_item = item.strip().strip('"').strip("'")
                story.append(Paragraph(f"• {clean_item}", style))
    
    def add_section_separator():
        """Add an elegant section separator"""
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="30%", thickness=1, lineCap='round', 
                              color=accent_color, spaceBefore=0, spaceAfter=8, hAlign='LEFT'))
    
    # ===== HEADER SECTION =====
    story.append(Paragraph(personal_info['name'].upper(), styles['ExecutiveName']))
    story.append(Paragraph(personal_info['title'], styles['ExecutiveTitle']))
    
    # Contact information in a single centered line
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
        contact_text = " • ".join(all_contact)
        story.append(Paragraph(contact_text, styles['ExecutiveContact']))
    
    # ===== EXECUTIVE SUMMARY =====
    story.append(Paragraph("EXECUTIVE SUMMARY", styles['ExecutiveSectionHeader']))
    add_section_separator()
    story.append(Paragraph(professional_summary, styles['ExecutiveBody']))
    
    # ===== PROFESSIONAL EXPERIENCE =====
    if work_experience:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for i, job in enumerate(work_experience):
            start_date = format_date(job['start_date'])
            end_date = format_date(job['end_date'])
            date_range = f"{start_date} – {end_date}"
            
            # Create experience header with border
            exp_table = Table([
                [
                    Paragraph(job['company'], styles['ExecutiveCompany']),
                    Paragraph(date_range, styles['ExecutiveDate'])
                ],
                [
                    Paragraph(job['position'], styles['ExecutivePosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.75, doc.width * 0.25])
            
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LINEBELOW', (0,0), (-1,0), 0.5, border_color),
            ]))
            
            story.append(exp_table)
            add_executive_bullet_list(job['description'])
            
            if i < len(work_experience) - 1:
                story.append(Spacer(1, 16))
    
    # ===== EDUCATION =====
    if education:
        story.append(Paragraph("EDUCATION", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
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
                    Paragraph(edu['institution'], styles['ExecutiveCompany']),
                    Paragraph(date_range, styles['ExecutiveDate'])
                ],
                [
                    Paragraph(edu['degree'], styles['ExecutivePosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.75, doc.width * 0.25])
            
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ]))
            
            story.append(edu_table)
    
    # ===== KEY ACHIEVEMENTS =====
    if achievements:
        story.append(Paragraph("KEY ACHIEVEMENTS", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for achievement in achievements:
            if isinstance(achievement, str):
                story.append(Paragraph(f"▶ {achievement}", styles['ExecutiveBullet']))
            else:
                title = achievement.get('title', achievement.get('name', ''))
                date_str = format_date(achievement.get('date', '')) if achievement.get('date') else ''
                category = achievement.get('category', '')
                
                if date_str and category:
                    achievement_header = f"▶ <b>{title}</b> <i>[{category} - {date_str}]</i>"
                elif date_str:
                    achievement_header = f"▶ <b>{title}</b> <i>[{date_str}]</i>"
                elif category:
                    achievement_header = f"▶ <b>{title}</b> <i>[{category}]</i>"
                else:
                    achievement_header = f"▶ <b>{title}</b>"
                
                story.append(Paragraph(achievement_header, styles['ExecutiveBullet']))
                
                if 'description' in achievement and achievement['description']:
                    if isinstance(achievement['description'], list):
                        for desc_item in achievement['description']:
                            sub_style = ParagraphStyle(
                                name="SubAchievement",
                                parent=styles['ExecutiveBullet'],
                                leftIndent=36,
                                fontSize=9 * font_size_adjustment
                            )
                            story.append(Paragraph(f"◦ {desc_item}", sub_style))
                    else:
                        sub_style = ParagraphStyle(
                            name="SubAchievement",
                            parent=styles['ExecutiveBullet'],
                            leftIndent=36,
                            fontSize=9 * font_size_adjustment
                        )
                        story.append(Paragraph(f"◦ {achievement['description']}", sub_style))
        
        story.append(Spacer(1, 8))
    
    # ===== ACADEMIC PROJECTS =====
    if academic_projects:
        story.append(Paragraph("PROJECTS", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for project in academic_projects:
            project_date = format_date(project['date'])
            
            project_table = Table([
                [
                    Paragraph(f"<b>{project['title']}</b>", styles['ExecutiveCompany']),
                    Paragraph(project_date, styles['ExecutiveDate'])
                ],
                [
                    Paragraph(f"<i>Technologies:</i> {project['technologies']}", styles['ExecutivePosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.75, doc.width * 0.25])
            
            project_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            
            story.append(project_table)
            add_executive_bullet_list(project['description'])
            
            if 'links' in project and project['links']:
                links_text = " | ".join([f"<b>{name}:</b> {url}" for name, url in project['links'].items()])
                story.append(Paragraph(links_text, styles['ExecutivePosition']))
            
            story.append(Spacer(1, 12))
    
    # ===== CERTIFICATIONS =====
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for cert in certifications:
            cert_date = format_date(cert['date'])
            
            cert_table = Table([
                [
                    Paragraph(f"<b>{cert['name']}</b>", styles['ExecutiveCompany']),
                    Paragraph(cert_date, styles['ExecutiveDate'])
                ],
                [
                    Paragraph(f"<i>Issued by:</i> {cert['issuer']}", styles['ExecutivePosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.75, doc.width * 0.25])
            
            cert_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            
            story.append(cert_table)
            
            if 'credential_id' in cert:
                story.append(Paragraph(f"<i>Credential ID:</i> {cert['credential_id']}", styles['ExecutivePosition']))
            
            if 'description' in cert:
                add_executive_bullet_list(cert['description'])
            
            story.append(Spacer(1, 12))
    
    # ===== HONORS & AWARDS =====
    if honors_awards:
        story.append(Paragraph("HONORS & AWARDS", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for award in honors_awards:
            if isinstance(award, str):
                story.append(Paragraph(f"🏅 {award}", styles['ExecutiveBullet']))
            else:
                title = award.get('title', award.get('name', ''))
                date_str = format_date(award.get('date', '')) if award.get('date') else ''
                organization = award.get('organization', award.get('issuer', ''))
                
                award_table = Table([
                    [
                        Paragraph(f"🏅 <b>{title}</b>", styles['ExecutiveCompany']),
                        Paragraph(date_str, styles['ExecutiveDate'])
                    ],
                ], colWidths=[doc.width * 0.75, doc.width * 0.25])
                
                award_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ]))
                
                story.append(award_table)
                
                if organization:
                    story.append(Paragraph(f"<i>Awarded by:</i> {organization}", styles['ExecutivePosition']))
                
                if 'description' in award and award['description']:
                    if isinstance(award['description'], list):
                        for desc_item in award['description']:
                            story.append(Paragraph(f"• {desc_item}", styles['ExecutiveBullet']))
                    else:
                        story.append(Paragraph(f"• {award['description']}", styles['ExecutiveBullet']))
                
                if 'value' in award and award['value']:
                    story.append(Paragraph(f"<i>Value:</i> {award['value']}", styles['ExecutivePosition']))
                
                story.append(Spacer(1, 8))
    
    # ===== PUBLICATIONS =====
    if publications:
        story.append(Paragraph("PUBLICATIONS", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for pub in publications:
            pub_date = format_date(pub['date'])
            
            pub_table = Table([
                [
                    Paragraph(f"<b>{pub['title']}</b>", styles['ExecutiveCompany']),
                    Paragraph(pub_date, styles['ExecutiveDate'])
                ],
                [
                    Paragraph(f"<i>Authors:</i> {pub['authors']}", styles['ExecutivePosition']),
                    ""
                ],
                [
                    Paragraph(f"<i>Published in:</i> {pub['journal']}", styles['ExecutivePosition']),
                    ""
                ]
            ], colWidths=[doc.width * 0.75, doc.width * 0.25])
            
            pub_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            
            story.append(pub_table)
            
            if 'url' in pub:
                story.append(Paragraph(f"<i>DOI/URL:</i> {pub['url']}", styles['ExecutivePosition']))
            
            if 'description' in pub:
                add_executive_bullet_list(pub['description'])
            
            story.append(Spacer(1, 12))
    
    # ===== CORE COMPETENCIES =====
    if skills:
        story.append(Paragraph("CORE COMPETENCIES", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        # Create a more elegant skills layout
        skills_per_row = 4 if page_size.lower() != "a4" else 3
        skills_table_data = []
        row = []
        
        for i, skill in enumerate(skills):
            row.append(Paragraph(f"◦ {skill}", styles['ExecutiveSkill']))
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
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 8))
    
    # ===== LANGUAGES =====
    if languages:
        story.append(Paragraph("LANGUAGES", styles['ExecutiveSectionHeader']))
        add_section_separator()
        languages_text = " ◦ ".join(languages)
        story.append(Paragraph(languages_text, styles['ExecutiveBody']))
    
    # ===== INTERESTS =====
    if hobbies:
        story.append(Paragraph("INTERESTS", styles['ExecutiveSectionHeader']))
        add_section_separator()
        hobbies_text = " ◦ ".join(hobbies)
        story.append(Paragraph(hobbies_text, styles['ExecutiveBody']))
    
    # ===== REFERENCES =====
    if referees:
        story.append(Paragraph("REFERENCES", styles['ExecutiveSectionHeader']))
        add_section_separator()
        
        for ref in referees:
            ref_data = [
                [
                    Paragraph(f"<b>{ref['name']}</b>", styles['ExecutiveCompany']),
                    Paragraph(f"<b>{ref['position']}</b>", styles["ExecutivePosition"])
                ],
                [
                    Paragraph(ref['organization'], styles["ExecutivePosition"]),
                    Paragraph(f"Phone: {ref['phone']}", styles['ExecutivePosition'])
                ],
                [
                    Paragraph(f"Email: {ref['email']}", styles['ExecutiveSkill']),
                    Paragraph(f"Relationship: {ref.get('relationship', 'N/A')}", styles["ExecutiveSkill"])
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
    
    doc.build(story)

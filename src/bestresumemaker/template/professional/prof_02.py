from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.units import inch, mm

def professional2(personal_info, professional_summary, work_experience, education, skills, 
                   academic_projects=None, certifications=None, publications=None, 
                   hobbies=None, languages=None, referees=None, achievements=None,
                   honors_awards=None, output_file="resume.pdf", page_size="letter"):
    
    # Set page size based on user preference
    if page_size.lower() == "a4":
        page_dimensions = A4
        margin_left_right = 15 * mm
        margin_top_bottom = 20 * mm
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
    
    # Custom color scheme
    primary_color = colors.HexColor("#2E86AB")
    secondary_color = colors.HexColor("#6C757D")
    accent_color = colors.HexColor("#F18F01")
    font_size_adjustment = 0.95 if page_size.lower() == "a4" else 1

    # Custom style names to avoid conflicts
    styles.add(ParagraphStyle(
        name="CustomNameTitle",
        fontSize=28 * font_size_adjustment,
        leading=32 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        textColor=primary_color
    ))

    styles.add(ParagraphStyle(
        name="CustomTitle",
        fontSize=16 * font_size_adjustment,
        leading=20 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=18,
        fontName='Helvetica',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="CustomContact",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_CENTER,
        spaceAfter=24,
        fontName='Helvetica'
    ))

    styles.add(ParagraphStyle(
        name="CustomSectionTitle",
        fontSize=14 * font_size_adjustment,
        leading=20 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        textColor=primary_color,
        borderPadding=(0, 0, 0, 6),
        borderColor=accent_color,
        borderWidth=1
    ))

    styles.add(ParagraphStyle(
        name="CustomCompany",
        fontSize=12 * font_size_adjustment,
        leading=16 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=colors.black
    ))

    styles.add(ParagraphStyle(
        name="CustomPosition",
        fontSize=11 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="CustomDate",
        fontSize=10 * font_size_adjustment,
        leading=12 * font_size_adjustment,
        alignment=TA_LEFT,
        spaceAfter=6,
        fontName='Helvetica-Oblique',
        textColor=secondary_color
    ))

    styles.add(ParagraphStyle(
        name="CustomBodyText",
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        textColor=colors.black,
        firstLineIndent=0,
        wordWrap='LTR',
        splitLongWords=True
    ))

    styles.add(ParagraphStyle(
        name="CustomBullet",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
        fontName='Helvetica',
        leftIndent=0,
        bulletIndent=0
    ))

    styles.add(ParagraphStyle(
        name="CustomJustifiedText",
        fontSize=10 * font_size_adjustment,
        leading=14 * font_size_adjustment,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica',
        textColor=colors.black
    ))

    def format_date(date_obj):
        """Helper function to format dates consistently"""
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%b %Y")
        elif isinstance(date_obj, str):
            return date_obj
        else:
            return str(date_obj)
    
    def add_bullet_list(items, style=styles['CustomBullet']):
        """Helper function to add bullet lists"""
        if isinstance(items, str):
            items = items.split('\n')
        
        for item in items:
            if item.strip():
                clean_item = item.strip().strip('"').strip("'")
                story.append(Paragraph(f"• {clean_item}", style))
    
    # ===== HEADER SECTION =====
    story.append(Paragraph(personal_info['name'].upper(), styles['CustomNameTitle']))
    story.append(Paragraph(personal_info['title'], styles['CustomTitle']))

    # Contact info - handle optional fields
    contact_items = []
    for field in ['email', 'phone', 'location', 'linkedin', 'github', 'website']:
        if field in personal_info and personal_info[field]:
            contact_items.append(personal_info[field])
    
    # Add contact info in rows if more than 3 items
    contact_rows = []
    for i in range(0, len(contact_items), 3):
        row = contact_items[i:i+3]
        while len(row) < 3:  # Pad with empty strings
            row.append('')
        contact_rows.append(row)
    
    if contact_rows:
        contact_table = Table(contact_rows, colWidths=[doc.width/3]*3)
        contact_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10 * font_size_adjustment),
            ('TEXTCOLOR', (0,0), (-1,-1), secondary_color),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(contact_table)
    
    story.append(HRFlowable(width="100%", thickness=1, lineCap='round', 
                          color=accent_color, spaceBefore=12, spaceAfter=12))
    # ===== PROFESSIONAL SUMMARY =====
    story.append(Paragraph("PROFESSIONAL PROFILE", styles['CustomSectionTitle']))
    story.append(Paragraph(professional_summary, styles["CustomBodyText"]))
    
    # ===== ACHIEVEMENTS =====

    if work_experience:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['CustomSectionTitle']))
        
        for job in work_experience:
            start_date = format_date(job['start_date'])
            end_date = format_date(job['end_date'])
            date_range = f"{start_date} - {end_date}"
            
            # Company and date on same line
            story.append(Paragraph(f"{job['company']} <font size='{10 * font_size_adjustment}' color='#{secondary_color.hexval()}'>{date_range}</font>", styles['CustomCompany']))
            story.append(Paragraph(job['position'], styles['CustomPosition']))
            
            add_bullet_list(job['description'])
            story.append(Spacer(1, 8))
    # ===== EDUCATION =====
    if education:
        story.append(Paragraph("EDUCATION", styles['CustomSectionTitle']))
        
        for edu in education:
            start_date = format_date(edu.get('start_date', ''))
            end_date = format_date(edu.get('graduation_date', edu.get('end_date', '')))
            
            # Format date range for education
            if start_date and end_date:
                date_range = f"{start_date} - {end_date}"
            elif end_date:
                date_range = end_date
            elif start_date:
                date_range = f"{start_date} - Present"
            else:
                date_range = ""
            
            story.append(Paragraph(f"{edu['institution']} <font size='{10 * font_size_adjustment}' color='#{secondary_color.hexval()}'>{date_range}</font>", styles['CustomCompany']))
            story.append(Paragraph(edu['degree'], styles['CustomPosition']))
            story.append(Spacer(1, 8))
    
    # ===== ACADEMIC PROJECTS =====
    if academic_projects:
        story.append(Paragraph("PROJECTS", styles['CustomSectionTitle']))
        
        for project in academic_projects:
            project_date = format_date(project['date'])
            
            story.append(Paragraph(f"{project['title']} <font size='{10 * font_size_adjustment}' color='#{secondary_color.hexval()}'>{project_date}</font>", styles["CustomCompany"]))
            story.append(Paragraph(f"Technologies: {project['technologies']}", styles['CustomPosition']))
            
            add_bullet_list(project['description'])
            
            # Add links if available
            if 'links' in project and project['links']:
                links_text = " | ".join([f"{name}: {url}" for name, url in project['links'].items()])
                story.append(Paragraph(f"Links: {links_text}", styles['CustomDate']))
            
            story.append(Spacer(1, 8))
    
    # ===== CERTIFICATIONS =====
    if certifications:
        story.append(Paragraph("CERTIFICATIONS", styles['CustomSectionTitle']))
        
        for cert in certifications:
            cert_date = format_date(cert['date'])
            
            story.append(Paragraph(f"{cert['name']} <font size='{10 * font_size_adjustment}' color='#{secondary_color.hexval()}'>{cert_date}</font>", styles['CustomCompany']))
            story.append(Paragraph(f"Issued by: {cert['issuer']}", styles['CustomPosition']))
            
            if 'credential_id' in cert:
                story.append(Paragraph(f"Credential ID: {cert['credential_id']}", styles['CustomDate']))
            
            if 'description' in cert:
                add_bullet_list(cert['description'])
            
            story.append(Spacer(1, 8))

    if achievements:
        story.append(Paragraph("KEY ACHIEVEMENTS", styles['CustomSectionTitle']))
        
        for achievement in achievements:
            # Handle both simple string format and detailed dictionary format
            if isinstance(achievement, str):
                story.append(Paragraph(f"• {achievement}", styles['CustomBullet']))
            else:
                # Dictionary format with optional date, category, and description
                title = achievement.get('title', achievement.get('name', ''))
                date_str = format_date(achievement.get('date', '')) if achievement.get('date') else ''
                category = achievement.get('category', '')
                
                # Format the achievement title with optional date and category
                if date_str and category:
                    achievement_header = f"{title} <font size='{9 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{category} - {date_str}]</font>"
                elif date_str:
                    achievement_header = f"{title} <font size='{9 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{date_str}]</font>"
                elif category:
                    achievement_header = f"{title} <font size='{9 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{category}]</font>"
                else:
                    achievement_header = title
                
                story.append(Paragraph(f"• {achievement_header}", styles['CustomBullet']))
                
                # Add description if provided
                if 'description' in achievement and achievement['description']:
                    if isinstance(achievement['description'], list):
                        for desc_item in achievement['description']:
                            story.append(Paragraph(f"  • {desc_item}", styles['CustomBullet']))
                    else:
                        story.append(Paragraph(f"  • {achievement['description']}", styles['CustomBullet']))
        
        story.append(Spacer(1, 8))
    
    # ===== HONORS & AWARDS =====
    if honors_awards:
        story.append(Paragraph("HONORS & AWARDS", styles['CustomSectionTitle']))
        
        for award in honors_awards:
            # Handle both simple string format and detailed dictionary format
            if isinstance(award, str):
                story.append(Paragraph(f"• {award}", styles['CustomBullet']))
            else:
                # Dictionary format with optional date, organization, and description
                title = award.get('title', award.get('name', ''))
                date_str = format_date(award.get('date', '')) if award.get('date') else ''
                organization = award.get('organization', award.get('issuer', ''))
                
                # Format the award title with optional date
                if date_str:
                    award_header = f"{title} <font size='{10 * font_size_adjustment}' color='#{secondary_color.hexval()}'>[{date_str}]</font>"
                else:
                    award_header = title
                
                story.append(Paragraph(award_header, styles['CustomCompany']))
                
                # Add organization if provided
                if organization:
                    story.append(Paragraph(f"Awarded by: {organization}", styles['CustomPosition']))
                
                # Add description if provided
                if 'description' in award and award['description']:
                    if isinstance(award['description'], list):
                        for desc_item in award['description']:
                            story.append(Paragraph(f"• {desc_item}", styles['CustomBullet']))
                    else:
                        story.append(Paragraph(f"• {award['description']}", styles['CustomBullet']))
                
                # Add monetary value if provided
                if 'value' in award and award['value']:
                    story.append(Paragraph(f"Value: {award['value']}", styles['CustomDate']))
        
        story.append(Spacer(1, 8))

    
    # ===== PUBLICATIONS =====
    if publications:
        story.append(Paragraph("PUBLICATIONS", styles['CustomSectionTitle']))
        
        for pub in publications:
            pub_date = format_date(pub['date'])
            
            story.append(Paragraph(f"{pub['title']} <font size='{10 * font_size_adjustment}' color='#{secondary_color.hexval()}'>{pub_date}</font>", styles["CustomCompany"]))
            story.append(Paragraph(f"Authors: {pub['authors']}", styles['CustomPosition']))
            story.append(Paragraph(f"Published in: {pub['journal']}", styles['CustomPosition']))
            
            if 'url' in pub:
                story.append(Paragraph(f"DOI/URL: {pub['url']}", styles['CustomDate']))
            
            if 'description' in pub:
                add_bullet_list(pub['description'])
            
            story.append(Spacer(1, 8))
    
    # ===== SKILLS =====
    if skills:
        story.append(Paragraph("KEY SKILLS", styles['CustomSectionTitle']))
        
        num_columns = 2 if page_size.lower() == "a4" else 3
        skills_table_data = []
        row = []
        
        for i, skill in enumerate(skills):
            row.append(Paragraph(f"• {skill}", styles['CustomBullet']))
            if (i + 1) % num_columns == 0:
                skills_table_data.append(row)
                row = []
        
        if row:
            while len(row) < num_columns:
                row.append("")
            skills_table_data.append(row)
        
        column_width = doc.width / num_columns
        skills_table = Table(skills_table_data, colWidths=[column_width] * num_columns)
        skills_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(skills_table)
    
    # ===== LANGUAGES =====
    if languages:
        story.append(Paragraph("LANGUAGES", styles['CustomSectionTitle']))
        languages_text = " • ".join(languages)
        story.append(Paragraph(languages_text, styles['CustomJustifiedText']))
    
    # ===== HOBBIES & INTERESTS ===== (FIXED)
    if hobbies:
        story.append(Paragraph("HOBBIES & INTERESTS", styles['CustomSectionTitle']))
        hobbies_text = " • ".join(hobbies)
        story.append(Paragraph(hobbies_text, styles['CustomJustifiedText']))
    
    # ===== REFERENCES ===== (FIXED)
    # ===== REFERENCES ===== (UPDATED FOR BETTER ALIGNMENT)
    if referees:
        story.append(Paragraph("REFERENCES", styles['CustomSectionTitle']))
        
        for ref in referees:
            # Create a table for each reference to align information properly
            ref_data = []
            
            # Row 1: Name and Position
            ref_data.append([
                Paragraph(ref['name'], styles['CustomCompany']),
                Paragraph(ref['position'], styles["CustomPosition"])
            ])
            
            # Row 2: Organization and Relationship (if available)
            if 'relationship' in ref and ref['relationship']:
                ref_data.append([
                    Paragraph(ref['organization'], styles["CustomPosition"]),
                    Paragraph(f"Relationship: {ref['relationship']}", styles["CustomDate"])
                ])
            else:
                ref_data.append([
                    Paragraph(ref['organization'], styles["CustomPosition"]),
                    Paragraph("", styles["CustomDate"])  # Empty cell
                ])
            
            # Row 3: Email and Phone
            ref_data.append([
                Paragraph(f"Email: {ref['email']}", styles['CustomBullet']),
                Paragraph(f"Phone: {ref['phone']}", styles['CustomBullet'])
            ])
            
            # Create table with proper column widths
            ref_table = Table(ref_data, colWidths=[doc.width/2, doc.width/2])
            ref_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('TOPPADDING', (0,0), (-1,-1), 2),
            ]))
            
            story.append(ref_table)
            story.append(Spacer(1, 12))
    

    doc.build(story)

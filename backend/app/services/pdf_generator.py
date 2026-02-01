"""
Service de génération de PDF à partir de Markdown
Utilise weasyprint pour créer des PDFs professionnels
"""
from io import BytesIO
import markdown
from weasyprint import HTML, CSS

class PDFGenerator:
    """Générateur de PDF pour CV et lettres de motivation"""
    
    # Template HTML de base avec CSS intégré (accolades doublées pour Python .format())
    CV_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                font-size: 11pt;
            }}
            
            h1 {{
                color: #2563eb;
                font-size: 24pt;
                margin-bottom: 0.3em;
                padding-bottom: 0.3em;
                border-bottom: 3px solid #2563eb;
            }}
            
            h2 {{
                color: #1e40af;
                font-size: 16pt;
                margin-top: 1.2em;
                margin-bottom: 0.5em;
                padding-bottom: 0.2em;
                border-bottom: 1px solid #cbd5e1;
            }}
            
            h3 {{
                color: #334155;
                font-size: 13pt;
                margin-top: 0.8em;
                margin-bottom: 0.3em;
            }}
            
            p {{
                margin: 0.5em 0;
            }}
            
            ul, ol {{
                margin: 0.5em 0;
                padding-left: 1.5em;
            }}
            
            li {{
                margin: 0.3em 0;
            }}
            
            strong {{
                color: #1e293b;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 1.5em;
            }}
            
            .contact-info {{
                text-align: center;
                color: #64748b;
                margin-bottom: 1.5em;
            }}
            
            .section {{
                margin-bottom: 1.5em;
                page-break-inside: avoid;
            }}
            
            .footer {{
                margin-top: 2em;
                padding-top: 1em;
                border-top: 1px solid #cbd5e1;
                text-align: center;
                font-size: 9pt;
                color: #94a3b8;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{candidate_name}</h1>
            <div class="contact-info">{contact_info}</div>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            CV généré le {date} | Job Hunter AI
        </div>
    </body>
    </html>
    """
    
    COVER_LETTER_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{
                size: A4;
                margin: 2.5cm;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.8;
                color: #333;
                font-size: 11pt;
            }}
            
            .header {{
                margin-bottom: 2em;
            }}
            
            .sender {{
                margin-bottom: 1.5em;
            }}
            
            .recipient {{
                margin-bottom: 2em;
            }}
            
            .date {{
                text-align: right;
                margin-bottom: 2em;
                color: #64748b;
            }}
            
            .content {{
                text-align: justify;
            }}
            
            .content p {{
                margin-bottom: 1em;
            }}
            
            .signature {{
                margin-top: 2em;
                text-align: right;
            }}
            
            h1 {{
                color: #2563eb;
                font-size: 18pt;
                margin-bottom: 0.5em;
            }}
            
            strong {{
                color: #1e293b;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="sender">
                <strong>{candidate_name}</strong><br>
                {contact_info}
            </div>
            
            <div class="recipient">
                <strong>{company_name}</strong><br>
                {company_address}
            </div>
            
            <div class="date">{date}</div>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="signature">
            <p>{candidate_name}</p>
        </div>
    </body>
    </html>
    """
    
    @staticmethod
    def markdown_to_html(markdown_text: str) -> str:
        """Convertit le Markdown en HTML"""
        return markdown.markdown(
            markdown_text,
            extensions=['extra', 'nl2br']
        )
    
    @staticmethod
    def generate_pdf(html_content: str) -> bytes:
        """Génère un PDF à partir de HTML"""
        html = HTML(string=html_content)
        pdf_file = BytesIO()
        html.write_pdf(pdf_file)
        pdf_file.seek(0)
        return pdf_file.read()
    
    @staticmethod
    def generate_cv_pdf(
        candidate_name: str,
        contact_info: str,
        content_markdown: str,
        date: str
    ) -> bytes:
        """
        Génère un PDF de CV
        
        Args:
            candidate_name: Nom du candidat
            contact_info: Informations de contact (email, téléphone, etc.)
            content_markdown: Contenu du CV en Markdown
            date: Date de génération
            
        Returns:
            bytes: PDF en bytes
        """
        # Convertir le Markdown en HTML
        content_html = PDFGenerator.markdown_to_html(content_markdown)
        
        # Injecter dans le template
        html = PDFGenerator.CV_TEMPLATE.format(
            title=f"CV - {candidate_name}",
            candidate_name=candidate_name,
            contact_info=contact_info,
            content=content_html,
            date=date
        )
        
        # Générer le PDF
        return PDFGenerator.generate_pdf(html)
    
    @staticmethod
    def generate_cover_letter_pdf(
        candidate_name: str,
        contact_info: str,
        company_name: str,
        company_address: str,
        content_markdown: str,
        date: str
    ) -> bytes:
        """
        Génère un PDF de lettre de motivation
        
        Args:
            candidate_name: Nom du candidat
            contact_info: Informations de contact
            company_name: Nom de l'entreprise
            company_address: Adresse de l'entreprise
            content_markdown: Contenu de la lettre en Markdown
            date: Date de génération
            
        Returns:
            bytes: PDF en bytes
        """
        # Convertir le Markdown en HTML
        content_html = PDFGenerator.markdown_to_html(content_markdown)
        
        # Injecter dans le template
        html = PDFGenerator.COVER_LETTER_TEMPLATE.format(
            title=f"Lettre de motivation - {company_name}",
            candidate_name=candidate_name,
            contact_info=contact_info,
            company_name=company_name,
            company_address=company_address,
            content=content_html,
            date=date
        )
        
        # Générer le PDF
        return PDFGenerator.generate_pdf(html)

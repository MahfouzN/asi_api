from django.http import FileResponse
from rest_framework.views import APIView
from gestion_comptes.models.autorite import AutoriteCompetente
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

class GeneratePDFView(APIView):
    def get(self, request, *args, **kwargs):
        # Créer un objet BytesIO pour stocker le PDF
        buffer = BytesIO()

        # Créer le document PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

        # Contenu du PDF
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1  # Centre le titre

        # Ajouter le titre
        elements.append(Paragraph("Liste des Autorités Compétentes", title_style))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Vérifier le rôle de l'utilisateur et récupérer les autorités
        if request.user.is_superadmin:
            autorites = AutoriteCompetente.objects.all()
        else:
            try:
                commune = request.user.personne.commune
                autorites = AutoriteCompetente.objects.filter(commune=commune)
            except AttributeError:
                autorites = AutoriteCompetente.objects.none()

        # Préparer les données pour le tableau
        data = [['Téléphone', 'Email', 'Nom', "Type d'autorité", 'Mot de passe']]
        for autorite in autorites:
            # Accéder au mot de passe directement
            password = autorite.password  # Récupérer le mot de passe en clair

            data.append([
                autorite.telephone,
                autorite.email,
                autorite.nom,
                autorite.type_autorite.nom,
                password  # Afficher le mot de passe en clair
            ])

        # Créer le tableau
        table = Table(data, colWidths=[1 * inch, 1.5 * inch, 1 * inch, 1 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ]))

        elements.append(table)

        # Construire le PDF
        doc.build(elements)

        # FileResponse avec le PDF
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='autorites_competentes.pdf')
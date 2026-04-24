"""
OrientAI — Génération du rapport PDF
Utilise reportlab pour produire un PDF avec les confirmations cochées par l'élève.
"""

import io
import math
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import KeepTogether

from donnees_rapport import MAPPING_QUESTIONS, SS_RAPPORT_NOMS, SS_NIVEAUX

# ── Couleurs ──────────────────────────────────────────────────────────────────
ROSE      = colors.HexColor("#d4667a")
GOLD      = colors.HexColor("#c9a84c")
DARK      = colors.HexColor("#1a1a2e")
MUTED     = colors.HexColor("#7a7a8c")
VERT      = colors.HexColor("#6b9e7e")
ORANGE    = colors.HexColor("#e8a87c")
LIGHT_BG  = colors.HexColor("#faf8f3")
WHITE     = colors.white

SS_COLORS_RL = {
    1: ORANGE,
    2: GOLD,
    3: VERT,
}
SS_NIVEAUX = {1: "À développer", 2: "Intermédiaire", 3: "Très développée"}


def _add_page_number(canvas, doc):
    """Ajoute numéro de page en bas de chaque page sauf la première."""
    page_num = canvas.getPageNumber()
    if page_num <= 1:
        return
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    # Numéro centré
    canvas.drawCentredString(A4[0] / 2, 1.2*cm, f"— {page_num} —")
    # Nom en bas à gauche
    canvas.setFont("Helvetica", 7)
    canvas.drawString(2.5*cm, 1.2*cm, "OrientAI v5.2")
    canvas.restoreState()


def _radar_image(ss_vals):
    """Génère le graphique radar et retourne un objet Image reportlab."""
    labels = [
        "Communication", "Esprit\ncritique", "Éthique",
        "Intel.\némotionnelle", "Intel.\nsociale",
        "Mgmt\nprojet", "Mgmt\néquipe", "Organisation"
    ]
    N = len(labels)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values = [v / 3 for v in ss_vals] + [ss_vals[0] / 3]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.set_facecolor('#faf8f3')
    fig.patch.set_facecolor('#faf8f3')

    # Zones de niveaux — couleurs plus marquées
    ax.fill(angles, [1/3]*(N+1), alpha=0.45, color='#e8a87c')   # À développer — orange vif
    ax.fill(angles, [2/3]*(N+1), alpha=0.30, color='#c9a84c')   # Intermédiaire — or
    ax.fill(angles, [1.0]*(N+1), alpha=0.20, color='#6b9e7e')   # Très développée — vert

    ax.plot(angles, values, 'o-', linewidth=2.5, color='#1a1a2e', markersize=5)
    ax.fill(angles, values, alpha=0.35, color='#1a1a2e')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=7, color='#1a1a2e')
    ax.set_ylim(0, 1)
    ax.set_yticks([1/3, 2/3, 1])
    ax.set_yticklabels(["À dév.", "Inter.", "Très dév."], size=6, color='#888')
    ax.grid(color='#cccccc', linestyle='--', linewidth=0.5)
    ax.spines['polar'].set_color('#cccccc')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#faf8f3')
    plt.close()
    buf.seek(0)
    return Image(buf, width=10*cm, height=10*cm)


def generer_pdf(prenom: str, nom: str, answers: list, profile: dict,
                confirmations: dict, top_metiers: list = None,
                classe: str = "") -> bytes:
    """
    Génère le rapport PDF.

    Args:
        prenom, nom: identité
        answers: réponses au questionnaire (0-3)
        profile: résultat compute_profile()
        confirmations: dict {(ss_idx, q_idx): True/False} — cases cochées par l'élève
        top_metiers: liste des métiers recommandés

    Returns:
        bytes du PDF
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    w = A4[0] - 5*cm  # largeur utile

    # Styles personnalisés
    s_titre = ParagraphStyle('titre', parent=styles['Normal'],
        fontSize=28, textColor=DARK, spaceAfter=6,
        fontName='Helvetica-Bold', alignment=TA_CENTER)
    s_sous = ParagraphStyle('sous', parent=styles['Normal'],
        fontSize=13, textColor=MUTED, spaceAfter=4,
        fontName='Helvetica', alignment=TA_CENTER)
    s_nom = ParagraphStyle('nom', parent=styles['Normal'],
        fontSize=22, textColor=ROSE, spaceBefore=20, spaceAfter=20,
        fontName='Helvetica-Bold', alignment=TA_CENTER)
    s_h1 = ParagraphStyle('h1', parent=styles['Normal'],
        fontSize=16, textColor=DARK, spaceBefore=16, spaceAfter=8,
        fontName='Helvetica-Bold')
    s_h2 = ParagraphStyle('h2', parent=styles['Normal'],
        fontSize=13, textColor=DARK, spaceBefore=12, spaceAfter=6,
        fontName='Helvetica-Bold')
    s_body = ParagraphStyle('body', parent=styles['Normal'],
        fontSize=9, textColor=DARK, spaceAfter=4, fontName='Helvetica',
        leading=13)
    s_small = ParagraphStyle('small', parent=styles['Normal'],
        fontSize=8, textColor=MUTED, spaceAfter=3, fontName='Helvetica',
        alignment=TA_CENTER)
    s_cell = ParagraphStyle('cell', parent=styles['Normal'],
        fontSize=8.5, textColor=DARK, fontName='Helvetica', leading=12)
    s_cell_bold = ParagraphStyle('cellb', parent=styles['Normal'],
        fontSize=8.5, textColor=DARK, fontName='Helvetica-Bold', leading=12)

    ss_vals = profile["ss"]
    score_moyen = sum(ss_vals) / len(ss_vals)
    points_forts = [SS_RAPPORT_NOMS[i] for i, v in enumerate(ss_vals) if v == 3]
    a_developper = [SS_RAPPORT_NOMS[i] for i, v in enumerate(ss_vals) if v == 1]

    story = []

    # Données communes à la page de garde
    nom_complet = f"{prenom} {nom}".strip()
    date_test   = datetime.now().strftime("%d %B %Y")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE DE COUVERTURE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.5*cm))

    # Bandeau sombre — "Orient" blanc + "AI" doré (sans emoji)
    cover_top = Table(
        [[Paragraph(
            "<font color='#FFFFFF'><b>Orient</b></font>"
            "<font color='#c9a84c'><b>AI</b></font>",
            ParagraphStyle('ct', parent=styles['Normal'],
                fontSize=38, textColor=WHITE, fontName='Helvetica-Bold',
                alignment=TA_CENTER, spaceAfter=0)
        )]],
        colWidths=[w]
    )
    cover_top.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK),
        ('TOPPADDING', (0,0), (-1,-1), 30),
        ('BOTTOMPADDING', (0,0), (-1,-1), 30),
        ('ROUNDEDCORNERS', [10, 10, 0, 0]),
    ]))
    story.append(cover_top)

    # Bandeau doré — sous-titre
    cover_sub = Table(
        [[Paragraph(
            "<font color='#FFFFFF'><b>Schéma de personnalité</b></font>",
            ParagraphStyle('cs', parent=styles['Normal'],
                fontSize=12, textColor=WHITE, fontName='Helvetica',
                alignment=TA_CENTER, spaceAfter=0)
        )]],
        colWidths=[w]
    )
    cover_sub.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [0, 0, 10, 10]),
    ]))
    story.append(cover_sub)
    story.append(Spacer(1, 1.2*cm))

    # ── Encadré identité centré avec bordure dorée ────────────────────────────
    id_cell = [
        Paragraph(nom_complet, ParagraphStyle('id_nom', parent=styles['Normal'],
            fontSize=24, textColor=DARK, fontName='Helvetica-Bold',
            alignment=TA_CENTER, spaceBefore=0, spaceAfter=10)),
    ]
    if classe:
        id_cell.append(Paragraph(classe, ParagraphStyle('id_classe', parent=styles['Normal'],
            fontSize=12, textColor=MUTED, fontName='Helvetica',
            alignment=TA_CENTER, spaceBefore=0, spaceAfter=14)))
    id_cell.append(Paragraph(
        f"Test réalisé le {date_test}",
        ParagraphStyle('id_date', parent=styles['Normal'],
            fontSize=10, textColor=MUTED, fontName='Helvetica',
            alignment=TA_CENTER, spaceBefore=0, spaceAfter=0)
    ))

    id_box = Table([[id_cell]], colWidths=[w * 0.78])
    id_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.5, GOLD),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fdfbf6")),
        ('TOPPADDING', (0,0), (-1,-1), 26),
        ('BOTTOMPADDING', (0,0), (-1,-1), 26),
        ('LEFTPADDING', (0,0), (-1,-1), 30),
        ('RIGHTPADDING', (0,0), (-1,-1), 30),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    # Centrer l'encadré dans la largeur de page
    cover_id = Table([[id_box]], colWidths=[w])
    cover_id.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(cover_id)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SOMMAIRE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Sommaire", ParagraphStyle('som_titre', parent=styles['Normal'],
        fontSize=18, textColor=DARK, fontName='Helvetica-Bold',
        spaceAfter=20)))
    story.append(HRFlowable(width=w, color=DARK, thickness=0.5))
    story.append(Spacer(1, 0.5*cm))

    section_num_metiers = "II" if top_metiers else None
    section_num_analyse = "III" if top_metiers else "II"

    sommaire_items = [
        ("I.", "Votre profil en un coup d'œil", "Tableau des soft skills + diagramme radar"),
    ]
    if top_metiers:
        sommaire_items.append(("II.", "Vos métiers recommandés", "Top 15 métiers compatibles avec votre profil"))
    sommaire_items.append((section_num_analyse + ".", "Analyse détaillée de vos soft skills",
        "Détail par compétence avec vos réponses"))

    for num, titre, desc in sommaire_items:
        row = Table(
            [[
                Paragraph(f"<b>{num}</b>", ParagraphStyle('sn', parent=styles['Normal'],
                    fontSize=11, textColor=GOLD, fontName='Helvetica-Bold')),
                Paragraph(f"<b>{titre}</b><br/><font color='#7a7a8c' size='8'>{desc}</font>",
                    ParagraphStyle('st', parent=styles['Normal'],
                    fontSize=11, textColor=DARK, fontName='Helvetica-Bold', leading=16)),
            ]],
            colWidths=[1.2*cm, w - 1.2*cm]
        )
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (0,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e8e4da")),
        ]))
        story.append(row)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # I. PROFIL EN UN COUP D'ŒIL
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("I. Votre profil en un coup d'œil", s_h1))
    story.append(HRFlowable(width=w, color=DARK, thickness=0.5))
    story.append(Spacer(1, 0.3*cm))

    # Tableau résumé SS
    data_ss = [["Soft skill", "Niveau"]]
    for i, ss_nom in SS_RAPPORT_NOMS.items():
        niveau = ss_vals[i]
        data_ss.append([ss_nom, SS_NIVEAUX[niveau]])

    ts_ss = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ])
    # Couleurs par niveau
    for i, (_, ss_nom) in enumerate(SS_RAPPORT_NOMS.items(), 1):
        niveau = ss_vals[i-1]
        ts_ss.add('BACKGROUND', (1, i), (1, i), SS_COLORS_RL[niveau])
        ts_ss.add('TEXTCOLOR', (1, i), (1, i), WHITE)
        ts_ss.add('FONTNAME', (1, i), (1, i), 'Helvetica-Bold')

    t_ss = Table(data_ss, colWidths=[12*cm, 5*cm])
    t_ss.setStyle(ts_ss)
    story.append(t_ss)
    story.append(Spacer(1, 0.5*cm))

    # Graphique radar
    story.append(Paragraph("Diagramme de personnalité", s_h2))
    radar_img = _radar_image(ss_vals)
    radar_img.hAlign = 'CENTER'
    story.append(radar_img)
    story.append(Spacer(1, 0.3*cm))

    # Légende radar
    legende_data = [["● À développer", "● Intermédiaire", "● Très développée"]]
    t_leg = Table(legende_data, colWidths=[w/3]*3)
    t_leg.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, 0), ORANGE),
        ('TEXTCOLOR', (1, 0), (1, 0), GOLD),
        ('TEXTCOLOR', (2, 0), (2, 0), VERT),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(t_leg)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # II. TOP 15 MÉTIERS
    # ══════════════════════════════════════════════════════════════════════════
    if top_metiers:
        story.append(Paragraph("II. Vos métiers recommandés", s_h1))
        story.append(HRFlowable(width=w, color=DARK, thickness=0.5))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(
            "Classés par compatibilité avec votre profil de soft skills.",
            s_body
        ))
        story.append(Spacer(1, 0.3*cm))

        data_met = [["#", "Métier", "Secteur", "Score"]]
        for rank, m in enumerate(top_metiers[:15], 1):
            score = m.get("score", 0)
            data_met.append([
                str(rank),
                m.get("metier", ""),
                m.get("secteur", "").split(" ; ")[0],
                f"{score}%"
            ])

        ts_met = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK),
            ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ])
        # Couleur score
        for rank, m in enumerate(top_metiers[:15], 1):
            score = m.get("score", 0)
            c = VERT if score >= 75 else GOLD if score >= 50 else ORANGE
            ts_met.add('BACKGROUND', (3, rank), (3, rank), c)
            ts_met.add('TEXTCOLOR', (3, rank), (3, rank), WHITE)
            ts_met.add('FONTNAME', (3, rank), (3, rank), 'Helvetica-Bold')

        t_met = Table(data_met, colWidths=[1.2*cm, 7*cm, 6*cm, 2*cm])
        t_met.setStyle(ts_met)
        story.append(t_met)
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(
            "Salaires indicatifs — Sources : ONISEP, APEC, INSEE, observatoires sectoriels. "
            "Les fourchettes peuvent varier selon l'expérience, la région et la taille de l'entreprise.",
            ParagraphStyle(
                'mention_salaire',
                parent=s_body,
                fontSize=7,
                textColor=colors.HexColor("#888888"),
                fontName='Helvetica-Oblique',
                spaceBefore=2,
            )
        ))
        story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # III. ANALYSE DÉTAILLÉE
    # ══════════════════════════════════════════════════════════════════════════
    section_num = "III" if top_metiers else "II"
    story.append(Paragraph(f"{section_num}. Analyse détaillée de vos soft skills", s_h1))
    story.append(HRFlowable(width=w, color=DARK, thickness=0.5))
    story.append(Spacer(1, 0.3*cm))

    # Mapping questions → SS
    ss_questions = {i: [] for i in range(8)}
    for q_idx, mapping in enumerate(MAPPING_QUESTIONS):
        sous_comp, ss_nom_map, textes = mapping
        ss_idx = next(
            (i for i, n in SS_RAPPORT_NOMS.items()
             if n.lower() in ss_nom_map.lower() or ss_nom_map.lower() in n.lower()), None
        )
        if ss_idx is not None:
            ss_questions[ss_idx].append((q_idx, sous_comp, textes))

    lettres = ["A", "B", "C", "D"]

    for ss_idx, ss_nom in SS_RAPPORT_NOMS.items():
        niveau = ss_vals[ss_idx]
        couleur = SS_COLORS_RL[niveau]
        niveau_txt = SS_NIVEAUX[niveau]

        # En-tête soft skill
        entete_data = [[
            Paragraph(f"<b>{ss_nom}</b>", ParagraphStyle('ess', fontSize=11,
                textColor=WHITE, fontName='Helvetica-Bold')),
            Paragraph(niveau_txt, ParagraphStyle('env', fontSize=9,
                textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_RIGHT))
        ]]
        t_hdr = Table(entete_data, colWidths=[13*cm, 4*cm])
        t_hdr.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), couleur),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (0, -1), 10),
            ('RIGHTPADDING', (-1, 0), (-1, -1), 10),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        story.append(t_hdr)
        story.append(Spacer(1, 0.2*cm))

        # Tableau sous-compétences
        data_tab = [[
            Paragraph("<b>Sous-compétence</b>", s_cell_bold),
            Paragraph("<b>Ce que vos réponses révèlent</b>", s_cell_bold),
            Paragraph("<b>Confirmé ?</b>", ParagraphStyle('ch', fontSize=8.5,
                textColor=DARK, fontName='Helvetica-Bold', alignment=TA_CENTER))
        ]]

        qs = ss_questions.get(ss_idx, [])
        for row_idx, (q_idx, sous_comp, textes) in enumerate(qs):
            ans_idx = answers[q_idx] if q_idx < len(answers) and answers[q_idx] is not None else 0
            lettre = lettres[ans_idx]
            texte = textes.get(lettre, "")

            # Récupérer la confirmation de l'élève
            confirmed = confirmations.get((ss_idx, q_idx), None)
            if confirmed is True:
                case = "☑ Oui   ☐ Non"
            elif confirmed is False:
                case = "☐ Oui   ☑ Non"
            else:
                case = "☐ Oui   ☐ Non"

            bg = colors.HexColor("#faf8f3") if row_idx % 2 == 0 else WHITE
            data_tab.append([
                Paragraph(sous_comp, s_cell_bold),
                Paragraph(texte, s_cell),
                Paragraph(case, ParagraphStyle('case', fontSize=8.5,
                    textColor=DARK, fontName='Helvetica', alignment=TA_CENTER)),
            ])

        ts_tab = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e8e4da")),
            ('TEXTCOLOR', (0, 0), (-1, 0), DARK),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ])
        # Alternance fond
        for i in range(1, len(data_tab)):
            if i % 2 == 1:
                ts_tab.add('BACKGROUND', (0, i), (-1, i), colors.HexColor("#faf8f3"))

        t_tab = Table(data_tab, colWidths=[4*cm, 10*cm, 3*cm])
        t_tab.setStyle(ts_tab)
        story.append(t_tab)
        story.append(Spacer(1, 0.5*cm))

        if ss_idx < 7:
            story.append(PageBreak())

    # ── Pied de page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width=w, color=MUTED, thickness=0.3))
    story.append(Paragraph(
        "Rapport généré par OrientAI v5.2 — Outil d'orientation par soft skills",
        ParagraphStyle('footer', fontSize=7, textColor=MUTED,
            alignment=TA_CENTER, fontName='Helvetica')
    ))

    # Pied de page spécifique à la page de garde (page 1)
    _date_gen = datetime.now().strftime("%d %B %Y")

    def _cover_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2, 1.8*cm,
            f"Généré le {_date_gen}  ·  OrientAI v5.2 — Confidentiel"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=_cover_footer, onLaterPages=_add_page_number)
    buf.seek(0)
    return buf.getvalue()

import io
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _clean_text(text: str) -> str:
    text = str(text)
    text = text.replace("**", "")
    text = text.replace("\u2022", "-")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")
    # Split very long unbroken chunks to avoid layout issues on cloud environments.
    text = re.sub(
        r"\S{70,}",
        lambda m: " ".join(m.group(0)[i:i + 35] for i in range(0, len(m.group(0)), 35)),
        text,
    )
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\u024F]", "", text)
    return text.strip()


def create_recipe_pdf(recipe_text, recipe_name):
    """
    Parse recipe markdown text and generate a clean PDF buffer.
    Returns:
        io.BytesIO
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title=f"{_clean_text(recipe_name)} Recipe",
        author="SmartChef AI",
    )

    base = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "RecipeTitle",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=1,
        textColor=colors.HexColor("#B22222"),
        spaceAfter=8,
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#333333"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.black,
    )

    story = []
    display_name = _clean_text(recipe_name) or "SmartChef Recipe"
    story.append(Paragraph("SmartChef AI Recipe", title_style))
    story.append(Paragraph(f"<b>{display_name}</b>", heading_style))
    story.append(Spacer(1, 6))

    for raw_line in str(recipe_text).splitlines():
        line = _clean_text(raw_line)
        if not line:
            story.append(Spacer(1, 4))
            continue

        if line.endswith(":"):
            story.append(Paragraph(line, heading_style))
            continue

        if line.startswith(("-", "*")):
            line = f"&#8226; {_clean_text(line[1:])}"
            story.append(Paragraph(line, body_style))
            continue

        if re.match(r"^\d+\.", line):
            story.append(Paragraph(line, body_style))
            continue

        story.append(Paragraph(line, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

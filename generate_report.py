
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)

# Grafana configuration
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
DASHBOARD_UID = "ad8gbz2"
DASHBOARD_SLUG = "riverbend-soc-metrics-dashboard"

TOKEN = os.getenv("GRAFANA_TOKEN")

# Report settings
OUTPUT_DIR = Path("reports")
IMAGE_DIR = OUTPUT_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

REPORT_DATE = datetime.now(timezone.utc).strftime("%Y%m%d")
PDF_PATH = OUTPUT_DIR / f"riverbend-soc-report-{REPORT_DATE}.pdf"

PANELS = [
    {"id": 1, "title": "Alert Volume"},
    {"id": 2, "title": "Mean Time to Detect (MTTD)"},
    {"id": 3, "title": "Mean Time to Respond (MTTR)"},
    {"id": 4, "title": "False Positive Rate"},
]


def render_panel(panel):
    """Render one Grafana panel as a PNG image."""

    url = (
        f"{GRAFANA_URL}/render/d-solo/"
        f"{DASHBOARD_UID}/{DASHBOARD_SLUG}"
    )

    params = {
        "panelId": panel["id"],
        "from": "now-7d",
        "to": "now",
        "width": 1200,
        "height": 500,
    }

    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=120,
    )

    response.raise_for_status()

    if "image/png" not in response.headers.get("Content-Type", ""):
        raise RuntimeError(
            f"Panel {panel['id']} did not return a PNG image."
        )

    image_path = IMAGE_DIR / f"panel-{panel['id']}.png"
    image_path.write_bytes(response.content)

    print(f"Rendered: {panel['title']}")


def generate_pdf():
    """Create the weekly SOC PDF report."""

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    story = []

    story.append(
        Paragraph(
            "Riverbend Microfinance Cooperative",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "Security Operations Center - Weekly Report",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph("Dashboard Metrics", styles["Heading1"])
    )

    story.append(
        Paragraph(
            "This report contains Grafana dashboard visualizations "
            "for alert volume, detection time, response time, and "
            "false-positive rate.",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 8 * mm))

    for index, panel in enumerate(PANELS):
        image_path = IMAGE_DIR / f"panel-{panel['id']}.png"

        story.append(
            Paragraph(panel["title"], styles["Heading2"])
        )

        image = Image(str(image_path))
        image._restrictSize(175 * mm, 95 * mm)
        story.append(image)
        story.append(Spacer(1, 8 * mm))

        if index < len(PANELS) - 1:
            story.append(PageBreak())

    story.append(Spacer(1, 5 * mm))

    story.append(
        Paragraph(
            "Note: Dashboard data in this demonstration uses "
            "synthetic training records and is not live operational data.",
            styles["Italic"],
        )
    )

    document.build(story)


def main():
    if not TOKEN:
        raise RuntimeError(
            "GRAFANA_TOKEN environment variable is not set."
        )

    print("Starting Riverbend SOC report generation...")

    for panel in PANELS:
        render_panel(panel)

    generate_pdf()

    print(f"\nPDF successfully generated: {PDF_PATH}")


if __name__ == "__main__":
    main()

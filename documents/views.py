import json
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files import File

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from .models import DiminishedValueReport

def home(request):
    return render(request, "documents/home.html")


def generate_pdf(report):

    folder = os.path.join(settings.MEDIA_ROOT, "dv_reports")
    os.makedirs(folder, exist_ok=True)

    filename = f"{report.report_number}.pdf"
    filepath = os.path.join(folder, filename)

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filepath)

    elements = []

    header_path = os.path.join(
        settings.BASE_DIR,
        "documents",
        "static",
        "documents",
        "header.png"
    )

    if os.path.exists(header_path):
        elements.append(Image(header_path, width=450, height=80))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>DIMINISHED VALUE APPRAISAL REPORT</b>", styles["Heading2"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Report Number: {report.report_number}", styles["Normal"]))
    elements.append(Paragraph(f"Claimant: {report.client}", styles["Normal"]))
    elements.append(Paragraph(f"Insurance Company: {report.insurance}", styles["Normal"]))
    elements.append(Paragraph(f"Claim Number: {report.claim_number}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        f"Vehicle: {report.vehicle_year} {report.vehicle_make} {report.vehicle_model} {report.vehicle_trim}",
        styles["Normal"]
    ))

    elements.append(Paragraph(f"VIN: {report.vin}", styles["Normal"]))
    elements.append(Paragraph(f"Mileage: {report.mileage}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Preloss Value: ${report.preloss_value}", styles["Normal"]))
    elements.append(Paragraph(f"Base DV: ${report.base_dv}", styles["Normal"]))
    elements.append(Paragraph(f"Adjusted DV: ${report.adjusted_dv}", styles["Normal"]))

    elements.append(Spacer(1, 20))

    signature_path = os.path.join(
        settings.BASE_DIR,
        "documents",
        "static",
        "documents",
        "signature.png"
    )

    if os.path.exists(signature_path):
        elements.append(Image(signature_path, width=200, height=60))

    elements.append(Paragraph(report.appraiser, styles["Normal"]))

    doc.build(elements)


    with open(filepath, "rb") as pdf_file:
        report.pdf_file.save(filename, File(pdf_file), save=True)


def save_report(request):

    if request.method != "POST":
        return JsonResponse({"status": "error"})

    data = json.loads(request.body)

    pre = float(data.get("preloss_retail") or 0)
    basepct = float(data.get("base_loss_pct") or 0)

    mod = (
        float(data.get("damage_modifier") or 0)
        + float(data.get("mileage_modifier") or 0)
        + float(data.get("other_modifier") or 0)
    )

    base_dv = pre * (basepct / 100)
    adjusted_dv = base_dv * (1 + mod / 100)


    report, created = DiminishedValueReport.objects.get_or_create(

        claim_number=data.get("claim_number"),
        vin=data.get("vin"),

        defaults={}
    )


    report.client = data.get("claimant_name")
    report.client_email = data.get("client_email")
    report.client_phone = data.get("client_phone")

    report.insurance = data.get("insurance_company")

    report.loss_date = data.get("loss_date") or None
    report.report_date = data.get("report_date") or None

    report.appraiser = data.get("appraiser_name")

    report.vehicle_year = data.get("vehicle_year")
    report.vehicle_make = data.get("vehicle_make")
    report.vehicle_model = data.get("vehicle_model")
    report.vehicle_trim = data.get("vehicle_trim")

    report.mileage = data.get("mileage") or None
    report.state = data.get("state")

    report.color_trim = data.get("color_trim")
    report.condition = data.get("preloss_condition")
    report.loss_type = data.get("loss_type")

    report.repair_facility = data.get("repair_facility")
    report.repair_total = float(data.get("repair_total") or 0)

    report.preloss_value = pre
    report.base_loss_pct = basepct

    report.damage_modifier = float(data.get("damage_modifier") or 0)
    report.mileage_modifier = float(data.get("mileage_modifier") or 0)
    report.other_modifier = float(data.get("other_modifier") or 0)

    report.damage_description = data.get("damage_description")

    report.base_dv = base_dv
    report.adjusted_dv = base_dv * (1 + mod / 100)

    report.status = "waiting"
    report.is_deleted = False

    report.full_clean()
    report.save()

    generate_pdf(report)

    return JsonResponse({

        "status": "success",

        "id": report.id,

        "report_number": report.report_number,

        "pdf_url": report.pdf_file.url

    })
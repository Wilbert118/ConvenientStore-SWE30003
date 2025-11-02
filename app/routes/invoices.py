from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response
from supabase import create_client, Client
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import os

bp = Blueprint("invoices", __name__, url_prefix="/invoices")

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@bp.route("/create/<int:sale_id>")
def create_invoice(sale_id):
    """create invoice and redirect to view"""
    invoice_url = f"/invoices/view/{sale_id}"
    data = {
        "sale_id": sale_id,
        "invoice_url": invoice_url,
        "generated_at": datetime.now().isoformat()
    }

    res = supabase.table("invoices").insert(data).execute()
    print("✅ Invoice creation result:", res)
    return redirect(invoice_url)


@bp.route("/view/<int:sale_id>")
def view_invoice(sale_id):
    """show invoice page"""
    res = supabase.table("invoices").select("*").eq("sale_id", sale_id).execute()
    invoice = res.data[0] if res.data else None
    return render_template("invoice_detail.html", invoice=invoice)


@bp.route("/api/<int:sale_id>")
def api_invoice(sale_id):
    """JSON API"""
    res = supabase.table("invoices").select("*").eq("sale_id", sale_id).execute()
    if res.data:
        return jsonify(res.data[0])
    else:
        return jsonify({"error": "Invoice not found"}), 404
    
@bp.route("/download/<int:sale_id>")
def download_invoice(sale_id):
    """生成并下载发票 PDF 文件"""
    res = supabase.table("invoices").select("*").eq("sale_id", sale_id).execute()
    if not res.data:
        return "Invoice not found", 404

    invoice = res.data[0]

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Invoice_{invoice['sale_id']}")

    x, y = 80, 800
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y, "Invoice Details")
    pdf.setFont("Helvetica", 12)
    y -= 30

    pdf.drawString(x, y, f"Invoice ID: {invoice['id']}")
    y -= 20
    pdf.drawString(x, y, f"Sale ID: {invoice['sale_id']}")
    y -= 20
    pdf.drawString(x, y, f"Invoice URL: {invoice['invoice_url']}")
    y -= 20
    pdf.drawString(x, y, f"Generated At: {invoice['generated_at']}")
    y -= 40
    pdf.drawString(x, y, "Thank you for your purchase!")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=invoice_{invoice['sale_id']}.pdf"
    return response
from flask import Blueprint, render_template, redirect, url_for, jsonify, make_response
from app.models.invoices_model import insert_invoice, get_invoice_by_sale_id, get_cart_items_by_sale_id, get_product_map, get_payment_by_sale_id
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@bp.route("/create/<int:sale_id>")
def create_invoice(sale_id):
    """create invoice and redirect to view"""
    res = insert_invoice(sale_id)
    print("✅ Invoice creation result:", res)
    return redirect(f"/invoices//view/{sale_id}")


@bp.route("/view/<int:sale_id>")
def view_invoice(sale_id):
    """show invoice page"""
    invoice = get_invoice_by_sale_id(sale_id)
    payment = get_payment_by_sale_id(sale_id)
    cart_items = get_cart_items_by_sale_id(sale_id)
    product_map = get_product_map()
    
    enriched_items = []
    total = 0.0
    
    for item in cart_items:
        product = product_map.get(item["product_id"])
        if product:
            item_total = product["price"] * item["quantity"]
            total += item_total
            enriched_items.append({
                "name": product["name"],
                "price": product["price"],
                "qty": item["quantity"],
                "subtotal": item_total
            })

    return render_template("invoice_detail.html", invoice=invoice,
                           payment=payment, items=enriched_items, total=total)


@bp.route("/api/<int:sale_id>")
def api_invoice(sale_id):
    """JSON API"""
    res = get_invoice_by_sale_id(sale_id)
    if res:
        return jsonify(res)
    else:
        return jsonify({"error": "Invoice not found"}), 404
    
@bp.route("/download/<int:sale_id>")
def download_invoice(sale_id):
    """Generate and download invoice PDF with enriched details"""
    invoice = get_invoice_by_sale_id(sale_id)
    if not invoice:
        return "Invoice not found", 404

    # Fetch cart items and product info
    cart_items = get_cart_items_by_sale_id(sale_id)
    product_map = get_product_map()

    
    enriched_items = []
    total = 0.0
    for item in cart_items:
        product = product_map.get(item["product_id"])
        if product:
            subtotal = item["quantity"] * product["price"]
            total += subtotal
            enriched_items.append({
                "name": product["name"],
                "qty": item["quantity"],
                "price": product["price"],
                "subtotal": subtotal
            })

    # Fetch payment info
    payment = get_payment_by_sale_id(sale_id)

    # Generate PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Invoice_{invoice['id']}")

    x, y = 80, 800
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y, "Invoice")
    pdf.setFont("Helvetica", 12)
    y -= 30

    pdf.drawString(x, y, f"Sale ID: {invoice['sale_id']}")
    y -= 20
    generated = datetime.fromisoformat(invoice["generated_at"])
    formatted = generated.strftime("%Y-%m-%d %H:%M")
    pdf.drawString(x, y, f"Generated At: {formatted}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, "Items:")
    y -= 20
    pdf.setFont("Helvetica", 11)

    for item in enriched_items:
        line = f"{item['qty']} x {item['name']} @ ${item['price']:.2f} = ${item['subtotal']:.2f}"
        pdf.drawString(x, y, line)
        y -= 18

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, y, f"Total: ${total:.2f}")
    y -= 30

    if payment:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, "Payment Info:")
        y -= 20
        pdf.setFont("Helvetica", 11)
        pdf.drawString(x, y, f"Method: {payment['method']}")
        y -= 18
        pdf.drawString(x, y, f"Status: {payment['status']}")
        y -= 18
        if payment.get("paid_at"):
            pdf.drawString(x, y, f"Paid At: {payment['paid_at'][:10]}")
            y -= 18

    y -= 30
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawString(x, y, "Thank you for your purchase!")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=invoice_{invoice['sale_id']}.pdf"
    return response

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for # type: ignore
from datetime import datetime
from core.auth_utils import role_required, login_required, get_trans
from core.db import ORDERS_DB, PAYMENTS_DB, save_orders, save_payments

business_bp = Blueprint('business', __name__)

@business_bp.route("/business")
@role_required(['business', 'admin'])
def business_portal():
    trans, lang = get_trans()
    user_id = session.get('user')
    user_role = session.get('role')
    if user_role == 'admin':
        orders = ORDERS_DB
        payments = PAYMENTS_DB
        incoming_orders = [o for o in ORDERS_DB if o.get('status') == 'Pending']
    else:
        orders = [o for o in ORDERS_DB if o.get('user_id') == user_id]
        payments = [p for p in PAYMENTS_DB if p.get('user_id') == user_id]
        incoming_orders = [o for o in ORDERS_DB if o.get('target_biz_id') == user_id and o.get('status') == 'Pending']
        
    return render_template("business_portal.html",
                           trans=trans, lang=lang,
                           orders=orders[-20:],  # pyre-ignore
                           incoming_orders=incoming_orders,
                           payments=payments[-20:])  # pyre-ignore

@business_bp.route("/business/create-order", methods=["POST"])
@login_required
def create_order():
    user_id = session.get('user')
    data = request.get_json(silent=True) or request.form.to_dict()
    order_id = f"AQ-{datetime.now().strftime('%Y%m%d')}-{len(ORDERS_DB)+1001}"
    
    # Target business or global marketplace
    target_biz = data.get("target_business_id", "GLOBAL")  # pyre-ignore
    
    order = {
        "id": order_id,
        "user_id": user_id,
        "target_biz_id": target_biz,
        "species": data.get("species", "N/A"),  # pyre-ignore
        "quantity": data.get("quantity", "1"),  # pyre-ignore
        "unit_price": data.get("unit_price", "0"),  # pyre-ignore
        "total_inr": data.get("total_inr", "₹0"),  # pyre-ignore
        "payment_method": data.get("payment_method", "UPI"),  # pyre-ignore
        "status": "Pending", # Starts as pending for business approval
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ORDERS_DB.append(order)
    save_orders()

    if request.is_json:
        return jsonify({"success": True, "order_id": order_id, "message": "Order placed! Awaiting business approval."})
    _, lang = get_trans()
    flash(f"Order {order_id} placed! Awaiting approval.", "info")
    return redirect(url_for("business.business_portal", lang=lang))

@business_bp.route("/business/order-action", methods=["POST"])
@role_required(['business', 'admin'])
def business_order_action():
    biz_id = session.get('user')
    data = request.get_json(silent=True) or request.form.to_dict()
    order_id = data.get("order_id")  # pyre-ignore
    action = data.get("action") # 'approve' or 'reject'  # pyre-ignore
    
    for order in ORDERS_DB:
        if order["id"] == order_id:
            # Check if this business is the target
            if order["target_biz_id"] == biz_id or session.get('role') == 'admin':
                order["status"] = "Confirmed" if action == "approve" else "Rejected"
                order["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if action == "approve":
                    # Create payment record on approval
                    payment = {
                        "id": f"PAY-{len(PAYMENTS_DB)+1}",
                        "user_id": order["user_id"],
                        "order_id": order_id,
                        "description": f"Order: {order['quantity']}T {order['species']}",
                        "amount": order["total_inr"].replace("₹", "").replace(",", ""),
                        "method": order["payment_method"],
                        "status": "Completed",
                        "type": "debit",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "icon": "🛒"
                    }
                    PAYMENTS_DB.append(payment)
                    save_payments()
                break
                
    save_orders()
    flash(f"Order {order_id} {action}ed.", "success")
    _, lang = get_trans()
    return redirect(url_for("business.business_portal", lang=lang))

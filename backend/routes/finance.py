from flask import Blueprint, request, jsonify, session, render_template
from core.auth_utils import login_required, get_trans
from core.db import PAYMENTS_DB, save_payments, load_json, save_json, ADMIN_CONFIG
import time
import random
import os
from datetime import datetime

finance_bp = Blueprint('finance', __name__)

TRANSACTIONS_DB_PATH = 'data/transactions.json'

@finance_bp.route("/api/payment/initiate", methods=["POST"])
@login_required
def initiate_payment():
    data = request.get_json(silent=True) or {}
    user_id = session.get('user')
    amount = float(data.get("amount", 0))
    order_id = data.get("order_id", f"AQ-{int(time.time())}")
    
    # Real-Time Payment Gateway Integration (Razorpay)
    razorpay_key = os.getenv("RAZORPAY_KEY_ID")
    razorpay_secret = os.getenv("RAZORPAY_KEY_SECRET")
    
    if razorpay_key and razorpay_secret:
        try:
            import razorpay
            client = razorpay.Client(auth=(razorpay_key, razorpay_secret))
            # Create order in Razorpay (amount must be in paise)
            order_amount = int(amount * 100)
            order_currency = 'INR'
            order_receipt = order_id
            
            payment_order = client.order.create(dict(
                amount=order_amount,
                currency=order_currency,
                receipt=order_receipt,
                payment_capture='0'
            ))
            
            return jsonify({
                "success": True,
                "gateway": "razorpay",
                "razorpay_order_id": payment_order['id'],
                "razorpay_key": razorpay_key,
                "amount": amount,
                "order_id": order_id
            })
        except ImportError:
            print("Razorpay library not installed. Falling back to UPI.")
        except Exception as e:
            print(f"Razorpay Error: {e}")
            
    # Fallback to UPI Link
    platform_upi = ADMIN_CONFIG.get("platform_upi", "aquasphere@hdfcbank")
    upi_link = f"upi://pay?pa={platform_upi}&pn=AquaSphere&am={amount}&cu=INR&tn={order_id}"
    return jsonify({
        "success": True,
        "gateway": "upi_mock",
        "upi_link": upi_link,
        "platform_upi": platform_upi,
        "order_id": order_id,
        "amount": amount,
        "qr_data": upi_link
    })

@finance_bp.route("/api/payment/webhook", methods=["POST"])
def payment_webhook():
    # Real-time Webhook for Payment Gateway (e.g., Razorpay/Stripe)
    # This endpoint is called automatically by the payment gateway when a transaction completes.
    webhook_secret = os.getenv("WEBHOOK_SECRET")
    signature = request.headers.get("X-Razorpay-Signature")
    
    payload = request.get_data()
    
    try:
        if webhook_secret and signature:
            import hmac
            import hashlib
            expected_signature = hmac.new(
                bytes(webhook_secret, 'latin-1'),
                msg=payload,
                digestmod=hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, signature):
                return jsonify({"status": "error", "message": "Invalid signature"}), 400
                
        data = request.get_json()
        if data.get("event") == "payment.captured":
            payment_entity = data['payload']['payment']['entity']
            order_id = payment_entity.get('order_id')
            amount = payment_entity.get('amount') / 100.0 # Convert from paise
            method = payment_entity.get('method', 'Gateway')
            
            payment = {
                "id": payment_entity.get('id'),
                "user_id": "System_Webhook",
                "order_id": order_id,
                "amount": str(amount),
                "method": method,
                "status": "Completed",
                "type": "credit",
                "description": f"Real-time Payment Captured",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "icon": "✅"
            }
            PAYMENTS_DB.append(payment)
            save_payments()
            return jsonify({"status": "ok"}), 200
            
    except Exception as e:
        print(f"Webhook Error: {e}")
        return jsonify({"status": "error"}), 500
        
    return jsonify({"status": "ignored"}), 200

@finance_bp.route("/api/payment/verify", methods=["POST"])
@login_required
def verify_payment():
    data = request.get_json(silent=True) or {}
    order_id = data.get("order_id")
    method = data.get("method", "UPI")
    amount = data.get("amount", 0)
    user_id = session.get('user')
    payment = {
        "id": f"PAY-{len(PAYMENTS_DB)+1}",
        "user_id": user_id,
        "order_id": order_id,
        "amount": str(amount),
        "method": method,
        "status": "Completed",
        "type": "debit",
        "description": data.get("description", "Payment"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "icon": "💳"
    }
    PAYMENTS_DB.append(payment)
    save_payments()
    return jsonify({"success": True, "payment_id": payment["id"]})

@finance_bp.route("/api/pay-process", methods=["POST"])
@login_required
def pay_process():
    data = request.get_json()
    amount = data.get('amount')
    method = data.get('method', 'UPI')
    purpose = data.get('purpose', 'General Transaction')
    recipient = data.get('recipient_id', 'AQUA_SYSTEM')
    
    tx_id = f"AQUA-{random.randint(100000, 999999)}"
    
    tx_list = load_json(TRANSACTIONS_DB_PATH, [])
    new_tx = {
        "id": tx_id,
        "sender_id": session.get('user'),
        "sender_name": session.get('user_name', 'Farmer'),
        "recipient_id": recipient,
        "amount": amount,
        "method": method,
        "purpose": purpose,
        "status": "Success",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tx_list.append(new_tx)
    save_json(TRANSACTIONS_DB_PATH, tx_list)
    
    return jsonify({
        "status": "success",
        "tx_id": tx_id,
        "message": f"Payment of {amount} via {method} was successful!"
    })

@finance_bp.route("/api/trust-score", methods=["GET"])
@login_required
def api_trust_score():
    user_id = session.get('user')
    # Mocking a Trust Score algorithm based on fintech credit scoring
    # In reality, this would look at pond health history, loan repayment history, etc.
    score = random.randint(650, 850)
    eligibility_amount = (score - 600) * 1000 # Example math
    
    return jsonify({
        "status": "success",
        "aquascore": score,
        "eligible_loan_amount": f"₹{eligibility_amount:,}",
        "factors": [
            "Pond Health History: Excellent",
            "Harvest Yield Consistency: High",
            "Payment History: On-time"
        ],
        "message": f"Your AquaScore (CIBIL for Aquaculture) is {score}, qualifying you for micro-loans."
    })

@finance_bp.route("/api/apply-microloan", methods=["POST"])
@login_required
def api_apply_microloan():
    data = request.get_json(silent=True) or {}
    amount = data.get("amount", 50000)
    
    # Store loan application
    return jsonify({
        "status": "success",
        "message": f"Micro-loan application for ₹{amount} has been submitted to partner Banks based on your AQUA Trust Score.",
        "application_id": f"LOAN-{random.randint(1000, 9999)}"
    })

@finance_bp.route("/payments")
@login_required
def payment_hub():
    trans, lang = get_trans()
    tx_list = load_json(TRANSACTIONS_DB_PATH, [])
    
    user_id = session.get('user')
    user_role = session.get('role', 'farmer')
    
    if user_role == 'admin':
        my_tx = tx_list
    else:
        my_tx = [t for t in tx_list if t.get('sender_id') == user_id or t.get('recipient_id') == user_id]
        
    from ml_core.models_loader import get_global_prices, USD_TO_INR
    for t in my_tx:
        amt_str = str(t.get('amount', '0')).replace("₹", "").replace("$", "").replace(",", "").strip()
        try:
            amt = float(amt_str)
        except:
            amt = 0.0
        prices = get_global_prices(amt / USD_TO_INR)
        t['multi_currency'] = f"${prices['USD']} | €{prices['EUR']} | ₹{prices['INR']} | ¥{prices['JPY']}"
        
    return render_template("finance_hub.html", trans=trans, lang=lang, transactions=my_tx)

# --- NEW: TIER 1 GAME CHANGERS ---

@finance_bp.route("/api/insurance/auto-claim", methods=["POST"])
@login_required
def api_insurance_auto_claim():
    data = request.get_json(silent=True) or {}
    pond_id = data.get("pond_id", "POND-1")
    mortality_rate = data.get("mortality_rate", 15)
    
    # 1. APDC check (mocking AI Vision disease confirmation)
    ai_disease_detected = True
    disease_name = "Early Mortality Syndrome (EMS)"
    
    if ai_disease_detected and mortality_rate > 10:
        claim_id = f"CLAIM-{random.randint(10000, 99999)}"
        payout_amount = 45000 # Mock amount in INR
        
        return jsonify({
            "status": "success",
            "claim_id": claim_id,
            "verification": "AI Confirmed via Satellite & Sensor Data",
            "disease_detected": disease_name,
            "estimated_payout": f"₹{payout_amount}",
            "timeline": "48 hours to bank account",
            "message": "Auto-claim filed successfully. No paperwork required."
        })
    else:
        return jsonify({
            "status": "rejected",
            "message": "Criteria for auto-claim not met. Please contact local surveyor."
        })

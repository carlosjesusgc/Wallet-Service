from flask import Blueprint, request, jsonify
from models.wallet_model import Wallet
from services.db_service import db
from decimal import Decimal

wallet_bp = Blueprint("wallet", __name__)

@wallet_bp.route("/<user_id>", methods=["GET"])
def get_wallet(user_id):
    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        return jsonify({"error": "Wallet not found"}), 404
    return jsonify({"user_id": wallet.user_id, "balance": float(wallet.balance)})

@wallet_bp.route("/<user_id>/add", methods=["POST"])
def add_savings(user_id):
    try:
        data = request.json
        amount = Decimal(str(data.get("amount", 0)))

        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            wallet = Wallet(user_id=user_id, balance=amount)
            db.session.add(wallet)
            message = "Wallet created and savings added"
        else:
            wallet.balance += amount
            message = "Savings updated"

        db.session.commit()

        return jsonify({"message": message, "balance": float(wallet.balance)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wallet_bp.route("/<user_id>/deduct", methods=["POST"])
def deduct_savings(user_id):
    try:
        data = request.json
        amount = Decimal(str(data.get("amount", 0)))

        wallet = Wallet.query.filter_by(user_id=user_id).first()

        wallet.balance -= amount
        message = "Savings deduct"

        db.session.commit()

        return jsonify({"message": message, "balance": float(wallet.balance)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
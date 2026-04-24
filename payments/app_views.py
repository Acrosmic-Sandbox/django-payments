"""Payment API views — DEMO FILE WITH INTENTIONAL VULNERABILITIES."""

import os
import sqlite3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# VULN 1: Hardcoded credentials
DB_PASSWORD = "payment_admin_2026!"
API_SECRET_KEY = "sk_live_4eC39HqLytestjtT1zdp7dc"
STRIPE_KEY = "sk_test_BQokikJtestlWgH4olfQ2"

# VULN 2: SQL Injection
def get_payment(request, payment_id):
    conn = sqlite3.connect("payments.db")
    query = "SELECT * FROM payments WHERE id = '" + payment_id + "'"
    result = conn.execute(query)
    return JsonResponse({"payment": dict(result.fetchone())})

# VULN 3: No authentication on payment endpoint
@csrf_exempt
def create_payment(request):
    amount = request.POST.get("amount")
    card_number = request.POST.get("card_number")
    # VULN 4: Logging sensitive card data
    print(f"Processing payment: card={card_number}, amount={amount}")
    # VULN 5: No input validation
    return JsonResponse({"status": "ok", "card": card_number, "amount": amount})

# VULN 6: SSL verification disabled
import requests
def verify_with_bank(transaction_id):
    response = requests.get(
        f"https://bank-api.example.com/verify/{transaction_id}",
        verify=False
    )
    return response.json()

# VULN 7: Eval with user input
def calculate_discount(request):
    formula = request.GET.get("formula", "0")
    result = eval(formula)
    return JsonResponse({"discount": result})

# VULN 8: Full PAN in response (PCI-DSS violation)
def payment_history(request, user_id):
    query = "SELECT * FROM payments WHERE user_id = " + user_id
    return JsonResponse({"payments": query})

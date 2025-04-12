
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import re
import google.generativeai as genai
import time

app = Flask(__name__)
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Base prompt
base_prompt = """
Who are you?
You are a world class model for predicting intent on online banking queries. 

What inputs will you get?
Your input will contain a text
text: a string feature.

What output should you give?
label: One of classification labels (0-76) corresponding to unique intents.
Intent names are mapped to label in the following way:

label intent (category)
0 activate_my_card
1 age_limit
2 apple_pay_or_google_pay
3 atm_support
4 automatic_top_up
5 balance_not_updated_after_bank_transfer
6 balance_not_updated_after_cheque_or_cash_deposit
7 beneficiary_not_allowed
8 cancel_transfer
9 card_about_to_expire
10 card_acceptance
11 card_arrival
12 card_delivery_estimate
13 card_linking
14 card_not_working
15 card_payment_fee_charged
16 card_payment_not_recognised
17 card_payment_wrong_exchange_rate
18 card_swallowed
19 cash_withdrawal_charge
20 cash_withdrawal_not_recognised
21 change_pin
22 compromised_card
23 contactless_not_working
24 country_support
25 declined_card_payment
26 declined_cash_withdrawal
27 declined_transfer
28 direct_debit_payment_not_recognised
29 disposable_card_limits
30 edit_personal_details
31 exchange_charge
32 exchange_rate
33 exchange_via_app
34 extra_charge_on_statement
35 failed_transfer
36 fiat_currency_support
37 get_disposable_virtual_card
38 get_physical_card
39 getting_spare_card
40 getting_virtual_card
41 lost_or_stolen_card
42 lost_or_stolen_phone
43 order_physical_card
44 passcode_forgotten
45 pending_card_payment
46 pending_cash_withdrawal
47 pending_top_up
48 pending_transfer
49 pin_blocked
50 receiving_money
51 Refund_not_showing_up
52 request_refund
53 reverted_card_payment?
54 supported_cards_and_currencies
55 terminate_account
56 top_up_by_bank_transfer_charge
57 top_up_by_card_charge
58 top_up_by_cash_or_cheque
59 top_up_failed
60 top_up_limits
61 top_up_reverted
62 topping_up_by_card
63 transaction_charged_twice
64 transfer_fee_charged
65 transfer_into_account
66 transfer_not_received_by_recipient
67 transfer_timing
68 unable_to_verify_identity
69 verify_my_identity
70 verify_source_of_funds
71 verify_top_up
72 virtual_card_not_working
73 visa_or_mastercard
74 why_verify_identity
75 wrong_amount_of_cash_received
76 wrong_exchange_rate_for_cash_withdrawal

What's the output format?

You should only respond with a label, enclosed in these tags <label_start> label  <label_end>
label should be an integer value from the above labels.

How to classify intent?
Use the knowledge and instruction given to you to make the best possible prediction.

"""

def extract_label(prediction):
    match = re.search(r"<label_start>\s*(\d+)\s*<label_end>", prediction)
    if match:
        return int(match.group(1))
    return -1

def get_prediction_from_gemini(user_query):
    prompt = base_prompt + f"\ntext: {user_query}\n"
    time.sleep(1)
    model = genai.GenerativeModel("models/gemini-2.0-flash-001")
    response = model.generate_content(prompt)
    return extract_label(response.text.strip())
label_to_intent = {
    0: "activate_my_card",
    1: "age_limit",
    2: "apple_pay_or_google_pay",
    3: "atm_support",
    4: "automatic_top_up",
    5: "balance_not_updated_after_bank_transfer",
    6: "balance_not_updated_after_cheque_or_cash_deposit",
    7: "beneficiary_not_allowed",
    8: "cancel_transfer",
    9: "card_about_to_expire",
    10: "card_acceptance",
    11: "card_arrival",
    12: "card_delivery_estimate",
    13: "card_linking",
    14: "card_not_working",
    15: "card_payment_fee_charged",
    16: "card_payment_not_recognised",
    17: "card_payment_wrong_exchange_rate",
    18: "card_swallowed",
    19: "cash_withdrawal_charge",
    20: "cash_withdrawal_not_recognised",
    21: "change_pin",
    22: "compromised_card",
    23: "contactless_not_working",
    24: "country_support",
    25: "declined_card_payment",
    26: "declined_cash_withdrawal",
    27: "declined_transfer",
    28: "direct_debit_payment_not_recognised",
    29: "disposable_card_limits",
    30: "edit_personal_details",
    31: "exchange_charge",
    32: "exchange_rate",
    33: "exchange_via_app",
    34: "extra_charge_on_statement",
    35: "failed_transfer",
    36: "fiat_currency_support",
    37: "get_disposable_virtual_card",
    38: "get_physical_card",
    39: "getting_spare_card",
    40: "getting_virtual_card",
    41: "lost_or_stolen_card",
    42: "lost_or_stolen_phone",
    43: "order_physical_card",
    44: "passcode_forgotten",
    45: "pending_card_payment",
    46: "pending_cash_withdrawal",
    47: "pending_top_up",
    48: "pending_transfer",
    49: "pin_blocked",
    50: "receiving_money",
    51: "Refund_not_showing_up",
    52: "request_refund",
    53: "reverted_card_payment?",
    54: "supported_cards_and_currencies",
    55: "terminate_account",
    56: "top_up_by_bank_transfer_charge",
    57: "top_up_by_card_charge",
    58: "top_up_by_cash_or_cheque",
    59: "top_up_failed",
    60: "top_up_limits",
    61: "top_up_reverted",
    62: "topping_up_by_card",
    63: "transaction_charged_twice",
    64: "transfer_fee_charged",
    65: "transfer_into_account",
    66: "transfer_not_received_by_recipient",
    67: "transfer_timing",
    68: "unable_to_verify_identity",
    69: "verify_my_identity",
    70: "verify_source_of_funds",
    71: "verify_top_up",
    72: "virtual_card_not_working",
    73: "visa_or_mastercard",
    74: "why_verify_identity",
    75: "wrong_amount_of_cash_received",
    76: "wrong_exchange_rate_for_cash_withdrawal"
}

@app.route("/predict-intent", methods=["POST"])
def predict_intent():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    label = get_prediction_from_gemini(query)
    intent = label_to_intent.get(label, "Unknown")

    return jsonify({"label": label,
                    "intent": intent
                    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, request, render_template, redirect,session
from forex_python.converter import CurrencyRates, CurrencyCodes,RatesNotAvailableError
from decimal import Decimal
app = Flask(__name__)
app.config["SECRET_KEY"] = "my-precious"


errors = []
@app.route('/currency')
def currency_home():
    return render_template("currency.html", errors = errors)
 

@app.route('/changed', methods=["POST"])
def currency_exchange():
    #first grab the user input values with request.form
    convert_f = request.form["convertingf"].upper()
    convert_t = request.form["convertingt"].upper()
    request_amount = request.form["amount"].upper()
    c = CurrencyRates()
    errors.clear()
    #clear error array so that we start the page fresh
    CurrCode = CurrencyCodes()
    try:
        float(request_amount)
    except ValueError:
        errors.append("Not a valid amount")
        request_amount= 0.0
    #checks to see if the amount is a float type, otherwise adds error and sets value to 0
    try:
        convert = c.get_rates(convert_f)
    except RatesNotAvailableError:
            errors.append(f"Not a valid code: {convert_f}")
    try:
        convert2 = c.get_rates(convert_t)
    except RatesNotAvailableError:
            errors.append(f"Not a valid code: {convert_t}")
    #these two trys check to see if any rates come up with the user input.  If none come up, it appends the error to the error array.
    print(errors)
    if errors:
        return redirect('/currency')
    #redirects us to the main page if any error was present and prints them in a list at the top
    exchange = round(c.convert(convert_f,convert_t, Decimal(request_amount)),2)
    symbol = CurrCode.get_symbol(convert_t)
    return render_template("currency.html", exchange = exchange, error_msg = errors, symbol = symbol, converted_f=convert_f,converted_t=convert_t,amount=request_amount)
    


from flask import Flask, request, render_template
from forex_python.converter import CurrencyRates
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
debug = DebugToolbarExtension(app)


@app.route('/')
def currency_exchange():
    convert_from = request.json["converting-from"].upper()
    convert_to = request.json["converting-to"].upper()
    request_amount = request.json["amount"].upper()
    c = CurrencyRates()
    c.convert(convert_from,convert_to, request_amount)
    errors = []
    """if convert_from not in forex_list
        errors.append("Not a valid code: convert_from")
    if convert_to not in forex_list
        errors.append("Not a valid code: convert_to")
    if type(request_amount) is not int
        errors.append("Not a valid amount")
        """
    symbol = c.get_symbol(convert_to)
    exhange = c.convert(convert_from,convert_to, request_amount)



    return render_template("currency.html", exchange = exchange, error_msg = errors)

import json
from datetime import datetime, timedelta

# uses the scipy library to calculate the XIRR
from scipy.optimize import newton

# Load the transaction JSON file
file_path = 'transaction_detail.json'

with open(file_path, 'r') as f:
    data = json.load(f)


# To get todays date and use it for NAV calculation
def get_today():
    return datetime.now().strftime('%d-%b-%Y')


# To parse transaction data and calculate units based on FIFO
def process_transactions(transactions):
    holdings = {}

    for trxn in transactions:
        scheme = trxn['scheme']
        folio = trxn['folio']
        units = float(trxn['trxnUnits'])
        amount = float(trxn['trxnAmount'])
        price = float(trxn['purchasePrice']) if trxn['purchasePrice'] else 0

        # Use a key combination of scheme and folio to track transactions at folio level (FIFO)
        key = (scheme, folio)

        if key not in holdings:
            holdings[key] = {'units': 0, 'transactions': []}

        # FIFO logic: If positive = a purchase, if negative = a sale
        if units > 0:
            holdings[key]['transactions'].append({
                'units': units,
                'price': price,
                'amount': amount,
                'date': trxn['trxnDate']
            })
            holdings[key]['units'] += units
        else:
            remaining_sale_units = abs(units)
            while remaining_sale_units > 0 and holdings[key]['transactions']:
                first_purchase = holdings[key]['transactions'][0]
                if first_purchase['units'] <= remaining_sale_units:
                    remaining_sale_units -= first_purchase['units']
                    holdings[key]['transactions'].pop(0)
                else:
                    first_purchase['units'] -= remaining_sale_units
                    remaining_sale_units = 0
            holdings[key]['units'] += units

    return holdings


# To calculate total portfolio value based on the latest NAV
def calculate_portfolio_value(holdings, dt_summary):
    total_value = 0
    for scheme, folio_data in holdings.items():
        scheme_code = scheme[0]
        for summary in dt_summary:
            if summary['scheme'] == scheme_code:
                nav = float(summary['nav'])
                value = folio_data['units'] * nav
                total_value += value
                break
    return total_value


# To calculate portfolio gain
def calculate_portfolio_gain(holdings, dt_summary):
    total_gain = 0
    print("Net Units and Value for Each Fund:")
    for scheme, folio_data in holdings.items():
        scheme_code = scheme[0]
        acquisition_cost = 0
        for summary in dt_summary:
            if summary['scheme'] == scheme_code:
                nav = float(summary['nav'])
                current_value = folio_data['units'] * nav
                acquisition_cost = sum([trxn['price'] * trxn['units'] for trxn in folio_data['transactions']])
                total_gain += (current_value - acquisition_cost)

                print(f"Scheme: {summary['schemeName']}")
                print(f" - Remaining Units: {folio_data['units']:.3f}")
                print(f" - Net Value as of Today: ₹{current_value:.2f}\n")

                break
    return total_gain


# To calculate XIRR
def xirr(cashflows):
    def npv(rate):
        total = 0.0
        for cf in cashflows:
            days = (cf['date'] - cashflows[0]['date']).days
            total += cf['amount'] / (1 + rate) ** (days / 365.0)
        return total

    return newton(npv, 0.1)


# Update the XIRR calculation using scipy's newton method
def calculate_xirr(holdings, total_portfolio_value):
    cashflows = []
    for scheme, folio_data in holdings.items():
        for trxn in folio_data['transactions']:
            cashflows.append({'date': datetime.strptime(trxn['date'], '%d-%b-%Y'), 'amount': -trxn['amount']})

    cashflows.append({'date': datetime.now(), 'amount': total_portfolio_value})

    xirr_value = xirr(cashflows)

    return xirr_value



# Main processing
dt_transaction = data['data'][0]['dtTransaction']
dt_summary = data['data'][0]['dtSummary']

holdings = process_transactions(dt_transaction)
total_portfolio_value = calculate_portfolio_value(holdings, dt_summary)
total_portfolio_gain = calculate_portfolio_gain(holdings, dt_summary)
xirr_value = calculate_xirr(holdings, total_portfolio_value)

# Print total portfolio value, gain, and XIRR
print(f"Total Portfolio Value: ₹{total_portfolio_value:.2f}")
print(f"Total Portfolio Gain: ₹{total_portfolio_gain:.2f}")
print(f"XIRR: {xirr_value:.2%}")

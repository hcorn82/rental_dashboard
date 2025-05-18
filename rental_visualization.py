import streamlit as st

st.title("Beach Haven Rental Profitability Calculator")

# Inputs
purchase_price = st.slider("Purchase Price ($)", 500000, 5000000, 2500000, step=50000, format="$%s")
down_payment = st.slider("Down Payment ($)", 100000, int(purchase_price), int(purchase_price * 0.25), step=25000, format="$%s")
loan = purchase_price - down_payment

weekly_rent = st.slider("Peak Season Weekly Rent ($)", 10000, 30000, 15000, step=500, format="$%s")
weeks_rented = st.slider("Peak Weeks Rented", 8, 16, 11, format="%d weeks")

# Shoulder season sliders
shoulder_nights = st.slider("Shoulder Season Nights Booked", 0, 60, 20, format="%d nights")
shoulder_rate = st.slider("Shoulder Nightly Rate ($)", 800, 4000, 1000, step=50, format="$%s")

# Format currency display with commas
def format_currency(value):
    return f"${value:,.0f}"

# Constants for fixed expense components
mortgage_rate_factor = 0.075
mortgage = loan * mortgage_rate_factor
property_tax = 0.0159 * purchase_price
insurance = 0.005 * purchase_price
maintenance = 0.01 * purchase_price
management = 0.005 * purchase_price
utilities_other = 0.004 * purchase_price  # 0.4% of purchase price

# Calculate total expenses and breakdown
expense_breakdown = {
    "Mortgage": mortgage,
    "Property Tax": property_tax,
    "Insurance": insurance,
    "Maintenance": maintenance,
    "Management": management,
    "Utilities & Other": utilities_other
}
total_expenses = sum(expense_breakdown.values())

# Rental income breakdown
summer_income = weekly_rent * weeks_rented
shoulder_income = shoulder_nights * shoulder_rate
total_income = summer_income + shoulder_income
total_nights_rented = (weeks_rented * 7) + shoulder_nights

# Cash flow calculation
cash_flow = total_income - total_expenses
ltr = round(loan / total_income, 2)

# ROI
roi = (cash_flow / down_payment) * 100

# Tax deductions
structure_value = 0.85 * purchase_price
annual_depreciation = round(structure_value / 27.5)
mortgage_interest = round(mortgage * 0.68)
closing_costs = 0.02 * purchase_price
total_deductions = annual_depreciation + mortgage_interest + closing_costs

# Outputs - Income and Expenses
st.subheader("Income Summary")
st.metric("Summer Rental Income", format_currency(summer_income))
st.metric("Shoulder Season Income", format_currency(shoulder_income))
st.metric("Total Rental Income", format_currency(total_income))
st.metric("Total Nights Rented", total_nights_rented)

st.subheader("Expense Breakdown")
col1, col2 = st.columns(2)
with col1:
    for category in list(expense_breakdown.keys())[:3]:
        st.metric(category, format_currency(expense_breakdown[category]))
with col2:
    for category in list(expense_breakdown.keys())[3:]:
        st.metric(category, format_currency(expense_breakdown[category]))
st.write(f"**Total Expenses:** {format_currency(total_expenses)}")

st.subheader("Cash Flow Summary")
st.metric("Net Cash Flow", format_currency(cash_flow))
st.metric("Loan-to-Rent Ratio", ltr)
st.metric("Down Payment", format_currency(down_payment))
st.metric("Loan Amount", format_currency(loan))

if cash_flow > 0:
    st.success("Positive Cash Flow!")
elif cash_flow < 0:
    st.error("Negative Cash Flow")
else:
    st.info("Break-even Cash Flow")

# ROI
st.subheader("Investment Metrics")
st.metric("ROI (Cash-on-Cash)", f"{roi:.2f}%")

# Tax deduction summary
st.subheader("Estimated Tax Write-Offs")
st.write(f"Annual Depreciation: {format_currency(annual_depreciation)}")
st.write(f"Mortgage Interest (Yr 1 est.): {format_currency(mortgage_interest)}")
st.write(f"Estimated Closing Costs: {format_currency(closing_costs)}")
st.write(f"Total Potential Deductions: {format_currency(total_deductions)}")

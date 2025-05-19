import streamlit as st

st.title("Beach Haven Rental Profitability Calculator")

# Inputs
purchase_price = st.slider("Purchase Price ($)", 500000, 5000000, 2500000, step=50000, format="$%s")
down_payment = st.slider("Down Payment ($)", 100000, int(purchase_price), int(purchase_price * 0.25), step=25000, format="$%s")
loan = purchase_price - down_payment

weekly_rent = st.slider("Peak Season Weekly Rent ($)", 5000, 30000, 15000, step=1000, format="$%s")
weeks_rented = st.slider("Peak Weeks Rented", 8, 16, 11, format="%d weeks")

# Shoulder season sliders
shoulder_nights = st.slider("Shoulder Season Nights Booked", 0, 60, 20, format="%d nights")
shoulder_rate = st.slider("Shoulder Nightly Rate ($)", 800, 4000, 1000, step=50, format="$%s")

# Format currency display
def format_currency(value):
    return f"${value:,.0f}"

# Constants for fixed expenses
mortgage_rate_factor = 0.075  # Approximate annual mortgage cost
mortgage = loan * mortgage_rate_factor
property_tax = 0.0159 * purchase_price
insurance = 0.005 * purchase_price
maintenance = 0.01 * purchase_price
management = 0.005 * purchase_price
utilities_other = 0.004 * purchase_price  # 0.4% of purchase price

# Expense breakdown dictionary
expense_breakdown = {
    "Mortgage": mortgage,
    "Property Tax": property_tax,
    "Insurance": insurance,
    "Maintenance": maintenance,
    "Management": management,
    "Utilities & Other": utilities_other
}
total_expenses = sum(expense_breakdown.values())

# Income calculations
summer_income = weekly_rent * weeks_rented
shoulder_income = shoulder_nights * shoulder_rate
total_income = summer_income + shoulder_income
total_nights_rented = (weeks_rented * 7) + shoulder_nights
cash_flow = total_income - total_expenses
ltr = round(loan / total_income, 2)

# Tax deduction estimates
structure_value = 0.85 * purchase_price
annual_depreciation = round(structure_value / 27.5)
mortgage_interest = round(mortgage * 0.68)
closing_costs = 0.02 * purchase_price
total_deductions = annual_depreciation + mortgage_interest + closing_costs

# 🔹 Year 1 Net Cash Flow after Closing Costs
year1_net_cash_flow = cash_flow - closing_costs

# Cash Flow Summary + Income Summary in one row
st.subheader("Financial Performance Overview")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Cash Flow Summary")
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

with col2:
    st.markdown("### Income Summary")
    st.metric("Summer Rental Income", format_currency(summer_income))
    st.metric("Shoulder Season Income", format_currency(shoulder_income))
    st.metric("Total Rental Income", format_currency(total_income))
    st.metric("Total Nights Rented", total_nights_rented)

# Year 1 net position
st.subheader("Year 1 Net Cash Position")
st.metric("Estimated Closing Costs", format_currency(closing_costs))
st.metric("Net Cash Flow After Closing", format_currency(year1_net_cash_flow))

if year1_net_cash_flow > 0:
    st.success("Positive Year 1 Net Cash Flow!")
elif year1_net_cash_flow < 0:
    st.error("Negative Year 1 Net Cash Flow")
else:
    st.info("Year 1 Cash Flow Break-Even")

# Expense Breakdown and Tax Write-Offs side by side with matching style
st.subheader("Detailed Financial Breakdown")
col_exp, col_tax = st.columns(2)

with col_exp:
    st.markdown("### Expense Breakdown")
    for category, amount in expense_breakdown.items():
        st.markdown(f"""
            <div style='margin-bottom: 0.5rem; font-size: 1.2rem;'>
                <strong>{category}</strong><br>
                <span style='font-size: 1.8rem;'>${amount:,.0f}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='margin-top: 1rem; font-size: 1.3rem;'>
            <strong>Total Expenses:</strong>
            <span style='font-size: 1.8rem; color: #ffffff; display: block;'>${total_expenses:,.0f}</span>
        </div>
    """, unsafe_allow_html=True)

with col_tax:
    st.markdown("### Estimated Tax Write-Offs")
    st.markdown(f"""
        <div style='font-size: 1.2rem; margin-bottom: 0.5rem;'><strong>Annual Depreciation:</strong> ${annual_depreciation:,.0f}</div>
        <div style='font-size: 1.2rem; margin-bottom: 0.5rem;'><strong>Mortgage Interest (Yr 1 est.):</strong> ${mortgage_interest:,.0f}</div>
        <div style='font-size: 1.2rem; margin-bottom: 0.5rem;'><strong>Estimated Closing Costs:</strong> ${closing_costs:,.0f}</div>
        <div style='font-size: 1.4rem; margin-top: 1rem;'><strong>Total Potential Deductions:</strong> ${total_deductions:,.0f}</div>
    """, unsafe_allow_html=True)

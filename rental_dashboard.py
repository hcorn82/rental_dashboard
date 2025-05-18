import streamlit as st

st.title("Beach Haven Rental Profitability Calculator")

# Inputs
loan = st.slider("Loan Amount ($)", 700000, 1200000, 850000, step=25000, format="$%d")
weekly_rent = st.slider("Peak Season Weekly Rent ($)", 10000, 30000, 15000, step=500, format="$%d")
weeks_rented = st.slider("Peak Weeks Rented", 8, 16, 11, format="%d weeks")

# Shoulder season sliders
shoulder_nights = st.slider("Shoulder Season Nights Booked", 0, 60, 20, format="%d nights")
shoulder_rate = st.slider("Shoulder Nightly Rate ($)", 300, 1500, 1000, step=50, format="$%d")

# Constants
fixed_expenses = 90000  # Tax, insurance, maintenance, mgmt
mortgage_rate_factor = 0.075  # Approximate annualized debt service cost

total_rent_income = (weekly_rent * weeks_rented) + (shoulder_nights * shoulder_rate)
mortgage = loan * mortgage_rate_factor
total_expenses = mortgage + fixed_expenses
cash_flow = total_rent_income - total_expenses
ltr = round(loan / total_rent_income, 2)

# Estimate tax write-offs
structure_value = 0.85 * (loan + (1200000 if loan < 1200000 else 1500000))  # estimate structure value as 85% of property
annual_depreciation = round(structure_value / 27.5)
mortgage_interest = round(mortgage * 0.68)  # Rough 68% of mortgage is interest in early years
closing_costs = 0.02 * (loan + (1200000 if loan < 1200000 else 1500000))  # estimate 2% of price

total_deductions = annual_depreciation + mortgage_interest + closing_costs

# Outputs
st.metric("Loan-to-Rent Ratio", ltr)
st.metric("Total Rental Income", f"${total_rent_income:,.0f}")
st.metric("Total Expenses", f"${total_expenses:,.0f}")
st.metric("Net Cash Flow", f"${cash_flow:,.0f}")

# Cash flow color status
if cash_flow > 0:
    st.success("Positive Cash Flow!")
elif cash_flow < 0:
    st.error("Negative Cash Flow")
else:
    st.info("Break-even Cash Flow")

# Tax deduction summary
st.subheader("Estimated Tax Write-Offs")
st.write(f"Annual Depreciation: ${annual_depreciation:,.0f}")
st.write(f"Mortgage Interest (Yr 1 est.): ${mortgage_interest:,.0f}")
st.write(f"Estimated Closing Costs: ${closing_costs:,.0f}")
st.write(f"Total Potential Deductions: ${total_deductions:,.0f}")

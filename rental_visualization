import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Beach Haven Rental Profitability Calculator")

# Inputs
loan = st.slider("Loan Amount ($)", 300000, 2500000, 850000, step=25000, format="$%s")
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
property_tax = 0.0159 * loan
insurance = 0.005 * loan
maintenance = 0.01 * loan
management = 0.005 * loan
utilities_other = 10000

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

# Tax deductions
structure_value = 0.85 * (loan + (1200000 if loan < 1200000 else 1500000))
annual_depreciation = round(structure_value / 27.5)
mortgage_interest = round(mortgage * 0.68)
closing_costs = 0.02 * (loan + (1200000 if loan < 1200000 else 1500000))
total_deductions = annual_depreciation + mortgage_interest + closing_costs

# Outputs - Income and Expenses
st.subheader("Income Summary")
st.metric("Summer Rental Income", format_currency(summer_income))
st.metric("Shoulder Season Income", format_currency(shoulder_income))
st.metric("Total Rental Income", format_currency(total_income))
st.metric("Total Nights Rented", total_nights_rented)

st.subheader("Expense Breakdown")
for category, amount in expense_breakdown.items():
    st.write(f"{category}: {format_currency(amount)}")
st.write(f"Total Expenses: {format_currency(total_expenses)}")

st.subheader("Cash Flow Summary")
st.metric("Net Cash Flow", format_currency(cash_flow))
st.metric("Loan-to-Rent Ratio", ltr)

if cash_flow > 0:
    st.success("Positive Cash Flow!")
elif cash_flow < 0:
    st.error("Negative Cash Flow")
else:
    st.info("Break-even Cash Flow")

# Tax deduction summary
st.subheader("Estimated Tax Write-Offs")
st.write(f"Annual Depreciation: {format_currency(annual_depreciation)}")
st.write(f"Mortgage Interest (Yr 1 est.): {format_currency(mortgage_interest)}")
st.write(f"Estimated Closing Costs: {format_currency(closing_costs)}")
st.write(f"Total Potential Deductions: {format_currency(total_deductions)}")

# Visualization - Pie chart for expenses
st.subheader("Expense Allocation Chart")
fig1, ax1 = plt.subplots()
ax1.pie(expense_breakdown.values(), labels=expense_breakdown.keys(), autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Visualization - Bar chart for cash flow vs income vs expenses
st.subheader("Income vs. Expenses vs. Cash Flow")
data = pd.DataFrame({
    'Category': ['Total Income', 'Total Expenses', 'Net Cash Flow'],
    'Amount': [total_income, total_expenses, cash_flow]
})
fig2, ax2 = plt.subplots()
colors = ['#4caf50', '#f44336', '#2196f3']
ax2.bar(data['Category'], data['Amount'], color=colors)
ax2.set_ylabel('Amount ($)')
ax2.set_title('Financial Overview')
st.pyplot(fig2)

import streamlit as st

st.set_page_config(page_title="Salary Calculator", page_icon="💰", layout="centered")

st.title("💰 Salary Calculator")
st.write("Enter your basic salary below to calculate the total amount with a 10% bonus.")

basic_salary = st.number_input("Enter Basic Salary:", min_value=0.0, format="%.2f")

if st.button("Calculate Total", type="primary"):
    total = basic_salary + (basic_salary * 0.10)
    st.success(f"**Total Salary (with 10% bonus):** {total:,.2f}")

st.markdown("---")
st.caption("Designed with Streamlit | Web App")

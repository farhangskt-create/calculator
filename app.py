import streamlit as st

st.set_page_config(page_title="Punjab Govt Salary Comparison App", page_icon="📊", layout="wide")

st.title("📊 Punjab Government Salary Comparison & Calculator")
st.write("Compare your salary according to the latest Punjab Government notification and allowances.")

st.sidebar.header("Input Salary Details")
basic_salary = st.sidebar.number_input("Enter Basic Salary:", min_value=0.0, value=50000.0, format="%.2f")

# فرضی یا نوٹیفیکیشن کے حساب سے الاؤنسز کا حساب
dearness_allowance = basic_salary * 0.35  # مثال کے طور پر 35% ڈیئرنس الاؤنس
house_rent = basic_salary * 0.45         # ہاؤس رینٹ الاؤنس
medical_allowance = 1500.0               # میڈیکل الاؤنس

total_salary = basic_salary + dearness_allowance + house_rent + medical_allowance

st.subheader("📋 Salary Breakdown & Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Previous / Basic Structure")
    st.metric(label="Basic Pay", value=f"Rs. {basic_salary:,.2f}")
    st.metric(label="Medical Allowance", value=f"Rs. {medical_allowance:,.2f}")

with col2:
    st.markdown("### Revised Notification Structure")
    st.metric(label="Estimated Dearness Allowance", value=f"Rs. {dearness_allowance:,.2f}")
    st.metric(label="House Rent Allowance", value=f"Rs. {house_rent:,.2f}")

st.markdown("---")
st.success(f"### 💰 Total Estimated Revised Salary: Rs. {total_salary:,.2f}")

st.info("Note: You can easily adjust the formula percentages in the code anytime according to the exact notification details.")

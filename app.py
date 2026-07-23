import streamlit as st
import pandas as pd

st.set_page_config(page_title="Punjab Pay & Allowances Comparison Statement", page_icon="📊", layout="wide")

st.markdown("<h2 style='text-align: center;'>PAY & ALLOWANCES COMPARISON STATEMENT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Government of the Punjab - Revised Basic Pay Scales 2026</b></p>", unsafe_allow_html=True)

# سائیڈ بار ان پٹس
st.sidebar.header("Employee Pay Inputs")
bps_grade = st.sidebar.selectbox("Select BPS Grade:", list(range(1, 23)), index=14) # ڈیفالٹ BPS-15
stage_no = st.sidebar.number_input("Enter Stage No:", min_value=1, max_value=30, value=10)
existing_basic = st.sidebar.number_input("Enter Existing Basic Pay (June 2026):", min_value=0.0, value=43720.00, format="%.2f")
is_disabled = st.sidebar.checkbox("Are you a Disabled Employee? (Special Conveyance)")

# پروفیشنل اور حقیقت پسندانہ خودکار حساب (موجودہ بیسک میں پوائنٹ ٹو پوائنٹ یا تخمینہ اضافہ)
revised_basic = existing_basic * 1.201

adhoc_2022_15 = 3615.00
adhoc_2025_10 = 4372.00
adhoc_2026_new = revised_basic * 0.07

# کنویئنس الاؤنس کا حساب
if is_disabled:
    special_conv_exist = 6000.00
    special_conv_revised = 10000.00
    conv_label = "Special Conveyance Allowance"
else:
    if bps_grade <= 4:
        special_conv_exist, special_conv_revised = 1785.00, 2678.00
    elif bps_grade <= 10:
        special_conv_exist, special_conv_revised = 1932.00, 2898.00
    elif bps_grade <= 15:
        special_conv_exist, special_conv_revised = 2856.00, 4284.00
    else:
        special_conv_exist, special_conv_revised = 5000.00, 7500.00
    conv_label = f"Conveyance Allowance (BPS {bps_grade})"

house_rent = 3524.00
personal_allowance = 1580.00
special_allow_2021 = 4030.00
special_all_15_22 = 3615.00
adhoc_2023 = 13223.00
adhoc_2024 = 10930.00
medical_allowance = 1500.00

# ٹوٹل گراس پے کا حساب
total_existing = (existing_basic + adhoc_2022_15 + adhoc_2025_10 + special_conv_exist + 
                  house_rent + personal_allowance + special_allow_2021 + special_all_15_22 + 
                  adhoc_2023 + adhoc_2024 + medical_allowance)

total_revised = (revised_basic + adhoc_2026_new + special_conv_revised + 
                 house_rent + personal_allowance + special_allow_2021 + special_all_15_22 + 
                 adhoc_2023 + adhoc_2024 + medical_allowance)

diff_total = total_revised - total_existing

# گراس پے کا موازنہ ٹیبل
data_gross = {
    "Pay & Allowances Details": [
        f"Basic Pay (BPS-{bps_grade} Stage {stage_no})",
        "Adhoc Relief 2022 (15%)",
        "Adhoc Relief 2025 (10%)",
        "Adhoc Relief 2026 (7% New)",
        conv_label,
        "House Rent Allowance 45%",
        "Personal Allowance",
        "Special Allow 2021 25%",
        "Special All 15% 22 (PS17)",
        "Adhoc Relief 2023 (35% Frozen)",
        "Adhoc Relief 2024 (25% Frozen)",
        "Medical Allowance",
        "TOTAL GROSS PAY"
    ],
    "Existing Pay (June 2026)": [
        f"Rs. {existing_basic:,.2f}",
        f"Rs. {adhoc_2022_15:,.2f}",
        f"Rs. {adhoc_2025_10:,.2f}",
        "Rs. 0.00",
        f"Rs. {special_conv_exist:,.2f}",
        f"Rs. {house_rent:,.2f}",
        f"Rs. {personal_allowance:,.2f}",
        f"Rs. {special_allow_2021:,.2f}",
        f"Rs. {special_all_15_22:,.2f}",
        f"Rs. {adhoc_2023:,.2f}",
        f"Rs. {adhoc_2024:,.2f}",
        f"Rs. {medical_allowance:,.2f}",
        f"Rs. {total_existing:,.2f}"
    ],
    "Difference (Change)": [
        f"+ Rs. {revised_basic - existing_basic:,.2f}",
        f"- Rs. {adhoc_2022_15:,.2f}",
        f"- Rs. {adhoc_2025_10:,.2f}",
        f"+ Rs. {adhoc_2026_new:,.2f}",
        f"+ Rs. {special_conv_revised - special_conv_exist:,.2f}",
        "Rs. 0.00", "Rs. 0.00", "Rs. 0.00", "Rs. 0.00", "Rs. 0.00", "Rs. 0.00", "Rs. 0.00",
        f"+ Rs. {diff_total:,.2f}"
    ],
    "Revised Pay (BPS-2026)": [
        f"Rs. {revised_basic:,.2f}",
        "Rs. 0 (Merged)",
        "Rs. 0 (Merged)",
        f"Rs. {adhoc_2026_new:,.2f}",
        f"Rs. {special_conv_revised:,.2f}",
        f"Rs. {house_rent:,.2f}",
        f"Rs. {personal_allowance:,.2f}",
        f"Rs. {special_allow_2021:,.2f}",
        f"Rs. {special_all_15_22:,.2f}",
        f"Rs. {adhoc_2023:,.2f}",
        f"Rs. {adhoc_2024:,.2f}",
        f"Rs. {medical_allowance:,.2f}",
        f"Rs. {total_revised:,.2f}"
    ]
}

st.subheader("1. Gross Pay Comparison")
df_gross = pd.DataFrame(data_gross)
st.table(df_gross)

# کٹوتیاں (Deductions) الگ سے ظاہر کرنا
income_tax = 461.00
gp_fund = 4290.00
benevolent_fund = 1312.00
group_insurance = 149.00
total_deductions = income_tax + gp_fund + benevolent_fund + group_insurance

net_existing = total_existing - total_deductions
net_revised = total_revised - total_deductions
net_diff = net_revised - net_existing

data_deductions = {
    "Mandatory Deductions": [
        "Income Tax",
        "GP Fund Subscription",
        "Benevolent Fund",
        "Group Insurance",
        "TOTAL DEDUCTIONS"
    ],
    "Amount": [
        f"Rs. {income_tax:,.2f}",
        f"Rs. {gp_fund:,.2f}",
        f"Rs. {benevolent_fund:,.2f}",
        f"Rs. {group_insurance:,.2f}",
        f"Rs. {total_deductions:,.2f}"
    ]
}

st.subheader("2. Mandatory Deductions")
df_deductions = pd.DataFrame(data_deductions)
st.table(df_deductions)

# نیٹ ٹیک ہوم پے سمری
st.subheader("3. Net Take-Home Pay Summary")
net_summary_data = {
    "Description": ["Existing Net Take-Home Pay", "Revised Net Take-Home Pay", "Net Monthly Advantage"],
    "Amount": [f"Rs. {net_existing:,.2f}", f"Rs. {net_revised:,.2f}", f"+ Rs. {net_diff:,.2f}"]
}
df_net = pd.DataFrame(net_summary_data)
st.table(df_net)

# ہائی لائٹس
st.markdown("### Key Highlights:")
st.markdown(f"- **Selected Grade & Stage:** BPS-{bps_grade}, Stage {stage_no} | **Disability Status:** {'Yes (Special Conveyance Rs. 10,000)' if is_disabled else 'No'}")
st.markdown("- **Basic Pay Scale Revision:** Adhoc Relief 2022 (15%) and 2025 (10%) are successfully merged into Basic Pay Scales.")
st.markdown(f"- **Net Take-Home Monthly Increase:** + Rs. {net_diff:,.2f}")

st.markdown("---")

# اسٹائلش پیغام
st.markdown("""
    <div style='padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='color: #1f77b4; margin: 0; font-family: sans-serif; letter-spacing: 1px;'>✨ BEST OF LUCK ✨</h2>
        <p style='margin: 8px 0 0 0; font-size: 18px; color: #2c3e50;'><b>BY M. FARHAN IQBAL</b></p>
    </div>
""", unsafe_allow_html=True)

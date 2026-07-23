import streamlit as st
import pandas as pd

st.set_page_config(page_title="Punjab Pay & Allowances Comparison Statement", page_icon="📊", layout="wide")

st.markdown("<h2 style='text-align: center;'>PAY & ALLOWANCES COMPARISON STATEMENT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Government of the Punjab - Revised Basic Pay Scales 2026</b></p>", unsafe_allow_html=True)

# سائیڈ بار میں ان پٹس (BPS، اسٹیج، بیسک پے، اور ڈس ایبلٹی کا آپشن)
st.sidebar.header("Employee Pay Inputs")
bps_grade = st.sidebar.selectbox("Select BPS Grade:", list(range(1, 23)), index=14) # ڈیفالٹ BPS-15
stage_no = st.sidebar.number_input("Enter Stage No:", min_value=1, max_value=30, value=10)
existing_basic = st.sidebar.number_input("Enter Existing Basic Pay (June 2026):", min_value=0.0, value=43720.00, format="%.2f")
revised_basic = st.sidebar.number_input("Enter Revised Basic Pay (BPS-2026):", min_value=0.0, value=52530.00, format="%.2f")
is_disabled = st.sidebar.checkbox("Are you a Disabled Employee? (Special Conveyance)")

adhoc_2022_15 = 3615.00
adhoc_2025_10 = 4372.00
adhoc_2026_new = revised_basic * 0.07  # نئے اسکیل کا 7%

# کنویئنس الاؤنس کا حساب ڈس ایبلٹی کے لحاظ سے
if is_disabled:
    special_conv_exist = 6000.00
    special_conv_revised = 10000.00  # نوٹیفیکیشن کے مطابق 6000 سے بڑھا کر 10000[cite: 1]
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

# ڈیٹا ٹیبل تیار کرنا
data = {
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

df = pd.DataFrame(data)
st.table(df)

# ہائی لائٹس
st.markdown("### Key Highlights:")
st.markdown(f"- **Selected Grade & Stage:** BPS-{bps_grade}, Stage {stage_no} | **Disability Status:** {'Yes (Special Conveyance Rs. 10,000)' if is_disabled else 'No'}[cite: 1]")
st.markdown("- **Basic Pay Scale Revision:** Adhoc Relief 2022 (15%) and 2025 (10%) are merged into Basic Pay Scales 2026[cite: 1].")
st.markdown("- **New Allowance:** Adhoc Relief Allowance 2026 @ 7% introduced on running New Basic Pay[cite: 1].")
st.markdown(f"- **Net Gross Monthly Increase:** + Rs. {diff_total:,.2f}")

st.markdown("---")
st.info("📌 **Note:** Actual net take-home pay will vary after mandatory deductions including Income Tax (e.g., Rs. 461), GP Fund Subscription (e.g., Rs. 4,290), Benevolent Fund (e.g., Rs. 1,312), Group Insurance (e.g., Rs. 149), and other departmental cuttings as per applicable government rules[cite: 2].")

# آخر میں آپ کا نام اور پیغام
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #2e6c80;'>Wish you best of luck! — <b>From Farhan Iqbal</b></h4>", unsafe_allow_html=True)

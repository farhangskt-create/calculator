import streamlit as st
import pandas as pd

st.set_page_config(page_title="Punjab Pay & Allowances Comparison 2026", page_icon="📊", layout="wide")

st.markdown("<h2 style='text-align: center;'>PAY & ALLOWANCES COMPARISON STATEMENT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Government of the Punjab - Revised Basic Pay Scales 2026</b></p>", unsafe_allow_html=True)

# سائیڈ بار میں یوزر سے ان پٹ لینا
st.sidebar.header("Employee Settings")
bps_grade = st.sidebar.selectbox("Select BPS Grade:", list(range(1, 23)), index=14) # ڈیفالٹ BPS-15
is_disabled = st.sidebar.checkbox("Are you a Disabled Employee? (Special Conveyance)")
existing_basic = st.sidebar.number_input("Existing Basic Pay (June 2026):", min_value=0.0, value=43720.0, format="%.2f")

# نوٹیفیکیشن کے مطابق بیسک پے اسکیل 2026 کے تخمینے (یا پوائنٹ ٹو پوائنٹ اضافہ تقریباً 20%)
# اسکیل کے لحاظ سے نیا بیسک پے طے کرنا
revised_basic = existing_basic * 1.20  # یا نوٹیفیکیشن کے اسکیل ٹیبل کے مطابق

# نوٹیفیکیشن کے رولز کے مطابق الاؤنسز
adhoc_2022_exist = existing_basic * 0.15
adhoc_2025_exist = existing_basic * 0.10
adhoc_2026_revised = revised_basic * 0.07

# سپیشل کنویئنس الاؤنس (صرف ڈس ایبل ہونے پر 10,000 ورنہ عام کنویئنس الاؤنس اسکیل کے مطابق)
if is_disabled:
    special_conv_exist = 6000.0
    special_conv_revised = 10000.0
    conv_label = "Special Conveyance Allowance"
else:
    # نوٹیفیکیشن کے مطابق گریڈ کے لحاظ سے کنویئنس الاؤنس
    if bps_grade <= 4:
        special_conv_exist, special_conv_revised = 1785.0, 2678.0
    elif bps_grade <= 10:
        special_conv_exist, special_conv_revised = 1932.0, 2898.0
    elif bps_grade <= 15:
        special_conv_exist, special_conv_revised = 2856.0, 4284.0
    else:
        special_conv_exist, special_conv_revised = 5000.0, 7500.0
    conv_label = f"Conveyance Allowance (BPS {bps_grade})"

adhoc_2023 = 13223.0  
adhoc_2024 = 10930.0  
other_fixed = 14249.0

# ٹوٹل گراس کا حساب
total_existing = existing_basic + adhoc_2022_exist + adhoc_2025_exist + special_conv_exist + adhoc_2023 + adhoc_2024 + other_fixed
total_revised = revised_basic + adhoc_2026_revised + special_conv_revised + adhoc_2023 + adhoc_2024 + other_fixed

diff_basic = revised_basic - existing_basic
diff_ad2022 = 0 - adhoc_2022_exist
diff_ad2025 = 0 - adhoc_2025_exist
diff_ad2026 = adhoc_2026_revised - 0
diff_conv = special_conv_revised - special_conv_exist
diff_total = total_revised - total_existing

# ڈیٹا ٹیبل بنانا
data = {
    "Pay & Allowances Details": [
        f"Basic Pay (BPS-{bps_grade})",
        "Adhoc Relief 2022 (15%)",
        "Adhoc Relief 2025 (10%)",
        "Adhoc Relief 2026 (7% New)",
        conv_label,
        "Adhoc Relief 2023 (35% Frozen)",
        "Adhoc Relief 2024 (25% Frozen)",
        "Other Fixed Allowances",
        "TOTAL GROSS PAY"
    ],
    "Existing Pay (June 2026)": [
        f"Rs. {existing_basic:,.2f}",
        f"Rs. {adhoc_2022_exist:,.2f}",
        f"Rs. {adhoc_2025_exist:,.2f}",
        "Rs. 0",
        f"Rs. {special_conv_exist:,.2f}",
        f"Rs. {adhoc_2023:,.2f}",
        f"Rs. {adhoc_2024:,.2f}",
        f"Rs. {other_fixed:,.2f}",
        f"Rs. {total_existing:,.2f}"
    ],
    "Difference (Change)": [
        f"+ Rs. {diff_basic:,.2f}",
        f"- Rs. {adhoc_2022_exist:,.2f}",
        f"- Rs. {adhoc_2025_exist:,.2f}",
        f"+ Rs. {diff_ad2026:,.2f}",
        f"+ Rs. {diff_conv:,.2f}",
        "Rs. 0",
        "Rs. 0",
        "Rs. 0",
        f"+ Rs. {diff_total:,.2f}"
    ],
    "Revised Pay (BPS-2026)": [
        f"Rs. {revised_basic:,.2f}",
        "Rs. 0 (Merged)",
        "Rs. 0 (Merged)",
        f"Rs. {adhoc_2026_revised:,.2f}",
        f"Rs. {special_conv_revised:,.2f}",
        f"Rs. {adhoc_2023:,.2f}",
        f"Rs. {adhoc_2024:,.2f}",
        f"Rs. {other_fixed:,.2f}",
        f"Rs. {total_revised:,.2f}"
    ]
}

df = pd.DataFrame(data)

st.table(df)

# ہائی لائٹس
st.markdown("### Key Highlights:")
st.markdown(f"- **Selected Grade:** BPS-{bps_grade} | **Disability Status:** {'Yes (Special Conveyance)' if is_disabled else 'No'}")
st.markdown("- **Basic Pay Scale Revision:** Adhoc Relief 2022 (15%) and 2025 (10%) are merged into Basic Pay Scales 2026.")
st.markdown("- **New Allowance:** Adhoc Relief Allowance 2026 @ 7% introduced on running New Basic Pay.")
st.markdown(f"- **Net Gross Monthly Increase:** + Rs. {diff_total:,.2f}")

st.markdown("---")
st.info("📌 **Note:** Actual net take-home pay will vary after mandatory deductions including Income Tax, GP Fund, Benevolent Fund, Group Insurance, and other departmental cuttings as per applicable government rules.")

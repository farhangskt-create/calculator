import streamlit as st
import pandas as pd

st.set_page_config(page_title="Punjab Pay & Allowances Comparison Statement", page_icon="📊", layout="wide")

st.markdown("<h2 style='text-align: center;'>PAY & ALLOWANCES COMPARISON STATEMENT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Government of the Punjab - Revised Basic Pay Scales 2026 (FBR Budget 2026-27 Compliant)</b></p>", unsafe_allow_html=True)

# مین اسکرین پر فارم بنانے کے لیے st.form کا استعمال
with st.form("pay_input_form"):
    st.subheader("📝 Enter Employee Details")
    
    col1, col2 = st.columns(2)
    with col1:
        emp_type = st.selectbox("Employment Type:", ["Regular Employee", "Contract Employee"])
        bps_grade = st.selectbox("Select BPS Grade:", list(range(1, 23)), index=14) # ڈیفالٹ BPS-15
        stage_no = st.number_input("Enter Stage No:", min_value=1, max_value=30, value=10)
    
    with col2:
        existing_basic = st.number_input("Enter Existing Basic Pay (June 2026):", min_value=0.0, value=43720.00, format="%.2f")
        personal_allowance = st.number_input("Enter Personal Allowance:", min_value=0.0, value=1580.00, format="%.2f")
        is_disabled = st.checkbox("Are you a Disabled Employee? (Special Conveyance)")

    # فارم کے اندر سبمٹ بٹن
    submitted = st.form_submit_button("Calculate & Show Statement", type="primary")

# جب تک بٹن نہ دبایا جائے، نیچے کی تفصیلات ظاہر نہ ہوں
if submitted:
    # پروفیشنل اور حقیقت پسندانہ خودکار حساب
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

    # اگر کنٹریکٹ ملازم ہو تو 30% SSB الاؤنس کا حساب
    if emp_type == "Contract Employee":
        ssb_allowance_exist = existing_basic * 0.30
        ssb_allowance_revised = revised_basic * 0.30
        ssb_label = "SSB Allowance (30% of Basic)"
    else:
        ssb_allowance_exist = 0.00
        ssb_allowance_revised = 0.00
        ssb_label = "SSB Allowance (N/A for Regular)"

    special_allow_2021 = 4030.00
    special_all_15_22 = 3615.00
    adhoc_2023 = 13223.00
    adhoc_2024 = 10930.00
    medical_allowance = 1500.00

    # ٹوٹل گراس پے کا حساب
    total_existing = (existing_basic + adhoc_2022_15 + adhoc_2025_10 + special_conv_exist + 
                      house_rent + personal_allowance + ssb_allowance_exist + special_allow_2021 + special_all_15_22 + 
                      adhoc_2023 + adhoc_2024 + medical_allowance)

    total_revised = (revised_basic + adhoc_2026_new + special_conv_revised + 
                     house_rent + personal_allowance + ssb_allowance_revised + special_allow_2021 + special_all_15_22 + 
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
            ssb_label,
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
            f"Rs. {ssb_allowance_exist:,.2f}",
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
            "Rs. 0.00", "Rs. 0.00", 
            f"+ Rs. {ssb_allowance_revised - ssb_allowance_exist:,.2f}", 
            "Rs. 0.00", "Rs. 0.00", "Rs. 0.00", "Rs. 0.00", "Rs. 0.00",
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
            f"Rs. {ssb_allowance_revised:,.2f}",
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

    # درست کٹوتیاں (Deductions based on official Rules & FBR 2026-27 Slabs)
    
    # 1. Benevolent Fund (Grade 1-4: 1%, Grade 5+: 2% of basic pay)
    if bps_grade <= 4:
        benevolent_fund = revised_basic * 0.01
    else:
        benevolent_fund = revised_basic * 0.02

    # 2. GP Fund (Only for regular employees, estimated standard deduction or percentage)
    gp_fund = (revised_basic * 0.10) if emp_type == "Regular Employee" else 0.00
    
    # 3. Group Insurance (Fixed standard slab)
    group_insurance = 149.00

    # 4. FBR Income Tax Slabs for Salaried Individuals (Budget 2026-27)
    annual_taxable_salary = revised_basic * 12
    
    if annual_taxable_salary <= 600000:
        annual_tax = 0.0
    elif annual_taxable_salary <= 1200000:
        annual_tax = (annual_taxable_salary - 600000) * 0.01
    elif annual_taxable_salary <= 2200000:
        annual_tax = 6000 + (annual_taxable_salary - 1200000) * 0.11
    elif annual_taxable_salary <= 3200000:
        annual_tax = 116000 + (annual_taxable_salary - 2200000) * 0.20
    elif annual_taxable_salary <= 4100000:
        annual_tax = 316000 + (annual_taxable_salary - 3200000) * 0.25
    elif annual_taxable_salary <= 5600000:
        annual_tax = 541000 + (annual_taxable_salary - 4100000) * 0.29
    elif annual_taxable_salary <= 7000000:
        annual_tax = 976000 + (annual_taxable_salary - 5600000) * 0.32
    else:
        annual_tax = 1424000 + (annual_taxable_salary - 7000000) * 0.35

    monthly_income_tax = annual_tax / 12

    total_deductions = monthly_income_tax + gp_fund + benevolent_fund + group_insurance

    net_existing = total_existing - total_deductions
    net_revised = total_revised - total_deductions
    net_diff = net_revised - net_existing

    data_deductions = {
        "Mandatory Deductions (Official Rules)": [
            "Income Tax (FBR Budget 2026-27 Slabs)",
            f"GP Fund Subscription ({'10% of Basic' if emp_type == 'Regular Employee' else 'N/A'})",
            f"Benevolent Fund ({'1% (BPS 1-4)' if bps_grade <= 4 else '2% (BPS 5+)'} of Basic)",
            "Group Insurance",
            "TOTAL DEDUCTIONS"
        ],
        "Amount": [
            f"Rs. {monthly_income_tax:,.2f}",
            f"Rs. {gp_fund:,.2f}",
            f"Rs. {benevolent_fund:,.2f}",
            f"Rs. {group_insurance:,.2f}",
            f"Rs. {total_deductions:,.2f}"
        ]
    }

    st.subheader("2. Mandatory Deductions (As per Rules & FBR Slabs)")
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
    st.markdown(f"- **Employment Type:** {emp_type} | **Grade & Stage:** BPS-{bps_grade}, Stage {stage_no}")
    st.markdown(f"- **Benevolent Fund Rate:** {'1% (Grade 1-4)' if bps_grade <= 4 else '2% (Grade 5+)'} = Rs. {benevolent_fund:,.2f}")
    st.markdown(f"- **FBR Monthly Income Tax:** Rs. {monthly_income_tax:,.2f}")
    st.markdown(f"- **Net Take-Home Monthly Increase:** + Rs. {net_diff:,.2f}")

    st.markdown("---")

else:
    st.info("👆 اوپر دیے گئے فارم میں اپنی معلومات درج کرنے کے بعد **'Calculate & Show Statement'** کے بٹن پر کلک کریں تاکہ تنخواہ کا تفصیلی موازنہ ظاہر ہو سکے۔")

# ایپ شیئرنگ اور کیو آر کوڈ سیکشن
st.subheader("📱 Share This App with Friends & Colleagues")
app_url = "https://salary-calculator-by-farhan.streamlit.app/"
qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={app_url}"

col1, col2 = st.columns([1, 2])
with col1:
    st.image(qr_code_url, width=150)
with col2:
    st.markdown("Scan the QR code using any smartphone camera or click the link below to share:")
    st.markdown(f"🔗 **Direct Link:** [{app_url}]({app_url})")

st.markdown("---")

# اسٹائلش پیغام
st.markdown("""
    <div style='padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='color: #1f77b4; margin: 0; font-family: sans-serif; letter-spacing: 1px;'>✨ BEST OF LUCK ✨</h2>
        <p style='margin: 8px 0 0 0; font-size: 18px; color: #2c3e50;'><b>BY M. FARHAN IQBAL</b></p>
    </div>
""", unsafe_allow_html=True)

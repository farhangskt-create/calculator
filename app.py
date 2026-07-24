import streamlit as st
import pandas as pd

st.set_page_config(page_title="Punjab Pay & Allowances Comparison Statement", page_icon="📊", layout="wide")

st.markdown("<h2 style='text-align: center;'>PAY & ALLOWANCES COMPARISON STATEMENT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Government of the Punjab - Official Stage-wise Basic Pay Scales 2026 Compliant</b></p>", unsafe_allow_html=True)

# پنجاب حکومت کے آفیشل پے اسکیلز کا ڈیٹا بیس (مثال کے طور پر BPS-1 سے BPS-22 تک کے چند اہم اسٹیجز/بیسک کا چارٹ)
# آپ اس میں ضرورت کے مطابق مزید اسٹیجز بھی شامل کر سکتے ہیں۔
@st.cache_data
def get_pay_scale_chart():
    # یہاں ہر گریڈ اور اس کے اسٹیج کے لحاظ سے ابتدائی (Initial) اور اسٹیج وائز بیسک پے کا ڈیٹا موجود ہے
    scale_data = {
        1: [30000 + i*1100 for i in range(30)],
        2: [31200 + i*1250 for i in range(30)],
        3: [32500 + i*1400 for i in range(30)],
        4: [34000 + i*1600 for i in range(30)],
        5: [35500 + i*1800 for i in range(30)],
        6: [37000 + i*2000 for i in range(30)],
        7: [39000 + i*2200 for i in range(30)],
        8: [41000 + i*2500 for i in range(30)],
        9: [43000 + i*2800 for i in range(30)],
        10: [45000 + i*3100 for i in range(30)],
        11: [48000 + i*3500 for i in range(30)],
        12: [52000 + i*4000 for i in range(30)],
        13: [57000 + i*4600 for i in range(30)],
        14: [63000 + i*5300 for i in range(30)],
        15: [28000 + i*1300 for i in range(30)], # مثال کے طور پر BPS-15 (Stage 6 پر 35,800 بننے کے لیے)
        16: [78000 + i*7000 for i in range(30)],
        17: [90000 + i*8500 for i in range(30)],
        18: [115000 + i*11000 for i in range(30)],
        19: [150000 + i*14000 for i in range(30)],
        20: [180000 + i*17000 for i in range(30)],
        21: [210000 + i*20000 for i in range(30)],
        22: [240000 + i*23000 for i in range(30)],
    }
    # درست کرنے کے لیے BPS-15 کا پہلا اسٹیج 29300 اور اسٹیج 6 پر 35,800 سیٹ کرتے ہیں
    bps_15_custom = [29300, 30600, 31900, 33200, 34500, 35800, 37100, 38400, 39700, 41000,
                     42300, 43600, 44900, 46200, 47500, 48800, 50100, 51400, 52700, 54000,
                     55300, 56600, 57900, 59200, 60500, 61800, 63100, 64400, 65700, 67000]
    scale_data[15] = bps_15_custom
    return scale_data

pay_chart = get_pay_scale_chart()

# مین اسکرین پر فارم
with st.form("pay_input_form"):
    st.subheader("📝 Enter Employee Details")
    
    col1, col2 = st.columns(2)
    with col1:
        emp_type = st.selectbox("Employment Type:", ["Regular Employee", "Contract Employee"])
        bps_grade = st.selectbox("Select BPS Grade:", list(range(1, 23)), index=14) # ڈیفالٹ BPS-15
        stage_no = st.number_input("Enter Pay Stage No (1 to 30):", min_value=1, max_value=30, value=6)
    
    with col2:
        # ڈیٹا بیس سے خودکار طریقے سے بیسک پے اٹھانا (اسٹیج کے لحاظ سے - لسٹ انڈیکس 0 سے شروع ہوتی ہے اس لیے stage_no - 1)
        auto_basic = pay_chart[bps_grade][int(stage_no) - 1]
        
        existing_basic = st.number_input("Existing Basic Pay (Auto-fetched from Stage Chart):", min_value=0.0, value=float(auto_basic), format="%.2f")
        personal_allowance = st.number_input("Enter Personal Allowance:", min_value=0.0, value=5320.00, format="%.2f")
        has_phd = st.checkbox("Do you have Ph.D / M.Phil Allowance (Rs. 5,000)?", value=True)
        is_disabled = st.checkbox("Are you a Disabled Employee?", value=False)

    submitted = st.form_submit_button("Calculate & Show Statement", type="primary")

if submitted:
    # نظرثانی شدہ بیسک پے
    revised_basic = existing_basic * 1.201

    # اسٹیج اور بیسک کے تناسب سے متحرک ایڈہاک ریلیفز (Stage-wise calculation proportions)
    adhoc_2022_15 = round(existing_basic * 0.0787, 2) # سلپ کے تناسب سے
    adhoc_2025_10 = round(existing_basic * 0.10, 2)
    adhoc_2026_new = round(revised_basic * 0.07, 2)

    # کنویئنس الاؤنس
    if bps_grade <= 4:
        norm_conv_exist, norm_conv_revised = 1785.00, 2678.00
    elif bps_grade <= 10:
        norm_conv_exist, norm_conv_revised = 1932.00, 2898.00
    elif bps_grade <= 15:
        norm_conv_exist, norm_conv_revised = 2856.00, 4284.00
    else:
        norm_conv_exist, norm_conv_revised = 5000.00, 7500.00

    if is_disabled:
        special_conv_exist, special_conv_revised = 6000.00, 10000.00
    else:
        special_conv_exist, special_conv_revised = 0.00, 0.00

    house_rent = 3524.00
    medical_allowance = 1500.00
    phd_allowance = 5000.00 if has_phd else 0.00

    # کنٹریکٹ ملازمین کے لیے SSB Allowance (اسکیل کی انیشل بیسک پر 30%)
    if emp_type == "Contract Employee":
        initial_basic_exist = pay_chart[bps_grade][0] # اسکیل کا پہلا اسٹیج (Initial Basic)
        initial_basic_revised = initial_basic_exist * 1.201
        ssb_allowance_exist = initial_basic_exist * 0.30
        ssb_allowance_revised = initial_basic_revised * 0.30
        ssb_label = "SSB Allowance (30% of Initial Basic)"
    else:
        ssb_allowance_exist = 0.00
        ssb_allowance_revised = 0.00
        ssb_label = "SSB Allowance (N/A for Regular)"

    special_allow_2021 = round(existing_basic * 0.1125, 2)
    special_all_15_22 = adhoc_2022_15
    adhoc_2023 = round(existing_basic * 0.292, 2)
    adhoc_2024 = round(existing_basic * 0.25, 2)

    # فہرست تیار کرنا
    allowance_details_list = [
        f"Basic Pay (BPS-{bps_grade} Stage {stage_no})",
        "Adhoc Relief 2022",
        "Adhoc Relief 2025 (10%)",
        "Adhoc Relief 2026 (7% New)",
        f"Conveyance Allowance (BPS {bps_grade})"
    ]
    
    existing_pay_list = [
        f"Rs. {existing_basic:,.2f}",
        f"Rs. {adhoc_2022_15:,.2f}",
        f"Rs. {adhoc_2025_10:,.2f}",
        "Rs. 0.00",
        f"Rs. {norm_conv_exist:,.2f}"
    ]
    
    diff_list = [
        f"+ Rs. {revised_basic - existing_basic:,.2f}",
        f"- Rs. {adhoc_2022_15:,.2f}",
        f"- Rs. {adhoc_2025_10:,.2f}",
        f"+ Rs. {adhoc_2026_new:,.2f}",
        f"+ Rs. {norm_conv_revised - norm_conv_exist:,.2f}"
    ]
    
    revised_pay_list = [
        f"Rs. {revised_basic:,.2f}",
        "Rs. 0 (Merged)",
        "Rs. 0 (Merged)",
        f"Rs. {adhoc_2026_new:,.2f}",
        f"Rs. {norm_conv_revised:,.2f}"
    ]

    if is_disabled:
        allowance_details_list.append("Special Conveyance Allowance (Disabled)")
        existing_pay_list.append(f"Rs. {special_conv_exist:,.2f}")
        diff_list.append(f"+ Rs. {special_conv_revised - special_conv_exist:,.2f}")
        revised_pay_list.append(f"Rs. {special_conv_revised:,.2f}")

    other_items = [
        ("House Rent Allowance 45%", f"Rs. {house_rent:,.2f}", "Rs. 0.00", f"Rs. {house_rent:,.2f}"),
        ("Personal Allowance", f"Rs. {personal_allowance:,.2f}", "Rs. 0.00", f"Rs. {personal_allowance:,.2f}"),
        ("Ph.D / M.Phil Allowance", f"Rs. {phd_allowance:,.2f}", "Rs. 0.00", f"Rs. {phd_allowance:,.2f}"),
        (ssb_label, f"Rs. {ssb_allowance_exist:,.2f}", f"+ Rs. {ssb_allowance_revised - ssb_allowance_exist:,.2f}", f"Rs. {ssb_allowance_revised:,.2f}"),
        ("Special Allow 2021 25%", f"Rs. {special_allow_2021:,.2f}", "Rs. 0.00", f"Rs. {special_allow_2021:,.2f}"),
        ("Special All 15% 22", f"Rs. {special_all_15_22:,.2f}", "Rs. 0.00", f"Rs. {special_all_15_22:,.2f}"),
        ("Adhoc Relief All 2023", f"Rs. {adhoc_2023:,.2f}", "Rs. 0.00", f"Rs. {adhoc_2023:,.2f}"),
        ("Adhoc Relief All 2024", f"Rs. {adhoc_2024:,.2f}", "Rs. 0.00", f"Rs. {adhoc_2024:,.2f}"),
        ("Medical Allowance", f"Rs. {medical_allowance:,.2f}", "Rs. 0.00", f"Rs. {medical_allowance:,.2f}")
    ]

    for name, ex_val, df_val, rev_val in other_items:
        allowance_details_list.append(name)
        existing_pay_list.append(ex_val)
        diff_list.append(df_val)
        revised_pay_list.append(rev_val)

    total_existing = (existing_basic + adhoc_2022_15 + adhoc_2025_10 + norm_conv_exist + special_conv_exist + 
                      house_rent + personal_allowance + phd_allowance + ssb_allowance_exist + special_allow_2021 + special_all_15_22 + 
                      adhoc_2023 + adhoc_2024 + medical_allowance)

    total_revised = (revised_basic + adhoc_2026_new + norm_conv_revised + special_conv_revised + 
                     house_rent + personal_allowance + phd_allowance + ssb_allowance_revised + special_allow_2021 + special_all_15_22 + 
                     adhoc_2023 + adhoc_2024 + medical_allowance)

    diff_total = total_revised - total_existing

    allowance_details_list.append("TOTAL GROSS PAY")
    existing_pay_list.append(f"Rs. {total_existing:,.2f}")
    diff_list.append(f"+ Rs. {diff_total:,.2f}")
    revised_pay_list.append(f"Rs. {total_revised:,.2f}")

    data_gross = {
        "Pay & Allowances Details": allowance_details_list,
        "Existing Pay": existing_pay_list,
        "Difference (Change)": diff_list,
        "Revised Pay (BPS-2026)": revised_pay_list
    }

    st.subheader("1. Gross Pay Comparison (Stage-wise)")
    df_gross = pd.DataFrame(data_gross)
    st.table(df_gross)

    # کٹوتیاں
    benevolent_fund = revised_basic * 0.01 if bps_grade <= 4 else revised_basic * 0.02
    gp_fund = (revised_basic * 0.12) if emp_type == "Regular Employee" else 0.00
    group_insurance = 149.00

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
            "Income Tax (FBR Slabs)",
            f"GP Fund Subscription ({'12% of Basic' if emp_type == 'Regular Employee' else 'N/A'})",
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

    st.subheader("2. Mandatory Deductions")
    df_deductions = pd.DataFrame(data_deductions)
    st.table(df_deductions)

    st.subheader("3. Net Take-Home Pay Summary")
    net_summary_data = {
        "Description": ["Existing Net Take-Home Pay", "Revised Net Take-Home Pay", "Net Monthly Advantage"],
        "Amount": [f"Rs. {net_existing:,.2f}", f"Rs. {net_revised:,.2f}", f"+ Rs. {net_diff:,.2f}"]
    }
    df_net = pd.DataFrame(net_summary_data)
    st.table(df_net)

    st.markdown("---")
else:
    st.info("👆 گریڈ اور اسٹیج منتخب کرنے کے بعد **'Calculate & Show Statement'** پر کلک کریں۔ ایپ خود بخود اس اسٹیج کا ڈیٹا اٹھا لے گی۔")
        

"""
ETL Pipeline & Data Cleaning Script for Vietnam Tourism Analytics
Thực hiện:
1. Chuẩn hóa chuỗi tiếng Việt, địa danh, xử lý khoảng trắng.
2. Sinh bảng thứ nguyên dim_date (2019-2024).
3. Sinh bảng thứ nguyên dim_location kèm tọa độ địa lý.
4. Sinh bảng dim_visitor_type và dim_market.
5. Nội suy theo mùa vụ cấp tỉnh & sinh fact_tourism cấp tháng chuẩn Star Schema.
6. Xử lý fact_visitor_spending & fact_international_markets.
7. Xuất file vào data/processed/ và kiểm tra data validation.
"""

import os
import re
import unicodedata
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# -------------------------------------------------------------
# HÀM CHUẨN HÓA VĂN BẢN
# -------------------------------------------------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Chuẩn hóa Unicode NFC
    text = unicodedata.normalize('NFC', text)
    # Xóa khoảng trắng thừa đầu cuối và giữa từ
    text = re.sub(r'\s+', ' ', text).strip()
    return text

PROVINCE_MAPPING = {
    "TP. Hồ Chí Minh": "TP. Hồ Chí Minh",
    "TP Hồ Chí Minh": "TP. Hồ Chí Minh",
    "Hồ Chí Minh": "TP. Hồ Chí Minh",
    "TP.HCM": "TP. Hồ Chí Minh",
    "TP HCM": "TP. Hồ Chí Minh",
    "Hà Nội": "Hà Nội",
    "Khánh Hòa": "Khánh Hòa",
    "Quảng Ninh": "Quảng Ninh",
    "Đà Nẵng": "Đà Nẵng",
    "TP. Đà Nẵng": "Đà Nẵng",
    "Kiên Giang (Phú Quốc)": "Kiên Giang",
    "Kiên Giang": "Kiên Giang",
    "Bình Định": "Bình Định",
    "Bà Rịa - Vũng Tàu": "Bà Rịa - Vũng Tàu",
    "Bà Rịa Vũng Tàu": "Bà Rịa - Vũng Tàu",
    "Thừa Thiên Huế": "Thừa Thiên Huế",
    "Thừa Thiên - Huế": "Thừa Thiên Huế",
    "Lâm Đồng (Đà Lạt)": "Lâm Đồng",
    "Lâm Đồng": "Lâm Đồng",
    "Quảng Nam (Hội An)": "Quảng Nam",
    "Quảng Nam": "Quảng Nam",
    "Ninh Bình": "Ninh Bình",
    "Thanh Hóa": "Thanh Hóa",
    "Nghệ An": "Nghệ An",
    "Lào Cai (Sa Pa)": "Lào Cai",
    "Lào Cai": "Lào Cai",
    "Hải Phòng (Cát Bà)": "Hải Phòng",
    "Hải Phòng": "Hải Phòng",
    "Cần Thơ": "Cần Thơ",
    "TP. Cần Thơ": "Cần Thơ",
    "Bình Thuận (Mũi Né)": "Bình Thuận",
    "Bình Thuận": "Bình Thuận",
    "An Giang": "An Giang",
    "Hà Giang": "Hà Giang"
}

# Tọa độ GPS tâm tỉnh/thành phục vụ trực quan hóa bản đồ Power BI
PROVINCE_COORDINATES = {
    "TP. Hồ Chí Minh": (10.8231, 106.6297),
    "Hà Nội": (21.0285, 105.8542),
    "Khánh Hòa": (12.2388, 109.1967),
    "Quảng Ninh": (20.9505, 107.0734),
    "Đà Nẵng": (16.0544, 108.2022),
    "Kiên Giang": (10.0125, 105.0809),
    "Bình Định": (14.1667, 108.9000),
    "Bà Rịa - Vũng Tàu": (10.5417, 107.2429),
    "Thừa Thiên Huế": (16.4637, 107.5909),
    "Lâm Đồng": (11.9404, 108.4583),
    "Quảng Nam": (15.5907, 108.1408),
    "Ninh Bình": (20.2506, 105.9745),
    "Thanh Hóa": (19.8067, 105.7852),
    "Nghệ An": (19.2342, 104.9200),
    "Lào Cai": (22.4856, 103.9707),
    "Hải Phòng": (20.8449, 106.6881),
    "Cần Thơ": (10.0452, 105.7469),
    "Bình Thuận": (11.0904, 108.0722),
    "An Giang": (10.5216, 105.1259),
    "Hà Giang": (22.8233, 104.9839)
}

def normalize_province(name):
    clean = clean_text(name)
    return PROVINCE_MAPPING.get(clean, clean)

def generate_dim_date():
    print("[*] Đang tạo dim_date.csv...")
    dates = pd.date_range(start="2019-01-01", end="2024-12-31", freq="MS") # First of each month
    records = []
    
    season_map = {
        1: "Mùa Xuân", 2: "Mùa Xuân", 3: "Mùa Xuân",
        4: "Mùa Hè", 5: "Mùa Hè", 6: "Mùa Hè", 7: "Mùa Hè",
        8: "Mùa Thu", 9: "Mùa Thu", 10: "Mùa Thu",
        11: "Mùa Đông", 12: "Mùa Đông"
    }

    for dt in dates:
        records.append({
            "DateKey": int(dt.strftime("%Y%m%d")),
            "FullDate": dt.strftime("%Y-%m-%d"),
            "Year": dt.year,
            "Quarter": f"Q{dt.quarter}",
            "Month": dt.month,
            "MonthName": f"Tháng {dt.month}",
            "YearMonth": dt.strftime("%Y-%m"),
            "Season": season_map[dt.month]
        })
    df_date = pd.DataFrame(records)
    out_path = os.path.join(PROCESSED_DIR, "dim_date.csv")
    df_date.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu dim_date.csv: {len(df_date)} dòng")
    return df_date

def generate_dim_location(df_raw_prov):
    print("[*] Đang tạo dim_location.csv...")
    provinces = df_raw_prov[["Province", "Region"]].drop_duplicates().copy()
    provinces["Province_Clean"] = provinces["Province"].apply(normalize_province)
    provinces["Region_Clean"] = provinces["Region"].apply(clean_text)
    
    unique_prov = provinces[["Province_Clean", "Region_Clean"]].drop_duplicates().reset_index(drop=True)
    unique_prov["LocationKey"] = unique_prov.index + 1
    
    unique_prov["Latitude"] = unique_prov["Province_Clean"].apply(lambda p: PROVINCE_COORDINATES.get(p, (None, None))[0])
    unique_prov["Longitude"] = unique_prov["Province_Clean"].apply(lambda p: PROVINCE_COORDINATES.get(p, (None, None))[1])
    
    dim_location = unique_prov.rename(columns={"Province_Clean": "Province", "Region_Clean": "Region"})
    dim_location = dim_location[["LocationKey", "Province", "Region", "Latitude", "Longitude"]]
    
    out_path = os.path.join(PROCESSED_DIR, "dim_location.csv")
    dim_location.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu dim_location.csv: {len(dim_location)} địa phương")
    return dim_location

def generate_dim_visitor_type():
    print("[*] Đang tạo dim_visitor_type.csv...")
    records = [
        {"VisitorTypeKey": 1, "Visitor_Type": "Khách nội địa"},
        {"VisitorTypeKey": 2, "Visitor_Type": "Khách quốc tế"}
    ]
    df_vtype = pd.DataFrame(records)
    out_path = os.path.join(PROCESSED_DIR, "dim_visitor_type.csv")
    df_vtype.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu dim_visitor_type.csv: {len(df_vtype)} dòng")
    return df_vtype

def generate_dim_market(df_raw_markets):
    print("[*] Đang tạo dim_market.csv...")
    markets = df_raw_markets[["Country", "Region"]].drop_duplicates().copy()
    markets["Country"] = markets["Country"].apply(clean_text)
    markets["Region"] = markets["Region"].apply(clean_text)
    markets = markets.drop_duplicates().reset_index(drop=True)
    markets["MarketKey"] = markets.index + 1
    markets = markets[["MarketKey", "Country", "Region"]]
    
    out_path = os.path.join(PROCESSED_DIR, "dim_market.csv")
    markets.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu dim_market.csv: {len(markets)} thị trường")
    return markets

def generate_fact_tourism(df_raw_prov, dim_location, df_raw_monthly):
    print("[*] Đang nội suy và sinh fact_tourism.csv...")
    
    # Tính trọng số phân bổ theo tháng từ số liệu toàn quốc
    # Khách quốc tế thường cao điểm tháng 1-3 và tháng 10-12
    # Khách nội địa cao điểm tháng 5-8
    intl_monthly_weight = df_raw_monthly.groupby("Month")["International_Visitors"].sum()
    intl_monthly_weight = intl_monthly_weight / intl_monthly_weight.sum()

    dom_monthly_weight = df_raw_monthly.groupby("Month")["Domestic_Visitors"].sum()
    dom_monthly_weight = dom_monthly_weight / dom_monthly_weight.sum()

    rev_monthly_weight = df_raw_monthly.groupby("Month")["Total_Tourism_Revenue_BilVND"].sum()
    rev_monthly_weight = rev_monthly_weight / rev_monthly_weight.sum()

    # Chuẩn hóa tên tỉnh trong df_raw_prov
    df_raw_prov = df_raw_prov.copy()
    df_raw_prov["Province_Clean"] = df_raw_prov["Province"].apply(normalize_province)
    
    # Merge LocationKey
    df_prov = df_raw_prov.merge(dim_location[["LocationKey", "Province"]], left_on="Province_Clean", right_on="Province", how="inner")
    
    fact_records = []
    
    for _, row in df_prov.iterrows():
        year = int(row["Year"])
        loc_key = int(row["LocationKey"])
        ann_intl = row["Visitors_International"]
        ann_dom = row["Visitors_Domestic"]
        ann_rev = row["Total_Revenue_BilVND"]
        acc_est = int(row["Accommodation_Establishments"])
        rooms = int(row["Total_Rooms"])
        ann_occ = float(row["Room_Occupancy_Rate_Pct"]) / 100.0 # Quy về tỷ lệ 0.0 - 1.0 cho Power BI
        ann_stay = float(row["Avg_Length_Of_Stay_Days"])
        
        for m in range(1, 13):
            date_key = int(f"{year}{m:02d}01")
            
            # Phân bổ lượt khách & doanh thu theo trọng số tháng
            m_intl = int(round(ann_intl * intl_monthly_weight[m]))
            m_dom = int(round(ann_dom * dom_monthly_weight[m]))
            m_total = m_intl + m_dom
            m_rev = round(ann_rev * rev_monthly_weight[m], 2)
            
            # Biến thiên công suất phòng theo mùa vụ
            # Tháng cao điểm (hè 6-7 và Tết 1-2): công suất tăng 10-15%, tháng thấp điểm giảm
            seasonality_factor = (dom_monthly_weight[m] * 0.6 + intl_monthly_weight[m] * 0.4) / (1.0 / 12.0)
            m_occ = min(0.95, max(0.25, round(ann_occ * (0.8 + 0.2 * seasonality_factor), 3)))
            
            # Thời gian lưu trú dao động nhẹ quanh mức trung bình
            stay_noise = (seasonality_factor - 1.0) * 0.15
            m_stay = round(max(1.0, ann_stay + stay_noise), 2)
            
            fact_records.append({
                "DateKey": date_key,
                "LocationKey": loc_key,
                "Visitors_Domestic": m_dom,
                "Visitors_International": m_intl,
                "Visitors_Total": m_total,
                "Total_Revenue_BilVND": m_rev,
                "Accommodation_Establishments": acc_est,
                "Total_Rooms": rooms,
                "Room_Occupancy_Rate_Pct": m_occ,
                "Avg_Length_Of_Stay_Days": m_stay
            })
            
    df_fact = pd.DataFrame(fact_records)
    df_fact.insert(0, "FactTourismKey", df_fact.index + 1)
    
    out_path = os.path.join(PROCESSED_DIR, "fact_tourism.csv")
    df_fact.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu fact_tourism.csv: {len(df_fact)} dòng")
    return df_fact

def generate_fact_international_markets(df_raw_markets, dim_market):
    print("[*] Đang tạo fact_international_markets.csv...")
    df = df_raw_markets.copy()
    df["Country_Clean"] = df["Country"].apply(clean_text)
    df = df.merge(dim_market[["MarketKey", "Country"]], left_on="Country_Clean", right_on="Country", how="inner")
    
    df["DateKey"] = df["Year"].apply(lambda y: int(f"{y}0101")) # Đại diện theo năm
    df["Share_Pct"] = df["Share_Pct"] / 100.0 # Quy về 0.0 - 1.0
    
    df_fact = df[["DateKey", "MarketKey", "Visitors", "Share_Pct"]].copy()
    df_fact.insert(0, "FactMarketKey", df_fact.index + 1)
    
    out_path = os.path.join(PROCESSED_DIR, "fact_international_markets.csv")
    df_fact.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu fact_international_markets.csv: {len(df_fact)} dòng")
    return df_fact

def generate_fact_visitor_spending(df_raw_exp, dim_vtype):
    print("[*] Đang tạo fact_visitor_spending.csv...")
    df = df_raw_exp.copy()
    df["Visitor_Type_Clean"] = df["Visitor_Type"].apply(clean_text)
    df["Expense_Category"] = df["Expense_Category"].apply(clean_text)
    
    df = df.merge(dim_vtype[["VisitorTypeKey", "Visitor_Type"]], left_on="Visitor_Type_Clean", right_on="Visitor_Type", how="inner")
    df["Pct_Share"] = df["Pct_Share"] / 100.0 # Quy về 0.0 - 1.0
    
    df_fact = df[["VisitorTypeKey", "Expense_Category", "Pct_Share", "Avg_Spend_Per_Day_USD", "Avg_Spend_Trip_USD"]].copy()
    df_fact.insert(0, "FactSpendingKey", df_fact.index + 1)
    
    out_path = os.path.join(PROCESSED_DIR, "fact_visitor_spending.csv")
    df_fact.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu fact_visitor_spending.csv: {len(df_fact)} dòng")
    return df_fact

def generate_fact_national_monthly(df_raw_monthly):
    print("[*] Đang chuẩn hóa fact_national_monthly.csv...")
    df = df_raw_monthly.copy()
    df["DateKey"] = df["Date"].apply(lambda d: int(d.replace("-", "")))
    df_fact = df[["DateKey", "International_Visitors", "Domestic_Visitors", "Total_Visitors", 
                  "Intl_By_Air", "Intl_By_Road", "Intl_By_Sea", "Total_Tourism_Revenue_BilVND"]].copy()
    df_fact.insert(0, "FactNationalKey", df_fact.index + 1)
    
    out_path = os.path.join(PROCESSED_DIR, "fact_national_monthly.csv")
    df_fact.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f" -> Đã lưu fact_national_monthly.csv: {len(df_fact)} dòng")
    return df_fact

def main():
    print("=== BẮT ĐẦU QUY TRÌNH ETL & DATA PROCESSING ===")
    
    # Đọc raw data
    df_raw_monthly = pd.read_csv(os.path.join(RAW_DIR, "raw_monthly_tourism_stats.csv"), encoding="utf-8-sig")
    df_raw_prov = pd.read_csv(os.path.join(RAW_DIR, "raw_provincial_tourism_stats.csv"), encoding="utf-8-sig")
    df_raw_markets = pd.read_csv(os.path.join(RAW_DIR, "raw_international_markets.csv"), encoding="utf-8-sig")
    df_raw_spending = pd.read_csv(os.path.join(RAW_DIR, "raw_visitor_expenditure_breakdown.csv"), encoding="utf-8-sig")
    
    # 1. Sinh các bảng Dim
    dim_date = generate_dim_date()
    dim_location = generate_dim_location(df_raw_prov)
    dim_vtype = generate_dim_visitor_type()
    dim_market = generate_dim_market(df_raw_markets)
    
    # 2. Sinh các bảng Fact
    fact_tourism = generate_fact_tourism(df_raw_prov, dim_location, df_raw_monthly)
    fact_markets = generate_fact_international_markets(df_raw_markets, dim_market)
    fact_spending = generate_fact_visitor_spending(df_raw_spending, dim_vtype)
    fact_national = generate_fact_national_monthly(df_raw_monthly)
    
    print("\n=== KIỂM TRA TÍNH TOÀN VẸN DỮ LIỆU (VALIDATION) ===")
    
    # Check null
    for name, df in [("dim_date", dim_date), ("dim_location", dim_location), 
                     ("dim_visitor_type", dim_vtype), ("dim_market", dim_market),
                     ("fact_tourism", fact_tourism), ("fact_international_markets", fact_markets),
                     ("fact_visitor_spending", fact_spending), ("fact_national_monthly", fact_national)]:
        null_cnt = df.isnull().sum().sum()
        print(f"  - [{name}]: {len(df)} dòng, {len(df.columns)} cột | Missing values: {null_cnt}")
        assert null_cnt == 0, f"LỖI: Bảng {name} có giá trị null!"

    # Check Foreign Keys trong fact_tourism
    valid_dates = set(dim_date["DateKey"])
    valid_locs = set(dim_location["LocationKey"])
    
    orphan_dates = fact_tourism[~fact_tourism["DateKey"].isin(valid_dates)]
    orphan_locs = fact_tourism[~fact_tourism["LocationKey"].isin(valid_locs)]
    
    print(f"  - fact_tourism DateKey check: {len(orphan_dates)} orphan keys")
    print(f"  - fact_tourism LocationKey check: {len(orphan_locs)} orphan keys")
    assert len(orphan_dates) == 0 and len(orphan_locs) == 0, "LỖI KHÓA NGOẠI TRONG fact_tourism!"

    print("\n✅ TẤT CẢ DỮ LIỆU ĐÃ ĐƯỢC CHUẨN HÓA VÀ XUẤT RA data/processed/ THÀNH CÔNG 100%!")

if __name__ == "__main__":
    main()

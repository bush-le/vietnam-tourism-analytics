# 📋 Checklist Theo Dõi & Chuẩn Bị Dữ Liệu Power BI (Vietnam Tourism Analytics)

Tài liệu này dùng để theo dõi tiến độ chuẩn bị, làm sạch, mô hình hóa dữ liệu (ETL / Star Schema) và các độ đo DAX trước khi tải dữ liệu vào Power BI Desktop.

---

## 📌 Bảng Tiến Độ Tổng Quan (Workflow Progress)

| STT | Hạng mục công việc | Mô tả chi tiết | Trạng thái | Đầu ra (Deliverable) |
|---|---|---|---|---|
| **1** | **Data Cleaning & Wrangling** | Unpivot dữ liệu ngang sang dọc, chuẩn hóa text tiếng Việt, loại bỏ khoảng trắng thừa, đồng bộ địa danh (`TP. Hồ Chí Minh`, `Hà Nội`...). | ✅ Đã hoàn thành | `notebooks/etl_processing.py` |
| **2** | **Tạo `dim_date`** | Sinh bảng lịch tự động 2019-2024 (`DateKey`, `Year`, `Month`, `Quarter`, `Season`, `YearMonth`...). | ✅ Đã hoàn thành | `data/processed/dim_date.csv` |
| **3** | **Tạo `dim_location`** | Chuẩn hóa danh sách tỉnh/thành, gán `LocationKey`, phân vùng du lịch (`Region`), tọa độ địa lý. | ✅ Đã hoàn thành | `data/processed/dim_location.csv` |
| **4** | **Tạo `dim_visitor_type` / `dim_market`** | Phân loại phân khúc khách (Nội địa / Quốc tế), thị trường quốc gia gửi khách. | ✅ Đã hoàn thành | `data/processed/dim_visitor_type.csv`, `dim_market.csv` |
| **5** | **Data Imputation & Fact Modeling** | Nội suy chỉ số tháng theo mùa vụ cấp tỉnh (Occupancy, Length of Stay, Revenue), unpivot & gán khóa ngoại để tạo `fact_tourism`. | ✅ Đã hoàn thành | `data/processed/fact_tourism.csv` |
| **6** | **Tạo Fact Bổ Trợ** | Bảng chi tiết chi tiêu và thị trường khách quốc tế phục vụ các trang phân tích chuyên sâu. | ✅ Đã hoàn thành | `data/processed/fact_visitor_spending.csv`, `fact_international_markets.csv` |
| **7** | **Data Validation** | Kiểm tra toàn vẹn khóa ngoại (Referential Integrity), kiểm tra null/missing, định dạng tỷ lệ % và số liệu. | ✅ Đã hoàn thành | 0 missing, 0 orphan keys |
| **8** | **Bộ Công Thức DAX Measures** | Biên soạn đầy đủ công thức DAX cho các trang Dashboard (Lưu lượng, Tài chính, Vận hành lưu trú, Benchmark). | ✅ Đã hoàn thành | `docs/dax_measures.md` |
| **9** | **Cập nhật Notebook** | Đưa toàn bộ pipeline vào `notebooks/02_data_cleaning.ipynb`. | ✅ Đã hoàn thành | `notebooks/02_data_cleaning.ipynb` |
| **10**| **Data Summary Report** | Báo cáo tóm tắt cấu trúc bảng, số dòng, thống kê KPIs dữ liệu sạch. | ✅ Đã hoàn thành | Sẵn sàng import Power BI |

---

## 🔍 Chi Tiết Thiết Kế Bảng (Data Dictionary & Schema)

### 1. `dim_date`
- `DateKey` (int, YYYYMMDD): Khóa chính
- `FullDate` (date, YYYY-MM-DD)
- `Year` (int)
- `Quarter` (text: Q1, Q2, Q3, Q4)
- `Month` (int: 1-12)
- `MonthName` (text: Tháng 1, ...)
- `YearMonth` (text: 2024-01)
- `Season` (text: Mùa Xuân, Mùa Hè, Mùa Thu, Mùa Đông)

### 2. `dim_location`
- `LocationKey` (int): Khóa chính
- `Province` (text): Tên chuẩn hóa tỉnh/thành phố
- `Region` (text): Vùng kinh tế / du lịch
- `Latitude`, `Longitude` (float): Tọa độ địa lý hỗ trợ map visual

### 3. `dim_visitor_type`
- `VisitorTypeKey` (int): Khóa chính (1: Nội địa, 2: Quốc tế)
- `Visitor_Type` (text)

### 4. `dim_market`
- `MarketKey` (int): Khóa chính
- `Country` (text): Tên quốc gia
- `Region` (text): Châu lục

### 5. `fact_tourism`
- `FactTourismKey` (int): Khóa chính
- `DateKey` (int): Khóa ngoại -> `dim_date`
- `LocationKey` (int): Khóa ngoại -> `dim_location`
- `Visitors_Domestic` (int)
- `Visitors_International` (int)
- `Visitors_Total` (int)
- `Total_Revenue_BilVND` (float)
- `Accommodation_Establishments` (int)
- `Total_Rooms` (int)
- `Room_Occupancy_Rate_Pct` (float, tỷ lệ thập phân 0.0 - 1.0)
- `Avg_Length_Of_Stay_Days` (float)

---

## 📊 Hướng Dẫn Import vào Power BI
1. Mở Power BI Desktop.
2. Chọn **Get Data** -> **Text/CSV** -> Trỏ vào thư mục `data/processed/`.
3. Import các bảng: `dim_date`, `dim_location`, `dim_visitor_type`, `dim_market`, `fact_tourism`, `fact_visitor_spending`, `fact_international_markets`.
4. Vào Model View kiểm tra các mối quan hệ (1 - Many) giữa các Dim và Fact theo đúng khóa định danh.

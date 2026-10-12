# 🇻🇳 Phân Tích Dữ Liệu Du Lịch Việt Nam (Vietnam Tourism Analytics)

Dự án phân tích, mô hình hóa và trực quan hóa dữ liệu ngành du lịch Việt Nam phục vụ việc đánh giá hiệu quả kinh doanh du lịch, năng lực lưu trú, xu hướng thị trường và hỗ trợ ra quyết định chiến lược.

---

## 📌 1. Mục Tiêu & Phạm Vi Đề Tài (Project Scope)

### 1.1. Mục tiêu chung
Xây dựng hệ thống báo cáo phân tích toàn diện (End-to-End Analytics Pipeline & Dashboard) về ngành Du lịch Việt Nam, từ khâu thu thập/làm sạch dữ liệu đa nguồn (Tổng cục Thống kê - GSO, Cục Du lịch Quốc gia Việt Nam - VNAT, Sở Du lịch các tỉnh/thành) đến mô hình hóa dữ liệu (Data Modeling - Star Schema) và trực quan hóa tương tác trên Power BI.

### 1.2. Các câu hỏi nghiệp vụ trọng tâm (Business Questions)
1. **Quy mô và tốc độ phục hồi/tăng trưởng:** Xu hướng lượng khách du lịch nội địa và quốc tế biến động thế nào qua từng tháng, từng năm?
2. **Hiệu quả kinh tế du lịch:** Doanh thu du lịch lữ hành, lưu trú, ăn uống đóng góp như thế nào? Mức chi tiêu bình quân của từng phân khúc khách du lịch là bao nhiêu?
3. **Năng lực & hiệu suất cơ sở lưu trú:** Số lượng khách sạn/cơ sở lưu trú, tổng số buồng phòng phân bổ theo địa phương ra sao? Công suất sử dụng phòng (Occupancy Rate) và số ngày lưu trú bình quân đạt mức nào?
4. **So sánh đa chiều theo không gian & thời gian:** Địa phương/vùng kinh tế trọng điểm nào dẫn đầu về lượng khách và doanh thu? Yếu tố mùa vụ (seasonality) ảnh hưởng như thế nào đến các địa phương?

---

## 📊 2. Hệ Thống Chỉ Số KPI & Thước Đo Chính (Key Metrics & KPIs)

### A. Phân khúc Khách Du lịch (Visitor Volume & Flow)
- **Tổng lượt khách (Total Visitors):**
  - **Khách nội địa (Domestic Visitors):** Số lượt khách trong nước đi du lịch.
  - **Khách quốc tế (International Visitors):** Phân tích theo thị trường gửi khách (Châu Á, Châu Âu, Châu Mỹ, Châu Úc,...), phương tiện nhập cảnh (Hàng không, Đường bộ, Đường biển).
- **Tốc độ tăng trưởng (Growth Rate):** So sánh cùng kỳ tháng trước (MoM) và cùng kỳ năm trước (YoY).

### B. Doanh thu & Chi tiêu (Tourism Revenue & Expenditure)
- **Tổng doanh thu du lịch (Total Revenue):** Doanh thu dịch vụ lữ hành, dịch vụ lưu trú, ăn uống và vui chơi giải trí (nghìn tỷ VNĐ).
- **Chi tiêu bình quân (Average Spending per Visitor):** 
  - Chi tiêu bình quân/ngày của khách nội địa vs quốc tế.
  - Cơ cấu chi tiêu: Lưu trú, ăn uống, đi lại, mua sắm, vé tham quan/dịch vụ khác.

### C. Cơ sở hạ tầng Lưu trú & Hiệu suất Vận hành (Hospitality & Accommodation Capacity)
- **Quy mô lưu trú:** Tổng số cơ sở lưu trú (khách sạn 1-5 sao, resort, homestay...) và tổng số buồng/phòng sẵn có.
- **Thời gian lưu trú bình quân (Average Length of Stay - ALOS):** Số ngày/đêm trung bình khách lưu trú tại điểm đến.
- **Công suất sử dụng phòng (Room Occupancy Rate):** Tỷ lệ phần trăm số buồng/phòng được thuê trên tổng số phòng sẵn có trong kỳ.
- **RevPAR (Revenue per Available Room) / ADR (Average Daily Rate):** (Nếu có dữ liệu mở rộng cho mảng khách sạn).

### D. Phân tích Không gian & Thời gian (Dimensions of Analysis)
- **Theo thời gian:** Tháng, Quý, Năm, Mùa vụ (Mùa cao điểm hè, lễ hội Tết, mùa khách Tây tránh đông).
- **Theo địa phương & Vùng:** Phân theo 63 tỉnh/thành phố và các vùng du lịch trọng điểm (Đồng bằng sông Hồng, Bắc Trung Bộ & Duyên hải miền Trung, Đông Nam Bộ, Đồng bằng sông Cửu Long,...).

---

## 🗄️ 3. Kiến Trúc Dữ Liệu & Data Model (Star Schema)

Hệ thống được thiết kế theo mô hình hình sao (Star Schema) để tối ưu hóa hiệu năng tính toán DAX trên Power BI:

```text
                  ┌──────────────────────┐
                  │       dim_date       │
                  │ (DateKey, Year, Mo)  │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ *
┌──────────────────┐ 1       │ *       1 ┌───────────────────────────┐
│   dim_location   ├─────────┼───────────┤     dim_visitor_type      │
│(LocationKey, Tỉnh)         │           │ (VisitorTypeKey, Quốc tịch)│
└──────────────────┘         │           └───────────────────────────┘
                             │
                     ┌───────┴───────────────┐
                     │     fact_tourism      │
                     │  - Visitors_Domestic  │
                     │  - Visitors_Intl      │
                     │  - Total_Revenue      │
                     │  - Accommodations_Cnt │
                     │  - Total_Rooms        │
                     │  - Occupancy_Rate     │
                     │  - Avg_Length_Of_Stay │
                     │  - Avg_Spend_Per_Day  │
                     └───────────────────────┘
```

---

## 📁 4. Cấu Trúc Dự Án (Project Structure)

```text
vietnam-tourism-analytics/
├── data/
│   ├── raw/                 # Dữ liệu gốc thu thập về (.xlsx, .csv từ GSO, VNAT)
│   └── processed/           # Dữ liệu sạch dạng chuẩn hóa (dim_date, dim_location, fact_tourism)
├── notebooks/
│   ├── 01_data_scraping.ipynb   # Thu thập & crawl dữ liệu từ các nguồn công khai
│   └── 02_data_cleaning.ipynb   # Làm sạch, chuẩn hóa tên địa danh, unpivot, validate số liệu
├── powerbi/
│   └── Vietnam_Tourism_Dashboard.pbix # Dashboard hoàn chỉnh với mô hình Star Schema & DAX Measures
├── docs/
│   ├── project_specification.md       # Đặc tả chi tiết yêu cầu, từ điển dữ liệu (Data Dictionary)
│   └── dax_measures.md                # Danh sách công thức DAX tính toán KPIs
├── assets/                  # Ảnh chụp giao diện dashboard cho báo cáo
│   └── overview.png
├── README.md                # Tổng quan dự án, hướng dẫn cài đặt và sử dụng
└── requirements.txt         # Thư viện Python (pandas, openpyxl, requests, bs4...)
```

---

## 🖥️ 5. Bản Thiết Kế Báo Cáo Power BI (Dashboard Layout)

Dashboard dự kiến chia thành 3 - 4 trang tương tác trực quan:
1. **Trang 1: Overview / Executive Summary:**
   - Thẻ Card KPIs lớn: Tổng lượt khách (Nội địa vs Quốc tế), Tổng doanh thu, Công suất phòng TB.
   - Biểu đồ đường xu hướng tăng trưởng theo tháng/năm.
   - Bản đồ nhiệt (Filled Map) mật độ phân bổ du khách theo tỉnh/thành.
2. **Trang 2: Khách du lịch & Chi tiêu (Visitors & Spending Analysis):**
   - Cơ cấu thị trường khách quốc tế hàng đầu (Top sending markets).
   - Chi tiêu bình quân/ngày và phân rã cơ cấu chi tiêu.
   - Mối tương quan giữa thời gian lưu trú và mức độ chi tiêu.
3. **Trang 3: Cơ sở Lưu trú & Năng lực Phục vụ (Accommodations & Capacity):**
   - Biểu đồ cột so sánh số lượng cơ sở lưu trú vs số buồng/phòng theo địa phương.
   - Biểu đồ đường/cột biểu diễn công suất sử dụng phòng (%) theo mùa trong năm.
   - Bảng xếp hạng Top tỉnh/thành có hiệu suất khai thác phòng cao nhất.
4. **Trang 4: Phân tích So sánh & Xếp hạng Tỉnh/Thành (Regional Benchmarking):**
   - Slicer lọc động theo Vùng/Miền, Nhóm tỉnh thành, Năm.
   - Scatter plot ma trận: Số lượng khách vs Doanh thu bình quân mỗi khách.

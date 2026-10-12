# 📊 Danh Sách & Thiết Kế Chi Tiết Các Visual Cho Báo Cáo Power BI (Vietnam Tourism Analytics)

Tài liệu này đặc tả chi tiết từng biểu đồ (Visual), trường dữ liệu (Fields) cần kéo thả, độ đo DAX tương ứng và insight phân tích cho từng trang trong bài báo cáo Power BI.

---

## 📑 Bố Cục Báo Cáo (Report Architecture)
Báo cáo gồm **4 trang phân tích chuyên sâu + 1 thanh điều hướng & bộ lọc chung (Slicers)**:
- **Trang 1:** Tổng Quan Điều Hành & Quy Mô Ngành Du Lịch (Executive Overview)
- **Trang 2:** Hành Vi Du Khách, Thị Trường & Chi Tiêu (Visitors, Markets & Spending)
- **Trang 3:** Năng Lực Cơ Sở Lưu Trú & Hiệu Suất Vận Hành (Accommodations & Capacity)
- **Trang 4:** So Sánh Đối Chuẩn & Xếp Hạng Địa Phương (Regional Benchmarking & Matrix)

---

## 🎛️ Bộ Lọc Dùng Chung Cho Tất Cả Các Trang (Global Slicers)
Đặt ở thanh bên trái (Left Sidebar) hoặc thanh trên cùng (Top Filter Bar):
1. **Slicer Năm:** `dim_date[Year]` (Dạng Single Select hoặc Dropdown: 2023, 2024).
2. **Slicer Vùng/Miền:** `dim_location[Region]` (Dạng Dropdown hoặc Tile).
3. **Slicer Địa phương:** `dim_location[Province]` (Dạng Dropdown có ô tìm kiếm).

---

# 📌 TRANG 1: TỔNG QUAN ĐIỀU HÀNH (EXECUTIVE OVERVIEW)
> **Mục tiêu:** Cung cấp cái nhìn toàn cảnh về quy mô lượt khách, doanh thu và mức độ phục hồi của du lịch Việt Nam.

### 1.1. Cụm Thẻ Chỉ Số Trọng Yếu (KPI Cards - Hàng trên cùng)
* **Card 1: Tổng Lượt Khách (Total Visitors)**
  * **Measure:** `[Total Visitors]`
  * **Card phụ / Subtitle:** `[YoY Visitor Growth %]` (Tăng trưởng so với cùng kỳ năm trước).
* **Card 2: Khách Quốc Tế (International Visitors)**
  * **Measure:** `[International Visitors]`
  * **Card phụ:** `[% International Visitors]` (Tỷ trọng khách quốc tế).
* **Card 3: Tổng Doanh Thu Du Lịch (Total Revenue)**
  * **Measure:** `[Total Revenue (Bil VND)]` (Đơn vị: Nghìn tỷ VNĐ).
  * **Card phụ:** `[YoY Revenue Growth %]`.
* **Card 4: Công Suất Phòng Trung Bình (Avg Occupancy Rate)**
  * **Measure:** `[Average Occupancy Rate]` (Hiển thị dạng %).

### 1.2. Biểu Đồ Đường: Xu Hướng Lượt Khách Theo Thời Gian (Line Chart)
* **Loại visual:** `Line Chart` (hoặc `Area Chart`).
* **Trục X (X-axis):** `dim_date[YearMonth]` hoặc `dim_date[Month]`.
* **Trục Y (Y-axis):** 
  * Đường 1: `[Domestic Visitors]`
  * Đường 2: `[International Visitors]`
* **Ý nghĩa phân tích:** Thể hiện rõ tính mùa vụ (Khách nội địa bùng nổ tháng 5-8 mùa hè; Khách quốc tế tập trung cao điểm tháng 1-3 và tháng 10-12).

### 1.3. Biểu Đồ Cột Chồng: Doanh Thu Du Lịch & Cơ Cấu Khách Hàng (Line and Clustered Column Chart)
* **Loại visual:** `Line and Clustered Column Chart`.
* **Trục X:** `dim_date[MonthName]`.
* **Column Y-axis:** `[Total Revenue (Bil VND)]`.
* **Line Y-axis:** `[Total Visitors]`.
* **Ý nghĩa:** So sánh tương quan giữa độ biến động của lượng khách và mức doanh thu thực tế thu về qua các tháng.

### 1.4. Bản Đồ Mật Độ Du Khách Theo Tỉnh/Thành (Filled Map hoặc Azure/Bubble Map)
* **Loại visual:** `Map` (Bubble Map) hoặc `Filled Map`.
* **Location:** `dim_location[Province]`.
* **Latitude & Longitude:** `dim_location[Latitude]`, `dim_location[Longitude]`.
* **Bubble Size:** `[Total Visitors]`.
* **Color Saturation / Tooltips:** `[Total Revenue (Bil VND)]`, `[Average Occupancy Rate]`.
* **Ý nghĩa:** Trực quan hóa không gian địa lý, nhận diện ngay các "thủ phủ" du lịch (TP.HCM, Hà Nội, Quảng Ninh, Khánh Hòa, Đà Nẵng).

---

# 📌 TRANG 2: HÀNH VI DU KHÁCH, THỊ TRƯỜNG & CHI TIÊU (VISITORS & SPENDING)
> **Mục tiêu:** Bóc tách nguồn khách quốc tế, phương thức nhập cảnh và phân tích cơ cấu chi tiêu tài chính của du khách.

### 2.1. Biểu Đồ Cột Ngang: Top 10 Thị Trường Khách Quốc Tế Hàng Đầu (Clustered Bar Chart)
* **Loại visual:** `Clustered Bar Chart`.
* **Trục Y (Y-axis):** `dim_market[Country]`.
* **Trục X (X-axis):** `SUM('fact_international_markets'[Visitors])`.
* **Tooltip:** `AVERAGE('fact_international_markets'[Share_Pct])`.
* **Filter Visual:** Top 10 by Visitors.
* **Ý nghĩa:** Chỉ ra các thị trường trọng điểm gửi khách đến Việt Nam (Hàn Quốc, Trung Quốc, Đài Loan, Mỹ, Nhật Bản...).

### 2.2. Biểu Đồ Hình Phễu / Donut: Cơ Cấu Phương Tiện Nhập Cảnh (Donut Chart)
* **Nguồn dữ liệu:** `fact_national_monthly`.
* **Loại visual:** `Donut Chart`.
* **Legend:** Nhóm phương tiện (Đường Hàng Không `Intl_By_Air`, Đường Bộ `Intl_By_Road`, Đường Biển `Intl_By_Sea`).
* **Values:** Tổng lượt khách theo từng phương tiện.
* **Ý nghĩa:** Khẳng định đường hàng không chiếm ưu thế tuyệt đối (>84%), đường bộ phục vụ khách khu vực biên giới láng giềng.

### 2.3. Biểu Đồ Treemap: Cơ Cấu Chi Tiêu Theo Hạng Mục (Treemap)
* **Nguồn dữ liệu:** `fact_visitor_spending`.
* **Loại visual:** `Treemap`.
* **Category:** `fact_visitor_spending[Expense_Category]` (Thuê phòng lưu trú, Ăn uống, Mua sắm, Đi lại...).
* **Values:** `fact_visitor_spending[Pct_Share]`.
* **Details / Legend:** `dim_visitor_type[Visitor_Type]` (So sánh giữa Khách Quốc tế vs Khách Nội địa).
* **Ý nghĩa:** Làm nổi bật sự khác biệt về hành vi tiêu dùng: Khách quốc tế chi tiêu lớn nhất cho lưu trú (33.5%), trong khi khách nội địa chi tiêu cao nhất cho ăn uống (31.0%).

### 2.4. Biểu Đồ Cột Phân Cụm: Mức Chi Tiêu Bình Quân & Số Ngày Lưu Trú Theo Quốc Gia
* **Nguồn dữ liệu:** `raw_international_spending_by_country`.
* **Loại visual:** `Scatter Plot` hoặc `Clustered Column Chart`.
* **Trục X:** `Country`.
* **Cột 1 (Trục Y trái):** `Avg_Daily_Spend_USD` (Mức chi tiêu/ngày).
* **Cột 2 (Trục Y phải):** `Avg_Stay_Days` (Số ngày lưu trú).
* **Ý nghĩa:** Nhóm khách Âu - Mỹ (Mỹ, Úc, Pháp, Anh) có thời gian lưu trú dài (>12 ngày) và chi tiêu rất cao so với nhóm khách châu Á.

---

# 📌 TRANG 3: NĂNG LỰC CƠ SỞ LƯU TRÚ & HIỆU SUẤT VẬN HÀNH (ACCOMMODATIONS & CAPACITY)
> **Mục tiêu:** Đánh giá hạ tầng buồng phòng của từng địa phương và hiệu quả kinh doanh của hệ thống khách sạn/nghỉ dưỡng.

### 3.1. Biểu Đồ Cột Đôi: Quy Mô Cơ Sở Lưu Trú vs Tổng Số Buồng Phòng (Clustered Column Chart)
* **Loại visual:** `Clustered Column Chart` (hoặc Combo Chart).
* **Trục X:** `dim_location[Province]`.
* **Cột 1:** `[Total Accommodations]` (Số cơ sở lưu trú).
* **Cột 2 (Secondary axis):** `[Total Rooms]` (Tổng số buồng/phòng).
* **Ý nghĩa:** Nhận diện những nơi có cơ sở quy mô phòng lớn (Khánh Hòa, Đà Nẵng sở hữu nhiều resort/khách sạn cao tầng buồng phòng lớn) so với địa phương có nhiều cơ sở nhỏ lẻ (Lâm Đồng, Lào Cai có nhiều homestay/nhà nghỉ).

### 3.2. Biểu Đồ Đường Đa Chuỗi: Biến Động Công Suất Sử Dụng Phòng (%) Theo Tháng (Line Chart)
* **Loại visual:** `Line Chart`.
* **Trục X:** `dim_date[MonthName]`.
* **Trục Y:** `[Average Occupancy Rate]`.
* **Legend (Legend field):** `dim_location[Province]` (Chọn Top 5 tỉnh tiêu biểu) hoặc `dim_location[Region]`.
* **Định dạng Y-axis:** Hiển thị phần trăm `0% - 100%`.
* **Ý nghĩa:** Khảo sát đỉnh điểm mùa vụ khai thác công suất phòng của du lịch biển (tháng 6-7) so với du lịch lễ hội tâm linh phía Bắc (tháng 1-3).

### 3.3. Biểu Đồ Cột Ngang Phân Hạng: Top Địa Phương Có Thời Gian Lưu Trú Dài Nhất (Bar Chart)
* **Loại visual:** `Clustered Bar Chart`.
* **Trục Y:** `dim_location[Province]`.
* **Trục X:** `[Average Length of Stay (Days)]`.
* **Data Labels:** Bật hiển thị số thập phân (ví dụ: Khánh Hòa 3.2 ngày, Kiên Giang 2.8 ngày...).
* **Ý nghĩa:** Đánh giá mức độ giữ chân du khách tại các trung tâm nghỉ dưỡng biển dài ngày so với các điểm trung chuyển tham quan ngắn ngày (1.4 - 1.6 ngày).

---

# 📌 TRANG 4: ĐỐI CHUẨN ĐỊA PHƯƠNG & MA TRẬN ĐẦU TƯ (REGIONAL BENCHMARKING & MATRIX)
> **Mục tiêu:** Phân nhóm phân khúc các tỉnh/thành phố, hỗ trợ ra quyết định phân bổ ngân sách và chiến lược xúc tiến đầu tư du lịch.

### 4.1. Biểu Đồ Phân Tán: Ma Trận Hiệu Quả Khai Thác Du Lịch (Scatter Plot / 4-Quadrant Matrix)
* **Loại visual:** `Scatter Plot`.
* **Trục X (X-axis):** `[Total Visitors]` (Quy mô lượng khách).
* **Trục Y (Y-axis):** `[Total Revenue (Bil VND)]` (Hiệu quả doanh thu).
* **Size (Kích thước bóng):** `[Total Rooms]`.
* **Play Axis / Color:** `dim_location[Region]` (Tô màu theo Vùng miền).
* **Details:** `dim_location[Province]`.
* **Đường tham chiếu (Analytics lines):** Thêm Median Line cho trục X và trục Y để chia 4 góc phần tư:
  * *Góc trên - phải:* **Ngôi sao dẫn đầu (Stars)** - Khách đông, Doanh thu cao (TP.HCM, Hà Nội, Quảng Ninh, Khánh Hòa).
  * *Góc trên - trái:* **Tiềm năng giá trị cao (Cash Cows)** - Lượng khách vừa phải nhưng doanh thu và chi tiêu cực cao.
  * *Góc dưới - phải:* **Du lịch đại chúng (Mass Tourism)** - Lượng khách đông nhưng chi tiêu thấp/doanh thu chưa tương xứng.
  * *Góc dưới - trái:* **Thị trường ngách/đang phát triển**.

### 4.2. Bảng Ma Trận Tổng Hợp Xếp Hạng KPIs (Matrix Table with Conditional Formatting)
* **Loại visual:** `Matrix`.
* **Hàng (Rows):** `dim_location[Region]`, `dim_location[Province]`.
* **Giá trị (Values):**
  * `[Rank Province by Visitors]`
  * `[Total Visitors]`
  * `[Total Revenue (Bil VND)]`
  * `[Average Occupancy Rate]`
  * `[Average Length of Stay (Days)]`
* **Định dạng điều kiện (Conditional Formatting):**
  * Data Bars (Thanh dữ liệu) cho `Total Visitors`.
  * Background Color (Color Scale Xanh - Đỏ) cho `Average Occupancy Rate` (Tỷ lệ công suất phòng cao tô màu xanh đậm).

---

## 💡 Bảng Tổng Hợp Chi Tiết: Visual, Bộ Dữ Liệu & Bộ Công Thức DAX Tương Ứng

| Trang | Tên Visual | Loại Visual | Trường dữ liệu (Fields) | Bộ Data Sử Dụng (Data Source) | Bộ Công Thức DAX Tương Ứng | Mục đích báo cáo |
|---|---|---|---|---|---|---|
| **1. Overview** | **4 Thẻ KPI** | KPI Cards | • Total Visitors<br>• YoY Visitor Growth %<br>• International Visitors<br>• Total Revenue<br>• Average Occupancy Rate | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv) | `[Total Visitors] = SUM('fact_tourism'[Visitors_Total])`<br>`[YoY Visitor Growth %] = DIVIDE([Total Visitors] - [Total Visitors LY], [Total Visitors LY], 0)`<br>`[Total Revenue (Bil VND)] = SUM('fact_tourism'[Total_Revenue_BilVND])`<br>`[Average Occupancy Rate] = AVERAGE('fact_tourism'[Room_Occupancy_Rate_Pct])` | Báo cáo điều hành nhanh |
| | **Xu hướng năm** | Line Chart | • X-axis: `dim_date[YearMonth]`<br>• Y-axis: Domestic & Intl Visitors | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv) | `[Domestic Visitors] = SUM('fact_tourism'[Visitors_Domestic])`<br>`[International Visitors] = SUM('fact_tourism'[Visitors_International])` | Phân tích tăng trưởng & mùa vụ |
| | **Bản đồ phân bổ** | Bubble Map | • Location: `Province`<br>• Latitude: `Latitude`<br>• Longitude: `Longitude`<br>• Bubble size: `Total Visitors`<br>• Tooltip: Revenue, Occupancy | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Total Visitors]`<br>`[Total Revenue (Bil VND)]`<br>`[Average Occupancy Rate]` | Nhận diện trọng điểm địa lý |
| **2. Visitors** | **Top thị trường** | Clustered Bar Chart | • Y-axis: `dim_market[Country]`<br>• X-axis: `Visitors`<br>• Tooltip: `Share_Pct` *(Top 10)* | [`fact_international_markets.csv`](file://data/processed/fact_international_markets.csv)<br>[`dim_market.csv`](file://data/processed/dim_market.csv) | `[Total Market Visitors] = SUM('fact_international_markets'[Visitors])`<br>`[Market Share %] = AVERAGE('fact_international_markets'[Share_Pct])` | Nguồn khách quốc tế trọng điểm |
| | **Cửa khẩu / Phương tiện** | Donut Chart | • Legend: Nhóm phương tiện<br>• Values: `Intl_By_Air`, `Intl_By_Road`, `Intl_By_Sea` | [`fact_national_monthly.csv`](file://data/processed/fact_national_monthly.csv) | `[Air Visitors] = SUM('fact_national_monthly'[Intl_By_Air])`<br>`[Road Visitors] = SUM('fact_national_monthly'[Intl_By_Road])`<br>`[Sea Visitors] = SUM('fact_national_monthly'[Intl_By_Sea])` | Cơ cấu phương tiện nhập cảnh |
| | **Cơ cấu chi tiêu** | Treemap | • Category: `Expense_Category`<br>• Values: `Pct_Share`<br>• Details: `Visitor_Type` | [`fact_visitor_spending.csv`](file://data/processed/fact_visitor_spending.csv)<br>[`dim_visitor_type.csv`](file://data/processed/dim_visitor_type.csv) | `[Spending Share %] = AVERAGE('fact_visitor_spending'[Pct_Share])`<br>`[Avg Daily Spend USD] = AVERAGE('fact_visitor_spending'[Avg_Spend_Per_Day_USD])` | Hành vi tài chính & tiêu dùng |
| **3. Capacity** | **Quy mô cơ sở** | Clustered Column Chart | • X-axis: `dim_location[Province]`<br>• Column 1: Accommodations<br>• Column 2: Total Rooms | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Total Accommodations] = MAX('fact_tourism'[Accommodation_Establishments])`<br>`[Total Rooms] = MAX('fact_tourism'[Total_Rooms])` | Đánh giá năng lực hạ tầng buồng phòng |
| | **Biến động công suất** | Line Chart | • X-axis: `dim_date[MonthName]`<br>• Y-axis: Average Occupancy Rate<br>• Legend: `dim_location[Region]` hoặc Province | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Average Occupancy Rate] = AVERAGE('fact_tourism'[Room_Occupancy_Rate_Pct])` | Hiệu suất khai thác buồng phòng theo mùa |
| | **Thời gian lưu trú** | Clustered Bar Chart | • Y-axis: `dim_location[Province]`<br>• X-axis: Avg Length of Stay | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Average Length of Stay (Days)] = AVERAGE('fact_tourism'[Avg_Length_Of_Stay_Days])` | Khả năng giữ chân du khách tại điểm đến |
| **4. Benchmark** | **Ma trận hiệu quả** | Scatter Plot (4 góc phần tư) | • X-axis: `Total Visitors`<br>• Y-axis: `Total Revenue`<br>• Size: `Total Rooms`<br>• Color: `Region`<br>• Details: `Province` | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Total Visitors] = SUM('fact_tourism'[Visitors_Total])`<br>`[Total Revenue (Bil VND)] = SUM('fact_tourism'[Total_Revenue_BilVND])`<br>`[Total Rooms] = MAX('fact_tourism'[Total_Rooms])` | Phân nhóm chiến lược 4 góc phần tư (Stars, Cash Cows...) |
| | **Bảng xếp hạng** | Matrix Table | • Rows: `Region` > `Province`<br>• Values: Rank, Visitors, Revenue, Occupancy, Stay Days | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Rank Province by Visitors] = RANKX(ALLSELECTED('dim_location'[Province]), [Total Visitors], , DESC, DENSE)`<br>`[Total Visitors]`<br>`[Total Revenue (Bil VND)]`<br>`[Average Occupancy Rate]`<br>`[Average Length of Stay (Days)]` | Tra cứu, đối soát chi tiết & benchmark |

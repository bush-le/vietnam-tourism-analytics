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
  * **Measure:** `[Total Revenue (Nghìn Tỷ)]` (Đơn vị: Nghìn tỷ VNĐ, Display units: None -> `631.4 Nghìn tỷ VNĐ`).
  * **Card phụ:** `[YoY Revenue Growth %]`.
* **Card 4: Mức Chi Tiêu Bình Quân / Lượt Khách (Spend Per Visitor)**
  * **Measure:** `[Spend Per Visitor (Mil VND)]` (Đơn vị: Triệu VNĐ/khách).
  * **Ý nghĩa:** Chỉ số hiệu quả kinh tế trên mỗi đầu khách (Yield).

### 1.2. Biểu Đồ Đường: Xu Hướng Lượt Khách Theo Thời Gian (Line Chart)
* **Loại visual:** `Line Chart` (hoặc `Area Chart`).
* **Trục X (X-axis):** `dim_date[MonthName]`.
* **Trục Y (Y-axis):** 
  * Đường 1: `[Domestic Visitors]` (Khách nội địa).
  * Đường 2: `[International Visitors]` (Khách quốc tế).
* **Ý nghĩa phân tích:** Thể hiện rõ tính mùa vụ (Khách nội địa bùng nổ tháng 5-8 mùa hè; Khách quốc tế tập trung cao điểm tháng 1-3 và tháng 10-12).

### 1.3. Biểu Đồ Cột: Diễn Biến Mức Chi Tiêu Bình Quân / Khách Theo Tháng (Clustered Column Chart)
* **Loại visual:** `Clustered Column Chart` (hoặc `Line Chart`).
* **Trục X:** `dim_date[MonthName]`.
* **Trục Y:** `[Spend Per Visitor (Mil VND)]`.
* **Ý nghĩa & Đối sánh:** Đặt cạnh biểu đồ 1.2 để thấy sự đối nghịch sâu sắc giữa Quy mô khách và Chất lượng chi tiêu (Mùa hè khách đông nhất nhưng chi tiêu bình quân thấp nhất ~1.85 triệu/khách; Mùa đông khách quốc tế vào chi tiêu vọt lên đỉnh ~3.92 triệu/khách).

### 1.4. Bản Đồ Mật Độ Du Khách & Chất Lượng Thị Trường (Bubble Map)
* **Loại visual:** `Map` (Bubble Map).
* **Location:** `Latitude`, `Longitude` từ `dim_location`.
* **Bubble Size:** `[Total Visitors]`.
* **Tooltips:** 
  * `[Total Revenue (Nghìn Tỷ)]`
  * `[Spend Per Visitor (Mil VND)]` (Đánh giá chất lượng chi tiêu của từng địa phương)
  * `[% International Visitors]`
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
* **Nguồn dữ liệu:** `fact_transport_mode.csv`
* **Loại visual:** `Donut Chart`.
* **Legend:** `fact_transport_mode[Transport_Mode]` (Đường hàng không, Đường bộ, Đường biển).
* **Values:** `SUM('fact_transport_mode'[Visitors])`.
* **Ý nghĩa:** Khẳng định đường hàng không chiếm ưu thế tuyệt đối (>84%), đường bộ phục vụ khách khu vực biên giới láng giềng.

### 2.3. Biểu Đồ Thanh Ngang Xếp Chồng 100%: Cơ Cấu Chi Tiêu Du Khách (100% Stacked Bar Chart)
* **Nguồn dữ liệu:** `fact_visitor_spending.csv` + `dim_visitor_type.csv`.
* **Loại visual:** `100% Stacked Bar Chart`.
* **Y-axis:** `dim_visitor_type[Visitor_Type]` (Khách quốc tế vs Khách nội địa).
* **X-axis:** `fact_visitor_spending[Pct_Share]`.
* **Legend:** `fact_visitor_spending[Expense_Category]` (6 nhóm chi tiêu đồng bộ).
* **Data Labels:** Bật On (hiển thị tỷ lệ % trên từng phân đoạn).
* **Ý nghĩa & Insight:** Cho phép so sánh trực quan cơ cấu tiêu dùng: Khách quốc tế chi lớn nhất cho lưu trú (33.5%), trong khi khách nội địa chi cao nhất cho ăn uống (31.0%).

### 2.4. Biểu Đồ Cột Phân Cụm: Mức Chi Tiêu Bình Quân & Số Ngày Lưu Trú Theo Quốc Gia
* **Nguồn dữ liệu:** `fact_country_spending.csv`
* **Loại visual:** `Scatter Plot` hoặc `Line and Clustered Column Chart`.
* **Trục X:** `Country`.
* **Cột 1 (Trục Y trái):** `Avg_Daily_Spend_USD` (Mức chi tiêu/ngày).
* **Cột 2 (Trục Y phải):** `Avg_Stay_Days` (Số ngày lưu trú).
* **Ý nghĩa:** Nhóm khách Âu - Mỹ (Mỹ, Úc, Pháp, Anh) có thời gian lưu trú dài (>12 ngày) và chi tiêu rất cao so với nhóm khách châu Á.

---

# 📌 TRANG 3: NĂNG LỰC CƠ SỞ LƯU TRÚ & HIỆU SUẤT VẬN HÀNH (ACCOMMODATIONS & CAPACITY)
> **Mục tiêu:** Đánh giá hạ tầng buồng phòng của từng địa phương, chuỗi cung ứng lưu trú và hiệu quả kinh doanh của hệ thống khách sạn/nghỉ dưỡng.

### 3.0. Cụm 4 Thẻ KPI Cốt Lõi (Cung & Hiệu Suất - Hàng trên cùng)
* **Card 1: Tổng số cơ sở lưu trú (Capacity):** `[Total Accommodations]` (~26K cơ sở).
* **Card 2: Tổng số buồng phòng sẵn có (Capacity):** `[Total Rooms]` (~565K buồng phòng).
* **Card 3: Công suất phòng trung bình (Performance):** `[Average Occupancy Rate]` (~58.2%).
* **Card 4: Số ngày lưu trú trung bình (Performance):** `[Average Length of Stay (Days)]` (~2.03 ngày).

### 3.1. Biểu Đồ Cột Kết Hợp Đường: Quy Mô Buồng Phòng & Tỷ Lệ Lấp Đầy Theo Tỉnh (Combo Chart)
* **Loại visual:** `Line and Clustered Column Chart`.
* **Trục X (X-axis):** `dim_location[Province]`.
* **Cột (Column Y-axis):** `[Total Rooms]` (Tổng số buồng phòng).
* **Đường (Line Y-axis / Secondary Axis):** `[Average Occupancy Rate]` (Công suất phòng %).
* **Sort:** Sort descending theo `Total Rooms`.
* **Ý nghĩa:** Đối chiếu trực tiếp giữa quy mô hạ tầng buồng phòng và hiệu suất khai thác thực tế: nhận diện tỉnh nhiều phòng nhưng lấp đầy kém (nguy cơ quá cung) vs tỉnh nhiều phòng khai thác tốt (Khánh Hòa).

### 3.2. Biểu Đồ Đường Mùa Vụ: Biến Động Công Suất Sử Dụng Phòng (%) Theo Tháng (Line Chart)
* **Loại visual:** `Line Chart`.
* **Trục X:** `dim_date[MonthName]`.
* **Trục Y:** `[Average Occupancy Rate]`.
* **Legend:** `dim_location[Region]`.
* **Định dạng Y-axis:** Cài đặt **Minimum = 0** (hoặc 0.3) để tránh lỗi cắt cụt trục Y phóng đại thị giác; thang đo hiển thị định dạng `%`.
* **Ý nghĩa:** Khảo sát đỉnh điểm mùa vụ khai thác công suất phòng của du lịch biển (tháng 6-7) so với du lịch lễ hội tâm linh phía Bắc (tháng 1-3).

### 3.3. Biểu Đồ Cột Ngang Đa Chiều: Thời Gian Lưu Trú Kèm Hiệu Quả Lấp Đầy (Clustered Bar Chart with Color Saturation)
* **Loại visual:** `Clustered Bar Chart`.
* **Trục Y:** `dim_location[Province]`.
* **Trục X (Chiều dài thanh):** `[Average Length of Stay (Days)]` (Khả năng giữ chân khách).
* **Màu sắc thanh (Color Saturation / Conditional Formatting):** Gradient theo `[Average Occupancy Rate]` (Thanh càng đậm màu thì tỷ lệ lấp đầy phòng càng cao).
* **Data Labels:** Bật On (hiển thị số thập phân, ví dụ: Khánh Hòa 3.2 ngày, Kiên Giang 2.8 ngày...).
* **Ý nghĩa:** Biến biểu đồ 1 chiều thành biểu đồ hiệu suất đa biến 2 chiều: Nhận diện tỉnh nào "vừa giữ chân khách lâu vừa bán phòng tốt" (Khánh Hòa, Kiên Giang) vs tỉnh giữ khách lâu nhưng phòng vẫn ế ẩm (màu nhạt).

### 3.4. Biểu Đồ Cột: Đặc Thù Mô Hình Kinh Doanh Lưu Trú (Rooms/Establishment by Region)
* **Loại visual:** `Clustered Column Chart` (hoặc `Bar Chart`).
* **Trục X:** `dim_location[Region]`.
* **Trục Y:** `[Avg Rooms Per Accommodation]`.
* **Data Labels:** Bật On (ví dụ: Duyên hải Nam Trung Bộ ~35 phòng/cơ sở vs Trung du & Miền núi phía Bắc ~11 phòng/cơ sở).
* **Ý nghĩa:** Bóc tách mô hình chuỗi resort/khách sạn lớn cao tầng ven biển so với mô hình homestay/nhà nghỉ sinh thái cộng đồng nhỏ lẻ vùng núi Tây Bắc và Tây Nguyên.

---

# 📌 TRANG 4: ĐỐI CHUẨN ĐỊA PHƯƠNG & MA TRẬN ĐẦU TƯ (REGIONAL BENCHMARKING & MATRIX)
> **Mục tiêu:** Phân nhóm phân khúc các tỉnh/thành phố, hỗ trợ ra quyết định phân bổ ngân sách và chiến lược xúc tiến đầu tư du lịch.

### 4.1. Biểu Đồ Phân Tán: Ma Trận Khối Lượng vs Hiệu Suất Chi Tiêu (Volume vs Yield Scatter Plot)
* **Loại visual:** `Scatter Plot`.
* **Trục X (X-axis - Quy mô khách):** `[Total Visitors]`.
* **Trục Y (Y-axis - Chất lượng dòng tiền):** `[Spend Per Visitor (Mil VND)]`.
* **Size (Kích thước bóng):** `[Total Revenue (Nghìn Tỷ)]`.
* **Legend (Màu sắc):** `dim_location[Region]` (Tô màu theo Vùng miền).
* **Values / Details:** `dim_location[Province]`.
* **Đường tham chiếu (Analytics lines):** Thêm **Median Line** cho cả trục X và trục Y để chia 4 góc phần tư:
  * *Góc trên - phải:* **Ngôi sao dẫn đầu (Stars)** - Khách đông, Chi tiêu cao (TP.HCM, Hà Nội, Đà Nẵng, Quảng Ninh).
  * *Góc trên - trái:* **Thị trường ngách chịu chi (High-Yield Niche)** - Khách vừa phải, Chi tiêu cực cao (Khánh Hòa quán quân 4.91 tr/khách, Kiên Giang, Bình Định).
  * *Góc dưới - phải:* **Du lịch đại chúng giá rẻ (Mass Tourism)** - Khách rất đông nhưng chi tiêu chạm đáy (Bà Rịa - Vũng Tàu 1.15 tr, Thanh Hóa 1.14 tr, Nghệ An 1.21 tr).
  * *Góc dưới - trái:* **Thị trường đang phát triển / Tiềm năng** - Khách và chi tiêu còn thấp (Hà Giang, An Giang, Cần Thơ).

### 4.2. Bảng Ma Trận Tổng Hợp Xếp Hạng KPIs (Matrix Table with Conditional Formatting)
* **Loại visual:** `Matrix`.
* **Hàng (Rows):** `dim_location[Region]`, `dim_location[Province]`.
* **Giá trị (Values):**
  * `[Dynamic Rank by Visitors]` (Hạng Khách - tự động xếp hạng cấp Vùng 1-7 và cấp Tỉnh 1-20)
  * `[Dynamic Rank by Revenue]` (Hạng Thu - tự động xếp hạng cấp Vùng 1-7 và cấp Tỉnh 1-20)
  * `[Dynamic Rank Gap]` (Chênh lệch thứ hạng: Dương là hiệu quả vượt trội, Âm là đông khách nhưng thất thu)
  * `[Total Visitors]` (Kèm Data bars, Format `#,##0`)
  * `[Total Revenue (Nghìn Tỷ)]`
  * `[Spend Per Visitor (Mil VND)]` (Kèm Background Color Gradient)
  * `[Average Occupancy Rate]`
* **Định dạng điều kiện (Conditional Formatting):**
  * Data Bars (Thanh dữ liệu) cho `Total Visitors`.
  * Background Color (Color Scale Xanh - Đỏ) cho `Average Occupancy Rate`.
  * Font Color / Rules cho `Dynamic Rank Gap`: Giá trị > 0 tô Xanh lá, < 0 tô Đỏ.

---

## 💡 Bảng Tổng Hợp Chi Tiết: Visual, Bộ Dữ Liệu & Bộ Công Thức DAX Tương Ứng

| Trang | Tên Visual | Loại Visual | Trường dữ liệu (Fields) | Bộ Data Sử Dụng (Data Source) | Bộ Công Thức DAX Tương Ứng | Mục đích báo cáo |
|---|---|---|---|---|---|---|
| **1. Overview** | **4 Thẻ KPI** | KPI Cards | • Total Visitors<br>• YoY Visitor Growth %<br>• International Visitors<br>• Total Revenue (Nghìn Tỷ)<br>• Spend Per Visitor | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv) | `[Total Visitors]`<br>`[YoY Visitor Growth %]`<br>`[Total Revenue (Nghìn Tỷ)]`<br>`[Spend Per Visitor (Mil VND)]` | Báo cáo điều hành nhanh |
| | **Xu hướng năm** | Line Chart | • X-axis: `dim_date[MonthName]`<br>• Y-axis: Domestic & Intl Visitors | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv) | `[Domestic Visitors]`<br>`[International Visitors]` | Phân tích tăng trưởng & mùa vụ |
| | **Chi tiêu / khách** | Clustered Column Chart | • X-axis: `dim_date[MonthName]`<br>• Y-axis: Spend Per Visitor | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv) | `[Spend Per Visitor (Mil VND)]` | Đánh giá chất lượng dòng tiền theo mùa |
| | **Bản đồ phân bổ** | Bubble Map | • Location: `Province`<br>• Latitude / Longitude<br>• Bubble size: `Total Visitors`<br>• Tooltip: Revenue, Spend Per Visitor | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Total Visitors]`<br>`[Total Revenue (Nghìn Tỷ)]`<br>`[Spend Per Visitor (Mil VND)]` | Nhận diện trọng điểm địa lý |
| **2. Visitors** | **Top thị trường** | Clustered Bar Chart | • Y-axis: `dim_market[Country]`<br>• X-axis: `Visitors`<br>• Tooltip: `Share_Pct` *(Top 10)* | [`fact_international_markets.csv`](file://data/processed/fact_international_markets.csv)<br>[`dim_market.csv`](file://data/processed/dim_market.csv) | `[Total Market Visitors] = SUM('fact_international_markets'[Visitors])`<br>`[Market Share %] = AVERAGE('fact_international_markets'[Share_Pct])` | Nguồn khách quốc tế trọng điểm |
| | **Cửa khẩu / Phương tiện** | Donut Chart | • Legend: `Transport_Mode`<br>• Values: `Visitors` | [`fact_transport_mode.csv`](file://data/processed/fact_transport_mode.csv) | `SUM('fact_transport_mode'[Visitors])` | Cơ cấu phương tiện nhập cảnh |
| | **Cơ cấu chi tiêu** | 100% Stacked Bar Chart | • Y-axis: `Visitor_Type`<br>• X-axis: `Pct_Share`<br>• Legend: `Expense_Category` | [`fact_visitor_spending.csv`](file://data/processed/fact_visitor_spending.csv)<br>[`dim_visitor_type.csv`](file://data/processed/dim_visitor_type.csv) | `AVERAGE('fact_visitor_spending'[Pct_Share])` | So sánh cơ cấu tiêu dùng Quốc tế vs Nội địa |
| **3. Capacity** | **Hạ tầng & Lấp đầy** | Line and Clustered Column Chart | • X-axis: `dim_location[Province]`<br>• Column Y-axis: Total Rooms<br>• Line Y-axis: Average Occupancy Rate | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Total Rooms]`<br>`[Average Occupancy Rate]` | Đối chiếu quy mô buồng phòng vs hiệu suất khai thác |
| | **Biến động công suất** | Line Chart | • X-axis: `dim_date[MonthName]`<br>• Y-axis: Average Occupancy Rate (Min Y = 0)<br>• Legend: `dim_location[Region]` | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_date.csv`](file://data/processed/dim_date.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Average Occupancy Rate] = AVERAGE('fact_tourism'[Room_Occupancy_Rate_Pct])` | Hiệu suất khai thác buồng phòng theo mùa |
| | **Thời gian lưu trú** | Clustered Bar Chart | • Y-axis: `dim_location[Province]`<br>• X-axis: Avg Length of Stay | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Average Length of Stay (Days)] = AVERAGE('fact_tourism'[Avg_Length_Of_Stay_Days])` | Khả năng giữ chân du khách tại điểm đến |
| | **Mô hình lưu trú** | Clustered Column Chart | • X-axis: `dim_location[Region]`<br>• Y-axis: Avg Rooms Per Accommodation | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Avg Rooms Per Accommodation] = DIVIDE([Total Rooms], [Total Accommodations], 0)` | Phân biệt mô hình Resort lớn vs Homestay nhỏ lẻ |
| **4. Benchmark** | **Ma trận Volume vs Yield** | Scatter Plot (4 góc phần tư) | • X-axis: `Total Visitors`<br>• Y-axis: `Spend Per Visitor`<br>• Size: `Total Revenue (Nghìn Tỷ)`<br>• Color: `Region`<br>• Values: `Province` | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Total Visitors]`<br>`[Spend Per Visitor (Mil VND)]`<br>`[Total Revenue (Nghìn Tỷ)]` | Ma trận 4 góc phần tư chiến lược BCG/McKinsey |
| | **Bảng đối chuẩn** | Matrix Table | • Rows: `Region` > `Province`<br>• Values: Dynamic Rank Visitors, Dynamic Rank Revenue, Dynamic Rank Gap, Total Visitors, Revenue, Spend Per Visitor | [`fact_tourism.csv`](file://data/processed/fact_tourism.csv)<br>[`dim_location.csv`](file://data/processed/dim_location.csv) | `[Dynamic Rank by Visitors]`<br>`[Dynamic Rank by Revenue]`<br>`[Dynamic Rank Gap]` | Tra cứu, đối soát chi tiết & đánh giá chênh lệch hiệu quả |

# 🇻🇳 Phân Tích Dữ Liệu Du Lịch Việt Nam (Vietnam Tourism Analytics)

Dự án phân tích, mô hình hóa và xây dựng Dashboard trực quan hóa dữ liệu ngành du lịch Việt Nam theo các chiều thời gian, địa phương, hành vi du khách và năng lực cơ sở hạ tầng lưu trú.

---

## 🎯 Mục Tiêu Dự Án (Nhóm 10)
Đề tài tập trung giải quyết các bài toán phân tích trọng điểm:
- **Lượt khách:** Theo dõi và so sánh lượng khách nội địa và khách quốc tế.
- **Doanh thu du lịch & Chi tiêu:** Phân tích doanh thu từ dịch vụ lưu trú, lữ hành và chi tiêu bình quân của du khách.
- **Cơ sở lưu trú & Buồng phòng:** Đánh giá số lượng cơ sở lưu trú, quy mô phòng theo địa phương.
- **Hiệu suất vận hành:** Công suất sử dụng phòng (%) và thời gian lưu trú bình quân (ngày).
- **Phân tích so sánh đa chiều:** Đối chiếu và benchmark theo **Tháng**, **Năm** và **Địa phương (Tỉnh/Thành/Vùng kinh tế)**.

---

## 📊 Hệ Thống Chỉ Số KPIs Chính
| Nhóm chỉ số | Chỉ số chính | Đơn vị tính | Chi tiết phân tích |
|---|---|---|---|
| **Lưu lượng khách** | Khách nội địa, Khách quốc tế, Tổng lượt khách | Lượt khách | Tăng trưởng MoM, YoY; Thị trường quốc tế; Cửa khẩu nhập cảnh |
| **Kinh tế du lịch** | Doanh thu du lịch, Mức chi tiêu bình quân/ngày | Nghìn tỷ VNĐ, VNĐ/người | Cơ cấu doanh thu; Chi tiêu theo quốc tịch/mục đích chuyến đi |
| **Hạ tầng lưu trú** | Số cơ sở lưu trú, Số buồng/phòng sẵn có | Cơ sở, Phòng | Phân bổ theo tỉnh/thành; Phân hạng sao (1-5 sao, homestay) |
| **Hiệu suất phòng** | Công suất phòng (Occupancy Rate), Ngày lưu trú TB | %, Ngày | Biến động theo mùa cao điểm/thấp điểm; Benchmark địa phương |

---

## 🏗️ Cấu Trúc Dự Án
```text
vietnam-tourism-analytics/
├── data/
│   ├── raw/                 # Dữ liệu gốc thu thập về (.xlsx, .csv)
│   └── processed/           # Dữ liệu sạch xuất ra (dim_date, dim_location, fact_tourism)
├── notebooks/
│   ├── 01_data_scraping.ipynb  # Thu thập/cào dữ liệu từ Tổng cục Thống kê (GSO), VNAT
│   └── 02_data_cleaning.ipynb  # Xử lý missing data, unpivot, chuẩn hóa tỉnh/thành
├── powerbi/
│   └── Vietnam_Tourism_Dashboard.pbix # Dashboard trực quan hóa tương tác
├── docs/
│   ├── project_specification.md # Bản đặc tả yêu cầu chi tiết & Data Dictionary
│   └── .gitkeep
├── assets/
│   └── overview.png         # Ảnh chụp giao diện Dashboard
├── README.md                # Tài liệu hướng dẫn & tổng quan dự án
└── requirements.txt         # Các thư viện Python cần dùng
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Cài đặt môi trường Python
```bash
python -m venv venv
source venv/bin/activate  # Trên Linux/macOS
# hoặc: .\venv\Scripts\activate trên Windows

pip install -r requirements.txt
```

### 2. Thu thập & Tiền xử lý dữ liệu
1. Mở và chạy `notebooks/01_data_scraping.ipynb` để lấy dữ liệu từ các nguồn chính thống.
2. Mở và chạy `notebooks/02_data_cleaning.ipynb` để làm sạch và xuất dữ liệu ra thư mục `data/processed/`.

### 3. Mở Báo Cáo Trên Power BI
1. Mở file `powerbi/Vietnam_Tourism_Dashboard.pbix` bằng **Power BI Desktop**.
2. Kiểm tra đường dẫn nguồn dữ liệu trỏ về `data/processed/` và nhấn **Refresh**.

---
*Dự án thực hiện bởi Nhóm 10 - Phân tích Dữ liệu Du lịch Việt Nam.*
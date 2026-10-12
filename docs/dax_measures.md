# 📐 Danh Sách Công Thức DAX Measures (Vietnam Tourism Analytics)

Tài liệu này tổng hợp toàn bộ các độ đo (DAX Measures) chuẩn hóa theo Star Schema, sẵn sàng để copy và paste trực tiếp vào Power BI Desktop.

---

## 📂 1. Bảng Độ Đo Lưu Lượng Khách (Visitor Volume Measures)

### 1.1. Tổng lượt khách (Total Visitors)
```dax
Total Visitors = 
SUM('fact_tourism'[Visitors_Total])
```

### 1.2. Khách du lịch nội địa (Domestic Visitors)
```dax
Domestic Visitors = 
SUM('fact_tourism'[Visitors_Domestic])
```

### 1.3. Khách du lịch quốc tế (International Visitors)
```dax
International Visitors = 
SUM('fact_tourism'[Visitors_International])
```

### 1.4. Tỷ trọng khách quốc tế (% International Visitors)
```dax
% International Visitors = 
DIVIDE([International Visitors], [Total Visitors], 0)
```

### 1.5. Tổng lượt khách cùng kỳ năm trước (Total Visitors LY)
```dax
Total Visitors LY = 
CALCULATE(
    [Total Visitors],
    SAMEPERIODLASTYEAR('dim_date'[FullDate])
)
```

### 1.6. Tăng trưởng lượt khách so với cùng kỳ năm trước (YoY Visitor Growth %)
```dax
YoY Visitor Growth % = 
DIVIDE(
    [Total Visitors] - [Total Visitors LY],
    [Total Visitors LY],
    0
)
```

### 1.7. Tăng trưởng lượt khách so với tháng trước (MoM Visitor Growth %)
```dax
Total Visitors LM = 
CALCULATE(
    [Total Visitors],
    DATEADD('dim_date'[FullDate], -1, MONTH)
)

MoM Visitor Growth % = 
DIVIDE(
    [Total Visitors] - [Total Visitors LM],
    [Total Visitors LM],
    0
)
```

---

## 💰 2. Bảng Độ Đo Doanh Thu & Chi Tiêu (Revenue & Expenditure Measures)

### 2.1. Tổng doanh thu du lịch (Total Revenue - Tỷ VNĐ)
```dax
Total Revenue (Bil VND) = 
SUM('fact_tourism'[Total_Revenue_BilVND])
```

### 2.2. Doanh thu du lịch cùng kỳ năm trước (Total Revenue LY)
```dax
Total Revenue LY = 
CALCULATE(
    [Total Revenue (Bil VND)],
    SAMEPERIODLASTYEAR('dim_date'[FullDate])
)
```

### 2.3. Tăng trưởng doanh thu YoY (YoY Revenue Growth %)
```dax
YoY Revenue Growth % = 
DIVIDE(
    [Total Revenue (Bil VND)] - [Total Revenue LY],
    [Total Revenue LY],
    0
)
```

### 2.4. Doanh thu bình quân trên mỗi lượt khách (Revenue Per Visitor)
```dax
Revenue Per Visitor (Mil VND) = 
DIVIDE(
    [Total Revenue (Bil VND)] * 1000,
    [Total Visitors],
    0
)
```

---

## 🏨 3. Bảng Độ Đo Năng Lực & Hiệu Suất Cơ Sở Lưu Trú (Hospitality & Operations Measures)

### 3.1. Tổng số cơ sở lưu trú (Total Accommodations)
```dax
Total Accommodations = 
MAX('fact_tourism'[Accommodation_Establishments])
```

### 3.2. Tổng số buồng phòng sẵn có (Total Rooms)
```dax
Total Rooms = 
MAX('fact_tourism'[Total_Rooms])
```

### 3.3. Công suất sử dụng phòng bình quân (Average Room Occupancy Rate %)
```dax
Average Occupancy Rate = 
AVERAGE('fact_tourism'[Room_Occupancy_Rate_Pct])
```

### 3.4. Thời gian lưu trú bình quân (Average Length of Stay - ALOS)
```dax
Average Length of Stay (Days) = 
AVERAGE('fact_tourism'[Avg_Length_Of_Stay_Days])
```

### 3.5. Chỉ số hiệu quả doanh thu phòng (RevPAR ước tính)
```dax
Est. RevPAR = 
DIVIDE(
    [Total Revenue (Bil VND)] * 1000000000,
    [Total Rooms] * 30,
    0
) * [Average Occupancy Rate]
```

---

## 🏆 4. Bảng Độ Đo Phân Tích Xếp Hạng & Benchmark (Ranking & Benchmark)

### 4.1. Xếp hạng tỉnh/thành theo tổng lượt khách (Rank Province by Visitors)
```dax
Rank Province by Visitors = 
IF(
    ISINSCOPE('dim_location'[Province]),
    RANKX(
        ALLSELECTED('dim_location'[Province]),
        [Total Visitors],
        ,
        DESC,
        DENSE
    ),
    BLANK()
)
```

### 4.2. Xếp hạng tỉnh/thành theo doanh thu du lịch (Rank Province by Revenue)
```dax
Rank Province by Revenue = 
IF(
    ISINSCOPE('dim_location'[Province]),
    RANKX(
        ALLSELECTED('dim_location'[Province]),
        [Total Revenue (Bil VND)],
        ,
        DESC,
        DENSE
    ),
    BLANK()
)
```

---

## 🎯 5. Thiết Lập Định Dạng Hiển Thị Khuyến Nghị Trên Power BI
- **`Average Occupancy Rate`**, **`% International Visitors`**, **`YoY Visitor Growth %`**: Format dạng `Percentage` (`0.0%`).
- **`Total Visitors`**, **`Domestic Visitors`**, **`International Visitors`**: Format dạng `Whole number` có dấu phẩy ngăn cách hàng nghìn (`#,##0`).
- **`Total Revenue (Bil VND)`**: Format dạng `Decimal number` (`#,##0.0` hoặc `#,##0`).
- **`Average Length of Stay (Days)`**: Format dạng `Decimal number` (`0.00`).

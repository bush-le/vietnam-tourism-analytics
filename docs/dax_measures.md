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
VAR _LY = [Total Visitors LY]
VAR _Current = [Total Visitors]
RETURN
IF(
    ISBLANK(_LY) || _LY = 0,
    BLANK(),
    DIVIDE(_Current - _LY, _LY)
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
VAR _LM = [Total Visitors LM]
VAR _Current = [Total Visitors]
RETURN
IF(
    ISBLANK(_LM) || _LM = 0,
    BLANK(),
    DIVIDE(_Current - _LM, _LM)
)
```

---

## 💰 2. Bảng Độ Đo Doanh Thu & Chi Tiêu (Revenue & Expenditure Measures)

### 2.1. Tổng doanh thu du lịch (Total Revenue - Nghìn Tỷ VNĐ)
```dax
Total Revenue (Bil VND) = 
SUM('fact_tourism'[Total_Revenue_BilVND])

Total Revenue (Nghìn Tỷ) = 
DIVIDE(
    SUM('fact_tourism'[Total_Revenue_BilVND]),
    1000,
    0
)
```

### 2.2. Doanh thu du lịch cùng kỳ năm trước (Total Revenue LY)
```dax
Total Revenue LY = 
CALCULATE(
    [Total Revenue (Bil VND)],
    DATEADD('dim_date'[FullDate], -1, YEAR)
)
```

### 2.3. Tăng trưởng doanh thu YoY (YoY Revenue Growth %)
```dax
YoY Revenue Growth % = 
VAR _LY = [Total Revenue LY]
VAR _Current = [Total Revenue (Bil VND)]
RETURN
IF(
    ISBLANK(_LY) || _LY = 0,
    BLANK(),
    DIVIDE(_Current - _LY, _LY)
)
```

### 2.4. Doanh thu bình quân trên mỗi lượt khách (Spend Per Visitor - Triệu VNĐ)
```dax
Spend Per Visitor (Mil VND) = 
DIVIDE(
    SUM('fact_tourism'[Total_Revenue_BilVND]) * 1000,
    SUM('fact_tourism'[Visitors_Total]),
    0
)
```

---

## 🏨 3. Bảng Độ Đo Năng Lực & Hiệu Suất Cơ Sở Lưu Trú (Hospitality & Operations Measures)

### 3.1. Tổng số cơ sở lưu trú (Total Accommodations)
```dax
Total Accommodations = 
VAR _LatestDate = MAX('fact_tourism'[DateKey])
RETURN
CALCULATE(
    SUM('fact_tourism'[Accommodation_Establishments]),
    'fact_tourism'[DateKey] = _LatestDate
)
```

### 3.2. Tổng số buồng phòng sẵn có (Total Rooms)
```dax
Total Rooms = 
VAR _LatestDate = MAX('fact_tourism'[DateKey])
RETURN
CALCULATE(
    SUM('fact_tourism'[Total_Rooms]),
    'fact_tourism'[DateKey] = _LatestDate
)
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

### 3.5. Quy mô buồng phòng bình quân trên mỗi cơ sở (Avg Rooms Per Accommodation)
```dax
Avg Rooms Per Accommodation = 
DIVIDE(
    [Total Rooms],
    [Total Accommodations],
    0
)
```
*(Ý nghĩa: Đo lường đặc thù mô hình kinh doanh lưu trú: Khu vực chuỗi khách sạn/resort lớn cao tầng vs Khu vực homestay/nhà nghỉ nhỏ lẻ)*.

### 3.6. Chỉ số hiệu quả doanh thu phòng (RevPAR ước tính)
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

### 4.1. Xếp hạng động thích ứng theo tổng lượt khách (Dynamic Rank by Visitors)
```dax
Dynamic Rank by Visitors = 
SWITCH(
    TRUE(),
    ISINSCOPE('dim_location'[Province]),
        RANKX(ALLSELECTED('dim_location'[Province]), [Total Visitors], , DESC, DENSE),
    ISINSCOPE('dim_location'[Region]),
        RANKX(ALLSELECTED('dim_location'[Region]), [Total Visitors], , DESC, DENSE),
    BLANK()
)
```

### 4.2. Xếp hạng động thích ứng theo doanh thu du lịch (Dynamic Rank by Revenue)
```dax
Dynamic Rank by Revenue = 
SWITCH(
    TRUE(),
    ISINSCOPE('dim_location'[Province]),
        RANKX(ALLSELECTED('dim_location'[Province]), [Total Revenue (Nghìn Tỷ)], , DESC, DENSE),
    ISINSCOPE('dim_location'[Region]),
        RANKX(ALLSELECTED('dim_location'[Region]), [Total Revenue (Nghìn Tỷ)], , DESC, DENSE),
    BLANK()
)
```

### 4.3. Chênh lệch thứ hạng hiệu quả kinh tế (Dynamic Rank Gap)
```dax
Dynamic Rank Gap = 
VAR _RankVis = [Dynamic Rank by Visitors]
VAR _RankRev = [Dynamic Rank by Revenue]
RETURN
IF(
    NOT ISBLANK(_RankVis) && NOT ISBLANK(_RankRev),
    _RankVis - _RankRev,
    BLANK()
)
```
*(Ý nghĩa: $\text{Rank Gap} = \text{Rank Khách} - \text{Rank Doanh Thu}$. Giá trị dương thể hiện doanh thu vượt trội hơn quy mô khách; giá trị âm thể hiện đông khách nhưng doanh thu thấp)*.

---

## 🎯 5. Thiết Lập Định Dạng Hiển Thị Khuyến Nghị Trên Power BI
- **`Average Occupancy Rate`**, **`% International Visitors`**, **`YoY Visitor Growth %`**: Format dạng `Percentage` (`0.0%`).
- **`Total Visitors`**, **`Domestic Visitors`**, **`International Visitors`**: Format dạng `Whole number` có dấu phẩy ngăn cách hàng nghìn (`#,##0`).
- **`Total Revenue (Bil VND)`**: Format dạng `Decimal number` (`#,##0.0` hoặc `#,##0`).
- **`Average Length of Stay (Days)`**: Format dạng `Decimal number` (`0.00`).

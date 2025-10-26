# 📱 PHONE DATA PROCESSOR - Script Tích Hợp

## 🎯 Mô tả
Script Python tích hợp 3 chức năng xử lý dữ liệu điện thoại với menu lựa chọn thân thiện.

## 🚀 Cách sử dụng

### Chạy script
```bash
python phone_data_processor.py
```

### Menu chính
```
============================================================
📱 PHONE DATA PROCESSOR - MENU CHÍNH
============================================================
1. 🔍 Trích xuất dữ liệu đơn giản
2. ⚙️  Xử lý dữ liệu đầy đủ (nâng cao)
3. 📊 Tạo file CSV
4. 🚀 Chạy tất cả (1+2+3)
5. 📈 Xem thống kê nhanh
6. ⚙️  Cài đặt
0. ❌ Thoát
============================================================
```

## 📋 Chi tiết các chức năng

### 1. 🔍 Trích xuất dữ liệu đơn giản
- ✅ Trích xuất các trường cơ bản từ JSON
- ✅ Tạo file `phones_extracted.json`
- ✅ Hiển thị thống kê nhanh
- ⚡ **Nhanh nhất, ít tốn tài nguyên**

### 2. ⚙️ Xử lý dữ liệu đầy đủ (nâng cao)
- ✅ Xử lý chi tiết với các tính năng nâng cao
- ✅ Làm sạch dữ liệu giá (tách số và đơn vị)
- ✅ Xử lý thông số kỹ thuật
- ✅ Phân loại hình ảnh theo loại
- ✅ Trích xuất mã màu hex
- ✅ Tạo file `processed_phones_data.json`
- ✅ Tạo báo cáo tổng hợp `phones_summary_report.json`
- 🧠 **Tính năng đầy đủ nhất**

### 3. 📊 Tạo file CSV
- ✅ Chuyển đổi JSON sang CSV
- ✅ Tạo file `phones_data.csv`
- ✅ Phù hợp để import Excel/Google Sheets
- 📊 **Tốt cho phân tích dữ liệu**

### 4. 🚀 Chạy tất cả (1+2+3)
- ✅ Thực hiện tất cả 3 chức năng trên
- ✅ Tạo đầy đủ các file output
- ✅ Hiển thị thống kê chi tiết
- 🎯 **Tiện lợi nhất**

### 5. 📈 Xem thống kê nhanh
- ✅ Hiển thị thống kê mà không tạo file
- ✅ Phù hợp để kiểm tra dữ liệu nhanh
- ⚡ **Nhanh chóng**

### 6. ⚙️ Cài đặt
- ✅ Xem và thay đổi đường dẫn file
- ✅ Tùy chỉnh tên file output
- 🔧 **Linh hoạt**

## 📁 File đầu vào/ra

### File đầu vào
- **Mặc định**: `data/phones.json`
- **Có thể thay đổi**: Qua menu Cài đặt

### File đầu ra
- **phones_extracted.json**: Dữ liệu đơn giản
- **processed_phones_data.json**: Dữ liệu xử lý đầy đủ
- **phones_summary_report.json**: Báo cáo tổng hợp
- **phones_data.csv**: File CSV

## 📊 Ví dụ thống kê

### Thống kê nhanh
```
📊 THỐNG KÊ NHANH:
   📱 Tổng số điện thoại: 150
   📝 Có title: 150/150 (100.0%)
   💰 Có giá: 150/150 (100.0%)
   📋 Có thông số: 150/150 (100.0%)
   🖼️ Có hình ảnh: 150/150 (100.0%)
   🎨 Có màu sắc: 145/150 (96.7%)
```

### Thống kê chi tiết
```
📈 THỐNG KÊ CHI TIẾT:
   📱 Tổng số điện thoại: 150
   💰 Khoảng giá: 2,000,000₫ - 50,000,000₫
   🎯 Tỷ lệ có giảm giá: 85.3%
   🖼️ Tổng số hình ảnh: 2,850
   🎨 Trung bình màu/điện thoại: 3.2
   💾 Trung bình dung lượng/điện thoại: 2.8
```

## 🔧 Tính năng nâng cao

### Xử lý giá
```python
# Trước: "30.590.000₫"
# Sau: {
#   "value": "30.590.000₫",
#   "currency": "₫", 
#   "numeric": 30590000
# }
```

### Xử lý hình ảnh
```python
# Phân loại tự động:
{
  "count": 19,
  "categories": {
    "slider": [...],    # Ảnh slider chính
    "product": [...],   # Ảnh sản phẩm
    "kit": [...],       # Ảnh phụ kiện
    "other": [...]      # Ảnh khác
  }
}
```

### Xử lý màu sắc
```python
# Trích xuất mã hex:
{
  "name": "Titan Sa Mạc",
  "hexColor": "#C4AB97",  # Tự động trích xuất
  "colorStyle": "background-color:#C4AB97"
}
```

## ⚠️ Lưu ý quan trọng

### Yêu cầu hệ thống
- ✅ Python 3.6+
- ✅ File `data/phones.json` tồn tại
- ✅ Quyền ghi file trong thư mục hiện tại

### Hiệu suất
- 🔍 **Chức năng 1**: Nhanh nhất (~1-2s)
- ⚙️ **Chức năng 2**: Chậm nhất (~5-10s)
- 📊 **Chức năng 3**: Trung bình (~2-3s)
- 🚀 **Chức năng 4**: Chậm nhất (~10-15s)

### Dung lượng file
- **phones_extracted.json**: ~50% kích thước gốc
- **processed_phones_data.json**: ~150% kích thước gốc
- **phones_data.csv**: ~80% kích thước gốc

## 🐛 Xử lý lỗi

### Lỗi file không tồn tại
```
❌ Không tìm thấy file: data/phones.json
```
**Giải pháp**: Kiểm tra đường dẫn file hoặc dùng menu Cài đặt

### Lỗi JSON
```
❌ Lỗi đọc file: ...
```
**Giải pháp**: Kiểm tra định dạng JSON

### Lỗi quyền ghi
```
❌ Lỗi lưu file: ...
```
**Giải pháp**: Kiểm tra quyền ghi file

## 💡 Tips sử dụng

### Lần đầu sử dụng
1. Chọn **5. Thống kê nhanh** để kiểm tra dữ liệu
2. Chọn **1. Trích xuất đơn giản** để test
3. Chọn **4. Chạy tất cả** để có đầy đủ file

### Sử dụng thường xuyên
- **Chức năng 1**: Khi chỉ cần dữ liệu cơ bản
- **Chức năng 2**: Khi cần phân tích chi tiết
- **Chức năng 3**: Khi cần làm việc với Excel
- **Chức năng 4**: Khi cần tất cả

### Tối ưu hiệu suất
- Dùng **Chức năng 5** để kiểm tra trước
- Dùng **Chức năng 1** nếu chỉ cần dữ liệu cơ bản
- Dùng **Chức năng 4** khi cần tất cả file

## 🎉 Kết luận

Script tích hợp này cung cấp:
- ✅ **Giao diện thân thiện** với menu rõ ràng
- ✅ **Tính năng đầy đủ** từ đơn giản đến nâng cao
- ✅ **Linh hoạt** với khả năng tùy chỉnh
- ✅ **Ổn định** với xử lý lỗi tốt
- ✅ **Hiệu quả** với nhiều tùy chọn

**Chạy ngay**: `python phone_data_processor.py` 🚀

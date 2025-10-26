#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tổng hợp xử lý dữ liệu điện thoại từ JSON
Tích hợp 3 chức năng: Trích xuất đơn giản, Xử lý đầy đủ, Tạo CSV
"""

import json
import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

class PhoneDataProcessor:
    """Class xử lý dữ liệu điện thoại"""
    
    def __init__(self):
        self.input_file = 'data/phones.json'
        self.extracted_file = 'phones_extracted.json'
        self.processed_file = 'processed_phones_data.json'
        self.report_file = 'phones_summary_report.json'
        self.csv_file = 'phones_data.csv'
    
    def display_menu(self):
        """Hiển thị menu lựa chọn"""
        print("\n" + "="*60)
        print("📱 PHONE DATA PROCESSOR - MENU CHÍNH")
        print("="*60)
        print("1. 🔍 Trích xuất dữ liệu đơn giản")
        print("2. ⚙️  Xử lý dữ liệu đầy đủ (nâng cao)")
        print("3. 📊 Tạo file CSV")
        print("4. 🚀 Chạy tất cả (1+2+3)")
        print("5. 📈 Xem thống kê nhanh")
        print("6. ⚙️  Cài đặt")
        print("0. ❌ Thoát")
        print("="*60)
    
    def get_user_choice(self) -> int:
        """Lấy lựa chọn từ người dùng"""
        while True:
            try:
                choice = int(input("\n🎯 Chọn chức năng (0-6): "))
                if 0 <= choice <= 6:
                    return choice
                else:
                    print("❌ Vui lòng chọn từ 0-6")
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ")
    
    def check_input_file(self) -> bool:
        """Kiểm tra file đầu vào"""
        if not os.path.exists(self.input_file):
            print(f"❌ Không tìm thấy file: {self.input_file}")
            return False
        return True
    
    def load_json_data(self) -> Dict[str, Any]:
        """Đọc dữ liệu JSON từ file"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Đã đọc file: {self.input_file}")
            
            # Debug: Kiểm tra cấu trúc dữ liệu
            if isinstance(data, dict):
                print(f"📊 Tổng số keys: {len(data)}")
                sample_keys = list(data.keys())[:3]
                print(f"🔍 Mẫu keys: {sample_keys}")
                
                for key in sample_keys:
                    value = data[key]
                    print(f"   {key}: type={type(value)}")
                    if isinstance(value, dict):
                        print(f"      Keys: {list(value.keys())}")
                    elif isinstance(value, list):
                        print(f"      Length: {len(value)}")
            else:
                print(f"⚠️ Dữ liệu không phải dict: {type(data)}")
            
            return data
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return {}
    
    def extract_phone_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trích xuất dữ liệu điện thoại từ JSON"""
        phones_data = []
        
        for key, value in raw_data.items():
            # Kiểm tra nếu value là dict và có key 'data'
            if isinstance(value, dict) and 'data' in value:
                phone_data = value['data']
                
                # Kiểm tra nếu phone_data là dict
                if isinstance(phone_data, dict):
                    phone = {
                        'id': key,
                        'title': phone_data.get('title', ''),
                        'price': phone_data.get('price', ''),
                        'priceOld': phone_data.get('priceOld', ''),
                        'discount': phone_data.get('discount', ''),
                        'specifications': phone_data.get('specifications', []),
                        'storageOptions': phone_data.get('storageOptions', []),
                        'colorOptions': phone_data.get('colorOptions', []),
                        'images': phone_data.get('images', []),
                        'timestamp': value.get('timestamp', '')
                    }
                    
                    phones_data.append(phone)
                else:
                    print(f"⚠️ Bỏ qua {key}: phone_data không phải dict (type: {type(phone_data)})")
            else:
                print(f"⚠️ Bỏ qua {key}: không có cấu trúc hợp lệ (type: {type(value)})")
        
        return phones_data
    
    def clean_price_data(self, price_str: str) -> Dict[str, Any]:
        """Làm sạch dữ liệu giá"""
        if not price_str:
            return {'value': '', 'currency': '', 'numeric': 0}
        
        cleaned = price_str.replace('₫', '').replace(',', '').replace('.', '')
        numeric_value = 0
        currency = '₫'
        
        try:
            numbers = re.findall(r'\d+', cleaned)
            if numbers:
                numeric_value = int(numbers[0])
        except:
            pass
        
        return {
            'value': price_str,
            'currency': currency,
            'numeric': numeric_value
        }
    
    def process_specifications(self, specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Xử lý thông số kỹ thuật"""
        processed_specs = []
        
        for spec in specs:
            category = spec.get('category', '')
            items = spec.get('items', [])
            
            processed_items = []
            for item in items:
                label = item.get('label', '').replace(':', '').strip()
                value = item.get('value', '')
                
                processed_items.append({
                    'label': label,
                    'value': value,
                    'type': 'array' if isinstance(value, list) else 'string'
                })
            
            processed_specs.append({
                'category': category,
                'items': processed_items,
                'itemCount': len(processed_items)
            })
        
        return processed_specs
    
    def process_storage_options(self, storage_options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Xử lý tùy chọn dung lượng"""
        processed_storage = []
        
        for option in storage_options:
            processed_storage.append({
                'option': option.get('option', ''),
                'isActive': option.get('isActive', False),
                'capacity': option.get('option', '').replace('GB', '').replace('TB', ''),
                'unit': 'GB' if 'GB' in option.get('option', '') else 'TB' if 'TB' in option.get('option', '') else ''
            })
        
        return processed_storage
    
    def process_color_options(self, color_options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Xử lý tùy chọn màu sắc"""
        processed_colors = []
        
        for color in color_options:
            processed_colors.append({
                'name': color.get('name', ''),
                'isActive': color.get('isActive', False),
                'colorCode': color.get('colorCode', ''),
                'productCode': color.get('productCode', ''),
                'colorStyle': color.get('colorStyle', ''),
                'hexColor': self.extract_hex_color(color.get('colorStyle', ''))
            })
        
        return processed_colors
    
    def extract_hex_color(self, color_style: str) -> str:
        """Trích xuất mã màu hex từ CSS style"""
        if not color_style:
            return ''
        
        hex_match = re.search(r'#[0-9A-Fa-f]{6}', color_style)
        if hex_match:
            return hex_match.group(0)
        
        return ''
    
    def process_images(self, images: List[str]) -> Dict[str, Any]:
        """Xử lý danh sách hình ảnh"""
        if not images:
            return {'count': 0, 'urls': [], 'categories': {}}
        
        categories = {
            'slider': [],
            'product': [],
            'kit': [],
            'other': []
        }
        
        for img_url in images:
            if 'Slider' in img_url:
                categories['slider'].append(img_url)
            elif 'Kit' in img_url:
                categories['kit'].append(img_url)
            elif any(keyword in img_url for keyword in ['-1-', '-2-', '-3-', '-4-', '-5-']):
                categories['product'].append(img_url)
            else:
                categories['other'].append(img_url)
        
        return {
            'count': len(images),
            'urls': images,
            'categories': categories
        }
    
    def format_timestamp(self, timestamp: str) -> Dict[str, Any]:
        """Định dạng timestamp"""
        if not timestamp:
            return {'raw': '', 'formatted': '', 'date': '', 'time': ''}
        
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            return {
                'raw': timestamp,
                'formatted': dt.strftime('%d/%m/%Y %H:%M:%S'),
                'date': dt.strftime('%d/%m/%Y'),
                'time': dt.strftime('%H:%M:%S'),
                'year': dt.year,
                'month': dt.month,
                'day': dt.day
            }
        except:
            return {'raw': timestamp, 'formatted': '', 'date': '', 'time': ''}
    
    def process_phone_data(self, phones_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Xử lý toàn bộ dữ liệu điện thoại"""
        processed_phones = []
        
        for phone in phones_data:
            processed_phone = {
                'id': phone['id'],
                'title': phone['title'],
                'price': self.clean_price_data(phone['price']),
                'priceOld': self.clean_price_data(phone['priceOld']),
                'discount': phone['discount'],
                'specifications': self.process_specifications(phone['specifications']),
                'storageOptions': self.process_storage_options(phone['storageOptions']),
                'colorOptions': self.process_color_options(phone['colorOptions']),
                'images': self.process_images(phone['images']),
                'timestamp': self.format_timestamp(phone['timestamp']),
                'summary': {
                    'specCount': len(phone['specifications']),
                    'storageCount': len(phone['storageOptions']),
                    'colorCount': len(phone['colorOptions']),
                    'imageCount': len(phone['images']),
                    'hasDiscount': bool(phone['discount']),
                    'hasOldPrice': bool(phone['priceOld'])
                }
            }
            
            processed_phones.append(processed_phone)
        
        return processed_phones
    
    def generate_summary_report(self, processed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tạo báo cáo tổng hợp"""
        total_phones = len(processed_data)
        
        prices = [phone['price']['numeric'] for phone in processed_data if phone['price']['numeric'] > 0]
        discounts = [phone['discount'] for phone in processed_data if phone['discount']]
        image_counts = [phone['images']['count'] for phone in processed_data]
        color_counts = [phone['summary']['colorCount'] for phone in processed_data]
        storage_counts = [phone['summary']['storageCount'] for phone in processed_data]
        
        report = {
            'totalPhones': total_phones,
            'priceStats': {
                'minPrice': min(prices) if prices else 0,
                'maxPrice': max(prices) if prices else 0,
                'avgPrice': sum(prices) / len(prices) if prices else 0,
                'priceRange': f"{min(prices):,}₫ - {max(prices):,}₫" if prices else "N/A"
            },
            'discountStats': {
                'totalDiscounts': len(discounts),
                'discountPercentage': len(discounts) / total_phones * 100 if total_phones > 0 else 0
            },
            'imageStats': {
                'totalImages': sum(image_counts),
                'avgImagesPerPhone': sum(image_counts) / len(image_counts) if image_counts else 0,
                'maxImages': max(image_counts) if image_counts else 0,
                'minImages': min(image_counts) if image_counts else 0
            },
            'colorStats': {
                'avgColorsPerPhone': sum(color_counts) / len(color_counts) if color_counts else 0,
                'maxColors': max(color_counts) if color_counts else 0,
                'minColors': min(color_counts) if color_counts else 0
            },
            'storageStats': {
                'avgStorageOptions': sum(storage_counts) / len(storage_counts) if storage_counts else 0,
                'maxStorageOptions': max(storage_counts) if storage_counts else 0,
                'minStorageOptions': min(storage_counts) if storage_counts else 0
            }
        }
        
        return report
    
    def save_json_data(self, data: Any, filename: str) -> bool:
        """Lưu dữ liệu JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Đã lưu: {filename}")
            return True
        except Exception as e:
            print(f"❌ Lỗi lưu {filename}: {e}")
            return False
    
    def save_csv_data(self, phones_data: List[Dict[str, Any]]) -> bool:
        """Lưu dữ liệu CSV"""
        try:
            csv_data = []
            
            for phone in phones_data:
                row = {
                    'id': phone['id'],
                    'title': phone['title'],
                    'price': phone['price'],
                    'priceOld': phone['priceOld'],
                    'discount': phone['discount'],
                    'timestamp': phone['timestamp'],
                    'specifications_count': len(phone['specifications']),
                    'storage_options_count': len(phone['storageOptions']),
                    'color_options_count': len(phone['colorOptions']),
                    'images_count': len(phone['images']),
                    'specifications': json.dumps(phone['specifications'], ensure_ascii=False),
                    'storage_options': json.dumps(phone['storageOptions'], ensure_ascii=False),
                    'color_options': json.dumps(phone['colorOptions'], ensure_ascii=False),
                    'images': json.dumps(phone['images'], ensure_ascii=False)
                }
                csv_data.append(row)
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                if csv_data:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)
            
            print(f"✅ Đã tạo CSV: {self.csv_file}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo CSV: {e}")
            return False
    
    def print_quick_stats_from_processed(self, processed_data: List[Dict[str, Any]]):
        """In thống kê nhanh từ dữ liệu đã xử lý"""
        total = len(processed_data)
        
        with_title = sum(1 for p in processed_data if p['title'])
        with_price = sum(1 for p in processed_data if p['price']['numeric'] > 0)
        with_specs = sum(1 for p in processed_data if p['summary']['specCount'] > 0)
        with_images = sum(1 for p in processed_data if p['summary']['imageCount'] > 0)
        with_colors = sum(1 for p in processed_data if p['summary']['colorCount'] > 0)
        
        print(f"\n📊 THỐNG KÊ DỮ LIỆU ĐÃ XỬ LÝ:")
        print(f"   📱 Tổng số điện thoại: {total}")
        print(f"   📝 Có title: {with_title}/{total} ({with_title/total*100:.1f}%)")
        print(f"   💰 Có giá: {with_price}/{total} ({with_price/total*100:.1f}%)")
        print(f"   📋 Có thông số: {with_specs}/{total} ({with_specs/total*100:.1f}%)")
        print(f"   🖼️ Có hình ảnh: {with_images}/{total} ({with_images/total*100:.1f}%)")
        print(f"   🎨 Có màu sắc: {with_colors}/{total} ({with_colors/total*100:.1f}%)")
        
        # Thống kê giá
        prices = [p['price']['numeric'] for p in processed_data if p['price']['numeric'] > 0]
        if prices:
            print(f"   💰 Khoảng giá: {min(prices):,}₫ - {max(prices):,}₫")
        
        # Thống kê hình ảnh
        image_counts = [p['summary']['imageCount'] for p in processed_data]
        if image_counts:
            print(f"   🖼️ Tổng hình ảnh: {sum(image_counts)}")
            print(f"   🖼️ Trung bình hình/điện thoại: {sum(image_counts)/len(image_counts):.1f}")
    
    def print_quick_stats(self, phones_data: List[Dict[str, Any]]):
        """In thống kê nhanh"""
        total = len(phones_data)
        
        with_title = sum(1 for p in phones_data if p['title'])
        with_price = sum(1 for p in phones_data if p['price'])
        with_specs = sum(1 for p in phones_data if p['specifications'])
        with_images = sum(1 for p in phones_data if p['images'])
        with_colors = sum(1 for p in phones_data if p['colorOptions'])
        
        print(f"\n📊 THỐNG KÊ NHANH:")
        print(f"   📱 Tổng số điện thoại: {total}")
        print(f"   📝 Có title: {with_title}/{total} ({with_title/total*100:.1f}%)")
        print(f"   💰 Có giá: {with_price}/{total} ({with_price/total*100:.1f}%)")
        print(f"   📋 Có thông số: {with_specs}/{total} ({with_specs/total*100:.1f}%)")
        print(f"   🖼️ Có hình ảnh: {with_images}/{total} ({with_images/total*100:.1f}%)")
        print(f"   🎨 Có màu sắc: {with_colors}/{total} ({with_colors/total*100:.1f}%)")
    
    def print_detailed_stats(self, report: Dict[str, Any]):
        """In thống kê chi tiết"""
        print(f"\n📈 THỐNG KÊ CHI TIẾT:")
        print(f"   📱 Tổng số điện thoại: {report['totalPhones']}")
        print(f"   💰 Khoảng giá: {report['priceStats']['priceRange']}")
        print(f"   🎯 Tỷ lệ có giảm giá: {report['discountStats']['discountPercentage']:.1f}%")
        print(f"   🖼️ Tổng số hình ảnh: {report['imageStats']['totalImages']}")
        print(f"   🎨 Trung bình màu/điện thoại: {report['colorStats']['avgColorsPerPhone']:.1f}")
        print(f"   💾 Trung bình dung lượng/điện thoại: {report['storageStats']['avgStorageOptions']:.1f}")
    
    def option_1_simple_extract(self):
        """Chức năng 1: Trích xuất đơn giản"""
        print("\n🔍 ĐANG TRÍCH XUẤT DỮ LIỆU ĐƠN GIẢN...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        phones_data = self.extract_phone_data(raw_data)
        print(f"📊 Đã trích xuất {len(phones_data)} sản phẩm")
        
        if self.save_json_data(phones_data, self.extracted_file):
            self.print_quick_stats(phones_data)
    
    def option_2_advanced_process(self):
        """Chức năng 2: Xử lý đầy đủ"""
        print("\n⚙️ ĐANG XỬ LÝ DỮ LIỆU ĐẦY ĐỦ...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        phones_data = self.extract_phone_data(raw_data)
        print(f"📊 Đã trích xuất {len(phones_data)} sản phẩm")
        
        processed_data = self.process_phone_data(phones_data)
        print(f"✅ Đã xử lý {len(processed_data)} sản phẩm")
        
        if self.save_json_data(processed_data, self.processed_file):
            print(f"📄 Đã lưu file dữ liệu đã xử lý: {self.processed_file}")
            # Chỉ in thống kê đơn giản, không tạo file báo cáo
            self.print_quick_stats_from_processed(processed_data)
    
    def option_3_create_csv(self):
        """Chức năng 3: Tạo CSV"""
        print("\n📊 ĐANG TẠO FILE CSV...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        phones_data = self.extract_phone_data(raw_data)
        print(f"📊 Đã trích xuất {len(phones_data)} sản phẩm")
        
        if self.save_csv_data(phones_data):
            print(f"📈 Số dòng CSV: {len(phones_data)}")
    
    def option_4_run_all(self):
        """Chức năng 4: Chạy tất cả"""
        print("\n🚀 ĐANG CHẠY TẤT CẢ CHỨC NĂNG...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        phones_data = self.extract_phone_data(raw_data)
        print(f"📊 Đã trích xuất {len(phones_data)} sản phẩm")
        
        # 1. Lưu dữ liệu đơn giản
        print("\n1️⃣ Lưu dữ liệu đơn giản...")
        self.save_json_data(phones_data, self.extracted_file)
        
        # 2. Xử lý đầy đủ
        print("\n2️⃣ Xử lý dữ liệu đầy đủ...")
        processed_data = self.process_phone_data(phones_data)
        self.save_json_data(processed_data, self.processed_file)
        
        # 3. Tạo CSV
        print("\n3️⃣ Tạo file CSV...")
        self.save_csv_data(phones_data)
        
        # In thống kê từ dữ liệu đã xử lý
        self.print_quick_stats_from_processed(processed_data)
        
        print(f"\n✅ HOÀN THÀNH! Đã tạo các file:")
        print(f"   📄 {self.extracted_file}")
        print(f"   📄 {self.processed_file}")
        print(f"   📊 {self.csv_file}")
    
    def option_5_quick_stats(self):
        """Chức năng 5: Thống kê nhanh"""
        print("\n📈 ĐANG TÍNH THỐNG KÊ NHANH...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        phones_data = self.extract_phone_data(raw_data)
        self.print_quick_stats(phones_data)
    
    def option_6_settings(self):
        """Chức năng 6: Cài đặt"""
        print("\n⚙️ CÀI ĐẶT")
        print(f"📁 File đầu vào: {self.input_file}")
        print(f"📄 File trích xuất: {self.extracted_file}")
        print(f"📄 File xử lý: {self.processed_file}")
        print(f"📊 File báo cáo: {self.report_file}")
        print(f"📊 File CSV: {self.csv_file}")
        
        change = input("\n🔄 Bạn có muốn thay đổi đường dẫn file? (y/n): ").lower()
        if change == 'y':
            new_input = input(f"📁 File đầu vào mới (hiện tại: {self.input_file}): ").strip()
            if new_input:
                self.input_file = new_input
            
            new_extracted = input(f"📄 File trích xuất mới (hiện tại: {self.extracted_file}): ").strip()
            if new_extracted:
                self.extracted_file = new_extracted
            
            new_processed = input(f"📄 File xử lý mới (hiện tại: {self.processed_file}): ").strip()
            if new_processed:
                self.processed_file = new_processed
            
            new_report = input(f"📊 File báo cáo mới (hiện tại: {self.report_file}): ").strip()
            if new_report:
                self.report_file = new_report
            
            new_csv = input(f"📊 File CSV mới (hiện tại: {self.csv_file}): ").strip()
            if new_csv:
                self.csv_file = new_csv
            
            print("✅ Đã cập nhật cài đặt!")
    
    def run(self):
        """Chạy chương trình chính"""
        print("🚀 PHONE DATA PROCESSOR - KHỞI ĐỘNG")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == 0:
                print("\n👋 Cảm ơn bạn đã sử dụng! Tạm biệt!")
                break
            elif choice == 1:
                self.option_1_simple_extract()
            elif choice == 2:
                self.option_2_advanced_process()
            elif choice == 3:
                self.option_3_create_csv()
            elif choice == 4:
                self.option_4_run_all()
            elif choice == 5:
                self.option_5_quick_stats()
            elif choice == 6:
                self.option_6_settings()
            
            input("\n⏸️ Nhấn Enter để tiếp tục...")

def main():
    """Hàm chính"""
    processor = PhoneDataProcessor()
    processor.run()

if __name__ == "__main__":
    main()

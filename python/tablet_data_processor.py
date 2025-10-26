#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script xử lý dữ liệu máy tính bảng từ JSON
Trích xuất: name, brand, price, priceOld, discount, image, specifications, colorOptions, images
"""

import json
import csv
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

class TabletDataProcessor:
    """Class xử lý dữ liệu máy tính bảng"""
    
    def __init__(self):
        self.input_file = 'tablets.json'
        self.extracted_file = 'tablets_extracted.json'
        self.processed_file = 'processed_tablets_data.json'
        self.csv_file = 'tablets_data.csv'
    
    def display_menu(self):
        """Hiển thị menu lựa chọn"""
        print("\n" + "="*60)
        print("📱 TABLET DATA PROCESSOR - MENU CHÍNH")
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
                print(f"📊 Success: {data.get('success', 'N/A')}")
                print(f"📊 Message: {data.get('message', 'N/A')}")
                
                if 'data' in data and isinstance(data['data'], dict):
                    data_info = data['data']
                    print(f"📊 Total products: {data_info.get('total', 'N/A')}")
                    
                    if 'products' in data_info and isinstance(data_info['products'], list):
                        print(f"📊 Products count: {len(data_info['products'])}")
                        
                        # Kiểm tra cấu trúc sản phẩm đầu tiên
                        if len(data_info['products']) > 0:
                            first_product = data_info['products'][0]
                            print(f"🔍 First product keys: {list(first_product.keys())}")
                            
                            if 'detail' in first_product:
                                detail = first_product['detail']
                                print(f"🔍 Detail keys: {list(detail.keys())}")
            else:
                print(f"⚠️ Dữ liệu không phải dict: {type(data)}")
            
            return data
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return {}
    
    def extract_tablet_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trích xuất dữ liệu máy tính bảng từ JSON"""
        tablets_data = []
        
        if not isinstance(raw_data, dict) or 'data' not in raw_data:
            print("❌ Cấu trúc dữ liệu không hợp lệ")
            return tablets_data
        
        data_section = raw_data['data']
        if not isinstance(data_section, dict) or 'products' not in data_section:
            print("❌ Không tìm thấy danh sách sản phẩm")
            return tablets_data
        
        products = data_section['products']
        if not isinstance(products, list):
            print("❌ Products không phải là danh sách")
            return tablets_data
        
        for product in products:
            if not isinstance(product, dict):
                print(f"⚠️ Bỏ qua sản phẩm không hợp lệ: {type(product)}")
                continue
            
            # Trích xuất thông tin cơ bản
            tablet = {
                'name': product.get('name', ''),
                'brand': product.get('brand', ''),
                'price': product.get('price', ''),
                'priceOld': product.get('priceOld', ''),
                'discount': product.get('discount', ''),
                'image': product.get('image', ''),
                'color': product.get('color', ''),
                'specifications': [],
                'colorOptions': [],
                'images': []
            }
            
            # Trích xuất thông tin chi tiết từ detail
            if 'detail' in product and isinstance(product['detail'], dict):
                detail = product['detail']
                
                # Cập nhật thông tin từ detail nếu có
                if detail.get('title'):
                    tablet['name'] = detail.get('title', tablet['name'])
                if detail.get('price'):
                    tablet['price'] = detail.get('price', tablet['price'])
                if detail.get('priceOld'):
                    tablet['priceOld'] = detail.get('priceOld', tablet['priceOld'])
                
                # Lấy specifications
                tablet['specifications'] = detail.get('specifications', [])
                
                # Lấy colorOptions
                tablet['colorOptions'] = detail.get('colorOptions', [])
                
                # Lấy images
                tablet['images'] = detail.get('images', [])
            
            tablets_data.append(tablet)
        
        return tablets_data
    
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
    
    def process_tablet_data(self, tablets_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Xử lý toàn bộ dữ liệu máy tính bảng"""
        processed_tablets = []
        
        for tablet in tablets_data:
            processed_tablet = {
                'name': tablet['name'],
                'brand': tablet['brand'],
                'price': self.clean_price_data(tablet['price']),
                'priceOld': self.clean_price_data(tablet['priceOld']),
                'discount': tablet['discount'],
                'image': tablet['image'],
                'color': tablet['color'],
                'specifications': self.process_specifications(tablet['specifications']),
                'colorOptions': self.process_color_options(tablet['colorOptions']),
                'images': self.process_images(tablet['images']),
                'summary': {
                    'specCount': len(tablet['specifications']),
                    'colorCount': len(tablet['colorOptions']),
                    'imageCount': len(tablet['images']),
                    'hasDiscount': bool(tablet['discount']),
                    'hasOldPrice': bool(tablet['priceOld'])
                }
            }
            
            processed_tablets.append(processed_tablet)
        
        return processed_tablets
    
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
    
    def save_csv_data(self, tablets_data: List[Dict[str, Any]]) -> bool:
        """Lưu dữ liệu CSV"""
        try:
            csv_data = []
            
            for tablet in tablets_data:
                row = {
                    'name': tablet['name'],
                    'brand': tablet['brand'],
                    'price': tablet['price'],
                    'priceOld': tablet['priceOld'],
                    'discount': tablet['discount'],
                    'image': tablet['image'],
                    'color': tablet['color'],
                    'specifications_count': len(tablet['specifications']),
                    'color_options_count': len(tablet['colorOptions']),
                    'images_count': len(tablet['images']),
                    'specifications': json.dumps(tablet['specifications'], ensure_ascii=False),
                    'color_options': json.dumps(tablet['colorOptions'], ensure_ascii=False),
                    'images': json.dumps(tablet['images'], ensure_ascii=False)
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
        
        with_name = sum(1 for p in processed_data if p['name'])
        with_brand = sum(1 for p in processed_data if p['brand'])
        with_price = sum(1 for p in processed_data if p['price']['numeric'] > 0)
        with_specs = sum(1 for p in processed_data if p['summary']['specCount'] > 0)
        with_images = sum(1 for p in processed_data if p['summary']['imageCount'] > 0)
        with_colors = sum(1 for p in processed_data if p['summary']['colorCount'] > 0)
        
        print(f"\n📊 THỐNG KÊ DỮ LIỆU MÁY TÍNH BẢNG ĐÃ XỬ LÝ:")
        print(f"   📱 Tổng số máy tính bảng: {total}")
        print(f"   📝 Có tên: {with_name}/{total} ({with_name/total*100:.1f}%)")
        print(f"   🏷️ Có brand: {with_brand}/{total} ({with_brand/total*100:.1f}%)")
        print(f"   💰 Có giá: {with_price}/{total} ({with_price/total*100:.1f}%)")
        print(f"   📋 Có thông số: {with_specs}/{total} ({with_specs/total*100:.1f}%)")
        print(f"   🖼️ Có hình ảnh: {with_images}/{total} ({with_images/total*100:.1f}%)")
        print(f"   🎨 Có màu sắc: {with_colors}/{total} ({with_colors/total*100:.1f}%)")
        
        # Thống kê giá
        prices = [p['price']['numeric'] for p in processed_data if p['price']['numeric'] > 0]
        if prices:
            print(f"   💰 Khoảng giá: {min(prices):,}₫ - {max(prices):,}₫")
        
        # Thống kê brand
        brands = {}
        for p in processed_data:
            brand = p['brand']
            if brand:
                brands[brand] = brands.get(brand, 0) + 1
        
        if brands:
            top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"   🏷️ Top brands: {', '.join([f'{brand}({count})' for brand, count in top_brands])}")
        
        # Thống kê hình ảnh
        image_counts = [p['summary']['imageCount'] for p in processed_data]
        if image_counts:
            print(f"   🖼️ Tổng hình ảnh: {sum(image_counts)}")
            print(f"   🖼️ Trung bình hình/máy tính bảng: {sum(image_counts)/len(image_counts):.1f}")
    
    def print_quick_stats(self, tablets_data: List[Dict[str, Any]]):
        """In thống kê nhanh"""
        total = len(tablets_data)
        
        with_name = sum(1 for p in tablets_data if p['name'])
        with_brand = sum(1 for p in tablets_data if p['brand'])
        with_price = sum(1 for p in tablets_data if p['price'])
        with_specs = sum(1 for p in tablets_data if p['specifications'])
        with_images = sum(1 for p in tablets_data if p['images'])
        with_colors = sum(1 for p in tablets_data if p['colorOptions'])
        
        print(f"\n📊 THỐNG KÊ NHANH:")
        print(f"   📱 Tổng số máy tính bảng: {total}")
        print(f"   📝 Có tên: {with_name}/{total} ({with_name/total*100:.1f}%)")
        print(f"   🏷️ Có brand: {with_brand}/{total} ({with_brand/total*100:.1f}%)")
        print(f"   💰 Có giá: {with_price}/{total} ({with_price/total*100:.1f}%)")
        print(f"   📋 Có thông số: {with_specs}/{total} ({with_specs/total*100:.1f}%)")
        print(f"   🖼️ Có hình ảnh: {with_images}/{total} ({with_images/total*100:.1f}%)")
        print(f"   🎨 Có màu sắc: {with_colors}/{total} ({with_colors/total*100:.1f}%)")
    
    def option_1_simple_extract(self):
        """Chức năng 1: Trích xuất đơn giản"""
        print("\n🔍 ĐANG TRÍCH XUẤT DỮ LIỆU MÁY TÍNH BẢNG ĐƠN GIẢN...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        tablets_data = self.extract_tablet_data(raw_data)
        print(f"📊 Đã trích xuất {len(tablets_data)} máy tính bảng")
        
        if self.save_json_data(tablets_data, self.extracted_file):
            self.print_quick_stats(tablets_data)
    
    def option_2_advanced_process(self):
        """Chức năng 2: Xử lý đầy đủ"""
        print("\n⚙️ ĐANG XỬ LÝ DỮ LIỆU MÁY TÍNH BẢNG ĐẦY ĐỦ...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        tablets_data = self.extract_tablet_data(raw_data)
        print(f"📊 Đã trích xuất {len(tablets_data)} máy tính bảng")
        
        processed_data = self.process_tablet_data(tablets_data)
        print(f"✅ Đã xử lý {len(processed_data)} máy tính bảng")
        
        if self.save_json_data(processed_data, self.processed_file):
            print(f"📄 Đã lưu file dữ liệu đã xử lý: {self.processed_file}")
            self.print_quick_stats_from_processed(processed_data)
    
    def option_3_create_csv(self):
        """Chức năng 3: Tạo CSV"""
        print("\n📊 ĐANG TẠO FILE CSV MÁY TÍNH BẢNG...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        tablets_data = self.extract_tablet_data(raw_data)
        print(f"📊 Đã trích xuất {len(tablets_data)} máy tính bảng")
        
        if self.save_csv_data(tablets_data):
            print(f"📈 Số dòng CSV: {len(tablets_data)}")
    
    def option_4_run_all(self):
        """Chức năng 4: Chạy tất cả"""
        print("\n🚀 ĐANG CHẠY TẤT CẢ CHỨC NĂNG MÁY TÍNH BẢNG...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        tablets_data = self.extract_tablet_data(raw_data)
        print(f"📊 Đã trích xuất {len(tablets_data)} máy tính bảng")
        
        # 1. Lưu dữ liệu đơn giản
        print("\n1️⃣ Lưu dữ liệu đơn giản...")
        self.save_json_data(tablets_data, self.extracted_file)
        
        # 2. Xử lý đầy đủ
        print("\n2️⃣ Xử lý dữ liệu đầy đủ...")
        processed_data = self.process_tablet_data(tablets_data)
        self.save_json_data(processed_data, self.processed_file)
        
        # 3. Tạo CSV
        print("\n3️⃣ Tạo file CSV...")
        self.save_csv_data(tablets_data)
        
        # In thống kê từ dữ liệu đã xử lý
        self.print_quick_stats_from_processed(processed_data)
        
        print(f"\n✅ HOÀN THÀNH! Đã tạo các file:")
        print(f"   📄 {self.extracted_file}")
        print(f"   📄 {self.processed_file}")
        print(f"   📊 {self.csv_file}")
    
    def option_5_quick_stats(self):
        """Chức năng 5: Thống kê nhanh"""
        print("\n📈 ĐANG TÍNH THỐNG KÊ NHANH MÁY TÍNH BẢNG...")
        
        if not self.check_input_file():
            return
        
        raw_data = self.load_json_data()
        if not raw_data:
            return
        
        tablets_data = self.extract_tablet_data(raw_data)
        self.print_quick_stats(tablets_data)
    
    def option_6_settings(self):
        """Chức năng 6: Cài đặt"""
        print("\n⚙️ CÀI ĐẶT MÁY TÍNH BẢNG")
        print(f"📁 File đầu vào: {self.input_file}")
        print(f"📄 File trích xuất: {self.extracted_file}")
        print(f"📄 File xử lý: {self.processed_file}")
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
            
            new_csv = input(f"📊 File CSV mới (hiện tại: {self.csv_file}): ").strip()
            if new_csv:
                self.csv_file = new_csv
            
            print("✅ Đã cập nhật cài đặt!")
    
    def run(self):
        """Chạy chương trình chính"""
        print("🚀 TABLET DATA PROCESSOR - KHỞI ĐỘNG")
        
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
    processor = TabletDataProcessor()
    processor.run()

if __name__ == "__main__":
    main()

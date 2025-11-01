#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để xoa truong 'color' khoi cac file JSON da xu ly
"""

import json
import os
import sys
from typing import Dict, Any, List

# Fix encoding cho Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def remove_color_field(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Xóa trường 'color' khỏi mỗi sản phẩm trong danh sách"""
    cleaned_data = []
    removed_count = 0
    
    for product in data:
        if not isinstance(product, dict):
            cleaned_data.append(product)
            continue
        
        # Tạo bản sao và xóa trường 'color'
        cleaned_product = {k: v for k, v in product.items() if k != 'color'}
        
        # Đếm số lượng đã xóa
        if 'color' in product:
            removed_count += 1
        
        cleaned_data.append(cleaned_product)
    
    return cleaned_data, removed_count


def process_file(file_path: str) -> bool:
    """Xử lý một file JSON để xóa trường 'color'"""
    if not os.path.exists(file_path):
        print(f"[WARN] Khong tim thay file: {file_path}")
        return False
    
    try:
        # Doc file
        print(f"[INFO] Dang doc: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"[WARN] File khong phai la mang JSON: {file_path}")
            return False
        
        print(f"   Tong so san pham: {len(data)}")
        
        # Xoa truong 'color'
        cleaned_data, removed_count = remove_color_field(data)
        
        # Luu lai file
        print(f"   Da xoa truong 'color' tu {removed_count} san pham")
        print(f"[INFO] Dang luu: {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
        print(f"[DONE] Hoan tat: {file_path}\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Loi khi xu ly {file_path}: {e}\n")
        return False


def main():
    """Hàm chính"""
    base_dir = os.path.dirname(__file__)
    
    # Danh sách các file cần xử lý
    files_to_process = [
        'processed_phones_data.json',
        'processed_tablets_data.json',
        'processed_smartwatches_data.json',
        'processed_laptops_data.json',
    ]
    
    print("=" * 80)
    print("XOA TRUONG 'color' KHOI CAC FILE JSON")
    print("=" * 80)
    print()
    
    success_count = 0
    for filename in files_to_process:
        file_path = os.path.join(base_dir, filename)
        if process_file(file_path):
            success_count += 1
    
    print("=" * 80)
    print(f"[DONE] Da xu ly {success_count}/{len(files_to_process)} files")
    print("=" * 80)


if __name__ == "__main__":
    main()


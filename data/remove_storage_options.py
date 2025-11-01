import json
import os
from pathlib import Path


def remove_storage_options_from_file(file_path: str, backup: bool = True):
    """Xóa trường storageOptions từ file JSON"""
    print(f"\n{'='*80}")
    print(f"Đang xử lý: {os.path.basename(file_path)}")
    
    # Đọc file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print(f"[ERROR] File không phải là mảng JSON")
        return
    
    # Tạo backup nếu cần
    if backup:
        backup_path = f"{file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Đã tạo backup: {os.path.basename(backup_path)}")
    
    # Đếm số lượng sản phẩm có storageOptions
    removed_count = 0
    total_count = len(data)
    
    # Duyệt qua và xóa storageOptions
    for item in data:
        if isinstance(item, dict) and "storageOptions" in item:
            del item["storageOptions"]
            removed_count += 1
    
    # Lưu lại file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Đã xóa storageOptions từ {removed_count}/{total_count} sản phẩm")
    print(f"[OK] Đã lưu file: {os.path.basename(file_path)}")


def main():
    """Duyệt qua tất cả file JSON trong thư mục data và xóa storageOptions"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_files = [
        "processed_phones_data.json",
        "processed_tablets_data.json",
        "processed_laptops_data.json",
        "processed_smartwatches_data.json"
    ]
    
    print("=" * 80)
    print("TOOL XÓA TRƯỜNG storageOptions")
    print("=" * 80)
    
    for filename in data_files:
        file_path = os.path.join(script_dir, filename)
        if os.path.exists(file_path):
            remove_storage_options_from_file(file_path, backup=True)
        else:
            print(f"[SKIP] Không tìm thấy: {filename}")
    
    print("\n" + "=" * 80)
    print("[DONE] Hoàn tất xử lý tất cả file")
    print("=" * 80)


if __name__ == "__main__":
    main()


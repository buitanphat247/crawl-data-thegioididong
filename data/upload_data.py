import json
import os
import re
from typing import Any, Dict, List, Optional

import requests

# Bearer token mặc định - cập nhật tại đây khi cần
DEFAULT_BEARER_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImlkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJ0YW4yNzA0MDdAZ21haWwuY29tIiwicGhvbmUiOiIwOTg0MzgwMjA1IiwiYXZhdGFyIjoiaHR0cHM6Ly9jZWxscGhvbmVzLmNvbS52bi9zZm9ydW0vd3AtY29udGVudC91cGxvYWRzLzIwMjQvMDIvYXZhdGFyLWFuaC1tZW8tY3V0ZS01LmpwZyIsImFkZHJlc3MiOiI1MC8xNCB2w7UgdGjhu4sgc8OhdSIsInJvbGVJZCI6MSwicm9sZU5hbWUiOiJhZG1pbiIsImlhdCI6MTc2MjAyNzY5NSwiZXhwIjoxNzYyMDMxMjk1fQ.Yv5y8Yr9axBCMhqQ6Df_MwBOkjz6CH8rDQlDK5X3Ft29jLd-LaDIZXeQCjbTSu77_btr7sUpc5L4uutDJvwIVA"


def get_bearer_token() -> str:
    """Lấy bearer token từ biến môi trường hoặc dùng token mặc định"""
    return os.getenv("API_BEARER_TOKEN") or DEFAULT_BEARER_TOKEN


def print_product_info(file_path):
    """Đọc và in thông tin sản phẩm từ file JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n{'='*80}")
    print(f"Đang đọc file: {os.path.basename(file_path)}")
    print(f"Tổng số sản phẩm: {len(data)}")
    print(f"{'='*80}\n")
    
    # Chỉ in 1 sản phẩm đầu tiên
    if not data:
        print("Không có dữ liệu sản phẩm")
        return
    idx, product = 1, data[0]
    print(f"\n--- Sản phẩm {idx} ---")
    product_name = product.get('title') or product.get('name', 'N/A')
    print(f"Name/Title: {product_name}")
    print(f"Brand: {product.get('brand', 'N/A')}")
    print(f"Price: {product.get('price', {}).get('value', 'N/A')}")
    print(f"Price Old: {product.get('priceOld', {}).get('value', 'N/A')}")
    print(f"Discount: {product.get('discount', 'N/A')}")
    print(f"Thumbnail Image: {product.get('image', 'N/A')}")
        
    # List images
    images = product.get('images', {})
    if images and isinstance(images, dict):
        image_urls = images.get('urls', [])
        print(f"List Images ({len(image_urls)} ảnh):")
        for img_idx, img_url in enumerate(image_urls, 1):
            print(f"  {img_idx}. {img_url}")
    else:
        print("List Images: N/A")
        
    # Color options
    color_options = product.get('colorOptions', [])
    if color_options:
        print(f"Color Options ({len(color_options)} màu):")
        for color_idx, color in enumerate(color_options, 1):
            color_name = color.get('name', 'N/A')
            color_hex = color.get('hexColor', 'N/A')
            print(f"  {color_idx}. {color_name} ({color_hex})")
    else:
        print("Color Options: N/A")
        
    # Specifications
    specifications = product.get('specifications', [])
    if specifications:
        print(f"Specifications ({len(specifications)} danh mục):")
        for spec_idx, spec in enumerate(specifications, 1):
            category = spec.get('category', 'N/A')
            items = spec.get('items', [])
            print(f"  {spec_idx}. {category} ({len(items)} items)")
            for item in items[:3]:  # Chỉ hiển thị 3 items đầu
                label = item.get('label', 'N/A')
                value = item.get('value', 'N/A')
                if isinstance(value, list):
                    value = ', '.join(map(str, value))
                print(f"     - {label}: {value}")
            if len(items) > 3:
                print(f"     ... và {len(items) - 3} items khác")
    else:
        print("Specifications: N/A")
    
    print("-" * 80)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[áàạảãăắằặẳẵâấầậẩẫ]", "a", text)
    text = re.sub(r"[éèẹẻẽêếềệểễ]", "e", text)
    text = re.sub(r"[íìịỉĩ]", "i", text)
    text = re.sub(r"[óòọỏõôốồộổỗơớờợởỡ]", "o", text)
    text = re.sub(r"[úùụủũưứừựửữ]", "u", text)
    text = re.sub(r"[ýỳỵỷỹ]", "y", text)
    text = re.sub(r"đ", "d", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    text = re.sub(r"-+", "-", text)
    return text


def get_category_id_by_name(name: str) -> int:
    name_lower = (name or "").lower()
    if any(k in name_lower for k in ["điện thoại", "phone", "smartphone", "iphone", "android"]):
        env_val = os.getenv("CATEGORY_ID_PHONE")
        if env_val and env_val.isdigit():
            return int(env_val)
        return 2
    if any(k in name_lower for k in ["laptop", "máy tính xách tay", "notebook", "macbook"]):
        env_val = os.getenv("CATEGORY_ID_LAPTOP")
        if env_val and env_val.isdigit():
            return int(env_val)
        return 3
    if any(k in name_lower for k in ["đồng hồ", "smartwatch", "watch"]):
        env_val = os.getenv("CATEGORY_ID_SMARTWATCH")
        if env_val and env_val.isdigit():
            return int(env_val)
        return 5
    if any(k in name_lower for k in ["máy tính bảng", "tablet", "ipad"]):
        env_val = os.getenv("CATEGORY_ID_TABLET")
        if env_val and env_val.isdigit():
            return int(env_val)
        return 1
    env_default = os.getenv("CATEGORY_ID_DEFAULT")
    if env_default and env_default.isdigit():
        return int(env_default)
    return 2


def create_product(session: requests.Session, base_url: str, product: Dict[str, Any], category_id: Optional[int] = None) -> Optional[int]:
    # Hỗ trợ cả "name" và "title"
    product_name = product.get("name") or product.get("title", "")
    # Extract brand từ name/title nếu không có trường brand
    brand = product.get("brand", "")
    if not brand and product_name:
        # Lấy từ đầu tiên của tên (ví dụ: "iPhone 16" -> "iPhone")
        parts = product_name.split()
        if parts:
            brand = parts[0]
    
    # Lấy thumbnailImage: ưu tiên image, sau đó lấy ảnh đầu tiên từ images.urls
    thumbnail_image = product.get("image", "")
    if not thumbnail_image:
        images = product.get("images", {})
        if isinstance(images, dict):
            image_urls = images.get("urls", [])
            if image_urls:
                thumbnail_image = image_urls[0]
        elif isinstance(images, list) and images:
            thumbnail_image = images[0]
    
    # Sử dụng category_id được truyền vào hoặc tự động detect
    if category_id is None:
        category_id = get_category_id_by_name(product_name)
    
    payload = {
        "name": product_name,
        "slug": slugify(product_name),
        "brand": brand,
        "categoryId": category_id,
        "price": product.get("price", {}).get("numeric", 0) or 0,
        "priceOld": product.get("priceOld", {}).get("numeric", 0) or 0,
        "discount": product.get("discount", ""),
        "thumbnailImage": thumbnail_image,
        "isPublished": True,
    }
    resp = session.post(f"{base_url}/api/v1/products", json=payload, timeout=30)
    if not resp.ok:
        print(f"[ERROR] Tạo product thất bại: {resp.status_code} {resp.text}")
        return None
    data = resp.json()
    product_id = data.get("id") or data.get("data", {}).get("id")
    print(f"[OK] Tạo product id={product_id}")
    return product_id


def upload_colors(session: requests.Session, base_url: str, product_id: int, colors: List[Dict[str, Any]]):
    for color in colors:
        hex_color = color.get("hexColor", "").strip()
        color_name = color.get("name", "")
        
        # Bỏ qua màu không có mã hex
        if not hex_color:
            print(f"[SKIP] Bỏ qua màu '{color_name}' - Không có mã hex")
            continue
        
        payload = {
            "productId": product_id,
            "name": color_name,
            "slug": slugify(color_name),
            "hexColor": hex_color,
        }
        resp = session.post(f"{base_url}/api/v1/product-colors", json=payload, timeout=30)
        if not resp.ok:
            print(f"[ERROR] Tạo màu thất bại: {resp.status_code} {resp.text}")
        else:
            print(f"[OK] Thêm màu: {payload['name']}")


def upload_images(session: requests.Session, base_url: str, product_id: int, image_urls: List[str]):
    for url in image_urls:
        payload = {"productId": product_id, "url": url}
        resp = session.post(f"{base_url}/api/v1/product-images", json=payload, timeout=30)
        if not resp.ok:
            print(f"[ERROR] Thêm ảnh thất bại: {resp.status_code} {resp.text}")
        else:
            print(f"[OK] Thêm ảnh: {url}")


def upload_specifications(session: requests.Session, base_url: str, product_id: int, specifications: List[Dict[str, Any]]):
    for group in specifications:
        group_name = group.get("category", "")
        for item in group.get("items", []):
            value = item.get("value")
            if isinstance(value, list):
                value = ", ".join(map(str, value))
            payload = {
                "productId": product_id,
                "groupName": group_name,
                "label": item.get("label", ""),
                "value": value or "",
                "type": item.get("type", "string"),
            }
            resp = session.post(
                f"{base_url}/api/v1/product-specifications", json=payload, timeout=30
            )
            if not resp.ok:
                print(
                    f"[ERROR] Thêm thông số thất bại: {resp.status_code} {resp.text}"
                )
            else:
                print(f"[OK] Thêm thông số: {group_name} - {payload['label']}")


def upload_first_tablet(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        print("[ERROR] Không có dữ liệu để upload")
        return

    product = data[0]
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    token = get_bearer_token()

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })

    product_id = create_product(session, base_url, product)
    if not product_id:
        return

    # Upload colors
    colors = product.get("colorOptions", [])
    if colors:
        upload_colors(session, base_url, product_id, colors)

    # Upload images
    images = product.get("images", {})
    urls = images.get("urls", []) if isinstance(images, dict) else []
    if urls:
        upload_images(session, base_url, product_id, urls)

    # Upload specifications
    specs = product.get("specifications", [])
    if specs:
        upload_specifications(session, base_url, product_id, specs)


def upload_all_tablets(file_path: str, category_id: int = 1):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        print("[ERROR] Không có dữ liệu để upload")
        return
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    token = get_bearer_token()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    print(f"[INFO] Bắt đầu upload {len(data)} sản phẩm tablets")
    skipped_count = 0
    for i, product in enumerate(data, 1):
        product_name = product.get('name', '')
        
        # Kiểm tra price: phải có price hoặc priceOld
        price_numeric = product.get("price", {}).get("numeric", 0) or 0
        price_old_numeric = product.get("priceOld", {}).get("numeric", 0) or 0
        
        if not price_numeric and not price_old_numeric:
            skipped_count += 1
            print(f"[SKIP] ({i}/{len(data)}) Bỏ qua {product_name} - Không có price")
            continue
        
        print(f"[INFO] ({i}/{len(data)}) {product_name} ...")
        product_id = create_product(session, base_url, product, category_id)
        if not product_id:
            continue
        colors = product.get("colorOptions", [])
        if colors:
            upload_colors(session, base_url, product_id, colors)
        images = product.get("images", {})
        urls = images.get("urls", []) if isinstance(images, dict) else []
        if urls:
            upload_images(session, base_url, product_id, urls)
        specs = product.get("specifications", [])
        if specs:
            upload_specifications(session, base_url, product_id, specs)
    print(f"\n[DONE] Hoàn tất upload tablets (categoryId={category_id})")
    if skipped_count > 0:
        print(f"[INFO] Đã bỏ qua {skipped_count} sản phẩm không có price")


def upload_all_smartwatches(file_path: str, category_id: int = 5):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        print("[ERROR] Không có dữ liệu để upload")
        return
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    token = get_bearer_token()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    print(f"[INFO] Bắt đầu upload {len(data)} sản phẩm smartwatches")
    skipped_count = 0
    for i, product in enumerate(data, 1):
        product_name = product.get('name', '')
        
        # Kiểm tra price: phải có price hoặc priceOld
        price_numeric = product.get("price", {}).get("numeric", 0) or 0
        price_old_numeric = product.get("priceOld", {}).get("numeric", 0) or 0
        
        if not price_numeric and not price_old_numeric:
            skipped_count += 1
            print(f"[SKIP] ({i}/{len(data)}) Bỏ qua {product_name} - Không có price")
            continue
        
        print(f"[INFO] ({i}/{len(data)}) {product_name} ...")
        product_id = create_product(session, base_url, product, category_id)
        if not product_id:
            continue
        colors = product.get("colorOptions", [])
        if colors:
            upload_colors(session, base_url, product_id, colors)
        images = product.get("images", {})
        urls = images.get("urls", []) if isinstance(images, dict) else []
        if urls:
            upload_images(session, base_url, product_id, urls)
        specs = product.get("specifications", [])
        if specs:
            upload_specifications(session, base_url, product_id, specs)
    print(f"\n[DONE] Hoàn tất upload smartwatches (categoryId={category_id})")
    if skipped_count > 0:
        print(f"[INFO] Đã bỏ qua {skipped_count} sản phẩm không có price")


def upload_all_laptops(file_path: str, category_id: int = 3):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        print("[ERROR] Không có dữ liệu để upload")
        return
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    token = get_bearer_token()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    print(f"[INFO] Bắt đầu upload {len(data)} sản phẩm laptops")
    skipped_count = 0
    for i, product in enumerate(data, 1):
        product_name = product.get('name', '')
        
        # Kiểm tra price: phải có price hoặc priceOld
        price_numeric = product.get("price", {}).get("numeric", 0) or 0
        price_old_numeric = product.get("priceOld", {}).get("numeric", 0) or 0
        
        if not price_numeric and not price_old_numeric:
            skipped_count += 1
            print(f"[SKIP] ({i}/{len(data)}) Bỏ qua {product_name} - Không có price")
            continue
        
        print(f"[INFO] ({i}/{len(data)}) {product_name} ...")
        product_id = create_product(session, base_url, product, category_id)
        if not product_id:
            continue
        colors = product.get("colorOptions", [])
        if colors:
            upload_colors(session, base_url, product_id, colors)
        images = product.get("images", {})
        urls = images.get("urls", []) if isinstance(images, dict) else []
        if urls:
            upload_images(session, base_url, product_id, urls)
        specs = product.get("specifications", [])
        if specs:
            upload_specifications(session, base_url, product_id, specs)
    print(f"\n[DONE] Hoàn tất upload laptops (categoryId={category_id})")
    if skipped_count > 0:
        print(f"[INFO] Đã bỏ qua {skipped_count} sản phẩm không có price")


def upload_all_phones(file_path: str, category_id: int = 2):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        print("[ERROR] Không có dữ liệu để upload")
        return
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    token = get_bearer_token()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    print(f"[INFO] Bắt đầu upload {len(data)} sản phẩm phones")
    skipped_count = 0
    for i, product in enumerate(data, 1):
        product_name = product.get('title', product.get('name', ''))
        
        # Kiểm tra price: phải có price hoặc priceOld
        price_numeric = product.get("price", {}).get("numeric", 0) or 0
        price_old_numeric = product.get("priceOld", {}).get("numeric", 0) or 0
        
        if not price_numeric and not price_old_numeric:
            skipped_count += 1
            print(f"[SKIP] ({i}/{len(data)}) Bỏ qua {product_name} - Không có price")
            continue
        
        print(f"[INFO] ({i}/{len(data)}) {product_name} ...")
        product_id = create_product(session, base_url, product, category_id)
        if not product_id:
            continue
        colors = product.get("colorOptions", [])
        if colors:
            upload_colors(session, base_url, product_id, colors)
        images = product.get("images", {})
        urls = images.get("urls", []) if isinstance(images, dict) else []
        if urls:
            upload_images(session, base_url, product_id, urls)
        specs = product.get("specifications", [])
        if specs:
            upload_specifications(session, base_url, product_id, specs)
    print(f"\n[DONE] Hoàn tất upload phones (categoryId={category_id})")
    if skipped_count > 0:
        print(f"[INFO] Đã bỏ qua {skipped_count} sản phẩm không có price")


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    
    # Danh sách files và categoryId tương ứng - UPLOAD TẤT CẢ FILES
    files_to_upload = [
        ('processed_laptops_data.json', upload_all_laptops, 3, 'laptops'),
        ('processed_tablets_data.json', upload_all_tablets, 1, 'tablets'),
        ('processed_phones_data.json', upload_all_phones, 2, 'phones'),
        ('processed_smartwatches_data.json', upload_all_smartwatches, 5, 'smartwatches'),
    ]
    
    print("=" * 80)
    print("CHẠY UPLOAD TẤT CẢ FILES")
    print("=" * 80)
    
    # Chạy lần lượt từng file
    for filename, upload_func, category_id, product_type in files_to_upload:
        file_path = os.path.join(base_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"\n⚠️ Không tìm thấy file: {filename}")
            continue
        
        print(f"\n{'='*80}")
        print(f"📱 BẮT ĐẦU UPLOAD {product_type.upper()} (categoryId={category_id})")
        print(f"📄 File: {filename}")
        print(f"{'='*80}\n")
        
        # In thông tin sản phẩm đầu tiên
        print_product_info(file_path)
        
        # Upload
        upload_func(file_path, category_id)
        
        print(f"\n✅ Hoàn tất {product_type}")
    
    print("\n" + "=" * 80)
    print("✅ ĐÃ HOÀN TẤT UPLOAD TẤT CẢ FILES")
    print("=" * 80)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test upload 1 sản phẩm smartwatch
"""

import json
import os
import sys
import requests
from typing import Dict, Any, Optional

# Fix encoding cho Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import từ upload_data.py
sys.path.insert(0, os.path.dirname(__file__))
from upload_data import get_bearer_token, create_product, upload_colors, upload_images, upload_specifications


def test_upload_one_smartwatch():
    """Test upload 1 sản phẩm smartwatch"""
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'processed_smartwatches_data.json')
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Khong tim thay file: {file_path}")
        return
    
    # Doc file
    print(f"[INFO] Dang doc: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        print("[ERROR] Khong co du lieu")
        return
    
    # Lay san pham dau tien
    product = data[0]
    print(f"\n{'='*80}")
    print(f"TEST UPLOAD 1 SAN PHAM SMARTWATCH")
    print(f"{'='*80}\n")
    
    # In thong tin san pham
    print("Thong tin san pham:")
    print(f"  Name: {product.get('name', 'N/A')}")
    print(f"  Brand: {product.get('brand', 'N/A')}")
    print(f"  Price: {product.get('price', {}).get('numeric', 0)}")
    print(f"  PriceOld: {product.get('priceOld', {}).get('numeric', 0)}")
    print(f"  Image: {product.get('image', 'N/A')[:80]}...")
    print(f"  Has colorOptions: {bool(product.get('colorOptions'))}")
    print(f"  Has images: {bool(product.get('images'))}")
    print(f"  Has specifications: {bool(product.get('specifications'))}")
    
    # Kiem tra cau truc images
    images = product.get("images")
    print(f"\n  Cau truc images: {type(images)}")
    if isinstance(images, dict):
        print(f"    - urls: {images.get('urls', [])[:3]}")
    elif isinstance(images, list):
        print(f"    - list: {images[:3]}")
    else:
        print(f"    - value: {images}")
    
    # Setup session
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080")
    token = get_bearer_token()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    
    category_id = 5
    
    print(f"\n{'='*80}")
    print(f"BAT DAU UPLOAD (categoryId={category_id})")
    print(f"{'='*80}\n")
    
    # Kiem tra price
    price_numeric = product.get("price", {}).get("numeric", 0) or 0
    price_old_numeric = product.get("priceOld", {}).get("numeric", 0) or 0
    
    if not price_numeric and not price_old_numeric:
        print("[SKIP] Khong co price")
        return
    
    # Upload product
    print("[1/4] Tao product...")
    try:
        product_id = create_product(session, base_url, product, category_id)
        if not product_id:
            print("[ERROR] Tao product that bai")
            return
        print(f"[SUCCESS] Product ID: {product_id}\n")
    except Exception as e:
        print(f"[ERROR] Loi khi tao product: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Upload colors
    print("[2/4] Upload colors...")
    colors = product.get("colorOptions", [])
    if colors:
        try:
            upload_colors(session, base_url, product_id, colors)
            print(f"[SUCCESS] Uploaded {len(colors)} colors\n")
        except Exception as e:
            print(f"[ERROR] Loi khi upload colors: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[SKIP] Khong co colors\n")
    
    # Upload images
    print("[3/4] Upload images...")
    images = product.get("images", {})
    urls = []
    if isinstance(images, dict):
        urls = images.get("urls", [])
    elif isinstance(images, list):
        urls = images
    
    if urls:
        try:
            upload_images(session, base_url, product_id, urls)
            print(f"[SUCCESS] Uploaded {len(urls)} images\n")
        except Exception as e:
            print(f"[ERROR] Loi khi upload images: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[SKIP] Khong co images\n")
    
    # Upload specifications
    print("[4/4] Upload specifications...")
    specs = product.get("specifications", [])
    if specs:
        try:
            upload_specifications(session, base_url, product_id, specs)
            print(f"[SUCCESS] Uploaded specifications\n")
        except Exception as e:
            print(f"[ERROR] Loi khi upload specifications: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[SKIP] Khong co specifications\n")
    
    print(f"{'='*80}")
    print(f"[DONE] Hoan tat test upload")
    print(f"{'='*80}")


if __name__ == "__main__":
    test_upload_one_smartwatch()


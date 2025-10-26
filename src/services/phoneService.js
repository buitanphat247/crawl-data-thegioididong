const puppeteer = require('puppeteer');
const fs = require('fs');
const { processMultiLineValue, saveCache, retryWithBackoff } = require('../utils/helpers');
const { crawlPhoneDetail } = require('./productDetailService');

// Hàm crawl điện thoại
async function crawlPhones() {
  try {
    console.log('📱 Đang crawl dữ liệu điện thoại từ thegioididong.com...');
    
    const browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox', 
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--disable-gpu'
      ],
      timeout: 60000
    });
    
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    // Truy cập trang điện thoại với retry
    await retryWithBackoff(async () => {
      console.log('🌐 Đang truy cập trang điện thoại...');
      await page.goto('https://www.thegioididong.com/dtdd#c=42&o=13&pi=8', { 
        waitUntil: 'domcontentloaded',
        timeout: 60000 
      });
      
      // Chờ thêm một chút để đảm bảo trang load hoàn toàn
      await page.waitForTimeout(5000);
    });
    
    // Chờ trang load hoàn toàn
    await page.waitForTimeout(3000);
    
    // Crawl dữ liệu sản phẩm cơ bản
    const products = await page.evaluate(() => {
      const productElements = document.querySelectorAll('li.item.ajaxed');
      const products = [];
      
      productElements.forEach((item, index) => {
        try {
          const link = item.querySelector('a.main-contain');
          const img = item.querySelector('img.thumb');
          const title = item.querySelector('h3');
          const price = item.querySelector('strong.price');
          const priceOld = item.querySelector('p.price-old');
          const percent = item.querySelector('span.percent');
          const rating = item.querySelector('b');
          const sold = item.querySelector('span');
          const gift = item.querySelector('p.item-gift');
          const compare = item.querySelector('.item-compare');
          const label = item.querySelector('.lb-tragop');
          
          if (link && title && price) {
            products.push({
              id: item.getAttribute('data-id') || '',
              productCode: item.getAttribute('data-productcode') || '',
              name: title.textContent.trim(),
              brand: link.getAttribute('data-brand') || '',
              price: price.textContent.trim(),
              priceOld: priceOld ? priceOld.textContent.trim() : '',
              discount: percent ? percent.textContent.trim() : '',
              image: img ? img.src : '',
              link: 'https://www.thegioididong.com' + link.getAttribute('href'),
              rating: rating ? rating.textContent.trim() : '',
              sold: sold ? sold.textContent.trim() : '',
              gift: gift ? gift.textContent.trim() : '',
              color: link.getAttribute('data-color') || '',
              dataPrice: item.getAttribute('data-price') || '',
              compare: compare ? compare.textContent.trim() : '',
              label: label ? label.textContent.trim() : '',
              dataIndex: item.getAttribute('data-index') || '',
              dataPos: item.getAttribute('data-pos') || ''
            });
          }
        } catch (error) {
          console.error('Error parsing product:', error);
        }
      });
      
      return products;
    });
    
    console.log(`📊 Đã crawl ${products.length} sản phẩm cơ bản, bắt đầu crawl chi tiết...`);
    
    // Crawl chi tiết cho từng sản phẩm - CHỈ LƯU NHỮNG SẢN PHẨM CÓ DETAIL HỢP LỆ
    const productsWithDetail = [];
    for (let i = 0; i < products.length; i++) {
      const product = products[i];
      console.log(`🔍 Crawl chi tiết sản phẩm ${i + 1}/${products.length}: ${product.name}`);
      
      try {
        const detail = await retryWithBackoff(async () => {
          return await crawlPhoneDetail(page, product.link);
        }, 2, 1000);
        
        if (detail) {
          // Kiểm tra nếu detail có dữ liệu hợp lệ
          const hasValidDetail = detail.title || 
                                detail.price || 
                                detail.label || 
                                (detail.specifications && detail.specifications.length > 0);
          
          if (hasValidDetail) {
            // CHỈ LƯU KHI CÓ DETAIL HỢP LỆ
            productsWithDetail.push({
              ...product,
              detail: detail
            });
            console.log(`✅ Đã lưu sản phẩm có detail: ${product.name}`);
          } else {
            // BỎ QUA SẢN PHẨM KHÔNG CÓ DETAIL HỢP LỆ
            console.log(`⚠️ Bỏ qua sản phẩm không có detail hợp lệ: ${product.name}`);
          }
        } else {
          // BỎ QUA SẢN PHẨM CRAWL DETAIL THẤT BẠI
          console.log(`❌ Bỏ qua sản phẩm crawl detail thất bại: ${product.name}`);
        }
      } catch (error) {
        console.error(`❌ Lỗi crawl chi tiết ${product.name}:`, error.message);
        console.log(`⚠️ Bỏ qua sản phẩm do lỗi: ${product.name}`);
      }
      
      // Chờ một chút giữa các request để tránh bị block
      await page.waitForTimeout(2000);
    }
    
    // Lưu cache cho toàn bộ danh sách sản phẩm
    const listCacheKey = `products_list`;
    saveCache(listCacheKey, productsWithDetail);
    
    await browser.close();
    
    return {
      success: true,
      message: `Crawl thành công ${productsWithDetail.length} sản phẩm điện thoại`,
      data: {
        total: productsWithDetail.length,
        products: productsWithDetail,
        crawledAt: new Date().toISOString()
      }
    };
    
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu điện thoại:', error);
    return {
      success: false,
      message: 'Lỗi khi crawl dữ liệu điện thoại',
      error: error.message
    };
  }
}

module.exports = {
  crawlPhones
};

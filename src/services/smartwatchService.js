const puppeteer = require('puppeteer');
const fs = require('fs');
const { processMultiLineValue } = require('../utils/helpers');
const { crawlSmartwatchDetail } = require('./productDetailService');

// Crawl dữ liệu đồng hồ thông minh từ thegioididong.com
async function crawlSmartwatches() {
  try {
    console.log('⌚ Đang crawl dữ liệu đồng hồ thông minh từ thegioididong.com...');
    
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    // Truy cập trang đồng hồ thông minh
    await page.goto('https://www.thegioididong.com/dong-ho-thong-minh#c=7077&o=13&pi=7', { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    // Chờ trang load hoàn toàn
    await page.waitForTimeout(3000);
    
    // Crawl dữ liệu sản phẩm đồng hồ thông minh
    const products = await page.evaluate(() => {
      const productElements = document.querySelectorAll('li.__cate_7077');
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
            // Lấy ảnh từ src hoặc data-src (lazy loading)
            let imageUrl = '';
            if (img) {
              imageUrl = img.src || img.getAttribute('data-src') || '';
            }
            
            products.push({
              id: item.getAttribute('data-id') || '',
              productCode: item.getAttribute('data-productcode') || '',
              name: title.textContent.trim(),
              brand: link.getAttribute('data-brand') || '',
              price: price.textContent.trim(),
              priceOld: priceOld ? priceOld.textContent.trim() : '',
              discount: percent ? percent.textContent.trim() : '',
              image: imageUrl,
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
          console.error('Error parsing smartwatch product:', error);
        }
      });
      
      return products;
    });
    
    // Xử lý dữ liệu nhiều dòng sau khi crawl cho tất cả các field
    products.forEach(product => {
      // Xử lý tất cả các field có thể có dữ liệu nhiều dòng
      const fieldsToProcess = [
        'name', 'brand', 'price', 'priceOld', 'discount', 'rating', 
        'sold', 'gift', 'color', 'compare', 'label'
      ];
      
      fieldsToProcess.forEach(field => {
        if (product[field]) {
          product[field] = processMultiLineValue(product[field]);
        }
      });
    });
    
    console.log(`📊 Đã crawl ${products.length} sản phẩm đồng hồ thông minh cơ bản, bắt đầu crawl chi tiết...`);
    
    // Khởi tạo file smartwatches.json với dữ liệu trống
    let smartwatchesData = {
      success: true,
      message: "Đang crawl dữ liệu đồng hồ thông minh...",
      data: {
        total: 0,
        products: [],
        crawledAt: new Date().toISOString()
      }
    };
    
    // Lưu file ban đầu
    fs.writeFileSync('./smartwatches.json', JSON.stringify(smartwatchesData, null, 2));
    console.log(`💾 Đã tạo file smartwatches.json`);
    
    // Crawl chi tiết cho từng sản phẩm đồng hồ thông minh
    const productsWithDetail = [];
    for (let i = 0; i < products.length; i++) {
      const product = products[i];
      console.log(`🔍 Crawl chi tiết đồng hồ thông minh ${i + 1}/${products.length}: ${product.name}`);
      
      try {
        const detail = await crawlSmartwatchDetail(page, product.link);
        
        if (detail) {
          // Kiểm tra nếu detail có dữ liệu hợp lệ
          const hasValidDetail = detail.title || 
                                detail.price || 
                                (detail.specifications && detail.specifications.length > 0);
          
          if (hasValidDetail) {
            const finalProduct = {
              ...product,
              detail: detail
            };
            
            productsWithDetail.push(finalProduct);
            
            // Lưu ngay sản phẩm vừa crawl được (chỉ lưu khi có detail hợp lệ)
            smartwatchesData.data.products.push(finalProduct);
            smartwatchesData.data.total = smartwatchesData.data.products.length;
            smartwatchesData.message = `Đã crawl ${smartwatchesData.data.total}/${products.length} sản phẩm đồng hồ thông minh`;
            
            fs.writeFileSync('./smartwatches.json', JSON.stringify(smartwatchesData, null, 2));
            console.log(`💾 Đã lưu sản phẩm ${i + 1}/${products.length}: ${product.name}`);
          } else {
            // Nếu detail không có dữ liệu hợp lệ, bỏ qua không lưu
            console.log(`⚠️ Bỏ qua sản phẩm ${i + 1}/${products.length} (không có dữ liệu detail): ${product.name}`);
          }
        } else {
          // Nếu crawl detail thất bại, bỏ qua không lưu
          console.log(`⚠️ Bỏ qua sản phẩm ${i + 1}/${products.length} (lỗi crawl detail): ${product.name}`);
        }
        
      } catch (error) {
        console.error(`❌ Lỗi crawl chi tiết ${product.link}:`, error);
        // Nếu crawl detail thất bại, bỏ qua không lưu
        console.log(`⚠️ Bỏ qua sản phẩm ${i + 1}/${products.length} (lỗi crawl detail): ${product.name}`);
      }
      
      // Chờ một chút giữa các request để tránh bị block
      await page.waitForTimeout(1000);
    }
    
    await browser.close();
    
    // Cập nhật thông báo cuối cùng
    smartwatchesData.message = `Crawl thành công ${productsWithDetail.length} sản phẩm đồng hồ thông minh với chi tiết`;
    smartwatchesData.data.crawledAt = new Date().toISOString();
    
    try {
      fs.writeFileSync('./smartwatches.json', JSON.stringify(smartwatchesData, null, 2));
      console.log(`💾 Đã hoàn thành lưu dữ liệu đồng hồ thông minh vào smartwatches.json`);
    } catch (error) {
      console.error('❌ Lỗi lưu file smartwatches.json cuối cùng:', error);
    }
    
    return smartwatchesData;
    
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu đồng hồ thông minh:', error);
    return {
      success: false,
      message: 'Lỗi khi crawl dữ liệu đồng hồ thông minh',
      error: error.message
    };
  }
}

module.exports = {
  crawlSmartwatches
};

const puppeteer = require('puppeteer');
const fs = require('fs');
const { processMultiLineValue } = require('../utils/helpers');
const { crawlTabletDetail } = require('./productDetailService');

// Crawl dữ liệu máy tính bảng từ thegioididong.com
async function crawlTablets() {
  try {
    console.log('📱 Đang crawl dữ liệu máy tính bảng từ thegioididong.com...');
    
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    // Truy cập trang máy tính bảng
    await page.goto('https://www.thegioididong.com/may-tinh-bang#c=522&o=13&pi=3', { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    // Chờ trang load hoàn toàn
    await page.waitForTimeout(3000);
    
    // Crawl dữ liệu sản phẩm máy tính bảng
    const products = await page.evaluate(() => {
      const productElements = document.querySelectorAll('li.__cate_522');
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
          console.error('Error parsing tablet product:', error);
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
    
    console.log(`📊 Đã crawl ${products.length} sản phẩm máy tính bảng cơ bản, bắt đầu crawl chi tiết...`);
    
    // Khởi tạo file tablets.json với dữ liệu trống
    let tabletsData = {
      success: true,
      message: "Đang crawl dữ liệu máy tính bảng...",
      data: {
        total: 0,
        products: [],
        crawledAt: new Date().toISOString()
      }
    };
    
    // Lưu file ban đầu
    fs.writeFileSync('./tablets.json', JSON.stringify(tabletsData, null, 2));
    console.log(`💾 Đã tạo file tablets.json`);
    
    // Crawl chi tiết cho từng sản phẩm máy tính bảng
    const productsWithDetail = [];
    for (let i = 0; i < products.length; i++) {
      const product = products[i];
      console.log(`🔍 Crawl chi tiết máy tính bảng ${i + 1}/${products.length}: ${product.name}`);
      
      try {
        const detail = await crawlTabletDetail(page, product.link);
        
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
            tabletsData.data.products.push(finalProduct);
            tabletsData.data.total = tabletsData.data.products.length;
            tabletsData.message = `Đã crawl ${tabletsData.data.total}/${products.length} sản phẩm máy tính bảng`;
            
            fs.writeFileSync('./tablets.json', JSON.stringify(tabletsData, null, 2));
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
    tabletsData.message = `Crawl thành công ${productsWithDetail.length} sản phẩm máy tính bảng với chi tiết`;
    tabletsData.data.crawledAt = new Date().toISOString();
    
    try {
      fs.writeFileSync('./tablets.json', JSON.stringify(tabletsData, null, 2));
      console.log(`💾 Đã hoàn thành lưu dữ liệu máy tính bảng vào tablets.json`);
    } catch (error) {
      console.error('❌ Lỗi lưu file tablets.json cuối cùng:', error);
    }
    
    return tabletsData;
    
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu máy tính bảng:', error);
    return {
      success: false,
      message: 'Lỗi khi crawl dữ liệu máy tính bảng',
      error: error.message
    };
  }
}

module.exports = {
  crawlTablets
};

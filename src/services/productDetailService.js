const puppeteer = require('puppeteer');
const { processMultiLineValue, saveCache, loadCache } = require('../utils/helpers');

// Hàm crawl chi tiết sản phẩm điện thoại
async function crawlPhoneDetail(page, productUrl) {
  try {
    // Tạo cache key từ URL
    const cacheKey = productUrl.replace(/[^a-zA-Z0-9]/g, '_');
    
    // Kiểm tra cache trước
    const cachedData = loadCache(cacheKey);
    if (cachedData) {
      console.log(`📂 Sử dụng cache cho: ${productUrl}`);
      return cachedData;
    }
    
    console.log(`🔍 Đang crawl chi tiết: ${productUrl}`);
    
    // Truy cập trang sản phẩm
    await page.goto(productUrl, { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    // Chờ trang load hoàn toàn
    await page.waitForTimeout(2000);
    
    // Crawl thông tin chi tiết sản phẩm
    const productDetail = await page.evaluate(() => {
      // Thông tin cơ bản
      const title = document.querySelector('h1')?.textContent?.trim() || '';
      const price = document.querySelector('.box-price-present')?.textContent?.trim() || '';
      const priceOld = document.querySelector('.box-price-old')?.textContent?.trim() || '';
      const discount = document.querySelector('.box-price-percent')?.textContent?.trim() || '';
      const label = document.querySelector('.label')?.textContent?.trim() || '';
      
      // Thông số kỹ thuật
      const specifications = [];
      const specItems = document.querySelectorAll('.specification-item .box-specifi');
      
      specItems.forEach(spec => {
        const category = spec.querySelector('h3')?.textContent?.trim() || '';
        const items = [];
        
        const specList = spec.querySelectorAll('ul.text-specifi li');
        specList.forEach(item => {
          const label = item.querySelector('aside:first-child')?.textContent?.trim() || '';
          const value = item.querySelector('aside:last-child')?.textContent?.trim() || '';
          
          if (label && value) {
            items.push({ label, value });
          }
        });
        
        if (category && items.length > 0) {
          specifications.push({ category, items });
        }
      });
      
      // Các phiên bản dung lượng
      const storageOptions = [];
      const storageItems = document.querySelectorAll('.box03__item.item');
      storageItems.forEach(item => {
        const text = item.textContent?.trim();
        const isActive = item.classList.contains('act');
        if (text && !text.includes('Titan') && !text.includes('#')) {
          storageOptions.push({ option: text, isActive });
        }
      });
      
      // Các màu sắc
      const colorOptions = [];
      const colorItems = document.querySelectorAll('.box03.color .box03__item.item');
      colorItems.forEach(item => {
        const text = item.textContent?.trim();
        const isActive = item.classList.contains('act');
        const colorCode = item.getAttribute('data-color');
        const productCode = item.getAttribute('data-code');
        const colorStyle = item.querySelector('i')?.getAttribute('style');
        
        if (text) {
          colorOptions.push({ 
            name: text, 
            isActive, 
            colorCode, 
            productCode,
            colorStyle 
          });
        }
      });
      
      // Hình ảnh sản phẩm từ slider/carousel - chỉ lấy từ 2 container cụ thể
      const images = [];
      
      // Lấy hình ảnh từ feature-img (slider chính) - chỉ lấy trong container này
      const featureContainer = document.querySelector('.feature-img');
      if (featureContainer) {
        const featureImages = featureContainer.querySelectorAll('.owl-stage .owl-item img');
        featureImages.forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      }
      
      // Lấy hình ảnh từ gallery-img (slider phụ) - chỉ lấy trong container này
      const galleryContainer = document.querySelector('.gallery-img');
      if (galleryContainer) {
        const galleryImages = galleryContainer.querySelectorAll('.owl-stage .owl-item img');
        galleryImages.forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      }
      
      return {
        title,
        price,
        priceOld,
        discount,
        label,
        specifications,
        storageOptions,
        colorOptions,
        images
      };
    });
    
    // Xử lý dữ liệu nhiều dòng sau khi crawl
    if (productDetail.specifications) {
      productDetail.specifications.forEach(spec => {
        if (spec.items) {
          spec.items.forEach(item => {
            if (typeof item.value === 'string') {
              item.value = processMultiLineValue(item.value);
            }
          });
        }
      });
    }
    
    // Kiểm tra nếu không có dữ liệu quan trọng thì không lưu cache
    const hasValidData = productDetail.title || 
                        productDetail.price || 
                        productDetail.label || 
                        (productDetail.specifications && productDetail.specifications.length > 0);
    
    if (hasValidData) {
      // Lưu cache chỉ khi có dữ liệu hợp lệ
      saveCache(cacheKey, productDetail);
      console.log(`✅ Đã lưu cache cho sản phẩm có dữ liệu: ${productUrl}`);
    } else {
      console.log(`⚠️ Bỏ qua cache cho sản phẩm không có dữ liệu: ${productUrl}`);
    }
    
    return productDetail;
    
  } catch (error) {
    console.error(`❌ Lỗi crawl chi tiết ${productUrl}:`, error);
    return null;
  }
}

// Hàm crawl chi tiết sản phẩm laptop
async function crawlLaptopDetail(page, productUrl) {
  try {
    // Tạo cache key từ URL
    const cacheKey = productUrl.replace(/[^a-zA-Z0-9]/g, '_');
    
    // Kiểm tra cache trước
    const cachedData = loadCache(cacheKey);
    if (cachedData) {
      console.log(`📂 Sử dụng cache cho: ${productUrl}`);
      return cachedData;
    }
    
    console.log(`🔍 Đang crawl chi tiết laptop: ${productUrl}`);
    
    // Truy cập trang sản phẩm
    await page.goto(productUrl, { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    // Chờ trang load hoàn toàn
    await page.waitForTimeout(2000);
    
    // Crawl thông tin chi tiết sản phẩm
    const productDetail = await page.evaluate(() => {
      // Thông tin cơ bản
      const title = document.querySelector('h1')?.textContent?.trim() || '';
      const price = document.querySelector('.bs_price strong')?.textContent?.trim() || '';
      const priceOld = document.querySelector('.bs_price em')?.textContent?.trim() || '';
      const rating = document.querySelector('.detail-rate p')?.textContent?.trim() || '';
      const sold = document.querySelector('.quantity-sale')?.textContent?.trim() || '';
      
      // Thông số kỹ thuật
      const specifications = [];
      const specItems = document.querySelectorAll('.specification-item .box-specifi');
      
      specItems.forEach(spec => {
        const category = spec.querySelector('h3')?.textContent?.trim() || '';
        const items = [];
        
        const specList = spec.querySelectorAll('ul.text-specifi li');
        specList.forEach(item => {
          const label = item.querySelector('aside:first-child')?.textContent?.trim() || '';
          const value = item.querySelector('aside:last-child')?.textContent?.trim() || '';
          
          if (label && value) {
            items.push({ label, value });
          }
        });
        
        if (category && items.length > 0) {
          specifications.push({ category, items });
        }
      });
      
      // Các màu sắc
      const colorOptions = [];
      const colorItems = document.querySelectorAll('.box03.color .box03__item.item');
      colorItems.forEach(item => {
        const text = item.textContent?.trim();
        const isActive = item.classList.contains('act');
        const colorCode = item.getAttribute('data-color');
        const productCode = item.getAttribute('data-code');
        const colorStyle = item.querySelector('i')?.getAttribute('style');
        
        if (text) {
          colorOptions.push({ 
            name: text, 
            isActive, 
            colorCode, 
            productCode,
            colorStyle 
          });
        }
      });
      
      // Hình ảnh sản phẩm từ slider/carousel
      const images = [];
      
      // Lấy hình ảnh từ feature-img (slider chính) - chỉ lấy trong container chính
      const featureContainer = document.querySelector('.feature-img');
      if (featureContainer) {
        const featureImages = featureContainer.querySelectorAll('.owl-stage .owl-item img');
        featureImages.forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      }
      
      // Lấy hình ảnh từ gallery-img (slider phụ) - chỉ lấy trong container chính
      const galleryContainer = document.querySelector('.gallery-img');
      if (galleryContainer) {
        const galleryImages = galleryContainer.querySelectorAll('.owl-stage .owl-item img');
        galleryImages.forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      }
      
      // Lấy hình ảnh từ slider chính (fallback) - chỉ trong container chính
      const mainSlider = document.querySelector('#slider-feature, #slider-default');
      if (mainSlider) {
        const sliderImages = mainSlider.querySelectorAll('.owl-stage .owl-item img');
        sliderImages.forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      }
      
      return {
        title,
        price,
        priceOld,
        rating,
        sold,
        specifications,
        colorOptions,
        images
      };
    });
    
    // Xử lý dữ liệu nhiều dòng cho detail
    if (productDetail.specifications) {
      productDetail.specifications.forEach(spec => {
        if (spec.items) {
          spec.items.forEach(item => {
            if (typeof item.value === 'string') {
              item.value = processMultiLineValue(item.value);
            }
          });
        }
      });
    }
    
    // Kiểm tra nếu không có dữ liệu quan trọng thì không lưu cache
    const hasValidData = productDetail.title || 
                        productDetail.price || 
                        (productDetail.specifications && productDetail.specifications.length > 0);
    
    if (hasValidData) {
      // Lưu cache chỉ khi có dữ liệu hợp lệ
      saveCache(cacheKey, productDetail);
      console.log(`✅ Đã lưu cache cho laptop có dữ liệu: ${productUrl}`);
    } else {
      console.log(`⚠️ Bỏ qua cache cho laptop không có dữ liệu: ${productUrl}`);
    }
    
    return productDetail;
    
  } catch (error) {
    console.error(`❌ Lỗi crawl chi tiết laptop ${productUrl}:`, error);
    return null;
  }
}

// Hàm crawl chi tiết sản phẩm máy tính bảng
async function crawlTabletDetail(page, productUrl) {
  try {
    // Tạo cache key từ URL
    const cacheKey = productUrl.replace(/[^a-zA-Z0-9]/g, '_');
    
    // Kiểm tra cache trước
    const cachedData = loadCache(cacheKey);
    if (cachedData) {
      console.log(`📂 Sử dụng cache cho tablet: ${productUrl}`);
      return cachedData;
    }
    
    console.log(`🔍 Đang crawl chi tiết tablet: ${productUrl}`);
    
    // Truy cập trang sản phẩm
    await page.goto(productUrl, { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    // Chờ trang load hoàn toàn
    await page.waitForTimeout(2000);
    
    // Debug: Kiểm tra cấu trúc trang
    const pageStructure = await page.evaluate(() => {
      return {
        title: document.querySelector('h1')?.textContent?.trim() || 'Không tìm thấy title',
        hasSpecification: document.querySelectorAll('.specification-item').length,
        hasBoxSpecifi: document.querySelectorAll('.box-specifi').length,
        hasPrice: document.querySelectorAll('.box-price-present, .bs_price').length,
        allH1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent?.trim()),
        allH2: Array.from(document.querySelectorAll('h2')).map(h => h.textContent?.trim()),
        bodyClasses: document.body.className,
        mainContent: document.querySelector('.main') ? 'Có main' : 'Không có main'
      };
    });
    
    console.log('🔍 Debug trang máy tính bảng:', JSON.stringify(pageStructure, null, 2));
    
    // Crawl thông tin chi tiết sản phẩm máy tính bảng
    const productDetail = await page.evaluate(() => {
      // Thông tin cơ bản - thử nhiều selector khác nhau
      const title = document.querySelector('h1')?.textContent?.trim() || 
                   document.querySelector('.box-name h1')?.textContent?.trim() || '';
      
      const price = document.querySelector('.box-price-present')?.textContent?.trim() || 
                   document.querySelector('.bs_price strong')?.textContent?.trim() || 
                   document.querySelector('.box-price strong')?.textContent?.trim() || '';
      
      const priceOld = document.querySelector('.box-price-old')?.textContent?.trim() || 
                      document.querySelector('.bs_price em')?.textContent?.trim() || 
                      document.querySelector('.box-price-old em')?.textContent?.trim() || '';
      
      const rating = document.querySelector('.detail-rate p')?.textContent?.trim() || 
                    document.querySelector('.rating p')?.textContent?.trim() || '';
      
      const sold = document.querySelector('.quantity-sale')?.textContent?.trim() || 
                  document.querySelector('.sold')?.textContent?.trim() || '';
      
      // Thông số kỹ thuật - thử nhiều selector
      const specifications = [];
      
      // Thử selector cho điện thoại trước
      let specItems = document.querySelectorAll('.specification-item .box-specifi');
      
      // Nếu không có, thử selector khác
      if (specItems.length === 0) {
        specItems = document.querySelectorAll('.box-specifi');
      }
      
      // Nếu vẫn không có, thử selector laptop
      if (specItems.length === 0) {
        specItems = document.querySelectorAll('.specification-item');
      }
      
      specItems.forEach(spec => {
        const category = spec.querySelector('h3')?.textContent?.trim() || 
                        spec.querySelector('h4')?.textContent?.trim() || '';
        const items = [];
        
        let specList = spec.querySelectorAll('ul.text-specifi li');
        
        // Nếu không có, thử selector khác
        if (specList.length === 0) {
          specList = spec.querySelectorAll('ul li');
        }
        
        specList.forEach(item => {
          const label = item.querySelector('aside:first-child')?.textContent?.trim() || 
                       item.querySelector('strong')?.textContent?.trim() || 
                       item.querySelector('span:first-child')?.textContent?.trim() || '';
          const value = item.querySelector('aside:last-child')?.textContent?.trim() || 
                       item.querySelector('span:last-child')?.textContent?.trim() || 
                       item.textContent?.replace(label, '').trim() || '';
          
          if (label && value && label !== value) {
            items.push({ label, value });
          }
        });
        
        if (category && items.length > 0) {
          specifications.push({ category, items });
        }
      });
      
      // Các màu sắc - thử nhiều selector
      const colorOptions = [];
      let colorItems = document.querySelectorAll('.box03.color .box03__item.item');
      
      // Nếu không có, thử selector khác
      if (colorItems.length === 0) {
        colorItems = document.querySelectorAll('.box03__item.item');
      }
      
      // Nếu vẫn không có, thử selector khác
      if (colorItems.length === 0) {
        colorItems = document.querySelectorAll('.color-option');
      }
      
      colorItems.forEach(item => {
        const text = item.textContent?.trim();
        const isActive = item.classList.contains('act') || item.classList.contains('active');
        const colorCode = item.getAttribute('data-color');
        const productCode = item.getAttribute('data-code');
        const colorStyle = item.querySelector('i')?.getAttribute('style');
        
        if (text) {
          colorOptions.push({ 
            name: text, 
            isActive, 
            colorCode, 
            productCode,
            colorStyle 
          });
        }
      });
      
      // Hình ảnh sản phẩm từ slider/carousel - thử nhiều selector
      const images = [];
      
      // Thử các selector khác nhau cho hình ảnh
      const imageSelectors = [
        '.feature-img .owl-stage .owl-item img',
        '.gallery-img .owl-stage .owl-item img',
        '#slider-feature .owl-stage .owl-item img',
        '#slider-default .owl-stage .owl-item img',
        '.owl-carousel .owl-stage .owl-item img',
        '.slider .owl-stage .owl-item img',
        '.product-images img',
        '.box-img img'
      ];
      
      imageSelectors.forEach(selector => {
        const imgs = document.querySelectorAll(selector);
        imgs.forEach(img => {
          const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-original');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      });
      
      return {
        title,
        price,
        priceOld,
        rating,
        sold,
        specifications,
        colorOptions,
        images
      };
    });
    
    // Xử lý dữ liệu nhiều dòng cho detail
    if (productDetail.specifications) {
      productDetail.specifications.forEach(spec => {
        if (spec.items) {
          spec.items.forEach(item => {
            if (typeof item.value === 'string') {
              item.value = processMultiLineValue(item.value);
            }
          });
        }
      });
    }
    
    // Kiểm tra nếu không có dữ liệu quan trọng thì không lưu cache
    const hasValidData = productDetail.title || 
                        productDetail.price || 
                        (productDetail.specifications && productDetail.specifications.length > 0);
    
    if (hasValidData) {
      // Lưu cache chỉ khi có dữ liệu hợp lệ
      saveCache(cacheKey, productDetail);
      console.log(`✅ Đã lưu cache cho tablet có dữ liệu: ${productUrl}`);
    } else {
      console.log(`⚠️ Bỏ qua cache cho tablet không có dữ liệu: ${productUrl}`);
    }
    
    return productDetail;
    
  } catch (error) {
    console.error(`❌ Lỗi crawl chi tiết tablet ${productUrl}:`, error);
    return null;
  }
}

// Hàm crawl chi tiết sản phẩm đồng hồ thông minh
async function crawlSmartwatchDetail(page, productUrl) {
  try {
    const cacheKey = productUrl.replace(/[^a-zA-Z0-9]/g, '_');
    const cachedData = loadCache(cacheKey);
    if (cachedData) {
      console.log(`📂 Sử dụng cache cho smartwatch: ${productUrl}`);
      return cachedData;
    }

    console.log(`🔍 Đang crawl chi tiết smartwatch: ${productUrl}`);
    await page.goto(productUrl, { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    await page.waitForTimeout(2000);

    // Debug: Kiểm tra cấu trúc trang
    const pageStructure = await page.evaluate(() => {
      return {
        title: document.querySelector('h1')?.textContent?.trim() || 'Không tìm thấy title',
        hasSpecification: document.querySelectorAll('.specification-item').length,
        hasBoxSpecifi: document.querySelectorAll('.box-specifi').length,
        hasPrice: document.querySelectorAll('.box-price-present, .bs_price').length,
        allH1: Array.from(document.querySelectorAll('h1')).map(h => h.textContent?.trim()),
        allH2: Array.from(document.querySelectorAll('h2')).map(h => h.textContent?.trim()),
        bodyClasses: document.body.className,
        mainContent: document.querySelector('.main') ? 'Có main' : 'Không có main'
      };
    });
    console.log('🔍 Debug trang smartwatch:', JSON.stringify(pageStructure, null, 2));

    const productDetail = await page.evaluate(() => {
      // Thông tin cơ bản - thử nhiều selector khác nhau
      const title = document.querySelector('h1')?.textContent?.trim() || 
                   document.querySelector('.box-name h1')?.textContent?.trim() || '';
      const price = document.querySelector('.box-price-present')?.textContent?.trim() || 
                   document.querySelector('.bs_price strong')?.textContent?.trim() || 
                   document.querySelector('.box-price strong')?.textContent?.trim() || '';
      const priceOld = document.querySelector('.box-price-old')?.textContent?.trim() || 
                      document.querySelector('.bs_price em')?.textContent?.trim() || 
                      document.querySelector('.box-price-old em')?.textContent?.trim() || '';
      const rating = document.querySelector('.detail-rate p')?.textContent?.trim() || 
                    document.querySelector('.rating p')?.textContent?.trim() || '';
      const sold = document.querySelector('.quantity-sale')?.textContent?.trim() || 
                  document.querySelector('.sold')?.textContent?.trim() || '';
      
      // Thông số kỹ thuật - thử nhiều selector
      const specifications = [];
      let specItems = document.querySelectorAll('.specification-item .box-specifi');
      if (specItems.length === 0) {
        specItems = document.querySelectorAll('.box-specifi');
      }
      if (specItems.length === 0) {
        specItems = document.querySelectorAll('.specification-item');
      }
      
      specItems.forEach(spec => {
        const category = spec.querySelector('h3')?.textContent?.trim() || 
                        spec.querySelector('h4')?.textContent?.trim() || '';
        const items = [];
        let specList = spec.querySelectorAll('ul.text-specifi li');
        if (specList.length === 0) {
          specList = spec.querySelectorAll('ul li');
        }
        specList.forEach(item => {
          const label = item.querySelector('aside:first-child')?.textContent?.trim() || 
                       item.querySelector('strong')?.textContent?.trim() || 
                       item.querySelector('span:first-child')?.textContent?.trim() || '';
          const value = item.querySelector('aside:last-child')?.textContent?.trim() || 
                       item.querySelector('span:last-child')?.textContent?.trim() || 
                       item.textContent?.replace(label, '').trim() || '';
          if (label && value && label !== value) {
            items.push({ label, value });
          }
        });
        if (category && items.length > 0) {
          specifications.push({ category, items });
        }
      });
      
      // Các màu sắc - thử nhiều selector
      const colorOptions = [];
      let colorItems = document.querySelectorAll('.box03.color .box03__item.item');
      if (colorItems.length === 0) {
        colorItems = document.querySelectorAll('.box03__item.item');
      }
      if (colorItems.length === 0) {
        colorItems = document.querySelectorAll('.color-option');
      }
      colorItems.forEach(item => {
        const text = item.textContent?.trim();
        const isActive = item.classList.contains('act') || item.classList.contains('active');
        const colorCode = item.getAttribute('data-color');
        const productCode = item.getAttribute('data-code');
        const colorStyle = item.querySelector('i')?.getAttribute('style');
        if (text) {
          colorOptions.push({ 
            name: text, 
            isActive, 
            colorCode, 
            productCode,
            colorStyle 
          });
        }
      });
      
      // Hình ảnh sản phẩm từ slider/carousel - thử nhiều selector
      const images = [];
      const imageSelectors = [
        '.feature-img .owl-stage .owl-item img',
        '.gallery-img .owl-stage .owl-item img',
        '#slider-feature .owl-stage .owl-item img',
        '#slider-default .owl-stage .owl-item img',
        '.owl-carousel .owl-stage .owl-item img',
        '.slider .owl-stage .owl-item img',
        '.product-images img',
        '.box-img img'
      ];
      imageSelectors.forEach(selector => {
        const imgs = document.querySelectorAll(selector);
        imgs.forEach(img => {
          const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-original');
          if (src && !images.includes(src)) {
            images.push(src);
          }
        });
      });
      
      return {
        title, price, priceOld, rating, sold, specifications, colorOptions, images
      };
    });
    
    if (productDetail.specifications) {
      productDetail.specifications.forEach(spec => {
        if (spec.items) {
          spec.items.forEach(item => {
            if (typeof item.value === 'string') {
              item.value = processMultiLineValue(item.value);
            }
          });
        }
      });
    }
    
    const hasValidData = productDetail.title || productDetail.price || (productDetail.specifications && productDetail.specifications.length > 0);
    if (hasValidData) {
      saveCache(cacheKey, productDetail);
      console.log(`✅ Đã lưu cache cho smartwatch có dữ liệu: ${productUrl}`);
    } else {
      console.log(`⚠️ Bỏ qua cache cho smartwatch không có dữ liệu: ${productUrl}`);
    }
    return productDetail;
  } catch (error) {
    console.error(`❌ Lỗi crawl chi tiết smartwatch ${productUrl}:`, error);
    return null;
  }
}

module.exports = {
  crawlPhoneDetail,
  crawlLaptopDetail,
  crawlTabletDetail,
  crawlSmartwatchDetail
};

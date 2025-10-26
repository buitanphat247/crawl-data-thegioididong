const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Cache file
const CACHE_FILE = './cache.json';

// Hàm xử lý dữ liệu nhiều dòng thành array
function processMultiLineValue(value) {
  if (!value || typeof value !== 'string') return value;
  
  // Tách theo xuống dòng và lọc các dòng trống
  const lines = value.split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0);
  
  // Nếu chỉ có 1 dòng, trả về string
  if (lines.length <= 1) return value.trim();
  
  // Nếu có nhiều dòng, trả về array
  return lines;
}

// Hàm lưu cache
function saveCache(key, data) {
  try {
    let cacheData = {};
    
    // Đọc cache hiện tại nếu có
    if (fs.existsSync(CACHE_FILE)) {
      try {
        const fileContent = fs.readFileSync(CACHE_FILE, 'utf8').trim();
        
        // Kiểm tra nếu file rỗng hoặc không phải JSON hợp lệ
        if (!fileContent || fileContent === '') {
          console.log('📂 Cache file rỗng, tạo cache mới');
          cacheData = {};
        } else {
          cacheData = JSON.parse(fileContent);
        }
      } catch (parseError) {
        console.error('❌ Lỗi parse cache file:', parseError.message);
        console.log('🗑️ Tạo cache mới do file bị hỏng');
        cacheData = {};
        
        // Xóa file cache bị hỏng
        try {
          fs.unlinkSync(CACHE_FILE);
          console.log('🗑️ Đã xóa cache file bị hỏng');
        } catch (deleteError) {
          console.error('❌ Không thể xóa cache file:', deleteError.message);
        }
      }
    }
    
    // Cập nhật cache
    cacheData[key] = {
      data: data,
      timestamp: new Date().toISOString()
    };
    
    // Lưu cache
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cacheData, null, 2));
    console.log(`💾 Đã lưu cache: ${key}`);
  } catch (error) {
    console.error('❌ Lỗi lưu cache:', error);
  }
}

// Hàm đọc cache
function loadCache(key) {
  try {
    if (fs.existsSync(CACHE_FILE)) {
      const fileContent = fs.readFileSync(CACHE_FILE, 'utf8').trim();
      
      // Kiểm tra nếu file rỗng hoặc không phải JSON hợp lệ
      if (!fileContent || fileContent === '') {
        console.log('📂 Cache file rỗng, bỏ qua');
        return null;
      }
      
      const cacheData = JSON.parse(fileContent);
      if (cacheData[key]) {
        console.log(`📂 Đã load cache: ${key}`);
        return cacheData[key].data;
      }
    }
  } catch (error) {
    console.error('❌ Lỗi đọc cache:', error.message);
    // Xóa file cache bị hỏng
    try {
      fs.unlinkSync(CACHE_FILE);
      console.log('🗑️ Đã xóa cache file bị hỏng');
    } catch (deleteError) {
      console.error('❌ Không thể xóa cache file:', deleteError.message);
    }
  }
  return null;
}

// Hàm retry với exponential backoff
async function retryWithBackoff(fn, maxAttempts = 3, baseDelay = 2000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) {
        throw error;
      }
      
      const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000;
      console.log(`⚠️ Retry ${attempt}/${maxAttempts} sau ${delay}ms: ${error.message}`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

module.exports = {
  processMultiLineValue,
  saveCache,
  loadCache,
  retryWithBackoff
};

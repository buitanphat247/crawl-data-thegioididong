const express = require('express');
const cors = require('cors');
const crawlService = require('./src/services/crawlService');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Crawl Data Phone API',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      phones: '/crawl-phones',
      laptops: '/crawl-laptops',
      tablets: '/crawl-tablets',
      smartwatches: '/crawl-smartwatches',
      health: '/health'
    }
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    message: 'Server hoạt động bình thường'
  });
});

// Crawl dữ liệu sản phẩm điện thoại từ thegioididong.com
app.get('/crawl-phones', async (req, res) => {
  try {
    const result = await crawlService.crawlPhones();
    
    if (result.success) {
      res.json(result);
    } else {
      res.status(500).json(result);
    }
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu điện thoại:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi crawl dữ liệu điện thoại',
      error: error.message
    });
  }
});

// Crawl dữ liệu laptop từ thegioididong.com
app.get('/crawl-laptops', async (req, res) => {
  try {
    const result = await crawlService.crawlLaptops();
    
    if (result.success) {
      res.json(result);
        } else {
      res.status(500).json(result);
    }
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu laptop:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi crawl dữ liệu laptop',
      error: error.message
    });
  }
});


// Crawl dữ liệu máy tính bảng từ thegioididong.com
app.get('/crawl-tablets', async (req, res) => {
  try {
    const result = await crawlService.crawlTablets();
    
    if (result.success) {
      res.json(result);
    } else {
      res.status(500).json(result);
    }
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu máy tính bảng:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi crawl dữ liệu máy tính bảng',
      error: error.message
    });
  }
});

// Crawl dữ liệu đồng hồ thông minh từ thegioididong.com
app.get('/crawl-smartwatches', async (req, res) => {
  try {
    const result = await crawlService.crawlSmartwatches();
    
    if (result.success) {
      res.json(result);
    } else {
      res.status(500).json(result);
    }
  } catch (error) {
    console.error('❌ Lỗi crawl dữ liệu đồng hồ thông minh:', error);
    res.status(500).json({
      success: false,
      message: 'Lỗi khi crawl dữ liệu đồng hồ thông minh',
      error: error.message
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server đang chạy tại http://localhost:${PORT}`);
  console.log(`📱 Crawl Data Phone API sẵn sàng!`);
  console.log(`📋 Endpoints:`);
  console.log(`   - GET /crawl-phones - Crawl điện thoại`);
  console.log(`   - GET /crawl-laptops - Crawl laptop`);
  console.log(`   - GET /crawl-tablets - Crawl máy tính bảng`);
  console.log(`   - GET /crawl-smartwatches - Crawl đồng hồ thông minh`);
  console.log(`   - GET /health - Health check`);
});

module.exports = app;
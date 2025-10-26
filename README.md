# Crawl Data Phone - Node.js Express với Puppeteer

Dự án crawl website sử dụng Node.js, Express và Puppeteer với nodemon để tự động reload.

## 🚀 Tính năng

- ✅ Crawl một trang đơn lẻ
- ✅ Crawl nhiều trang cùng lúc
- ✅ Tự động reload với nodemon
- ✅ API RESTful đầy đủ
- ✅ Cấu hình linh hoạt
- ✅ Xử lý lỗi tốt

## 📦 Cài đặt

### 1. Clone dự án
```bash
git clone <repository-url>
cd crawl-data-phone
```

### 2. Cài đặt dependencies
```bash
npm install
```

### 3. Chạy dự án

#### Chế độ development (với nodemon)
```bash
npm run dev
```

#### Chế độ production
```bash
npm start
```

## 🔧 Cấu hình

Chỉnh sửa file `config.js` để thay đổi cấu hình:

```javascript
module.exports = {
  PORT: 3000,
  PUPPETEER: {
    HEADLESS: true,
    TIMEOUT: 30000
  },
  CRAWLING: {
    MAX_CONCURRENT_PAGES: 5,
    REQUEST_DELAY: 1000
  }
};
```

## 📡 API Endpoints

### 1. Trang chủ
```
GET /
```

### 2. Health Check
```
GET /health
```

### 3. Crawl một trang
```
POST /api/crawl/single
Content-Type: application/json

{
  "url": "https://example.com"
}
```

### 4. Crawl nhiều trang
```
POST /api/crawl/multiple
Content-Type: application/json

{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ]
}
```

### 5. Trạng thái crawling
```
GET /api/crawl/status
```

## 📁 Cấu trúc dự án

```
crawl-data-phone/
├── src/
│   ├── controllers/
│   │   └── crawlController.js
│   ├── routes/
│   │   └── crawlRoutes.js
│   ├── services/
│   │   └── puppeteerService.js
│   └── utils/
├── server.js
├── config.js
├── package.json
├── nodemon.json
└── README.md
```

## 🛠️ Scripts

- `npm start` - Chạy server production
- `npm run dev` - Chạy server development với nodemon
- `npm test` - Chạy tests (chưa có)

## 🔍 Ví dụ sử dụng

### Crawl một trang
```bash
curl -X POST http://localhost:3000/api/crawl/single \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Crawl nhiều trang
```bash
curl -X POST http://localhost:3000/api/crawl/multiple \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example1.com", "https://example2.com"]}'
```

## 📝 Ghi chú

- Server sẽ chạy tại `http://localhost:3000`
- Nodemon sẽ tự động reload khi có thay đổi code
- Puppeteer sẽ chạy ở chế độ headless mặc định
- Có thể thay đổi cấu hình trong file `config.js`

## 🐛 Troubleshooting

### Lỗi Puppeteer
- Đảm bảo đã cài đặt đầy đủ dependencies
- Kiểm tra kết nối internet
- Thử chạy với `PUPPETEER_HEADLESS=false` để debug

### Lỗi Port đã được sử dụng
- Thay đổi PORT trong `config.js`
- Hoặc kill process đang sử dụng port 3000

## 📄 License

MIT License

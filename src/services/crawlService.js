// Import các service con
const { crawlPhones } = require('./phoneService');
const { crawlLaptops } = require('./laptopService');
const { crawlTablets } = require('./tabletService');
const { crawlSmartwatches } = require('./smartwatchService');
const { crawlPhoneDetail } = require('./productDetailService');

module.exports = {
  crawlPhones,
  crawlLaptops,
  crawlTablets,
  crawlSmartwatches,
  crawlProductDetail: crawlPhoneDetail // Giữ tên cũ để tương thích
};

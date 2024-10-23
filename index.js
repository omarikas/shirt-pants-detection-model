const puppeteer = require('puppeteer');
const fs = require('fs');
const axios = require('axios');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless:false});
  const page = await browser.newPage();

  // Navigate to Google Images
  await page.goto('https://www.google.com/search?q=pants&sca_esv=31fc9eb8bb598b81&sxsrf=ADLYWIL3sgngwcKDik_Mfd_rzcZkg6G3Vw:1729585870556&source=hp&biw=1279&bih=454&ei=zmIXZ8LeH4G6hbIPo_CTiAs&iflsig=AL9hbdgAAAAAZxdw3hyH2WqEednhU_4rN6KU9U-pamdO&ved=0ahUKEwjC_a67yaGJAxUBXUEAHSP4BLEQ4dUDCBA&uact=5&oq=shirt&gs_lp=EgNpbWciBXNoaXJ0Mg0QABiABBixAxhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFSNsCUABYAHAAeACQAQCYAaMBoAGjAaoBAzAuMbgBA8gBAIoCC2d3cy13aXotaW1nmAIBoAKsAZgDAIgGAZIHAzAuMaAH8AQ&sclient=img&udm=2');

  // Scroll to load more images
  let previousHeight;
  try {
    previousHeight = await page.evaluate('document.body.scrollHeight');
    var i=0;
    while (i<10) {
        i++;
      previousHeight = await page.evaluate('document.body.scrollHeight');
      await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
      await page.waitForNetworkIdle() // Wait for images to load
    }
  } catch (err) {
    console.log(err);
  }

  // Extract image URLs
  const imageUrls = await page.evaluate(() => {
    const images = Array.from(document.querySelectorAll('img'));
    return images.map(img => img.src).filter(src => src.includes('http'));
  });

  // Limit the result to 500 images
  const limitedImageUrls = imageUrls.slice(0, 500);

  // Ensure the download directory exists
  const downloadDir = './downloaded_images2';
  if (!fs.existsSync(downloadDir)) {
    fs.mkdirSync(downloadDir);
  }

  const downloadImage = async (url, filepath) => {
    try {
      // Make a HEAD request to get the Content-Length
      const headResponse = await axios.head(url);
      const contentLength = parseInt(headResponse.headers['content-length'], 10);
  
      // Check if the content length is less than 1KB (1024 bytes)
      if (contentLength < 1024) {
        console.log(`Skipping image (too small): ${url} - Size: ${contentLength} bytes`);
        return; // Skip downloading this image
      }
  
      // Proceed with the download if the image size is sufficient
      const response = await axios({
        url,
        responseType: 'stream',
      });
      
      response.data.pipe(fs.createWriteStream(filepath));
  
      return new Promise((resolve, reject) => {
        response.data.on('end', () => {
          resolve();
        });
  
        response.data.on('error', err => {
          reject(err);
        });
      });
    } catch (err) {
      console.error(`Error downloading image: ${url}`, err);
    }
  };
  

  // Download the images and save them to the directory
  for (let i = 0; i < limitedImageUrls.length; i++) {
    const imageUrl = limitedImageUrls[i];
    const imagePath = path.resolve(downloadDir, `image_${i + 1}.jpg`);
    console.log(`Downloading image ${i + 1}...`);
    await downloadImage(imageUrl, imagePath);
  }

  console.log('Images downloaded successfully!');

  await browser.close();
})();

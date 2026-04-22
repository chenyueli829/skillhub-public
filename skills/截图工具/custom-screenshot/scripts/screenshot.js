#!/usr/bin/env node
/**
 * OpenClaw Screenshot Tool
 * 
 * 使用 puppeteer + Chrome for Testing，无黑屏、无外部依赖
 * 
 * 用法:
 *   node screenshot.js <url> <output_path> [width] [height] [wait_ms] [full_page] [scale]
 * 
 * 示例:
 *   node screenshot.js http://localhost:3000 /tmp/demo.png
 *   node screenshot.js http://localhost:8888 /tmp/launchpad.png 1440 900 2000
 *   node screenshot.js http://localhost:5173 /tmp/app.png 1280 800 3000 true
 *   node screenshot.js http://localhost:3000 /tmp/highres.png 1440 900 2000 false 3
 */

// 查找 puppeteer 模块的函数
function findPuppeteer() {
  // 首先尝试从环境变量获取
  if (process.env.PUPPETEER_PATH) {
    try {
      const puppeteer = require(process.env.PUPPETEER_PATH);
      console.error(`Found puppeteer from environment variable: ${process.env.PUPPETEER_PATH}`);
      return puppeteer;
    } catch (e) {
      console.error(`Failed to load puppeteer from environment variable: ${e.message}`);
    }
  }
  
  const paths = [
    // 尝试从当前目录查找
    './node_modules/puppeteer',
    // 尝试从上级目录查找
    '../node_modules/puppeteer',
    '../../node_modules/puppeteer',
    // 尝试从全局安装查找
    'puppeteer'
  ];
  
  for (const path of paths) {
    try {
      const puppeteer = require(path);
      console.error(`Found puppeteer at: ${path}`);
      return puppeteer;
    } catch (e) {
      // 继续尝试下一个路径
    }
  }
  
  throw new Error('Could not find puppeteer. Please install it with: npm install puppeteer');
}

const puppeteer = findPuppeteer();

const [,, url, outputPath, widthStr, heightStr, waitStr, fullPageStr, scaleStr] = process.argv;
const fs = require('fs');
const path = require('path');

if (!url || !outputPath) {
  console.error('Usage: node screenshot.js <url> <output_path> [width=1280] [height=800] [wait_ms=2000] [full_page=false]');
  process.exit(1);
}

// 验证 URL 格式
try {
  new URL(url);
} catch (e) {
  console.error(JSON.stringify({ ok: false, error: 'Invalid URL format', url }));
  process.exit(1);
}

const width    = parseInt(widthStr)  || 1280;
const height   = parseInt(heightStr) || 800;
const waitMs   = parseInt(waitStr)   || 2000;
const fullPage = fullPageStr === 'true';
const scale    = parseInt(scaleStr)   || parseInt(process.env.PUPPETEER_SCALE) || 2;

// 验证 scale 参数范围
if (scale < 1 || scale > 4) {
  console.error(JSON.stringify({ ok: false, error: 'Scale must be between 1 and 4', scale }));
  process.exit(1);
}

// 确保输出目录存在
const outputDir = path.dirname(outputPath);
try {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.error(`Created output directory: ${outputDir}`);
  }
} catch (e) {
  console.error(JSON.stringify({ ok: false, error: `Failed to create output directory: ${e.message}`, path: outputPath }));
  process.exit(1);
}

(async () => {
  let browser;
  try {
    console.error(`Launching browser...`);
    browser = await puppeteer.default.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-web-security',
        '--allow-running-insecure-content'
      ]
    });

    console.error(`Creating new page...`);
    const page = await browser.newPage();
    await page.setViewport({ width, height, deviceScaleFactor: scale });

    // 导航到目标 URL
    console.error(`Navigating to ${url}...`);
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // 等待额外时间确保动画/渲染完成
    if (waitMs > 0) {
      console.error(`Waiting for ${waitMs}ms to ensure rendering completion...`);
      await new Promise(r => setTimeout(r, waitMs));
    }

    // 截图
    console.error(`Taking screenshot to ${outputPath}...`);
    await page.screenshot({
      path: outputPath,
      fullPage,
      type: 'png'
    });

    const stat = fs.statSync(outputPath);
    console.error(`Screenshot saved successfully: ${outputPath} (${stat.size} bytes)`);
    console.log(JSON.stringify({
      ok: true,
      path: outputPath,
      size: stat.size,
      width,
      height,
      scale,
      url
    }));

  } catch (e) {
    console.error(`Error: ${e.message}`);
    console.error(JSON.stringify({ ok: false, error: e.message, url, path: outputPath }));
    process.exit(1);
  } finally {
    if (browser) {
      console.error(`Closing browser...`);
      await browser.close();
    }
  }
})();

#!/usr/bin/env node
/**
 * OpenClaw Multi-Screenshot Tool
 * 
 * 对同一个 URL 截取多张截图（不同交互状态）
 * 
 * 用法: node multi-screenshot.js <config_json>
 * config_json 格式:
 * {
 *   "url": "http://localhost:3000",
 *   "outputDir": "/tmp",
 *   "prefix": "demo",
 *   "viewport": { "width": 1280, "height": 800 },
 *   "scale": 2,
 *   "shots": [
 *     { "name": "main",   "waitMs": 2000 },
 *     { "name": "dark",   "waitMs": 500, "js": "document.documentElement.classList.add('dark')" },
 *     { "name": "scroll", "waitMs": 500, "js": "window.scrollTo(0, document.body.scrollHeight/2)" }
 *   ]
 * }
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
const fs = require('fs');
const path = require('path');

const configArg = process.argv[2];
if (!configArg) {
  console.error('Usage: node multi-screenshot.js <config_json_string_or_file>');
  process.exit(1);
}

let config;
try {
  // 支持 JSON 字符串或文件路径
  config = configArg.startsWith('{') ? JSON.parse(configArg) : JSON.parse(fs.readFileSync(configArg, 'utf8'));
} catch(e) {
  console.error('Invalid config:', e.message);
  process.exit(1);
}

const {
  url,
  outputDir = '/tmp',
  prefix = 'screenshot',
  viewport = { width: 1280, height: 800 },
  scale = parseInt(process.env.PUPPETEER_SCALE) || 2,
  shots = [{ name: 'main', waitMs: 2000 }],
  initialWaitMs = 2000
} = config;

// 验证 URL 格式
try {
  new URL(url);
} catch (e) {
  console.error(JSON.stringify({ ok: false, error: 'Invalid URL format', url }));
  process.exit(1);
}

// 确保输出目录存在
try {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.error(`Created output directory: ${outputDir}`);
  }
} catch (e) {
  console.error(JSON.stringify({ ok: false, error: `Failed to create output directory: ${e.message}`, outputDir }));
  process.exit(1);
}

// 验证 shots 配置
if (!Array.isArray(shots) || shots.length === 0) {
  console.error(JSON.stringify({ ok: false, error: 'Invalid shots configuration: must be a non-empty array' }));
  process.exit(1);
}

// 验证 scale 参数范围
if (scale < 1 || scale > 4) {
  console.error(JSON.stringify({ ok: false, error: 'Scale must be between 1 and 4', scale }));
  process.exit(1);
}

(async () => {
  let browser;
  const results = [];
  
  try {
    console.error(`Launching browser...`);
    browser = await puppeteer.default.launch({
      headless: true,
      args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage']
    });

    console.error(`Creating new page...`);
    const page = await browser.newPage();
    await page.setViewport({ ...viewport, deviceScaleFactor: scale });

    console.error(`Navigating to ${url}...`);
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
    
    if (initialWaitMs > 0) {
      console.error(`Waiting for ${initialWaitMs}ms for initial page load...`);
      await new Promise(r => setTimeout(r, initialWaitMs));
    }

    console.error(`Starting to take ${shots.length} screenshots...`);
    for (const shot of shots) {
      try {
        console.error(`Processing screenshot: ${shot.name}`);
        
        // 执行 JS（如切换暗色模式、点击按钮等）
        if (shot.js) {
          console.error(`  Executing JS: ${shot.js}`);
          await page.evaluate(shot.js);
        }

        // 点击元素
        if (shot.click) {
          console.error(`  Clicking element: ${shot.click}`);
          await page.click(shot.click).catch(() => {
            console.error(`  Warning: Failed to click element ${shot.click}`);
          });
        }

        // 等待
        if (shot.waitMs > 0) {
          console.error(`  Waiting for ${shot.waitMs}ms...`);
          await new Promise(r => setTimeout(r, shot.waitMs || 500));
        }

        const outPath = path.join(outputDir, `${prefix}-${shot.name}.png`);
        console.error(`  Taking screenshot to: ${outPath}`);
        await page.screenshot({
          path: outPath,
          fullPage: shot.fullPage || false,
          type: 'png'
        });

        const stat = fs.statSync(outPath);
        console.error(`  Screenshot saved: ${outPath} (${stat.size} bytes)`);
        results.push({ name: shot.name, path: outPath, size: stat.size, ok: true });
      } catch(e) {
        console.error(`  Error taking screenshot ${shot.name}: ${e.message}`);
        results.push({ name: shot.name, ok: false, error: e.message });
      }
    }

    console.error(`All screenshots completed. Results: ${results.filter(r => r.ok).length} success, ${results.filter(r => !r.ok).length} failed`);
    console.log(JSON.stringify({ ok: true, results }));
  } catch(e) {
    console.error(`Error: ${e.message}`);
    console.error(JSON.stringify({ ok: false, error: e.message, results }));
    process.exit(1);
  } finally {
    if (browser) {
      console.error(`Closing browser...`);
      await browser.close();
    }
  }
})();

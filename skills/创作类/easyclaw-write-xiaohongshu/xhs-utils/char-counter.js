#!/usr/bin/env node
/**
 * 小红书字数检查器
 * 标题 ≤ 20 字符，正文 ≤ 1000 字符
 */

import fs from 'fs';

const TITLE_LIMIT = 20;
const BODY_LIMIT = 1000;
const TITLE_SAFE = 18;
const BODY_SAFE = 950;

function countChars(text) {
  return text ? text.length : 0;
}

function checkTitle(title) {
  const count = countChars(title);
  const status = count <= TITLE_LIMIT ? '✅' : '❌';
  const warning = count > TITLE_SAFE && count <= TITLE_LIMIT ? '⚠️ 接近上限' : '';
  
  return {
    status,
    count,
    limit: TITLE_LIMIT,
    warning,
    passed: count <= TITLE_LIMIT
  };
}

function checkBody(body) {
  const count = countChars(body);
  const status = count <= BODY_LIMIT ? '✅' : '❌';
  const warning = count > BODY_SAFE && count <= BODY_LIMIT ? '⚠️ 接近上限' : '';
  
  return {
    status,
    count,
    limit: BODY_LIMIT,
    warning,
    passed: count <= BODY_LIMIT
  };
}

function suggestTrim(text, targetLimit, type) {
  if (text.length <= targetLimit) return text;
  
  const suggestions = [];
  
  // 删除冗余词
  const redundantWords = ['总的来说', '综上所述', '因此', '首先', '其次', '最后', '不容错过', '速速', '非常', '真的', '超级'];
  let trimmed = text;
  redundantWords.forEach(word => {
    trimmed = trimmed.replace(new RegExp(word, 'g'), '');
  });
  
  if (trimmed.length < text.length) {
    suggestions.push(`删除冗余词可节省 ${text.length - trimmed.length} 字符`);
  }
  
  // 合并句子
  const merged = trimmed.replace(/\n\n+/g, '\n');
  if (merged.length < trimmed.length) {
    suggestions.push(`合并空行可节省 ${trimmed.length - merged.length} 字符`);
  }
  
  // 缩短句子
  const shortened = merged.replace(/进行一个/g, '做')
                          .replace(/可以说是/g, '是')
                          .replace(/真的是/g, '是')
                          .replace(/的话/g, '');
  
  return {
    original: text,
    trimmed: shortened,
    saved: text.length - shortened.length,
    suggestions
  };
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
📏 小红书字数检查器

用法:
  node char-counter.js <标题> <正文文件>
  node char-counter.js --title "标题文本"
  node char-counter.js --body-file path/to/body.txt
  node char-counter.js --demo

选项:
  --title, -t    检查标题
  --body, -b     检查正文
  --body-file    从文件读取正文
  --demo         运行示例
  --help, -h     显示帮助
`);
    process.exit(0);
  }
  
  if (args.includes('--demo')) {
    console.log('📝 示例检查:\n');
    
    const demoTitle = '打工人带饭｜5 天不重样 30 元/天';
    const demoBody = `周一：鸡腿饭🍗
鸡腿 8 元 + 西兰花 3 元 + 米饭 2 元
空气炸锅 20 分钟，懒人必备

周二：番茄鸡蛋面🍅
鸡蛋 2 元 + 番茄 3 元 + 挂面 2 元
10 分钟搞定，汤汁拌饭绝了`;
    
    const titleResult = checkTitle(demoTitle);
    const bodyResult = checkBody(demoBody);
    
    console.log(`标题："${demoTitle}"`);
    console.log(`  ${titleResult.status} ${titleResult.count}/${titleResult.limit} 字符 ${titleResult.warning}`);
    console.log();
    console.log(`正文：${bodyResult.count}/${bodyResult.limit} 字符 ${bodyResult.warning}`);
    console.log(`  ${bodyResult.status} 符合发布要求`);
    
    return;
  }
  
  if (args.includes('--title') || args.includes('-t')) {
    const titleIndex = args.indexOf('--title') > -1 ? args.indexOf('--title') : args.indexOf('-t');
    const title = args[titleIndex + 1];
    const result = checkTitle(title);
    
    console.log(`\n📝 标题检查结果:`);
    console.log(`  "${title}"`);
    console.log(`  ${result.status} ${result.count}/${result.limit} 字符 ${result.warning}`);
    console.log(`  ${result.passed ? '✅ 可以发布' : '❌ 需要修改'}\n`);
    
    process.exit(result.passed ? 0 : 1);
  }
  
  if (args.includes('--body-file')) {
    const fileIndex = args.indexOf('--body-file');
    const filePath = args[fileIndex + 1];
    
    try {
      const body = fs.readFileSync(filePath, 'utf-8');
      const result = checkBody(body);
      
      console.log(`\n📝 正文检查结果 (${filePath}):`);
      console.log(`  ${result.status} ${result.count}/${result.limit} 字符 ${result.warning}`);
      console.log(`  ${result.passed ? '✅ 可以发布' : '❌ 需要修改'}\n`);
      
      process.exit(result.passed ? 0 : 1);
    } catch (e) {
      console.error(`❌ 读取文件失败：${e.message}`);
      process.exit(1);
    }
  }
  
  // 默认用法：直接传入标题和正文
  if (args.length >= 2) {
    const title = args[0];
    const body = args.slice(1).join(' ');
    
    const titleResult = checkTitle(title);
    const bodyResult = checkBody(body);
    
    console.log('\n📏 小红书字数检查报告\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`标题：${titleResult.status} ${titleResult.count}/${titleResult.limit} 字符 ${titleResult.warning}`);
    console.log(`正文：${bodyResult.status} ${bodyResult.count}/${bodyResult.limit} 字符 ${bodyResult.warning}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`总状态：${titleResult.passed && bodyResult.passed ? '✅ 可以发布' : '❌ 需要修改'}\n`);
    
    process.exit(titleResult.passed && bodyResult.passed ? 0 : 1);
  }
}

main();

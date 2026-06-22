#!/usr/bin/env node
/**
 * 小红书爆款规律分析器
 * 分析标题、正文、封面的爆款规律
 */

import fs from 'fs';

// 常见爆款关键词分类
const KEYWORD_PATTERNS = {
  identity: ['打工人', '学生党', '宝妈', '上班族', '北漂', '沪漂', '新手', '小白', '懒人'],
  benefit: ['省钱', '不重样', '快速', '快手', '简单', '搞定', '必备', '绝了', '真香'],
  number: ['\\d+ 天', '\\d+ 元', '\\d+ 分钟', '\\d+ 道', '一周', '一个月', 'Top\\d+'],
  emotion: ['终于', '后悔', '惊喜', '意外', '救命', '宝藏', '私藏', '亲测'],
  action: ['收藏', '码住', '抄作业', '照做', '跟着买', '闭眼入']
};

// 标题句式模板
const TITLE_PATTERNS = [
  { name: '身份 + 利益', regex: /(.+?)(省钱 | 不重样 | 快速 | 简单)/, example: '打工人带饭｜5 天不重样' },
  { name: '数字 + 结果', regex: /(\d+.*?)(搞定 | 完成 | 学会)/, example: '10 分钟搞定一周便当' },
  { name: '对比反差', regex: /(以前 | 之前).*?(现在 | 后来)/, example: '以前点外卖，现在带饭' },
  { name: '清单合集', regex: /(合集 | 清单 | 大全 | 汇总)/, example: '一周便当合集' },
  { name: '避坑指南', regex: /(避坑 | 踩雷 | 不要 | 别)/, example: '新手化妆避坑' }
];

function analyzeTitle(titles) {
  if (!Array.isArray(titles) || titles.length === 0) {
    return { error: '需要提供标题数组' };
  }
  
  const results = {
    lengthStats: {
      avg: 0,
      min: Infinity,
      max: 0,
      distribution: {}
    },
    patterns: {},
    keywords: {
      identity: [],
      benefit: [],
      number: [],
      emotion: [],
      action: []
    },
    symbols: {
      emoji: 0,
      pipe: 0,
      bracket: 0
    }
  };
  
  titles.forEach(title => {
    // 长度统计
    const len = title.length;
    results.lengthStats.avg += len;
    results.lengthStats.min = Math.min(results.lengthStats.min, len);
    results.lengthStats.max = Math.max(results.lengthStats.max, len);
    results.lengthStats.distribution[len] = (results.lengthStats.distribution[len] || 0) + 1;
    
    // 句式匹配
    TITLE_PATTERNS.forEach(pattern => {
      if (pattern.regex.test(title)) {
        results.patterns[pattern.name] = (results.patterns[pattern.name] || 0) + 1;
      }
    });
    
    // 关键词统计
    Object.entries(KEYWORD_PATTERNS).forEach(([type, patterns]) => {
      patterns.forEach(pattern => {
        const regex = new RegExp(pattern);
        if (regex.test(title)) {
          const cleanPattern = pattern.replace(/\\/g, '').replace(/\[\^0-9\]/g, '\\d+');
          results.keywords[type].push(cleanPattern);
        }
      });
    });
    
    // 符号统计
    if (/[🍳🍱🥗🍜🥘🍲]/.test(title)) results.symbols.emoji++;
    if (title.includes('|') || title.includes('｜')) results.symbols.pipe++;
    if (title.includes('[') || title.includes('(')) results.symbols.bracket++;
  });
  
  results.lengthStats.avg = Math.round(results.lengthStats.avg / titles.length);
  
  return results;
}

function analyzeBody(bodies) {
  if (!Array.isArray(bodies) || bodies.length === 0) {
    return { error: '需要提供正文数组' };
  }
  
  const results = {
    structure: {
      avgParagraphs: 0,
      avgSentences: 0,
      hasList: 0,
      hasSteps: 0,
      hasCTA: 0
    },
    tone: {
      firstPerson: 0,
      casual: 0,
      emotional: 0
    },
    content: {
      avgLength: 0,
      hasPrice: 0,
      hasTime: 0,
      hasSpecific: 0
    }
  };
  
  bodies.forEach(body => {
    const paragraphs = body.split(/\n\n+/);
    results.structure.avgParagraphs += paragraphs.length;
    
    const sentences = body.split(/[.!?。！？]/);
    results.structure.avgSentences += sentences.length;
    
    // 结构检测
    if (/^\s*[-•*]\s+/m.test(body) || /^\s*\d+\.\s+/m.test(body)) {
      results.structure.hasList++;
    }
    if (/第一步 | 首先 | 然后 | 最后|Step\d+/.test(body)) {
      results.structure.hasSteps++;
    }
    if (/评论 | 告诉我 | 你们 | 大家 | 互动/.test(body)) {
      results.structure.hasCTA++;
    }
    
    // 语气检测
    if (/我 | 我的 | 我觉得 | 我发现/.test(body)) {
      results.tone.firstPerson++;
    }
    if (/绝了 | 真的 | 超级 | 太 | 好用到哭/.test(body)) {
      results.tone.emotional++;
    }
    
    // 内容检测
    results.content.avgLength += body.length;
    if (/\d+ 元|\d+ 块|￥|\$/.test(body)) results.content.hasPrice++;
    if (/\d+ 分钟|\d+ 小时|\d+ 天/.test(body)) results.content.hasTime++;
  });
  
  const count = bodies.length;
  results.structure.avgParagraphs = Math.round(results.structure.avgParagraphs / count);
  results.structure.avgSentences = Math.round(results.structure.avgSentences / count);
  results.content.avgLength = Math.round(results.content.avgLength / count);
  
  return results;
}

function generateReport(titleAnalysis, bodyAnalysis) {
  console.log('\n📊 小红书爆款规律分析报告\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  if (titleAnalysis.error) {
    console.log(`❌ 标题分析：${titleAnalysis.error}`);
  } else {
    console.log('📝 标题规律分析');
    console.log(`  平均长度：${titleAnalysis.lengthStats.avg} 字符 (范围：${titleAnalysis.lengthStats.min}-${titleAnalysis.lengthStats.max})`);
    console.log();
    
    console.log('  热门句式:');
    Object.entries(titleAnalysis.patterns)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .forEach(([name, count]) => {
        console.log(`    • ${name}: ${count}次`);
      });
    console.log();
    
    console.log('  高频关键词:');
    const allKeywords = [
      ...titleAnalysis.keywords.identity,
      ...titleAnalysis.keywords.benefit,
      ...titleAnalysis.keywords.emotion
    ].filter(Boolean);
    const keywordFreq = {};
    allKeywords.forEach(k => keywordFreq[k] = (keywordFreq[k] || 0) + 1);
    Object.entries(keywordFreq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .forEach(([word, count]) => {
        console.log(`    • ${word}: ${count}次`);
      });
    console.log();
    
    console.log('  符号使用:');
    console.log(`    • Emoji 标题：${titleAnalysis.symbols.emoji}个`);
    console.log(`    • 分隔符｜：${titleAnalysis.symbols.pipe}个`);
    console.log();
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  if (bodyAnalysis.error) {
    console.log(`❌ 正文分析：${bodyAnalysis.error}`);
  } else {
    console.log('📄 正文规律分析');
    console.log(`  平均长度：${bodyAnalysis.content.avgLength} 字符`);
    console.log(`  平均段落：${bodyAnalysis.structure.avgParagraphs}段`);
    console.log();
    
    console.log('  结构特征:');
    console.log(`    • 含清单格式：${bodyAnalysis.structure.hasList}/${bodyAnalysis.content.avgLength > 0 ? bodyAnalysis.content.avgLength : 1}篇`);
    console.log(`    • 含步骤说明：${bodyAnalysis.structure.hasSteps}篇`);
    console.log(`    • 含互动引导：${bodyAnalysis.structure.hasCTA}篇`);
    console.log();
    
    console.log('  语气风格:');
    console.log(`    • 第一人称：${bodyAnalysis.tone.firstPerson}篇`);
    console.log(`    • 情绪表达：${bodyAnalysis.tone.emotional}篇`);
    console.log();
    
    console.log('  信息密度:');
    console.log(`    • 含价格信息：${bodyAnalysis.content.hasPrice}篇`);
    console.log(`    • 含时间信息：${bodyAnalysis.content.hasTime}篇`);
    console.log();
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log('💡 爆款三要素建议:');
  console.log('  1. 标题：身份标签 + 具体数字 + 明确利益点');
  console.log('  2. 正文：清单/步骤格式 + 第一人称叙述 + 互动结尾');
  console.log('  3. 信息：价格/时间等具体数据提升可信度');
  console.log();
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
📊 小红书爆款规律分析器

用法:
  node pattern-analyzer.js --demo
  node pattern-analyzer.js --titles <file.json>
  node pattern-analyzer.js --bodies <file.json>
  node pattern-analyzer.js --input <file.json>

选项:
  --demo         运行示例
  --titles       分析标题 (JSON 数组文件)
  --bodies       分析正文 (JSON 数组文件)
  --input        完整输入 (含 titles 和 bodies 字段)
  --help, -h     显示帮助
`);
    process.exit(0);
  }
  
  if (args.includes('--demo')) {
    const demoTitles = [
      '打工人带饭｜5 天不重样 30 元/天',
      '一周便当合集｜新手必看',
      '10 分钟快手菜｜懒人必备',
      '学生党省钱攻略｜一天 20 元',
      '新手化妆避坑｜别乱买'
    ];
    
    const demoBodies = [
      `周一：鸡腿饭🍗\n鸡腿 8 元 + 西兰花 3 元\n空气炸锅 20 分钟\n\n你们明天想吃什么？`,
      `这 5 道菜我做了无数次\n每道都不超过 15 分钟\n收藏起来慢慢做\n\n评论区告诉我你喜欢哪道`,
      `以前天天点外卖\n现在自己带饭\n一个月省了 1000 块\n\n打工人真的不容易`
    ];
    
    const titleAnalysis = analyzeTitle(demoTitles);
    const bodyAnalysis = analyzeBody(demoBodies);
    generateReport(titleAnalysis, bodyAnalysis);
    return;
  }
  
  // 文件输入处理
  const filePath = args[args.indexOf('--input') + 1] || 
                   args[args.indexOf('--titles') + 1] || 
                   args[args.indexOf('--bodies') + 1];
  
  if (!filePath) {
    console.error('❌ 请提供输入文件路径');
    process.exit(1);
  }
  
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    const titles = data.titles || [];
    const bodies = data.bodies || [];
    
    const titleAnalysis = titles.length > 0 ? analyzeTitle(titles) : { error: '无标题数据' };
    const bodyAnalysis = bodies.length > 0 ? analyzeBody(bodies) : { error: '无正文数据' };
    
    generateReport(titleAnalysis, bodyAnalysis);
  } catch (e) {
    console.error(`❌ 读取或解析文件失败：${e.message}`);
    process.exit(1);
  }
}

main();

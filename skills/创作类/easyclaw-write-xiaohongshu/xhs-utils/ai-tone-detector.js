#!/usr/bin/env node
/**
 * 小红书 AI 味检测器
 * 检测文案是否过于 AI 化，并提供修改建议
 */

import fs from 'fs';

// AI 味关键词/句式 (需要避免)
const AI_PATTERNS = {
  formal: {
    patterns: ['综上所述', '总的来说', '因此', '由此可见', '基于以上', '首先其次最后', '总而言之'],
    label: '过于正式',
    severity: 'high'
  },
  marketing: {
    patterns: ['不容错过', '速速', '赶紧', '立刻', '马上', '限时', '抢购', '福利'],
    label: '营销号口吻',
    severity: 'high'
  },
  generic: {
    patterns: ['大家', '用户', '受众', '建议如下', '值得注意的是', '需要指出'],
    label: '泛泛而谈',
    severity: 'medium'
  },
  excessive: {
    patterns: ['非常非常', '超级超级', '真的真的', '太太太'],
    label: '过度修饰',
    severity: 'medium'
  },
  robot: {
    patterns: ['作为一名', '在这篇文章中', '本文将', '笔者', '我们来看看'],
    label: '机器人口吻',
    severity: 'high'
  }
};

// 真人感关键词 (鼓励使用)
const HUMAN_PATTERNS = {
  firstPerson: {
    patterns: ['我', '我的', '我觉得', '我发现', '我当时', '我踩过的坑'],
    label: '第一人称'
  },
  uncertainty: {
    patterns: ['可能', '也许', '我感觉', '我猜', '不确定', '个人觉得'],
    label: '适度不确定'
  },
  specific: {
    patterns: ['那天', '当时', '那天早上', '那一刻', '突然'],
    label: '具体细节'
  },
  casual: {
    patterns: ['绝了', '真的', '太', '好用到哭', '香到', '笑死'],
    label: '口语化'
  },
  imperfect: {
    patterns: ['但是', '不过', '其实', '说实话', '有一说一'],
    label: '不完美表达'
  }
};

function detectAIPatterns(text) {
  const issues = [];
  
  Object.entries(AI_PATTERNS).forEach(([type, { patterns, label, severity }]) => {
    patterns.forEach(pattern => {
      const regex = new RegExp(pattern, 'g');
      const matches = text.match(regex);
      if (matches) {
        issues.push({
          type,
          label,
          severity,
          pattern,
          count: matches.length,
          suggestion: getSuggestion(type, pattern)
        });
      }
    });
  });
  
  return issues;
}

function detectHumanPatterns(text) {
  const scores = {};
  
  Object.entries(HUMAN_PATTERNS).forEach(([type, { patterns, label }]) => {
    let count = 0;
    patterns.forEach(pattern => {
      const matches = text.match(new RegExp(pattern, 'g'));
      if (matches) count += matches.length;
    });
    scores[type] = { label, count };
  });
  
  return scores;
}

function getSuggestion(type, pattern) {
  const suggestions = {
    formal: {
      '综上所述': '删掉，直接说结论',
      '总的来说': '删掉，直接说结论',
      '因此': '换成"所以"或直接省略',
      '首先其次最后': '用自然过渡，不要序号'
    },
    marketing: {
      '不容错过': '换成"我觉得不错"',
      '速速': '换成"可以试试"',
      '赶紧': '换成"有时间可以"',
      '立刻': '换成"我一般是"'
    },
    generic: {
      '大家': '换成"我"或具体人群',
      '用户': '换成"我"或"朋友"',
      '建议如下': '换成"我是这样做的"'
    },
    robot: {
      '作为一名': '直接说"我是"',
      '在这篇文章中': '删掉',
      '本文将': '换成"我想分享"'
    }
  };
  
  return suggestions[type]?.[pattern] || `考虑换成更口语化的表达`;
}

function calculateScore(aiIssues, humanScores) {
  let score = 100;
  aiIssues.forEach(issue => {
    if (issue.severity === 'high') score -= 15 * issue.count;
    else if (issue.severity === 'medium') score -= 8 * issue.count;
    else score -= 3 * issue.count;
  });
  
  Object.values(humanScores).forEach(({ count }) => {
    score += Math.min(count * 2, 20);
  });
  
  return Math.max(0, Math.min(100, score));
}

function getLevel(score) {
  if (score >= 80) return { level: '优秀', emoji: '✅', desc: '真人感很强，可以直接发布' };
  if (score >= 60) return { level: '良好', emoji: '👍', desc: '有少量 AI 味，建议微调' };
  if (score >= 40) return { level: '一般', emoji: '⚠️', desc: 'AI 味较明显，需要修改' };
  return { level: '较差', emoji: '❌', desc: 'AI 味很重，建议重写' };
}

function generateReport(text, aiIssues, humanScores, score) {
  console.log('\n🤖 小红书 AI 味检测报告\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  const level = getLevel(score);
  console.log(`📊 综合得分：${score}/100`);
  console.log(`   ${level.emoji} ${level.level} - ${level.desc}`);
  console.log();
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  if (aiIssues.length === 0) {
    console.log('✅ 未发现明显 AI 味表达\n');
  } else {
    console.log('⚠️ AI 味表达检测:\n');
    
    const grouped = {};
    aiIssues.forEach(issue => {
      if (!grouped[issue.label]) grouped[issue.label] = [];
      grouped[issue.label].push(issue);
    });
    
    Object.entries(grouped).forEach(([label, issues]) => {
      console.log(`  【${label}】`);
      issues.forEach(issue => {
        console.log(`    • "${issue.pattern}" 出现 ${issue.count}次`);
        console.log(`      建议：${issue.suggestion}`);
      });
      console.log();
    });
  }
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log('✅ 真人感表达统计:\n');
  Object.entries(humanScores).forEach(([type, { label, count }]) => {
    const bar = '█'.repeat(Math.min(count, 10));
    console.log(`  ${label}: ${bar} (${count}次)`);
  });
  console.log();
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log('💡 修改建议:\n');
  console.log('  1. 多用"我"开头，少用"大家/用户"');
  console.log('  2. 加入具体细节 (时间、地点、感受)');
  console.log('  3. 允许不完美，用"可能/也许/我觉得"');
  console.log('  4. 删掉"综上所述/总的来说"等过渡词');
  console.log('  5. 像跟朋友聊天，不要像写文章');
  console.log();
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
🤖 小红书 AI 味检测器

用法:
  node ai-tone-detector.js --demo
  node ai-tone-detector.js --text "文案内容"
  node ai-tone-detector.js --file <path>

选项:
  --demo         运行示例
  --text         直接检测文本
  --file         从文件读取文本
  --help, -h     显示帮助
`);
    process.exit(0);
  }
  
  if (args.includes('--demo')) {
    const aiText = `
综上所述，这款产品的性价比非常高。
首先，它的价格非常便宜。
其次，它的功能非常强大。
因此，我非常推荐大家购买。
值得注意的是，这是一款不容错过的产品。
`;
    
    const humanText = `
说实话，这个东西我用了两周了。
当时买的时候还有点犹豫，怕踩坑。
结果发现真香，特别是早上赶时间的时候。
不过有一说一，颜色选择确实少了点。
但总体来说，我觉得学生党可以冲。
`;
    
    console.log('\n📝 示例 1: AI 味较重的文案\n');
    const aiIssues1 = detectAIPatterns(aiText);
    const humanScores1 = detectHumanPatterns(aiText);
    const score1 = calculateScore(aiIssues1, humanScores1);
    generateReport(aiText, aiIssues1, humanScores1, score1);
    
    console.log('\n📝 示例 2: 真人感较强的文案\n');
    const aiIssues2 = detectAIPatterns(humanText);
    const humanScores2 = detectHumanPatterns(humanText);
    const score2 = calculateScore(aiIssues2, humanScores2);
    generateReport(humanText, aiIssues2, humanScores2, score2);
    
    return;
  }
  
  let text;
  
  if (args.includes('--text')) {
    const textIndex = args.indexOf('--text');
    text = args.slice(textIndex + 1).join(' ');
  } else if (args.includes('--file')) {
    const filePath = args[args.indexOf('--file') + 1];
    try {
      text = fs.readFileSync(filePath, 'utf-8');
    } catch (e) {
      console.error(`❌ 读取文件失败：${e.message}`);
      process.exit(1);
    }
  } else {
    console.error('❌ 请提供 --text 或 --file 参数');
    process.exit(1);
  }
  
  const aiIssues = detectAIPatterns(text);
  const humanScores = detectHumanPatterns(text);
  const score = calculateScore(aiIssues, humanScores);
  
  generateReport(text, aiIssues, humanScores, score);
  process.exit(score >= 60 ? 0 : 1);
}

main();

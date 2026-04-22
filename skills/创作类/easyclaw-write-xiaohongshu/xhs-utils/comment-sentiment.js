#!/usr/bin/env node
/**
 * 小红书评论情感共鸣分析器
 * 分析评论中的情感触发点和共鸣原因
 */

import fs from 'fs';

// 共鸣点分类
const RESONANCE_CATEGORIES = {
  painPoint: {
    keywords: ['我也是', '真的', '太真实了', '感同身受', '说到心坎里', '就是我', '本人'],
    label: '共同痛点'
  },
  identity: {
    keywords: ['打工人', '学生党', '宝妈', '上班族', '北漂', '同龄人', '姐妹'],
    label: '身份认同'
  },
  solution: {
    keywords: ['终于', '有救了', '拯救', '解决', '办法', '管用', '有效'],
    label: '焦虑与解决'
  },
  value: {
    keywords: ['值得', '性价比', '省钱', '实用', '干货', '良心'],
    label: '价值观认同'
  },
  surprise: {
    keywords: ['没想到', '居然', '意外', '原来', '还能这样', '涨知识'],
    label: '反差/意外'
  },
  actionable: {
    keywords: ['收藏', '码住', '抄作业', '照做', '试试', '安排'],
    label: '可复制性'
  },
  share: {
    keywords: ['转发', '分享', '推荐', '给朋友', '闺蜜', '同事'],
    label: '分享欲'
  },
  question: {
    keywords: ['求', '怎么', '哪里', '什么', '多少钱', '链接'],
    label: '好奇/询问'
  }
};

// 互动设计模式
const INTERACTION_PATTERNS = [
  { type: 'question', keywords: ['你们', '大家', '有没有', '觉得', '吗'], label: '提问互动' },
  { type: 'choice', keywords: ['哪个', '还是', 'A 还是 B', '选'], label: '选择互动' },
  { type: 'fill', keywords: ['评论区', '留言', '告诉我', '说'], label: '评论引导' },
  { type: 'action', keywords: ['收藏', '点赞', '关注', '转发'], label: '行动号召' },
  { type: 'keyword', keywords: ['扣 1', '蹲', '求', '想要'], label: '关键词互动' }
];

function categorizeComment(comment) {
  const categories = [];
  
  Object.entries(RESONANCE_CATEGORIES).forEach(([key, { keywords, label }]) => {
    const matches = keywords.filter(kw => comment.includes(kw));
    if (matches.length > 0) {
      categories.push({
        category: key,
        label,
        matches,
        excerpt: comment.length > 50 ? comment.slice(0, 50) + '...' : comment
      });
    }
  });
  
  return categories;
}

function analyzeComments(comments) {
  if (!Array.isArray(comments) || comments.length === 0) {
    return { error: '需要提供评论数组' };
  }
  
  const results = {
    total: comments.length,
    categories: {},
    topComments: [],
    interactionSuggestions: []
  };
  
  // 统计各共鸣点出现次数
  comments.forEach(comment => {
    const categories = categorizeComment(comment);
    categories.forEach(cat => {
      if (!results.categories[cat.category]) {
        results.categories[cat.category] = {
          label: cat.label,
          count: 0,
          examples: []
        };
      }
      results.categories[cat.category].count++;
      if (results.categories[cat.category].examples.length < 3) {
        results.categories[cat.category].examples.push(cat.excerpt);
      }
    });
  });
  
  // 找出共鸣度最高的评论
  const commentScores = comments.map((comment, index) => ({
    index,
    comment,
    score: categorizeComment(comment).length
  }));
  
  results.topComments = commentScores
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map(item => ({
      comment: item.comment,
      resonanceCount: item.score
    }));
  
  // 分析互动设计建议
  const interactionAnalysis = {};
  comments.forEach(comment => {
    INTERACTION_PATTERNS.forEach(pattern => {
      if (pattern.keywords.some(kw => comment.includes(kw))) {
        interactionAnalysis[pattern.type] = (interactionAnalysis[pattern.type] || 0) + 1;
      }
    });
  });
  
  results.interactionSuggestions = Object.entries(interactionAnalysis)
    .sort((a, b) => b[1] - a[1])
    .map(([type, count]) => {
      const pattern = INTERACTION_PATTERNS.find(p => p.type === type);
      return {
        type: pattern?.label || type,
        count,
        suggestion: getInteractionSuggestion(type)
      };
    });
  
  return results;
}

function getInteractionSuggestion(type) {
  const suggestions = {
    question: '在结尾增加开放性问题，如"你们呢？"',
    choice: '提供选项让用户选择，如"A 还是 B？"',
    fill: '引导用户分享经历，如"评论区告诉我"',
    action: '温和引导互动，如"有用记得收藏"',
    keyword: '设置关键词互动，如"想要扣 1"'
  };
  return suggestions[type] || '增加互动元素';
}

function generateReport(analysis) {
  console.log('\n💬 小红书评论情感共鸣分析报告\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  if (analysis.error) {
    console.log(`❌ 分析失败：${analysis.error}`);
    return;
  }
  
  console.log(`📊 总评论数：${analysis.total}条\n`);
  
  console.log('🎯 共鸣点分布 (从高到低):');
  console.log();
  
  const sortedCategories = Object.entries(analysis.categories)
    .sort((a, b) => b[1].count - a[1].count);
  
  sortedCategories.forEach(([key, data], index) => {
    const percentage = Math.round((data.count / analysis.total) * 100);
    const bar = '█'.repeat(Math.min(percentage / 5, 20));
    console.log(`${index + 1}. ${data.label}`);
    console.log(`   ${bar} ${data.count}条 (${percentage}%)`);
    console.log(`   示例:`);
    data.examples.forEach(ex => {
      console.log(`     • "${ex}"`);
    });
    console.log();
  });
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log('🔥 高共鸣评论 Top5:');
  analysis.topComments.forEach((item, index) => {
    console.log(`${index + 1}. [${item.resonanceCount}个共鸣点]`);
    console.log(`   "${item.comment}"`);
    console.log();
  });
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log('💡 互动设计建议:');
  analysis.interactionSuggestions.forEach((suggestion, index) => {
    console.log(`${index + 1}. ${suggestion.type}`);
    console.log(`   出现 ${suggestion.count}次 → ${suggestion.suggestion}`);
    console.log();
  });
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  // 总结
  console.log('📝 总结建议:');
  const topResonance = sortedCategories.slice(0, 3).map(([, data]) => data.label);
  console.log(`  核心共鸣点：${topResonance.join(' + ')}`);
  console.log(`  建议在内容中强化这些情感触发点`);
  console.log();
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
💬 小红书评论情感共鸣分析器

用法:
  node comment-sentiment.js --demo
  node comment-sentiment.js --input <file.json>
  node comment-sentiment.js --file <path>

选项:
  --demo         运行示例
  --input        评论 JSON 数组文件或字符串
  --file         从文件读取评论
  --help, -h     显示帮助

输入格式:
  ["评论 1", "评论 2", ...]
`);
    process.exit(0);
  }
  
  if (args.includes('--demo')) {
    const demoComments = [
      '太真实了！我也是每天不知道吃什么',
      '打工人表示真的需要这个，收藏了',
      '终于有救了，明天就试试',
      '姐妹求问这个多少钱啊',
      '我也是学生党，这个预算刚刚好',
      '没想到还能这样做，涨知识了',
      '已收藏，周末照做',
      '你们公司食堂多少钱一顿？',
      '真的省钱，我一个月省了 500',
      '转发给闺蜜了，她也需要'
    ];
    
    const analysis = analyzeComments(demoComments);
    generateReport(analysis);
    return;
  }
  
  let comments;
  
  if (args.includes('--input')) {
    const inputPath = args[args.indexOf('--input') + 1];
    try {
      const content = fs.readFileSync(inputPath, 'utf-8');
      comments = JSON.parse(content);
    } catch {
      try {
        comments = JSON.parse(inputPath);
      } catch {
        console.error('❌ 无法解析输入，请提供有效的 JSON 数组');
        process.exit(1);
      }
    }
  } else if (args.includes('--file')) {
    const filePath = args[args.indexOf('--file') + 1];
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      comments = JSON.parse(content);
    } catch (e) {
      console.error(`❌ 读取文件失败：${e.message}`);
      process.exit(1);
    }
  } else {
    console.error('❌ 请提供 --input 或 --file 参数');
    process.exit(1);
  }
  
  if (!Array.isArray(comments)) {
    console.error('❌ 输入必须是评论数组');
    process.exit(1);
  }
  
  const analysis = analyzeComments(comments);
  generateReport(analysis);
}

main();

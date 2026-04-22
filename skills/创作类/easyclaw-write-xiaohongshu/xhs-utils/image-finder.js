#!/usr/bin/env node
/**
 * 小红书配图搜索器
 * 搜索 9:16 竖图，优先免版权来源
 */

import fs from 'fs';

const IMAGE_SOURCES = {
  pexels: {
    name: 'Pexels',
    searchUrl: (query, orientation = 'portrait') => 
      `https://www.pexels.com/search/${encodeURIComponent(query)}/?orientation=${orientation}`,
    api: 'https://api.pexels.com/v1/search',
    note: '需 API Key，免费额度充足'
  },
  unsplash: {
    name: 'Unsplash',
    searchUrl: (query, orientation = 'portrait') => 
      `https://unsplash.com/s/photos/${encodeURIComponent(query)}?orientation=portrait`,
    api: 'https://api.unsplash.com/search/photos',
    note: '需 API Key，免费额度充足'
  },
  pixabay: {
    name: 'Pixabay',
    searchUrl: (query) => 
      `https://pixabay.com/images/search/${encodeURIComponent(query)}/`,
    api: 'https://pixabay.com/api/',
    note: '需 API Key，免费额度充足'
  }
};

// 常见主题的图片搜索关键词映射
const KEYWORD_MAPPING = {
  '带饭': ['bento box', 'meal prep', 'lunch box', 'homemade lunch'],
  '便当': ['bento', 'japanese lunch', 'meal prep container'],
  '美食': ['food', 'delicious', 'homemade food', 'cooking'],
  '化妆': ['makeup', 'cosmetics', 'beauty routine', 'makeup tutorial'],
  '穿搭': ['outfit', 'fashion', 'daily look', 'street style'],
  '学习': ['study', 'notebook', 'desk setup', 'studying'],
  '健身': ['workout', 'gym', 'fitness', 'exercise'],
  '旅行': ['travel', 'destination', 'vacation', 'trip'],
  '家居': ['home decor', 'interior', 'room', 'cozy home'],
  '咖啡': ['coffee', 'cafe', 'latte', 'coffee shop']
};

function mapKeywords(topic) {
  const mapped = [];
  
  Object.entries(KEYWORD_MAPPING).forEach(([cn, ens]) => {
    if (topic.includes(cn)) {
      mapped.push(...ens);
    }
  });
  
  if (mapped.length === 0) {
    mapped.push(topic);
  }
  
  return [...new Set(mapped)];
}

function generateSearchLinks(topic) {
  const keywords = mapKeywords(topic);
  const results = [];
  
  Object.entries(IMAGE_SOURCES).forEach(([key, source]) => {
    keywords.forEach(kw => {
      results.push({
        source: source.name,
        keyword: kw,
        url: source.searchUrl(kw),
        note: source.note
      });
    });
  });
  
  return results;
}

function formatImageSuggestion(topic, links) {
  console.log('\n🖼️ 小红书配图搜索建议\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log(`📝 主题：${topic}`);
  console.log(`🔑 映射关键词：${mapKeywords(topic).join(', ')}`);
  console.log();
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log('🔗 推荐搜索链接:\n');
  
  const grouped = {};
  links.forEach(link => {
    if (!grouped[link.source]) grouped[link.source] = [];
    grouped[link.source].push(link);
  });
  
  Object.entries(grouped).forEach(([source, items]) => {
    console.log(`  【${source}】`);
    items.slice(0, 3).forEach((item, idx) => {
      console.log(`    ${idx + 1}. "${item.keyword}"`);
      console.log(`       ${item.url}`);
      console.log(`       ${item.note}`);
      console.log();
    });
  });
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log('💡 选图建议:\n');
  console.log('  1. 优先选择 9:16 竖图 (1080x1920 或类似比例)');
  console.log('  2. 图片要清晰、光线好、主体突出');
  console.log('  3. 避免水印、logo、文字覆盖');
  console.log('  4. 风格与内容调性一致 (温馨/专业/活泼)');
  console.log('  5. 1-2 张即可，不要太多');
  console.log();
  
  console.log('⚖️ 版权提醒:\n');
  console.log('  • Pexels/Unsplash/Pixabay 均为免版权商用');
  console.log('  • 仍建议标注图片来源 (可选)');
  console.log('  • 避免使用有明显人物肖像的图片商用');
  console.log();
}

function mockSearch(topic) {
  const mockImages = {
    '带饭': [
      { url: 'https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg', desc: '便当盒装食物' },
      { url: 'https://images.pexels.com/photos/3764636/pexels-photo-3764636.jpeg', desc: '自制午餐' }
    ],
    '化妆': [
      { url: 'https://images.pexels.com/photos/1621191/pexels-photo-1621191.jpeg', desc: '化妆品摆放' },
      { url: 'https://images.pexels.com/photos/2063598/pexels-photo-2063598.jpeg', desc: '化妆过程' }
    ],
    '美食': [
      { url: 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg', desc: '美食特写' },
      { url: 'https://images.pexels.com/photos/958543/pexels-photo-958543.jpeg', desc: '餐桌食物' }
    ]
  };
  
  const images = mockImages[topic] || mockImages['美食'];
  
  console.log('\n🖼️ 模拟搜索结果 (示例图片)\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  console.log(`📝 主题：${topic}\n`);
  console.log('推荐图片:\n');
  
  images.forEach((img, idx) => {
    console.log(`  ${idx + 1}. ${img.desc}`);
    console.log(`     ${img.url}`);
    console.log(`     比例：9:16 (竖图)`);
    console.log(`     来源：Pexels (免版权)`);
    console.log();
  });
  
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log('⚠️  注：以上为示例链接，实际使用请搜索最新图片\n');
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
🖼️ 小红书配图搜索器

用法:
  node image-finder.js --demo
  node image-finder.js --topic "带饭"
  node image-finder.js --topic "化妆" --mock
  node image-finder.js --links "美食"

选项:
  --demo         运行示例
  --topic        搜索主题 (中文)
  --links        仅生成搜索链接
  --mock         使用模拟结果 (无需 API)
  --help, -h     显示帮助
`);
    process.exit(0);
  }
  
  if (args.includes('--demo')) {
    mockSearch('带饭');
    return;
  }
  
  if (args.includes('--topic')) {
    const topicIndex = args.indexOf('--topic');
    const topic = args[topicIndex + 1];
    
    if (args.includes('--mock')) {
      mockSearch(topic);
    } else if (args.includes('--links')) {
      const links = generateSearchLinks(topic);
      formatImageSuggestion(topic, links);
    } else {
      const links = generateSearchLinks(topic);
      formatImageSuggestion(topic, links);
      console.log('\n');
      mockSearch(topic);
    }
    
    return;
  }
  
  console.error('❌ 请提供 --topic 参数');
  process.exit(1);
}

main();

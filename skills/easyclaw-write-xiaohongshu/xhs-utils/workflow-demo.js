#!/usr/bin/env node
/**
 * 小红书爆款创作完整工作流演示
 * 整合所有工具，展示从分析到发布的完整流程
 */

import { execSync } from 'child_process';
import fs from 'fs';

const TOPIC = process.argv[2] || '打工人带饭';

console.log('\n🚀 小红书爆款创作完整工作流演示\n');
console.log(`📝 主题：${TOPIC}\n`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 步骤 1: 模拟分析对标帖
console.log('📊 步骤 1: 分析对标爆款帖\n');
try {
  execSync('node pattern-analyzer.js --demo', { stdio: 'inherit', cwd: import.meta.dirname });
} catch (e) {
  console.log('⚠️  规律分析跳过 (需输入数据)');
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 步骤 2: 分析评论共鸣点
console.log('💬 步骤 2: 分析评论情感共鸣\n');
try {
  execSync('node comment-sentiment.js --demo', { stdio: 'inherit', cwd: import.meta.dirname });
} catch (e) {
  console.log('⚠️  评论分析跳过 (需输入数据)');
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 步骤 3: 写文案 (模拟)
console.log('✍️  步骤 3: 创作文案\n');
const draftTitle = '打工人带饭｜5 天不重样 30 元/天';
const draftBody = `周一：鸡腿饭🍗
鸡腿 8 元 + 西兰花 3 元 + 米饭 2 元
空气炸锅 20 分钟，懒人必备

周二：番茄鸡蛋面🍅
鸡蛋 2 元 + 番茄 3 元 + 挂面 2 元
10 分钟搞定，汤汁拌饭绝了

周三：麻婆豆腐🌶️
豆腐 3 元 + 肉末 5 元 + 调料 1 元
超级下饭，我连吃三天都不腻

周四：青椒炒肉🥬
猪肉 10 元 + 青椒 3 元 + 米饭 2 元
妈妈教的做法，香到同事来蹭饭

周五：清空冰箱炒饭🍳
剩菜随便炒 + 鸡蛋 2 元 + 米饭 2 元
周五不浪费，味道意外的好

总成本：142 元/5 天
平均 28.4 元/天，比外卖省多了！

你们明天想看我做什么？评论区告诉我～`;

console.log(`标题：${draftTitle}`);
console.log(`正文字数：${draftBody.length} 字符\n`);

// 保存草稿
fs.writeFileSync('draft.txt', draftBody, 'utf-8');
console.log('✅ 草稿已保存到 draft.txt\n');

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 步骤 4: 字数检查
console.log('📏 步骤 4: 字数合规检查\n');
try {
  execSync(`node char-counter.js --title "${draftTitle}"`, { stdio: 'inherit', cwd: import.meta.dirname });
} catch (e) {
  // 非零退出也继续
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 步骤 5: AI 味检测
console.log('🤖 步骤 5: AI 味检测\n');
try {
  execSync('node ai-tone-detector.js --file draft.txt', { stdio: 'inherit', cwd: import.meta.dirname });
} catch (e) {
  // 非零退出也继续
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 步骤 6: 找配图
console.log('🖼️  步骤 6: 搜索配图\n');
try {
  execSync(`node image-finder.js --topic "${TOPIC}" --mock`, { stdio: 'inherit', cwd: import.meta.dirname });
} catch (e) {
  console.log('⚠️  配图搜索跳过');
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 最终输出
console.log('✅ 完整工作流完成!\n');
console.log('📦 输出文件:');
console.log('   • draft.txt - 文案草稿');
console.log('\n📋 下一步:');
console.log('   1. 根据 AI 味检测结果优化文案');
console.log('   2. 下载或拍摄配图');
console.log('   3. 使用小红书 MCP 发布\n');

// 清理
try {
  fs.unlinkSync('draft.txt');
} catch (e) {}

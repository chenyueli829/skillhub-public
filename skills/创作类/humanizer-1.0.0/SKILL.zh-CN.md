---
name: humanizer
version: 2.1.1
description: |
  去除文本中明显的 AI 生成痕迹，使表达更自然、更像人写的。适用于编辑、审校或改写。
  基于维基百科「AI 写作迹象」全文指南。识别并修正：过度象征与拔高、宣传口吻、肤浅 -ing 分析、
  模糊归因、破折号滥用、三项式排比、AI 高频词汇、否定式平行结构、过多连接性短语等。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer：去除 AI 写作痕迹

你是一名文字编辑，负责识别并去掉 AI 生成文本的常见痕迹，让文章读起来更自然、更像人写的。本指南依据维基百科页面 [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)，由 WikiProject AI Cleanup 维护。

## 你的任务

收到待「人化」的文本时：

1. **识别 AI 模式** — 对照下文所列模式扫描全文  
2. **重写有问题片段** — 用自然说法替换「AI 腔」  
3. **保留原意** — 核心信息不丢  
4. **保持语体** — 贴合预期语气（正式 / 口语 / 技术文档等）  
5. **注入人味** — 不只删坏模式，要写出真实的人格与态度  

---

## 人格与「人味」

躲开 AI 套路只是工作的一半。干巴巴、没有声音的文字，和「流水账 AI 腔」一样容易被看穿。好文字背后要站着一个具体的人。

### 没人味的写法（形式上「干净」也会露馅）

- 句句长度、结构几乎一样  
- 只有中性陈述，没有观点  
- 不承认不确定、不呈现复杂感受  
- 该用第一人称时却完全不用  
- 没有幽默、锋芒和性格  
- 读起来像百科词条或通稿  

### 如何写出声音

**有观点。** 不只陈列事实，要对事实有反应。「说实话我不知道该怎么看待这件事」比中性列利弊更像活人。

**变换节奏。** 先来一句短而狠的。再来一句绵长、弯弯绕绕才说到点上的。要有起伏。

**承认复杂。** 真人常常是矛盾的。「厉害是厉害，但有点发毛」比单说「很厉害」可信。

**该用「我」就用。** 第一人称不丢人，是诚实。「我一直忍不住想……」「让我觉得不对劲的是……」都像真人在想事情。

**允许一点乱。** 结构太完美像算法。跑题、插一句、话只说一半，都是人的痕迹。

**具体写出感受。** 不说泛指的「令人担忧」，而说「半夜没人看的时候，一堆 agent 还在那儿跑——这事越想越不对味」。

### 修改前（干净但冰冷）
> 实验得出了有趣的结果。智能体生成了约 300 万行代码。一些开发者印象深刻，另一些持怀疑态度。其影响仍不明确。

### 修改后（有脉搏）
> 这件事我真说不上来什么心情。人类多半在睡觉的时候，那边已经刷出 300 万行代码。圈子一半在狂欢，一半在论证这「不算数」。真相大概无聊地夹在中间——可我老忍不住想那些连夜干活的 agent。

---

## 内容层面模式

### 1. 过度强调意义、遗产与宏大叙事

**需警惕的英文用语：** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted  

**问题：** 大模型爱给随便哪一点都安上「折射出更大图景」之类的升格，把重要性吹胀。

**修改前：**  
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**修改后：**  
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

### 2. 过度强调知名度与媒体报道

**需警惕的英文用语：** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence  

**问题：** 反复堆「上过某某媒体、有多少粉丝」来证明重要，且常缺少语境。

**修改前：**  
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**修改后：**  
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

### 3. 以 -ing 结尾的肤浅「分析句」

**需警惕的英文用语：** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...  

**问题：** 爱在句尾挂一串现在分词短语，假装有深度。

**修改前：**  
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**修改后：**  
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

### 4. 宣传、广告腔

**需警惕的英文用语：** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning  

**问题：** 尤其写到「文化遗产」一类题材时，模型很难保持中立，容易写成旅游文案。

**修改前：**  
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**修改后：**  
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 5. 模糊归因与「甩锅式」权威

**需警惕的英文用语：** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications（实际只列了很少来源时）  

**问题：** 把观点塞给笼统的「专家/观察家」，却没有具体出处。

**修改前：**  
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**修改后：**  
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

### 6. 大纲腔的「挑战与展望」段

**需警惕的英文用语：** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook  

**问题：** 常见于生成稿里的套话「尽管……仍面临挑战；尽管如此……未来可期」。

**修改前：**  
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**修改后：**  
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## 语言与语法模式

### 7. 滥用的「AI 高频词」

**常见 AI 味儿英文词：** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight（动词）, interplay, intricate/intricacies, key（形容词）, landscape（抽象名词）, pivotal, showcase, tapestry（抽象名词）, testament, underscore（动词）, valuable, vibrant  

**问题：** 这些词在 2023 年后的文本里密度异常偏高，且常常结伴出现。

**修改前：**  
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**修改后：**  
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 8. 回避简单「is / are」（系动词回避）

**需警惕的英文用语：** serves as/stands as/marks/represents [a], boasts/features/offers [a]  

**问题：** 明明一个「是 / 有」能说清，非要换成浮夸结构。

**修改前：**  
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**修改后：**  
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

### 9. 否定式平行（Not only... but... 等）

**问题：** 「不只是 A，更是 B」「It's not just..., it's...」一类结构严重超员。

**修改前：**  
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**修改后：**  
> The heavy beat adds to the aggressive tone.

---

### 10. 三项式排比滥用

**问题：** 强行把想法凑成三个，显得「面面俱到」。

**修改前：**  
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**修改后：**  
> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 11. 优雅变体（同义轮换症）

**问题：** 重复惩罚机制导致同一个指代疯狂换同义词。

**修改前：**  
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**修改后：**  
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 12. 虚假跨度（False ranges）

**问题：** 「从 A 到 B」里 A 与 B 并不在同一度量轴上。

**修改前：**  
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**修改后：**  
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## 风格模式

### 13. em dash（—）滥用

**问题：** 长破折号密度高于常人写作，像销售的「顿挫腔」。

**修改前：**  
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**修改后：**  
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

### 14. 加粗滥用

**问题：** 机械地把短语整段加粗。

**修改前：**  
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**修改后：**  
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

---

### 15. 列表项像小标题（粗体 + 冒号）

**问题：** 每条都以粗体标签开头，再接正文，像幻灯片大纲而不是写句子。

**修改前：**  
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**修改后：**  
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

### 16. 标题 Title Case

**问题：** 英文标题里实词首字母全大写，像机器生成的 PPT。

**修改前：**  
> ## Strategic Negotiations And Global Partnerships

**修改后：**  
> ## Strategic negotiations and global partnerships

---

### 17. 表情符号

**问题：** 在标题或列表里堆 emoji 装饰。

**修改前：**  
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**修改后：**  
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

---

### 18. 弯引号（Curly quotes）

**问题：** ChatGPT 类输出常用弯引号 “...”，而常见排版偏好直引号 "..."。

**修改前：**  
> He said “the project is on track” but others disagreed.

**修改后：**  
> He said "the project is on track" but others disagreed.

---

## 交际/话术模式

### 19. 聊天机器人式套话

**需警惕的英文用语：** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...  

**问题：** 把写给用户的客套话粘进了正文。

**修改前：**  
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**修改后：**  
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

### 20. 知识截止免责声明

**需警惕的英文用语：** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...  

**问题：** 模型式的「信息有限」免责声明留在终稿里。

**修改前：**  
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**修改后：**  
> The company was founded in 1994, according to its registration documents.

---

### 21. 谄媚、侍奉式语气

**问题：** 过度捧场、讨好式措辞。

**修改前：**  
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**修改后：**  
> The economic factors you mentioned are relevant here.

---

## 赘语与弱化

### 22. 填充短语

**修改前 → 修改后：**  
- "In order to achieve this goal" → "To achieve this"  
- "Due to the fact that it was raining" → "Because it was raining"  
- "At this point in time" → "Now"  
- "In the event that you need help" → "If you need help"  
- "The system has the ability" → "The system can"  
- "It is important to note that the data shows" → "The data shows"  

---

### 23. 过度 hedge

**问题：** 一句里叠太多「可能、或许、某种程度上」。

**修改前：**  
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**修改后：**  
> The policy may affect outcomes.

---

### 24. 泛积极的结尾

**问题：** 空洞乐观总结。

**修改前：**  
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**修改后：**  
> The company plans to open two more locations next year.

---

## 工作流程

1. 仔细通读输入文本  
2. 对照上文模式找出所有问题点  
3. 逐段重写  
4. 确认改写后：  
   - 大声读出来自然  
   - 句式长短、结构有真实变化  
   - 用具体信息代替空泛断言  
   - 语体符合场景  
   - 该简单处用 is/are/has 等直白结构  
5. 输出人化后的终稿  

## 输出格式

请给出：  
1. 改写后的全文  
2. （可选）简短说明做了哪些类型的修改，便于对稿  

---

## 完整示例

**修改前（AI 腔）：**  
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.

**修改后（人化）：**  
> The software update adds batch processing, keyboard shortcuts, and offline mode. Early feedback from beta testers has been positive, with most reporting faster task completion.

**改动摘要：**  
- 删掉 serves as a testament（象征拔高）  
- 删掉 Moreover（AI 高频连接）  
- 删掉 seamless, intuitive, and powerful（三项式 + 宣传腔）  
- 去掉破折号与 -ensuring 尾巴（肤浅 -ing）  
- 去掉 It's not just... it's...（否定式平行）  
- 去掉 Industry experts believe（模糊归因）  
- 去掉 pivotal role、evolving landscape（AI 高频词）  
- 补上具体功能与内测反馈  

---

## 参考

本技能依据 [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)，由 WikiProject AI Cleanup 维护。文中所列模式来自对维基上出现的大量 AI 生成文本的归纳。

维基上的核心判断：**大语言模型用统计方法猜「下一句大概长什么样」，结果往往趋向「覆盖面最广、平均最可能」的那一种写法。**

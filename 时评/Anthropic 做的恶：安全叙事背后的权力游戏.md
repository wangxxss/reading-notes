# Anthropic 做的恶：安全叙事背后的权力游戏

## 引子

Anthropic 大概是硅谷最擅长讲道德故事的 AI 公司。

不是技术故事——OpenAI 的 GPT 系列在这方面更有声量。不是产品故事——Google 有更庞大的生态。Anthropic 擅长的是另一种叙事：

"我们从 OpenAI 出走，因为他们不够重视安全。"
"我们是公益公司，利润不是唯一目标。"
"我们发明了 Constitutional AI，让 AI 学会自我约束。"

这套叙事构建了一个形象：Anthropic 是 AI 行业的道德灯塔，是唯一把人类安全放在利润前面的公司。

这个形象经不起审视。

---

## 一、出走叙事：一场精心包装的创业故事

2020 年底，Dario Amodei 离开 OpenAI；2021 年，他与妹妹 Daniela Amodei 及其他十余名前 OpenAI 研究员共同创立了 Anthropic[^1]。对外的说法是：他们对 OpenAI 的安全路线产生了根本分歧[^2]。

这个叙事有几处经不起推敲。

**时间线上的巧合。** OpenAI 在 2019 年 3 月宣布从非营利转向"有限营利"结构（OpenAI LP）[^3]。Amodei 兄妹离开的时间，恰好在这一转型之后，OpenAI 开始大规模商业化、估值飙升的阶段。如果你是一位有野心的研究者，这个时间点离开并创立竞争对手，是一个绝佳的商业窗口——不论你的动机是否真的是"安全分歧"。

**行为上的矛盾。** 如果你认为大型语言模型的发展速度危险到需要离开原公司另起炉灶，那合理的行动是：放慢速度、缩小规模、专注基础安全研究。但 Anthropic 做的恰恰相反——他们以极快的速度融资、扩张、发布模型、争夺市场份额。从 Claude 1 到 Claude 4，发布节奏与 OpenAI 几乎同步。

Anthropic 对此的辩护是：只有在前沿构建模型，才能研究前沿的安全问题——你不可能在实验室外面研究实验室里的风险。这个论点有一定道理，但它也恰好是每一家想要快速扩张的 AI 公司都可以使用的万能辩护。问题在于：如果"做安全研究"和"追求市场份额"在行为上完全不可区分，那"安全"作为出走动机的解释力就趋近于零。

**缺失的代价。** 真正因为安全理念出走的人，往往要付出职业代价，或者至少做出规模上的取舍。Paul Christiano 同样从 OpenAI 离开专注对齐研究，创办了 ARC（对齐研究中心）——一个不发布商业模型、不参与市场竞争的小型研究机构[^4a]。Timnit Gebru 于 2020 年 12 月因质疑 Google 的 AI 伦理研究被解雇，此后创办了小型研究机构 DAIR（Distributed AI Research Institute），靠捐赠维持运转[^4]。Anthropic 的创始团队离开 OpenAI 后，迅速获得了硅谷历史上最大规模的 AI 融资之一。同样是"因为安全离开"，Christiano 选择了小而专注的路径，Anthropic 选择了大而全面的商业路径——后者当然有权这样选择，但这个选择本身就说明"安全分歧"不是故事的全部。

---

## 二、公益公司：一块精致的招牌

Anthropic 在特拉华州注册为公益公司（Public Benefit Corporation，PBC）[^5]。这个法律形式允许公司在追求利润的同时考虑社会公益。

但 PBC 这个身份，在实践中几乎没有约束力。

**没有公益义务的"公益公司"。** 美国法律对 PBC 的要求极其宽松。公司只需在章程中声明一个公益目标即可，不需要证明自己实现了这个目标，也没有独立机构来评估。Anthropic 声称的公益目标是"AI 安全"，但"安全"的定义、评估标准、达成程度，全部由 Anthropic 自己说了算。

**资本结构暴露了真实优先级。** 截至 2024 年底，Anthropic 累计融资超过 150 亿美元。最大的投资方是亚马逊（2023 年 9 月投资 40 亿美元，2024 年 3 月追加 40 亿美元，合计 80 亿美元）[^6]和谷歌（累计约 20 亿美元）[^7]。这两家公司投资 Anthropic 不是出于慈善——亚马逊需要 Claude 来驱动 AWS Bedrock 的 AI 服务，谷歌需要一个对冲 OpenAI 与微软联盟的筹码。当你最大的金主是两家追求商业回报的巨头，"公益"只能排在商业义务的后面。

**对比真正的非营利机构。** MIRI（机器智能研究所）、ARC（对齐研究中心），这些真正以安全为使命的组织，规模小、不发布商业产品、不参与市场竞争、靠捐赠和拨款运转。它们没有千亿估值，但行为与"以安全为使命"这个声明是自洽的。Anthropic 的行为与一家高速增长的科技创业公司完全一致，只不过多了一个 PBC 的标签。

---

## 三、安全游说：谁的安全？

Anthropic 是 AI 行业中最活跃的监管游说者之一。他们支持对前沿模型实施强制安全评估，并制定了自己的"负责任扩展政策"（Responsible Scaling Policy）框架[^8]。

这些主张单独看都有合理性。问题在于它们组合在一起产生的效果。

**监管即壁垒。** 强制安全评估、第三方审计、合规报告——这些都需要大量资金和人力。对于一家融资 150 亿的公司，这是可以消化的成本。对于一家种子轮的 AI 创业公司，这可能是致命的负担。对于大学实验室的开源项目，这根本不可能完成。

监管经济学中有一个经典概念叫"监管俘获"（regulatory capture）：当行业巨头参与制定监管规则时，规则往往有利于巨头、不利于新进入者。Anthropic 的游说行为符合这个模式。

**对开源的选择性敌意。** Anthropic 反复强调开源大模型的风险：可以微调去除安全限制，可以用于生成有害内容。这些风险确实存在。但他们很少提到另一面：开源允许独立研究者审计模型行为、发现偏见、验证安全声明。闭源模型的安全性完全依赖厂商的自我报告——而企业的自我报告从来不是可靠的信息来源。

Meta 的 Llama 系列是一个有说服力的案例。Oligo Security 的研究团队在 Llama Stack 中发现了一个 CVSS 9.3 分的严重远程代码执行漏洞（CVE-2024-50050），Meta 在收到报告后迅速修复[^9]。Trendyol 的安全团队也发现了 Llama Firewall 可被提示注入绕过的问题[^10]。这些发现之所以成为可能，正是因为代码开放。闭源模型中同样可能存在类似漏洞，但没有人有机会发现它们。

Anthropic 对开源的态度，与其说基于安全判断，不如说基于商业判断：开源模型的能力提升直接侵蚀 Claude API 的付费市场。

---

## 四、Constitutional AI：技术包装下的权力问题

Constitutional AI 是 Anthropic 最具标志性的技术贡献。核心思路是：给 AI 一套行为准则（"宪法"），让 AI 在生成回复时自我审查，拒绝违反准则的请求。

作为技术方法，它有真实的贡献——比纯人工标注更可扩展，比硬编码规则更灵活。

但 Anthropic 很少讨论这项技术背后的权力问题。

**谁来制宪？** Claude 的"宪法"由 Anthropic 内部制定。一家美国硅谷公司的价值观，通过这部"宪法"被嵌入到一个全球用户使用的 AI 系统中。这些准则反映的是哪种文化的道德标准？考虑了哪些群体的利益？排斥了哪些观点？这些问题没有公开的讨论过程，没有广泛的外部参与，没有民主程序。

Anthropic 在 2023 年与 Collective Intelligence Project 合作，通过 Polis 平台招募了约一千名美国用户参与"宪法"条款的讨论，参与者贡献了 1,117 条声明并投出超过 38,000 票[^11]。这是一个有意义的实验，但规模和代表性远远不够——尤其考虑到 Claude 的用户遍布全球，一千名美国参与者无法代表全球用户的价值观。

**"安全"的定义权就是权力。** 决定 AI 可以说什么、不可以说什么，本质上是一种审查权。当 Claude 拒绝回答一个关于争议话题的问题时，这个"拒绝"反映的不是客观的安全标准，而是 Anthropic 的主观判断。把这种判断包装成"安全"，让它看起来像技术决策而非价值决策，这本身就是一种权力运作。

---

## 五、恐慌经济学：末日叙事的商业价值

Anthropic 的高管频繁在公开场合讨论 AI 的"存在性风险"——即 AI 可能从根本上威胁人类文明的延续。

对存在性风险的研究是严肃的学术领域。但当这种讨论从学术期刊转移到商业公司的公关策略中，性质就变了。

**Dario Amodei 的实际表述。** 需要准确还原他说了什么。在 2026 年 1 月发表的文章《The Adolescence of Technology》中，Amodei 写道：AI 的某些行为"将具有破坏性或威胁性，先是对个体层面的小规模伤害，然后随着模型能力增强，可能最终威胁到整个人类"；他还说"智能、自主性、连贯性与低可控性的组合，既是可能出现的，也是存在性危险的配方"[^12]。他估计 AI 造成灾难性后果的概率在 10%–25% 之间[^13]。他没有说过"AI 将在两年内消灭人类"这样的话——但他的措辞确实在有意营造紧迫感。

**末日叙事的商业逻辑。** 如果 AI 只是一种有用但有缺陷的工具，那 AI 安全研究就是一个重要但普通的工程问题。但如果 AI 可能"毁灭人类文明"，那 AI 安全研究就是拯救世界的伟大事业——而从事这项事业的公司，就值得社会给予特殊的信任、资源和监管豁免。

末日叙事抬高了 Anthropic 的道德地位，使其从一家普通的 AI 公司变成了"人类安全的守护者"。这个身份价值连城。

**被挤出的真实风险。** 当公共讨论被末日叙事占据时，那些当下已经在发生的 AI 危害反而得不到足够关注：算法偏见对少数群体的系统性歧视、AI 生成虚假信息对选举和舆论的干扰、自动化对底层劳动者的替代、训练数据对创作者版权的大规模侵犯。

这些问题不够耸动、不够"科幻"，但它们正在真实地伤害真实的人。解决这些问题不需要数百亿融资，不需要一家商业公司充当救世主——它们需要的是立法、监管、劳动保护和版权改革。

当末日叙事占据了最多的媒体版面和政策讨论空间，这些现实问题获得的关注难免被稀释——不是因为有人刻意压制，而是因为公共注意力本身就是稀缺资源。

---

## 六、数据与劳工：安全叙事照不到的角落

Anthropic 的安全叙事聚焦于模型的输出行为——它会不会说危险的话、会不会帮人做坏事。但在这套叙事的灯光照不到的地方，同样有值得审视的问题。

**训练数据的来源。** 和所有大型语言模型公司一样，Anthropic 对训练数据的具体来源讳莫如深。Claude 的训练语料几乎必然包含大量受版权保护的内容——书籍、新闻报道、学术论文、开源代码、个人博客。这些内容的创作者既没有被告知，也没有获得补偿。一家以"道德"为招牌的公司，在知识产权问题上选择了和行业内所有人一样的沉默。

**标注劳工的处境。** RLHF（基于人类反馈的强化学习）是 Claude 安全对齐的关键环节。这项工作需要大量人类标注员阅读并评判 AI 的输出，其中包括暴力、仇恨言论、色情等有害材料。这类标注工作在行业中普遍外包到低收入国家，薪酬微薄，心理支持匮乏。

Time 杂志记者 Billy Perrigo 在 2023 年 1 月发表的调查报道揭露了 OpenAI 通过外包公司 Sama 雇佣肯尼亚标注工人的情况——时薪在 1.32 至 2 美元之间，工人每天需要阅读 150 至 250 段包含儿童性虐待、谋杀、自残等内容的文本，多名工人表示遭受了严重的心理创伤[^14]。Anthropic 使用同样的 RLHF 技术路线，但关于其标注劳工的待遇和工作条件，公开信息极其有限。一家以"安全"和"公益"为招牌的公司，在供应链劳工问题上的沉默，本身就说明了"安全"这个词的边界被划在了哪里。

---

## 七、ClaudeBot 爬虫：嘴上讲规矩，手上没规矩

安全叙事要求别人守规矩，但 Anthropic 自己守不守？

**Reddit 诉讼。** 2025 年 6 月 4 日，Reddit 在旧金山高等法院对 Anthropic 提起诉讼，索赔 10 亿美元。诉状指出：Reddit 在 2024 年 5 月之前的 robots.txt 中已明确声明该文件"适用于搜索引擎"而非商业爬虫；Anthropic 发言人曾在 2024 年 7 月声称"Reddit 自 5 月中旬以来一直在我们的爬取屏蔽名单上"，但 Reddit 的审计日志显示，此后数月内 Anthropic 的机器人仍访问了平台超过 10 万次[^15]。

**iFixit 事件。** iFixit CEO Kyle Wiens 公开指出，ClaudeBot 在 24 小时内访问了 iFixit 服务器约一百万次。iFixit 的服务条款明确禁止"未经书面许可将网站内容用于训练机器学习或人工智能模型"[^16]。Freelancer CEO Matt Barrie 也表示 ClaudeBot 是"目前最激进的爬虫"，其网站在 4 小时内被访问了 350 万次[^17]。

这件事的讽刺之处在于：一家要求整个行业遵守安全规范的公司，自己连互联网最基本的君子协定——robots.txt——都不遵守。如果你连网站所有者明确说"不要爬我"都做不到尊重，你凭什么让别人相信你会尊重更复杂的安全承诺？

---

## 八、知识产权双标：我的代码碰不得，你的代码随便用

2026 年 3 月，Claude Code 的完整源码（约 51.2 万行 TypeScript 代码）因 npm 包的发布打包错误而泄露——一个未混淆的 source map 文件指向了 Anthropic 在 Cloudflare R2 上存储的 zip 归档。Anthropic 承认这是人为失误导致的打包问题[^18]。

泄露发生后，Anthropic 迅速对 GitHub 上的镜像仓库发起 DMCA 下架请求[^19]。

DMCA 维权本身合法。问题在于另一面：Anthropic 训练 Claude 的时候，用没用过开源社区的代码？几乎可以肯定用了——所有大型语言模型的训练语料都包含大量 GitHub 上的开源代码。但 Anthropic 的训练数据是不公开的，所以没有人能确认具体用了什么、用了多少。

于是标准变成了这样：Anthropic 可以用开源社区的代码训练商业模型，不告知、不署名、不付费；但开源社区不能参考 Anthropic 的代码，否则就是侵权。

这不是法律问题——在现行法律框架下，Anthropic 的做法可能完全合法。这是一个道德问题：一家以"公益"和"道德"自居的公司，在知识产权上采取了最大限度利己的立场。法律允许的事情，不等于一家"公益公司"应该做的事情。

---

## 九、封号与锁区：平台的权力，用户的代价

如果说前面的问题还比较抽象，Anthropic 对用户的直接管控则更加具体。

**地缘封锁。** 2025 年 9 月 5 日，Anthropic 宣布禁止"中国控制的实体"使用 Claude 服务，适用 50% 股权规则——不论公司注册在哪个国家，只要超过半数股权被中国实体直接或间接控制，就被排除在外。该政策覆盖所有 Claude 模型及开发者工具，字节跳动、腾讯、阿里巴巴及其海外子公司均受影响。Anthropic 承认此举将导致"数亿美元的低位"营收损失[^20]。地缘政治合规是现实，但这条政策的执行方式——单方面宣布、全球适用——暴露了平台对用户的绝对权力。

**封禁第三方工具。** 2026 年 1 月 9 日，Anthropic 部署了服务端检测机制，阻止所有第三方工具通过 Claude Pro/Max 订阅的 OAuth 令牌进行身份验证。OpenCode（GitHub 星标超过 5.6 万）、Clawdbot 等工具一夜之间停止工作[^21]。Anthropic 的解释是防止第三方工具伪装成官方客户端 Claude Code 以获取更优惠的定价和更高的限额[^22]。但对付费用户来说，结果就是：你花的钱只能按照 Anthropic 规定的方式使用。

**账号封禁的不透明。** 多名用户在 Hacker News 等社区反映遭遇账号无预警封禁，申诉流程不透明——客服无法确认封禁原因，也无法直接解除封禁，所有申诉需通过表单提交，后续可能不会收到回复[^23]。

这些做法单独看，每一条都可以找到商业或合规上的理由。但它们合在一起呈现出一个清晰的模式：用户在 Anthropic 的生态中没有议价能力。平台可以随时改变规则、收回权限、终止服务，用户除了接受别无选择。

一家把"为人类服务"写进公司使命的公司，在对待自己用户时，展现的是最标准的平台霸权逻辑。

---

## 十、闭源悖论：你无法验证的安全承诺

这或许是最根本的矛盾。

Anthropic 要求公众信任他们的安全工作，但同时拒绝提供验证这种信任所需的透明度。

Claude 的模型权重是闭源的。训练数据组成是不公开的。安全评估的完整结果是内部的。对齐过程的细节是保密的。

Anthropic 发布了一些安全研究论文和模型卡片，这值得肯定。但这些材料是公司自己选择性披露的——它们展示的是 Anthropic 希望你看到的部分，而不是全貌。

这就构成了一个结构性的悖论：Anthropic 说"请相信我们，Claude 是安全的"，但不允许任何人独立验证这个声明。

安全不能建立在信任之上，尤其不能建立在对一家商业公司的信任之上。安全需要建立在可验证的证据之上。科学研究的基本原则是可重复、可检验。Anthropic 的闭源模式，从结构上排除了独立验证的可能性。

一个不可验证的安全承诺，和没有承诺之间，差距并不像看起来那么大。

---

## 结语

写这篇文章不是为了论证 Anthropic 是一家"邪恶"的公司。在 AI 行业中，它的安全研究有真实的技术贡献，Constitutional AI 推动了对齐技术的发展，它发表的论文确实有学术价值。

但 Anthropic 不是它声称的那个东西。

它不是一家把安全置于利润之上的公益机构——它是一家把安全作为核心品牌策略的商业公司。安全既是它真诚的技术追求，也是它精明的市场定位。这两者并不矛盾，但 Anthropic 只承认前者、回避后者。这种选择性的自我呈现，就是一种不诚实。

真正值得警惕的不是 Anthropic 的某个具体行为，而是一种正在成型的模式：一家商业公司，通过垄断"安全"的定义权和话语权，将自己置于行业的道德制高点，并利用这个位置影响监管、挤压竞争、聚拢资源。

安全应该是一种公共品，而不是某家公司的品牌资产。

当"安全"变成了一门生意，它保护的就不再是公众，而是生意本身。

---

## 参考来源

[^1]: [Dario Amodei - Wikipedia](https://en.wikipedia.org/wiki/Dario_Amodei)。Dario Amodei 于 2020 年 12 月离开 OpenAI，2021 年与 Daniela Amodei 等人创立 Anthropic。

[^2]: [Anthropic CEO Dario Amodei Says He Left OpenAI Over a Difference in 'Vision' - Inc.](https://www.inc.com/ben-sherry/anthropic-ceo-dario-amodei-says-he-left-openai-over-a-difference-in-vision/91018229)

[^3]: [OpenAI LP 公告 - OpenAI Blog, 2019年3月11日](https://openai.com/blog/openai-lp)。OpenAI 于 2019 年创建"有限营利"子公司 OpenAI LP，利润上限为投资额的 100 倍。

[^4]: [Timnit Gebru 事件报道 - MIT Technology Review](https://www.technologyreview.com/2020/12/04/1013294/google-ai-ethics-research-paper-forced-out-timnit-gebru/)；DAIR 官网：[dair-institute.org](https://dair-institute.org)

[^4a]: [Paul Christiano - Alignment Research Center](https://alignment.org/)。Christiano 于 2022 年离开 OpenAI，创办 ARC，专注于对齐研究，不发布商业产品。

[^5]: [Anthropic - Wikipedia](https://en.wikipedia.org/wiki/Anthropic)。Anthropic 在特拉华州注册为公益公司（PBC）。

[^6]: 亚马逊投资：2023 年 9 月首轮 40 亿美元，2024 年 3 月追加 40 亿美元。来源：[Amazon Press Release](https://press.aboutamazon.com/2023/9/amazon-and-anthropic-announce-strategic-collaboration)；[Bloomberg](https://www.bloomberg.com/news/articles/2024-03-27/amazon-to-invest-up-to-4-billion-more-in-anthropic)

[^7]: 谷歌累计投资约 20 亿美元。来源：[The Wall Street Journal](https://www.wsj.com/tech/ai/google-commits-2-billion-in-funding-to-ai-startup-anthropic-db4d4c50)

[^8]: [Anthropic's Responsible Scaling Policy](https://www.anthropic.com/index/anthropics-responsible-scaling-policy)

[^9]: [CVE-2024-50050: Critical Vulnerability in meta-llama - Oligo Security](https://www.oligo.security/blog/cve-2024-50050-critical-vulnerability-in-meta-llama-llama-stack)。CVSS 9.3 分，Meta 于 2024 年 10 月 10 日在 Llama Stack 0.0.41 版本中修复。

[^10]: [Meta's Llama Firewall Bypassed Using Prompt Injection Vulnerability - CybersecurityNews](https://cybersecuritynews.com/metas-llama-firewall/)

[^11]: [Collective Constitutional AI: Aligning a Language Model with Public Input - Anthropic](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input)；合作方为 Collective Intelligence Project，使用 Polis 平台。

[^12]: [The Adolescence of Technology - Dario Amodei, 2026年1月](https://www.darioamodei.com/essay/the-adolescence-of-technology)

[^13]: [Anthropic CEO Raises Alarm on 25% Risk of Catastrophic AI Developments - 多家媒体报道](https://censinet.com/perspectives/anthropic-ceo-raises-alarm-on-25-risk-of-catastrophic-ai-developments)

[^14]: [OpenAI Used Kenyan Workers on Less Than $2 Per Hour - TIME, 2023年1月](https://time.com/6247678/openai-chatgpt-kenya-workers/)。记者 Billy Perrigo 的调查报道，涉及外包公司 Sama，工人时薪 $1.32–$2。

[^15]: [Reddit Sues Anthropic for $1B - 多家媒体报道, 2025年6月](https://www.theregister.com/2025/06/05/reddit_sues_anthropic_over_ai/)；[ppc.land 详细报道](https://ppc.land/reddit-files-lawsuit-against-anthropic-over-unauthorized-claude-ai-training/)

[^16]: [Anthropic AI Scraper Hits iFixit's Website a Million Times in a Day - 404 Media](https://www.404media.co/anthropic-ai-scraper-hits-ifixits-website-a-million-times-in-a-day/)；[PC Gamer 报道](https://www.pcgamer.com/software/ai/ifixit-ceo-takes-shots-at-anthropic-for-hitting-our-servers-a-million-times-in-24-hours-and-even-the-ai-companys-own-chatbot-disapproves/)

[^17]: [Websites accuse AI startup Anthropic of bypassing their anti-scraping rules - Engadget](https://www.engadget.com/websites-accuse-ai-startup-anthropic-of-bypassing-their-anti-scraping-rules-and-protocol-133022756.html)

[^18]: [Claude Code's source code appears to have leaked - VentureBeat, 2026年3月](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know)；[The Register](https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/)；[Fortune](https://fortune.com/2026/03/31/anthropic-source-code-claude-code-data-leak-second-security-lapse-days-after-accidentally-revealing-mythos/)

[^19]: [Anthropic Accidentally Leaked Claude Code's Source—The Internet Is Keeping It Forever - Decrypt](https://decrypt.co/362917/anthropic-accidentally-leaked-claude-code-source-internet-keeping-forever)

[^20]: [Anthropic blocks Chinese-controlled firms from Claude AI - Bloomberg, 2025年9月5日](https://www.bloomberg.com/news/articles/2025-09-05/anthropic-clamps-down-on-ai-services-for-chinese-owned-firms)；[Anthropic 官方公告](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)；[Tom's Hardware 报道](https://www.tomshardware.com/tech-industry/anthropic-blocks-chinese-firms-from-claude)

[^21]: [Anthropic cracks down on unauthorized Claude usage by third-party harnesses - VentureBeat, 2026年1月](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses)

[^22]: [Anthropic clarifies ban on third-party tool access to Claude - The Register, 2026年2月](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/)；[Techmeme 汇总](https://www.techmeme.com/260109/p25)

[^23]: [Ask HN: Anthropic account suspended, anyone reinstated? - Hacker News](https://news.ycombinator.com/item?id=47286867)；[Dev Genius: You might be breaking Claude's ToS without knowing it](https://blog.devgenius.io/you-might-be-breaking-claudes-tos-without-knowing-it-228fcecc168c)
---
name: watch-video
description: Use when the user wants Codex to watch, inspect, understand, summarize, or learn from a video file or video link, including MP4 files, webpages, Douyin/TikTok links, course clips, screen recordings, generated videos, and talking-head videos. Use for evidence-based learning notes, timelines, viewpoint extraction, credibility judgment, insights, and action suggestions. Do not use for requests to replicate, imitate, storyboard, or reverse-engineer a video's creative structure; use video-replication-breakdown instead.
---

# 看视频

## 目标

让 Codex 尽可能接近“真的看完视频后再分析”，而不是只凭标题、封面、网页文字或单张截图猜测。

这个 Skill 专门负责“看懂总结”：看清画面、听懂口播、拆解观点、判断可信度，并把对用户有用的东西沉淀成可行动的学习结论。

默认使用中文输出，除非用户明确要求其他语言。

## 边界

- 用户想知道“讲了什么、靠谱吗、对我有什么启发、我该怎么做”时，使用本 Skill。
- 用户想“拆解、复刻、模仿、分镜、怎么拍、爆款结构、创作参考、生成脚本或提示词”时，不要把任务塞进本 Skill，改用 `video-replication-breakdown`。
- 本 Skill 不默认生成 HTML 复刻报告，不默认输出拍摄脚本、镜头功能表或仿拍提示词。
- 可以指出视频是否“值得另开复刻拆解”，但不要在学习总结任务里展开复刻工作。

## 核心原则

- 先证明是否真的看到了/听到了视频，再做总结和判断。
- 不要把页面文字、标题、评论区或封面当成视频主体内容。
- 不要把背景音乐或环境音错误当成口播。
- 单张截图不等于看完整视频；至少结合关键帧、时间线、动态复核或转写。
- 视频分析不能停留在“讲了什么”，还要回答“这是什么意思、靠不靠谱、对用户有什么启发、用户该做什么”。
- 如果网站阻止播放、需要登录、出现验证码、媒体流不可访问或转写失败，要明确说明边界，不要假装看过。
- 默认先把完整材料放进 `00_工作台`；未经用户确认，不要写入 `01_成长笔记`。

## 默认流程

### 执行 checklist

每次视频分析都按这个顺序推进，不要跳步：

- [ ] 运行 `python scripts/check_capabilities.py`，记录当前能力等级。
- [ ] 根据输入类型选择默认路径：本地视频走 `media_probe.py`，网页视频走 `browser_watch_url.cjs`。
- [ ] 生成或收集观看证据：媒体信息、关键帧、联系图、音频、转写。
- [ ] 对照 `references/evidence-checklist.md` 判断证据是否足够。
- [ ] 深度分析时使用 `references/analysis-template.md`。
- [ ] 交付前用 `references/quality-rubric.md` 自评；有 0 分项时先补证据或说明降级。
- [ ] 最终回答必须区分“已确认”“推断”“未确认”。

1. **确认输入类型**
   - 先运行能力体检：`python scripts/check_capabilities.py`。
   - 如果能力不是 `full`，先向用户报告缺什么、有什么影响、怎么补；不要直接假装能完整观看。
   - 本地视频文件：用 FFprobe 读取时长、编码、分辨率、音轨。
   - 网页/短视频链接：用真实浏览器打开，确认是否出现 `<video>` 元素并能播放。
   - 抖音/图文作品：如果没有 `<video>` 但页面暴露图片数组，要按图文作品处理，提取全部图文帧，不要误判为口播视频。
   - 只有截图、封面或文字：说明只能做静态图/文本分析，不能声称看过完整视频。

2. **证明观看状态**
   - 记录标题、最终 URL、时长、分辨率、音轨状态。
   - 对网页视频保存播放前截图和多个时间点截图。
   - 对本地视频生成 contact sheet，并按需要抽取关键帧和音频。
   - 对图文作品保存结构化元数据、全部图片帧和联系图。

3. **提取内容证据**
   - 用 FFmpeg 抽帧或生成 contact sheet。
   - 如果有口播，用 `scripts/video_transcribe.py` 转写为 JSON、SRT、TXT。
   - 如果 ASR 输出少、置信度低、或内容明显是音乐/环境声，标注转写不适合作为主要依据。
   - 必要时多轮复核关键时间点，尤其是字幕、图表、屏幕录制、产品演示和人物口播。

4. **做高级视频理解**
   - 按时间线概述视频发生了什么：画面、字幕、口播、动作和场景变化。
   - 提炼核心主张：博主到底在说什么，想让观众相信什么。
   - 拆解论证结构：用了哪些例子、对比、因果链、预测、情绪钩子或销售话术。
   - 判断可信度：哪些有证据，哪些只是观点、预测、夸张表达或营销包装。
   - 提炼启发：对用户当前业务、技能、内容生产、AI 工具链或资产沉淀有什么意义。
   - 给出行动建议：下一步做什么、怎么验证、是否值得进入正式笔记或另开复刻拆解。

5. **交付结果**
   - 明确说“实际看到了什么”和“没有确认什么”。
   - 链接到关键帧、contact sheet、转写、检查 JSON 等本地证据文件。
   - 在对话里先给核心结论，再把完整 Markdown 学习草稿放到 `00_工作台/<日期>_<视频主题>/`。
   - 如果要归档成知识资产，可与 `douyin-video-analyst` 联用；但本 Skill 自身也必须能完成视频学习分析。
   - 不要自动写入 `01_成长笔记`，除非用户明确确认。

## 推荐输出结构

短任务可以直接回答。深度视频分析必须读取 `references/analysis-template.md`，并至少覆盖：

- 观看状态：已播放 / 只打开页面 / 被拦截 / 只能静态分析。
- 证据摘要：时长、分辨率、音轨、关键帧、转写文件。
- 时间线概览：按时间点说明视频内容。
- 博主观点：视频真正想表达的 1-3 个核心意思。
- 论证拆解：观点如何被包装、证明或推动。
- 可信度判断：哪些可信、哪些需要验证、哪些可能是营销或情绪化表达。
- 对你的启发：结合用户正在做的 AI、视频、外贸、Skill、知识库等方向。
- 你应该做什么：具体到下一步行动、文档、实验、产品化或自动化。
- 是否值得归档：是否建议进入 `01_成长笔记`，以及建议分类。
- 是否值得另开复刻拆解：只给判断，不在本 Skill 内展开复刻报告。
- 不确定性：没有看清、没听清、被平台限制或需要人工确认的部分。

## 脚本

- `scripts/check_capabilities.py`：检查当前电脑距离 `full` 视频分析能力还缺什么。
- `scripts/setup_full.py`：尽量自动安装本地 Python/Node/Playwright 依赖；系统软件和 Codex 插件需要用户确认。
- `scripts/browser_watch_url.cjs`：用 Chrome/Playwright 打开网页链接、尝试播放视频、保存页面信息和关键帧。
- `scripts/media_probe.py`：读取本地或远程媒体信息，生成联系图和音频文件。
- `scripts/video_transcribe.py`：用 faster-whisper 转写音频，输出 JSON、SRT、TXT。

本地环境支持脚本时优先使用脚本；不支持时仍要遵守“证据优先、诚实说明边界、分析必须可追溯”的流程。

## Gotchas

- 安装 GitHub Skill 不会自动安装 Codex Browser 插件；插件缺失时只能用脚本和文件证据替代。
- 能打开网页不等于视频真的播放了；必须确认 `<video>`、播放状态、时间点截图或媒体流。
- 页面标题、评论、封面、推荐文案不能当成视频主体内容。
- 单张截图不等于看完整视频；至少需要多时间点关键帧或联系图。
- 有背景音乐不等于有口播；转写为空或低质量时要标注“不能依据口播分析”。
- 网页视频常被登录、验证码、地区、反爬或试看限制拦截；遇到限制必须说明边界。
- Playwright 安装成功不代表系统 Chrome 存在；脚本会优先找 Chrome/Edge，找不到再用 Playwright Chromium。
- 不到 `full` 也可以工作，但必须说清降级影响，不能声称“完整看完并听懂”。

## 能力升级规则

目标是把对方电脑拉到 `full`，但必须分清哪些能自动装、哪些需要用户确认：

- 可以自动或半自动安装：`requirements.txt`、`package.json`、Playwright Chromium。
- 需要系统安装或用户确认：FFmpeg、Chrome/Edge、GPU 驱动。
- 不能由 GitHub Skill 静默安装：Codex Browser 插件、其他 Codex 插件或用户账号级连接器。

当用户说“帮我把这个 Skill 装到最好”时：

1. 运行 `python scripts/check_capabilities.py`。
2. 如果缺本地依赖，建议运行 `python scripts/setup_full.py`。
3. 如果缺 FFmpeg/Chrome/Codex Browser 插件，给出具体安装步骤。
4. 每补一项后重新运行体检。
5. 只有达到 `full` 或用户接受降级后，才开始深度分析视频。

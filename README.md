# 看懂视频 Skill

让 Codex 更可靠地“看懂视频”：打开网页视频、读取本地视频、抽关键帧、提取音频、转写口播，并基于证据做时间线分析、观点拆解、可信度判断和行动建议。

这个 Skill 只负责“看懂总结”。它告诉你视频讲了什么、是否靠谱、对你有什么启发、你下一步应该怎么做。它不负责复刻、仿拍、分镜、镜头功能表、HTML 创作报告或爆款结构反向工程；这些需求请安装并使用 `video-replication-breakdown`。

## 下载后第一步

安装 Skill 后先重启 Codex，然后在 Skill 目录运行：

```bash
python scripts/check_capabilities.py
```

它会告诉你当前电脑处于哪一个等级：

- `minimal`：只能做静态或文本级分析，不能声称完整看过视频。
- `recommended`：能用 FFmpeg/ffprobe 读取视频、抽帧、提取音频、生成联系图。
- `full`：能真实打开网页视频、抽帧、转写口播、生成时间线证据，并做动态复核。

## 一步步升级到 full

先运行自动安装脚本：

```bash
python scripts/setup_full.py
```

它会安装能自动装的本地依赖：

- Python 依赖：`faster-whisper`
- Node 依赖：`playwright`
- Playwright Chromium 浏览器

它不会静默安装系统软件或 Codex 插件。缺这些时，它会明确告诉你怎么补：

- FFmpeg / ffprobe
- Chrome / Edge
- Codex Browser 插件
- 其他视频理解或转写相关 Skill

每补完一项，重新运行：

```bash
python scripts/check_capabilities.py
```

直到达到 `full`，或者明确知道还差哪一项。

## 给同事的 setup prompt

可以让同事复制这段给 Codex：

```text
请帮我安装并升级 watch-video-skill 到 full 能力。先运行 scripts/check_capabilities.py，告诉我这台电脑缺什么；能自动安装的依赖请运行 scripts/setup_full.py；不能自动装的系统软件或 Codex 插件，请一步步引导我安装。每完成一步都重新检测，直到达到 full 或明确说明还差什么。
```

## 适合什么时候用

- 你发来一个视频链接，说“帮我看一下这个视频”。
- 你发来本地 MP4、录屏、课程片段、网页视频、短视频链接。
- 你希望 Codex 像人一样先看完，再总结、拆解、判断和给建议。
- 你想把刷到的干货视频变成结构化学习资产。
- 你想知道“这个视频讲了什么、靠不靠谱、我该怎么做”。

不适合：

- “拆解这个视频让我复刻。”
- “帮我提取分镜、脚本、提示词。”
- “这个爆款视频怎么拍出来？”

这些问题属于 `video-replication-breakdown`。

## 能做什么

- 真实打开视频链接或读取本地视频文件。
- 确认视频是否真的播放。
- 读取时长、分辨率、音轨等媒体信息。
- 抽取关键帧，生成整段联系图。
- 提取音频并进行口播转写。
- 按时间线说明视频讲了什么。
- 拆解博主观点、论证方式、可信度和潜在营销话术。
- 结合你的业务和学习目标，提炼启发和下一步行动。
- 默认输出聊天核心结论和 `00_工作台` Markdown 学习草稿。

## 和其他视频 Skill 的关系

`watch-video` 是“学习理解”：负责真实观看、抽帧、转写、证据和通用分析。

`douyin-video-analyst` 是“抖音学习资产分析师”：更偏向把短视频内容沉淀成学习文档、选题、项目、Skill 和行动计划。

`video-replication-breakdown` 是“视频复刻拆解”：当目标不是学习总结，而是拆出分镜、节奏、风格、复刻脚本和 HTML 案例资产时使用。

## 安装

在另一台电脑上通过 skill-installer 安装：

```text
https://github.com/huojiaheng123-cpu/watch-video-skill
```

完整迁移说明见 [install.md](install.md)。

如果你也想获得“复刻拆解”能力，再安装：

```text
https://github.com/huojiaheng123-cpu/video-replication-breakdown-skill
```

## 主要文件

- `SKILL.md`：Skill 工作流程。
- `install.md`：从新电脑升级到 full 的完整说明。
- `requirements.txt`：Python 依赖。
- `package.json`：Node / Playwright 依赖。
- `scripts/check_capabilities.py`：能力体检脚本。
- `scripts/setup_full.py`：本地依赖安装向导。
- `scripts/browser_watch_url.cjs`：网页视频真实播放检查。
- `scripts/media_probe.py`：媒体信息、联系图、音频提取。
- `scripts/video_transcribe.py`：faster-whisper 口播转写。
- `references/evidence-checklist.md`：视频观看证据清单。
- `references/analysis-template.md`：深度分析模板。
- `references/quality-rubric.md`：交付前质量自评。

## 使用示例

```text
帮我看这个视频，告诉我博主讲的是什么意思，对我有什么启发，我应该做什么。
```

Codex 应该先确认是否真的能播放或读取视频，再基于关键帧、图文帧、转写和媒体信息给出结构化学习分析；不应该生成复刻拆解或 HTML 案例报告。

# watch-video Skill

让 Codex 更可靠地“看视频”：打开网页视频、读取本地视频、抽关键帧、提取音频、转写口播，并基于证据做时间线分析、观点拆解、可信度判断和行动建议。

这个 skill 的重点不是一下载就保证满血，而是 **下载后先自检，再一步步把当前电脑升级到 full 能力**。

## 下载后第一步

安装 skill 后先重启 Codex，然后在 skill 目录运行：

```bash
python scripts/check_capabilities.py
```

它会告诉你当前电脑处于哪个等级：

- `minimal`：只能做静态或文本级分析，不能声称完整看过视频。
- `recommended`：能用 FFmpeg/ffprobe 读取视频、抽帧、提取音频、生成联系图。
- `full`：能真实打开网页视频、抽帧、转写口播、生成时间线证据，并做动态复查。

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
- 其他视频理解或转写相关 skill

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

## 能做什么

- 真实打开视频链接或读取本地视频文件。
- 确认视频是否真的播放。
- 读取时长、分辨率、音轨等媒体信息。
- 抽取关键帧，生成整段联系图。
- 提取音频并进行口播转写。
- 按时间线说明视频讲了什么。
- 拆解博主观点、论证方式、可信度和潜在营销话术。
- 结合你的业务和学习目标，提炼启发和下一步行动。
- 输出可沉淀为文档、脚本、服务、skill 或项目案例的资产。

## 安装

在另一台电脑上通过 skill-installer 安装：

```text
https://github.com/huojiaheng123-cpu/watch-video-skill
```

完整迁移说明见 [install.md](install.md)。

## 主要文件

- `SKILL.md`：skill 工作流程。
- `install.md`：从新电脑升级到 full 的完整说明。
- `requirements.txt`：Python 依赖。
- `package.json`：Node / Playwright 依赖。
- `scripts/check_capabilities.py`：能力体检脚本。
- `scripts/setup_full.py`：本地依赖安装向导。
- `scripts/browser_watch_url.cjs`：网页视频真实播放检查。
- `scripts/media_probe.py`：媒体信息、联系图、音频提取。
- `scripts/video_transcribe.py`：faster-whisper 口播转写。
- `references/evidence-checklist.md`：视频观看证据清单。

## 使用示例

```text
帮我看这个视频，告诉我博主讲的是什么意思，对我有什么启发，我应该做什么。
```

Codex 应该先确认当前能力等级，再基于关键帧、转写和媒体信息给出结构化分析。能力不足时，必须说明边界，不能假装完整看过视频。

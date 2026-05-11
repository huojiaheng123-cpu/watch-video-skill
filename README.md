# 看视频 Skill

这是一个通用 Codex skill，用来让 Codex 更可靠地观看和分析视频，而不是只凭封面、标题、网页文字或单张截图猜测。

它的职责不是“普通看一下”，而是尽量做到：

- 真实打开视频链接或读取本地视频文件。
- 确认视频是否真的播放。
- 读取时长、分辨率、音轨等媒体信息。
- 抽取关键帧、生成整段联系图。
- 提取音频并进行口播转写。
- 按时间线说明视频讲了什么。
- 拆解博主观点、论证方式、可信度和潜在营销话术。
- 结合你的业务和学习目标，提炼启发和下一步行动。
- 输出可沉淀为文档、脚本、服务、skill 或项目案例的资产。

## 适合什么时候用

- 你发来一个视频链接，说“帮我看一下这个视频”。
- 你发来本地 MP4、录屏、课程片段、网页视频、短视频链接。
- 你希望 Codex 像人一样先看完，再总结、拆解、判断和给建议。
- 你想把刷到的干货视频变成结构化学习资产。

## 和抖音视频分析 Skill 的关系

`watch-video` 是“高级看视频能力”：负责真实观看、抽帧、转写、证据和通用分析。

`douyin-video-analyst` 是“抖音学习资产分析师”：更偏向把短视频内容沉淀成学习文档、选题、项目、skill 和行动计划。

两者可以配合使用：先用 `watch-video` 确认和拆解视频，再用 `douyin-video-analyst` 做知识资产归档。对于普通视频分析，`watch-video` 自身也应能直接输出完整分析。

## 主要文件

- `SKILL.md`：skill 使用说明。
- `scripts/browser_watch_url.cjs`：网页视频真实播放检查。
- `scripts/media_probe.py`：媒体信息、联系图、音频提取。
- `scripts/video_transcribe.py`：faster-whisper 口播转写。
- `references/evidence-checklist.md`：视频观看证据清单。

## 安装

在另一台电脑上通过 skill-installer 安装：

```text
https://github.com/huojiaheng123-cpu/watch-video-skill
```

安装后重启 Codex，然后先做能力体检：

```bash
python scripts/check_capabilities.py
```

如果要把环境尽量升级到 full：

```bash
python scripts/setup_full.py
```

这个脚本会安装本地 Python/Node/Playwright 依赖，但不会静默安装系统软件或 Codex 插件。缺 FFmpeg、Chrome/Edge、Codex Browser 插件时，它会告诉你缺什么、有什么用、下一步怎么装。

更完整的迁移说明见 [`install.md`](install.md)。

## 能力等级

- `minimal`：只能做静态或文本级分析，不能声称完整看过视频。
- `recommended`：能用 FFmpeg/ffprobe 读取视频、抽帧、提取音频、生成联系图。
- `full`：能真实打开网页视频、抽帧、转写口播、生成时间线证据，并做动态复查。

## 使用示例

```text
帮我看这个视频，告诉我博主讲的是什么意思，对我有什么启发，我应该做什么。
```

Codex 应该先确认是否真的能播放视频，再基于关键帧、转写和媒体信息给出结构化分析。

## 给同事的 setup prompt

可以让同事复制这段给 Codex：

```text
请帮我安装并升级 watch-video-skill 到 full 能力。先运行 scripts/check_capabilities.py，告诉我这台电脑缺什么；能自动安装的依赖请运行 scripts/setup_full.py；不能自动装的系统软件或 Codex 插件，请一步步引导我安装。每完成一步都重新检测，直到达到 full 或明确说明还差什么。
```

# watch-video 安装与 full 能力升级

这个 skill 的目标不是“复制文件后立刻满血”，而是让 Codex 能根据当前电脑自适应检查缺口，并一步步把环境拉到 `full`。

## 能力等级

- `minimal`：只能做静态/文本级分析，不能声称完整看过视频。
- `recommended`：有 FFmpeg/ffprobe，能读取本地视频、抽帧、提取音频和生成联系图。
- `full`：有 FFmpeg/ffprobe、Playwright/浏览器、本地转写能力，并且 Codex 可使用浏览器/媒体预览能力做动态复查。

## 第一步：运行体检

在 skill 目录运行：

```bash
python scripts/check_capabilities.py
```

如果当前电脑没有 `python` 命令，可以试：

```bash
py scripts/check_capabilities.py
python3 scripts/check_capabilities.py
```

## 第二步：自动安装本地依赖

这一步会安装 Python/Node 项目依赖和 Playwright Chromium：

```bash
python scripts/setup_full.py
```

它不会静默安装系统软件或 Codex 插件。系统级项目需要用户确认后安装。

## 第三步：补系统能力

### FFmpeg / ffprobe

Windows：

```powershell
winget install Gyan.FFmpeg
```

macOS：

```bash
brew install ffmpeg
```

装完后重开终端，再运行：

```bash
ffmpeg -version
ffprobe -version
python scripts/check_capabilities.py
```

### Chrome / Edge / Playwright 浏览器

推荐安装 Chrome 或 Edge。没有系统浏览器时，运行：

```bash
npx playwright install chromium
```

### faster-whisper

```bash
python -m pip install -r requirements.txt
```

第一次转写可能会下载模型。CPU 可以用，但较慢；有 NVIDIA GPU 时效果更好。

## 第四步：补 Codex 插件能力

GitHub skill 不能静默安装 Codex 插件。需要在 Codex 中启用或安装：

- Browser / browser-use：用于真实打开网页、播放视频、截图复查。
- 可选 video-understand / audio-transcribe 类 skill：用于本地视频理解和转写辅助。

安装或启用后重启 Codex。

## full 前的使用边界

如果 `check_capabilities.py` 仍不是 `full`，Codex 必须明确说明当前边界：

- 缺 FFmpeg：不能可靠抽帧、提取音频或生成联系图。
- 缺 Playwright/浏览器：不能确认网页视频真实播放。
- 缺 faster-whisper：不能本地转写口播。
- 缺 Codex Browser 插件：不能直接在 Codex 里动态预览网页/视频。

不要在能力不足时声称“完整看完了视频”。

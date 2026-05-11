const fs = require("fs/promises");
const path = require("path");
const { chromium } = require("playwright");

function safeName(value) {
  return String(value || "video")
    .replace(/[^\w.-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80);
}

async function main() {
  const inputUrl = process.argv[2];
  if (!inputUrl) {
    throw new Error("Usage: node browser_watch_url.cjs <url> [slug]");
  }

  const slug = safeName(process.argv[3] || "video");
  const outDir = path.join(process.cwd(), "video-watch-output", slug);
  await fs.mkdir(outDir, { recursive: true });

  const browser = await chromium.launch({
    executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    headless: true,
    args: [
      "--disable-blink-features=AutomationControlled",
      "--no-sandbox",
      "--autoplay-policy=no-user-gesture-required",
    ],
  });

  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    locale: "zh-CN",
    timezoneId: "Asia/Shanghai",
    userAgent:
      "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
  });

  const page = await context.newPage();
  const responses = [];
  const failedRequests = [];
  page.on("response", (response) => {
    const contentType = response.headers()["content-type"] || "";
    if (/video|audio|mpegurl|json|html/.test(contentType)) {
      responses.push({
        status: response.status(),
        url: response.url().slice(0, 1000),
        contentType,
      });
    }
  });
  page.on("requestfailed", (request) => {
    failedRequests.push({
      url: request.url().slice(0, 1000),
      failure: request.failure()?.errorText || "",
    });
  });

  let navError = null;
  try {
    await page.goto(inputUrl, { waitUntil: "domcontentloaded", timeout: 45000 });
  } catch (error) {
    navError = error.message;
  }

  await page.waitForTimeout(8000);
  await page.screenshot({ path: path.join(outDir, "before-play.png"), fullPage: true });

  try {
    await page.mouse.click(195, 430);
  } catch {}

  const playResult = await page.evaluate(async () => {
    const video = document.querySelector("video");
    if (!video) return { ok: false, reason: "no video element" };
    video.playsInline = true;
    try {
      await video.play();
      return { ok: true, paused: video.paused, readyState: video.readyState };
    } catch (error) {
      video.muted = true;
      await video.play().catch(() => {});
      return { ok: false, error: error.message, paused: video.paused, readyState: video.readyState };
    }
  });

  await page.waitForTimeout(2500);
  const info = await page.evaluate(() => {
    const videos = [...document.querySelectorAll("video")].map((v) => ({
      src: v.currentSrc || v.src || "",
      poster: v.poster || "",
      paused: v.paused,
      duration: Number.isFinite(v.duration) ? v.duration : null,
      currentTime: v.currentTime,
      readyState: v.readyState,
      width: v.videoWidth,
      height: v.videoHeight,
    }));
    const audios = [...document.querySelectorAll("audio")].map((a) => ({
      src: a.currentSrc || a.src || "",
      duration: Number.isFinite(a.duration) ? a.duration : null,
      paused: a.paused,
      readyState: a.readyState,
    }));
    return {
      title: document.title,
      url: location.href,
      bodyText: (document.body?.innerText || "").slice(0, 12000),
      videos,
      audios,
    };
  });

  const duration = info.videos[0]?.duration || 30;
  const targets = [0.5, 3, 6, 12, 20, 35, 60, Math.max(0.5, duration - 1)]
    .filter((v, i, arr) => v <= duration && arr.indexOf(v) === i);
  const frames = [];
  for (const targetTime of targets) {
    const state = await page.evaluate(async (time) => {
      const video = document.querySelector("video");
      if (!video) return null;
      video.pause();
      video.currentTime = Math.min(time, Math.max(0, (video.duration || time) - 0.25));
      await new Promise((resolve) => {
        const done = () => resolve();
        video.addEventListener("seeked", done, { once: true });
        setTimeout(done, 2500);
      });
      return {
        currentTime: video.currentTime,
        duration: Number.isFinite(video.duration) ? video.duration : null,
        paused: video.paused,
        readyState: video.readyState,
        width: video.videoWidth,
        height: video.videoHeight,
        src: video.currentSrc || video.src || "",
      };
    }, targetTime);
    const framePath = path.join(outDir, `seek-${String(targetTime).replace(".", "-")}s.png`);
    await page.screenshot({ path: framePath, fullPage: true });
    frames.push({ targetTime, state, framePath });
  }

  const htmlPath = path.join(outDir, "page.html");
  const jsonPath = path.join(outDir, "watch-result.json");
  await fs.writeFile(htmlPath, await page.content(), "utf8");
  await fs.writeFile(
    jsonPath,
    JSON.stringify(
      { navError, inputUrl, info, playResult, frames, responses, failedRequests, htmlPath, outDir },
      null,
      2,
    ),
    "utf8",
  );
  await browser.close();

  console.log(JSON.stringify({ ok: true, navError, info, playResult, frames, jsonPath, htmlPath, outDir }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

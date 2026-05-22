// ============ DOM refs ============
const titleInput = document.getElementById('title-input');
const subtitleInput = document.getElementById('subtitle-input');
const summaryInput = document.getElementById('summary-input');
const titleText = document.getElementById('title-text');
const subtitleText = document.getElementById('subtitle-text');
const summaryText = document.getElementById('summary-text');
const slide = document.getElementById('slide');
const hudDate = document.getElementById('hud-date');
const charCount = document.getElementById('char-count');
const fullscreenBtn = document.getElementById('fullscreen-btn');
const previewFrame = document.querySelector('.preview-frame');

// ============ 实时预览：文本同步 ============
function syncText() {
  titleText.textContent = titleInput.value || '未来已来';
  subtitleText.textContent = subtitleInput.value || '';
  summaryText.textContent = summaryInput.value || '';
  charCount.textContent = `${summaryInput.value.length} 字符`;
  fitTitle();
}

// 标题自适应：从最大字号递减，直到单行不溢出（或到达最小值）
function fitTitle() {
  // 根据当前风格挑选基础字号 / 字距
  let max, baseSpacing;
  if (slide.classList.contains('style-warm')) {
    max = 140; baseSpacing = 12;
  } else if (slide.classList.contains('style-mono')) {
    max = 168; baseSpacing = 2;
  } else if (slide.classList.contains('style-guofeng')) {
    max = 150; baseSpacing = 14;
  } else if (slide.classList.contains('style-fresh')) {
    max = 140; baseSpacing = 6;
  } else {
    max = 128; baseSpacing = 4;
  }
  const min = 56;
  const step = 4;

  let size = max;
  titleText.style.fontSize = size + 'px';
  titleText.style.letterSpacing = baseSpacing + 'px';

  while (titleText.scrollWidth > titleText.clientWidth && size > min) {
    size -= step;
    titleText.style.fontSize = size + 'px';
    const ratio = size / max;
    titleText.style.letterSpacing = (baseSpacing * ratio).toFixed(1) + 'px';
  }
}

[titleInput, subtitleInput, summaryInput].forEach(el => {
  el.addEventListener('input', syncText);
});
syncText();

// ============ 当前日期 ============
function updateDate() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const dateStr = `${y}.${m}.${day}`;
  hudDate.textContent = dateStr;
  const monoTime = document.getElementById('mono-time');
  if (monoTime) monoTime.textContent = dateStr;
}
updateDate();

// ============ 风格切换（科技 / 温情） ============
const stylePresets = {
  tech: {
    title: '未来已来',
    subtitle: 'THE FUTURE IS NOW',
    summary: '在人工智能与算力革命的浪潮中，重新定义生产力的边界，探索属于这个时代的可能性。'
  },
  mono: {
    title: '少即是多',
    subtitle: 'LESS IS MORE',
    summary: '删繁就简，回归本质。在这个被信息淹没的时代，让设计回到最初的纯粹与克制。'
  },
  warm: {
    title: '人间值得',
    subtitle: '愿你 不负 时光',
    summary: '愿你历经山河，仍觉人间值得；愿你走过千帆，归来仍是少年。把每一个寻常日子，过成想要的模样。'
  },
  guofeng: {
    title: '山河岁月',
    subtitle: '一纸长卷 千年清风',
    summary: '笔墨纸砚之间，藏着千年的山河岁月。一卷长卷，一段往事，一壶茶里见乾坤，方寸之地有天地。'
  },
  fresh: {
    title: '慢一点',
    subtitle: 'slow living',
    summary: '一杯茶、一本书、一缕阳光。把日子过慢一点，让心安静一点，把每个清晨都过成想留住的样子。'
  }
};

let userEdited = { title: false, subtitle: false, summary: false };
[titleInput, subtitleInput, summaryInput].forEach((el, i) => {
  const key = ['title', 'subtitle', 'summary'][i];
  el.addEventListener('input', () => { userEdited[key] = true; });
});

document.querySelectorAll('.style-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const style = btn.dataset.style;
    slide.className = slide.className.replace(/style-\w+/, `style-${style}`);

    // 如果用户没有手动改过对应字段，自动替换为该风格的示例内容
    const preset = stylePresets[style];
    if (!userEdited.title)    { titleInput.value = preset.title; }
    if (!userEdited.subtitle) { subtitleInput.value = preset.subtitle; }
    if (!userEdited.summary)  { summaryInput.value = preset.summary; }
    syncText();
    fitTitle();
  });
});

// ============ 主题切换 ============
document.querySelectorAll('.theme-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const theme = btn.dataset.theme;
    slide.className = slide.className.replace(/theme-\w+/, `theme-${theme}`);
  });
});

// ============ 布局切换 ============
document.querySelectorAll('.layout-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const layout = btn.dataset.layout;
    slide.className = slide.className.replace(/layout-\w+/, `layout-${layout}`);
    fitTitle();
  });
});

// 字体加载完成后再拟合一次（避免字体未就绪时的测量误差）
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(fitTitle);
}

// ============ 自适应缩放：slide 1920×1080 -> 容器 ============
function resizeSlide() {
  const rect = previewFrame.getBoundingClientRect();
  const scale = rect.width / 1920;
  slide.style.transform = `scale(${scale})`;
}
window.addEventListener('resize', resizeSlide);
// 等字体加载完成后再缩放，避免抖动
window.addEventListener('load', resizeSlide);
setTimeout(resizeSlide, 100);

// ============ 全屏预览 ============
fullscreenBtn.addEventListener('click', () => {
  if (!document.fullscreenElement) {
    previewFrame.requestFullscreen?.();
  } else {
    document.exitFullscreen?.();
  }
});

document.addEventListener('fullscreenchange', () => {
  setTimeout(resizeSlide, 50);
});

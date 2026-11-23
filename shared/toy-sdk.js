/**
 * AI-Interactive-Taxonomy Shared Toy SDK (Zero-dependency)
 * 1. 自动检测是否在主应用 iframe 中打开，若是则加上 body.in-iframe 隐藏重复返回栏
 * 2. 自动监听主应用的亮/暗色主题切换事件并同步到 data-theme
 * 3. 提供 ToySDK.markCompleted() 供玩具在用户达成顿悟点时主动上报完成进度
 */
(function () {
  const isIframe = window.self !== window.top;
  if (isIframe) {
    document.addEventListener("DOMContentLoaded", () => {
      document.body.classList.add("in-iframe");
    });
  }

  function applyTheme(theme) {
    if (theme === "dark" || theme === "light") {
      document.documentElement.setAttribute("data-theme", theme);
    }
  }

  // 初始化主题（优先 URL 参数，其次 localStorage）
  const params = new URLSearchParams(window.location.search);
  const initialTheme = params.get("theme") || localStorage.getItem("tax_theme_v1") || "light";
  applyTheme(initialTheme);

  window.addEventListener("message", (event) => {
    if (!event.data || typeof event.data !== "object") return;
    if (event.data.type === "TAX_THEME_CHANGE") {
      applyTheme(event.data.theme);
    }
  });

  window.ToySDK = {
    isEmbedded: isIframe,
    markCompleted(note) {
      if (isIframe) {
        window.parent.postMessage({ type: "TAX_TOY_COMPLETED", note: note || "" }, "*");
      }
    }
  };
})();

import { getUserCode } from "@/content-scripts/leetcodeContent";

const observeCodeChanges = (
  callback: (code: string, language: string) => void,
) => {
  const codeEditor = document.querySelector('[data-track-load="code_editor"]');

  if (!codeEditor) {
    console.warn("Code editor not found for observation.");
    return;
  }

  const viewLines = codeEditor.querySelector(".view-lines");
  if (!viewLines) {
    console.warn("View lines not found for observation.");
    return;
  }

  // Debounce setup to avoid excessive calls
  let debounceTimer: number | null = null;
  const debounceDelay = 1000; // 1 second debounce

  const observer = new MutationObserver(() => {
    clearTimeout(debounceTimer!);
    debounceTimer = window.setTimeout(() => {
      const { code, language } = getUserCode();
      callback(code, language);
    }, debounceDelay);
  });

  observer.observe(viewLines, {
    childList: true,
    subtree: true,
    characterData: true,
    characterDataOldValue: true,
  });

  return observer;
};

const initCodeObserver = () => {
  const observer = observeCodeChanges((code, language) => {
    // Dispatch event for local listeners (e.g., for UI updates)
    window.dispatchEvent(
      new CustomEvent("CODE_CHANGED", { detail: { code, language } }),
    );
  });

  return () => observer?.disconnect();
};

// Listen for requests from sidepanel to get current code
chrome.runtime.onMessage.addListener((request, _, sendResponse) => {
  if (request.type === "getLatestCode") {
    const { code, language } = getUserCode();
    sendResponse({ data: { code, language } });
  }
  return true;
});

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initCodeObserver);
} else {
  initCodeObserver();
}

const LEETCODE_ORIGIN = "https://leetcode.com";

chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error(error));

chrome.tabs.onUpdated.addListener(async (tabId, _, tab) => {
  if (!tab.url) return;
  const url = new URL(tab.url);

  if (url.origin === LEETCODE_ORIGIN) {
    await chrome.sidePanel.setOptions({
      tabId,
      path: "index.html",
      enabled: true,
    });
    await chrome.sidePanel.open({ tabId });
    console.log("Side panel opened for LeetCode");
  } else {
    await chrome.sidePanel.setOptions({
      tabId,
      enabled: false,
    });
  }
});

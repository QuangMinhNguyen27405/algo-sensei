// Content script to interact with the active webpage
chrome.runtime.onMessage.addListener((message, _, sendResponse) => {
  if (message.type === "GET_PAGE_HTML") {
    const html = document.documentElement.outerHTML;
    sendResponse({ html });
    return true;
  }

  if (message.type === "GET_PAGE_TEXT") {
    // Get just the text content
    const text = document.body.innerText;
    sendResponse({ text });
    return true;
  }

  if (message.type === "GET_PAGE_INFO") {
    // Get page metadata
    const info = {
      title: document.title,
      url: window.location.href,
      description:
        document
          .querySelector('meta[name="description"]')
          ?.getAttribute("content") || "",
    };
    sendResponse(info);
    return true;
  }
});

console.log("Content script loaded");

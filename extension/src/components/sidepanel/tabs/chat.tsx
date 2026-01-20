import { Thread } from "@/components/assistant-ui/thread";
import { TabsContent } from "@/components/ui/tabs";
import { EnvConfig } from "@/config/env";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import {
  AssistantChatTransport,
  useChatRuntime,
} from "@assistant-ui/react-ai-sdk";
import { useMemo } from "react";

const getCodeFromPage = async (): Promise<{
  code: string;
  language: string;
  problemDescription?: string;
}> => {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tabId = tabs[0]?.id;
      if (!tabId) {
        resolve({ code: "", language: "" });
        return;
      }

      chrome.tabs.sendMessage(
        tabId,
        { type: "getProblemAndCode" },
        (response) => {
          if (chrome.runtime.lastError || !response?.data) {
            resolve({ code: "", language: "" });
            return;
          }
          resolve({
            code: response.data.code || "",
            language: response.data.language || "",
            problemDescription: response.data.problemDescription || "",
          });
        },
      );
    });
  });
};

export const Chat = () => {
  const transport = useMemo(
    () =>
      new AssistantChatTransport({
        api: `${EnvConfig.get().VITE_API_URL}/agent/chat-test`,
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
          Accept: "text/event-stream",
        },
        body: async () => {
          const { code, language, problemDescription } =
            await getCodeFromPage();
          console.log("Sending chat request with:", {
            code,
            language,
            problemDescription,
          });
          return {
            user_id: "12345",
            session_id: "session_1",
            code,
            language,
            problem_description: problemDescription,
          };
        },
      }),
    [],
  );

  const runtime = useChatRuntime({
    transport,
    onError: (error) => {
      console.error("Chat runtime error:", error);
    },
  });

  return (
    <TabsContent value="chat" className="flex-1 overflow-hidden">
      <AssistantRuntimeProvider runtime={runtime}>
        <div className="flex flex-col h-full">
          <Thread />
        </div>
      </AssistantRuntimeProvider>
    </TabsContent>
  );
};

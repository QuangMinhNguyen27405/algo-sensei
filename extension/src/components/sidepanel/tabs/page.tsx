import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { TabsContent } from "@/components/ui/tabs";
import { FileCode } from "lucide-react";
import { useState } from "react";

export const Page = () => {
  const [loading_page, setLoadingPage] = useState(false);
  const [problem, setProblem] = useState<string[]>([]);
  const [codeComplexity, setCodeComplexity] = useState<{
    code: string;
    language: string;
    error?: string;
  } | null>(null);

  const getProblem = async () => {
    setLoadingPage(true);
    try {
      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true,
      });
      if (tab.id) {
        const response = await chrome.tabs.sendMessage(tab.id, {
          type: "getProblem",
        });
        setProblem(response.data);
      }
    } catch (error) {
      console.error("Error getting problem:", error);
    } finally {
      setLoadingPage(false);
    }
  };

  const getCodeComplexity = async () => {
    setLoadingPage(true);
    try {
      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true,
      });
      if (tab.id) {
        const response = await chrome.tabs.sendMessage(tab.id, {
          type: "getCodeComplexity",
        });
        setCodeComplexity(response.data);
      }
    } catch (error) {
      console.error("Error getting code complexity:", error);
    } finally {
      setLoadingPage(false);
    }
  };

  return (
    <TabsContent value="page" className="flex-1 overflow-hidden w-full">
      <ScrollArea className="h-full w-full">
        <div className="space-y-4 p-4 w-full max-w-full overflow-hidden">
          <div>
            <h2 className="text-base font-semibold flex items-center gap-2 mb-2">
              <FileCode className="h-4 w-4" />
              Current Page Content
            </h2>
            <p className="text-muted-foreground mb-4">
              Retrieve and view the current webpage's HTML and metadata
            </p>
          </div>

          <div className="space-y-3">
            <Button
              onClick={getProblem}
              disabled={loading_page}
              className="w-full">
              {loading_page ? "Loading..." : "Get Problem Data"}
            </Button>
            <Button
              onClick={getCodeComplexity}
              variant="outline"
              disabled={loading_page}
              className="w-full">
              {loading_page ? "Loading..." : "Get Code & Language"}
            </Button>
          </div>

          {codeComplexity && (
            <Card className="overflow-hidden w-full">
              <CardHeader className="overflow-hidden w-full">
                <CardTitle className="text-base">Code Information</CardTitle>
                <CardDescription className="overflow-hidden w-full">
                  <div className="space-y-2 mt-2">
                    <div>
                      <Label className="text-xs font-medium">Language:</Label>
                      <p className="text-sm font-semibold">
                        {codeComplexity.language}
                      </p>
                    </div>
                    {codeComplexity.error && (
                      <div>
                        <Label className="text-xs font-medium text-red-600">
                          Error:
                        </Label>
                        <p className="text-sm text-red-600">
                          {codeComplexity.error}
                        </p>
                      </div>
                    )}
                    {codeComplexity.code && (
                      <div>
                        <Label className="text-xs font-medium">
                          Current Code:
                        </Label>
                        <ScrollArea className="h-48 w-full rounded-md border mt-2">
                          <pre className="p-4 text-xs bg-slate-950 text-slate-50 overflow-x-auto">
                            <code>{codeComplexity.code}</code>
                          </pre>
                        </ScrollArea>
                      </div>
                    )}
                  </div>
                </CardDescription>
              </CardHeader>
            </Card>
          )}

          {problem.length > 0 && (
            <Card className="overflow-hidden w-full">
              <CardHeader className="overflow-hidden w-full">
                <CardTitle className="text-base">Problem Details</CardTitle>
                <CardDescription className="overflow-hidden w-full">
                  <div className="space-y-2 mt-2 w-full">
                    <ScrollArea className="h-96 w-full rounded-md border">
                      <div
                        className="p-4 text-sm w-full"
                        style={{
                          wordBreak: "break-word",
                          overflowWrap: "break-word",
                        }}>
                        {problem.map((line, index) => (
                          <p
                            key={index}
                            className="mb-2"
                            style={{
                              wordBreak: "break-word",
                              overflowWrap: "break-word",
                              whiteSpace: "pre-wrap",
                            }}>
                            {line}
                          </p>
                        ))}
                      </div>
                    </ScrollArea>
                  </div>
                </CardDescription>
              </CardHeader>
            </Card>
          )}
        </div>
      </ScrollArea>
    </TabsContent>
  );
};

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { TabsContent } from "@/components/ui/tabs";

export const Home = () => {
  return (
    <TabsContent value="home" className="flex-1 overflow-hidden">
      <ScrollArea className="h-full">
        <div className="space-y-4 p-4">
          <div>
            <h2 className="text-base font-semibold flex items-center gap-2 mb-2">
              Welcome to Sidepanel Template
              <Badge variant="secondary">v1.0.0</Badge>
            </h2>
            <p className="text-muted-foreground mb-4">
              A modern browser extension template built with WXT, Tailwind CSS
              4.0, and shadcn/ui components.
            </p>
            <div className="grid gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">🚀 Modern Stack</CardTitle>
                  <CardDescription>
                    Built with WXT, React, TypeScript, and Tailwind CSS 4.0 for
                    the best developer experience.
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base">
                    🎨 Beautiful Design
                  </CardTitle>
                  <CardDescription>
                    Clean and accessible UI components from shadcn/ui library.
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base">
                    ⚡ Fast Development
                  </CardTitle>
                  <CardDescription>
                    Hot reload and modern build tools for rapid development.
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>
          </div>
        </div>
      </ScrollArea>
    </TabsContent>
  );
};

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { TabsContent } from "@/components/ui/tabs";
import { useSettings } from "@/hooks/use-settings";
import { useTheme } from "@/hooks/use-theme";
import { Monitor, Moon, Sun } from "lucide-react";

const config = {
  features: {
    enableChat: true,
    maxTokens: 4096,
  },
};

export const Settings = () => {
  const { appearance, system, updateAppearance, updateSystem, resetSettings } =
    useSettings();

  const themeOptions = [
    { value: "system", label: "System", icon: Monitor },
    { value: "light", label: "Light", icon: Sun },
    { value: "dark", label: "Dark", icon: Moon },
  ] as const;

  const { resolvedTheme: _resolvedTheme, setTheme } = useTheme({
    theme: appearance.theme,
    onThemeChange: (theme) => updateAppearance({ theme }),
  });

  const handleSyncIntervalChange = (value: string) => {
    const interval = parseInt(value);
    if (!isNaN(interval) && interval > 0) {
      updateSystem({ syncInterval: interval });
    }
  };

  return (
    <TabsContent value="settings" className="flex-1 overflow-hidden">
      <ScrollArea className="h-full">
        <div className="space-y-6 p-4">
          {/* Appearance Settings */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">Appearance</h3>
              <p className="text-xs text-muted-foreground mb-4">
                Customize the look and feel
              </p>
            </div>

            <div className="space-y-3">
              <Label className="text-sm font-medium">Theme</Label>
              <div className="grid grid-cols-3 gap-2">
                {themeOptions.map((option) => {
                  const Icon = option.icon;
                  const isActive = appearance.theme === option.value;
                  return (
                    <Button
                      key={option.value}
                      variant={isActive ? "default" : "outline"}
                      size="sm"
                      onClick={() => setTheme(option.value)}
                      className="flex flex-col gap-1 h-auto py-3">
                      <Icon className="h-4 w-4" />
                      <span className="text-xs">{option.label}</span>
                    </Button>
                  );
                })}
              </div>
            </div>
          </div>

          <Separator />

          {/* System Settings */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">System Settings</h3>
              <p className="text-xs text-muted-foreground mb-4">
                Core extension functionality
              </p>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">Notifications</Label>
                <p className="text-xs text-muted-foreground">
                  Enable push notifications
                </p>
              </div>
              <Switch
                checked={system.notifications}
                onCheckedChange={(checked: boolean) =>
                  updateSystem({ notifications: checked })
                }
              />
            </div>

            <Separator />

            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">
                  Sync Interval (minutes)
                </Label>
                <p className="text-xs text-muted-foreground">
                  Data synchronization frequency
                </p>
              </div>
              <Input
                type="number"
                value={system.syncInterval}
                onChange={(e) => handleSyncIntervalChange(e.target.value)}
                className="w-20 h-8 text-xs"
                min="1"
              />
            </div>
          </div>

          <Separator />

          {/* Runtime Configuration - Read Only */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">Runtime Configuration</h3>
              <p className="text-xs text-muted-foreground mb-4">
                Values from app.config.ts (read-only)
              </p>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">
                  Config Chat Status
                </Label>
                <p className="text-xs text-muted-foreground">
                  Chat setting from runtime config
                </p>
              </div>
              <Badge
                variant={config.features?.enableChat ? "default" : "secondary"}
                className="text-xs">
                {config.features?.enableChat ? "Enabled" : "Disabled"}
              </Badge>
            </div>

            <Separator />

            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium">Config Max Tokens</Label>
                <p className="text-xs text-muted-foreground">
                  Token limit from runtime config
                </p>
              </div>
              <Badge variant="outline" className="text-xs">
                {config.features?.maxTokens}
              </Badge>
            </div>
          </div>

          <Separator />

          <div className="flex gap-2">
            <Button
              variant="outline"
              className="flex-1"
              onClick={resetSettings}>
              Reset
            </Button>
            <Button className="flex-1">Save Changes</Button>
          </div>
        </div>
      </ScrollArea>
    </TabsContent>
  );
};

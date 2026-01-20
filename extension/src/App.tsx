import { TabToggle } from "@/components/sidepanel/tabToggle";
import { Chat } from "@/components/sidepanel/tabs/chat";
import { Profile } from "@/components/sidepanel/tabs/profile";
import { Settings } from "@/components/sidepanel/tabs/settings";
import { Tabs } from "@/components/ui/tabs";
import { useSettings } from "@/hooks/use-settings";

const App = () => {
  const { ui, loading, updateUI } = useSettings();

  const handleTabChange = (value: string) => {
    updateUI({ activeTab: value });
  };

  if (loading) {
    return (
      <div className="flex flex-col h-screen bg-background">
        <div className="flex-1 flex items-center justify-center">
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <div className="flex-1 overflow-hidden">
        <Tabs
          value={ui.activeTab}
          onValueChange={handleTabChange}
          className="h-full flex flex-col gap-0">
          <TabToggle />

          <Chat />
          <Profile />
          <Settings />
        </Tabs>
      </div>
    </div>
  );
};

export default App;

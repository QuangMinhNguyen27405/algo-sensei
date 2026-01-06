import { Tabs } from "@/components/ui/tabs";
import { Header } from "@/components/sidepanel/header";
import { TabToggle } from "@/components/sidepanel/tabToggle";
import { Home } from "@/components/sidepanel/tabs/home";
import { Page } from "@/components/sidepanel/tabs/page";
import { Profile } from "@/components/sidepanel/tabs/profile";
import { useSettings } from "@/hooks/use-settings";
import { Settings } from "@/components/sidepanel/tabs/settings";

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
      <Header />
      {/* Content */}
      <div className="flex-1 overflow-hidden">
        <Tabs
          value={ui.activeTab}
          onValueChange={handleTabChange}
          className="h-full flex flex-col gap-0">
          <TabToggle />

          <Home />
          <Page />

          <Profile />
          <Settings />
        </Tabs>
      </div>
    </div>
  );
};

export default App;

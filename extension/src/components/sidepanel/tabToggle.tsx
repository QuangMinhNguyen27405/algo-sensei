import { TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MessageCircle, Settings, User } from "lucide-react";

export const TabToggle = () => {
  const tabs = [
    { value: "chat", icon: MessageCircle, label: "Chat" },
    { value: "profile", icon: User, label: "Profile" },
    { value: "settings", icon: Settings, label: "Settings" },
  ];
  return (
    <TabsList className="h-auto rounded-none border-b bg-transparent p-3 w-full">
      {tabs.map((tab) => (
        <TabsTrigger
          key={tab.value}
          value={tab.value}
          className="data-[state=active]:after:bg-primary relative rounded-none py-2 px-3 flex items-center gap-2 after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 data-[state=active]:bg-transparent data-[state=active]:shadow-none flex-1">
          <tab.icon className="h-4 w-4" />
          {tab.label}
        </TabsTrigger>
      ))}
    </TabsList>
  );
};

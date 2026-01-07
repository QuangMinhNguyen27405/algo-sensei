import { TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FileCode, House, Settings, User } from "lucide-react";

export const TabToggle = () => {
  return (
    <TabsList className="h-auto rounded-none border-b bg-transparent p-0 w-full">
      <TabsTrigger
        value="home"
        className="data-[state=active]:after:bg-primary relative rounded-none py-2 px-4 flex items-center gap-2 after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 data-[state=active]:bg-transparent data-[state=active]:shadow-none flex-1">
        <House className="h-4 w-4" />
        Home
      </TabsTrigger>
      <TabsTrigger
        value="page"
        className="data-[state=active]:after:bg-primary relative rounded-none py-2 px-4 flex items-center gap-2 after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 data-[state=active]:bg-transparent data-[state=active]:shadow-none flex-1">
        <FileCode className="h-4 w-4" />
        Page
      </TabsTrigger>
      <TabsTrigger
        value="profile"
        className="data-[state=active]:after:bg-primary relative rounded-none py-2 px-4 flex items-center gap-2 after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 data-[state=active]:bg-transparent data-[state=active]:shadow-none flex-1">
        <User className="h-4 w-4" />
        Profile
      </TabsTrigger>
      <TabsTrigger
        value="settings"
        className="data-[state=active]:after:bg-primary relative rounded-none py-2 px-4 flex items-center gap-2 after:absolute after:inset-x-0 after:bottom-0 after:h-0.5 data-[state=active]:bg-transparent data-[state=active]:shadow-none flex-1">
        <Settings className="h-4 w-4" />
        Settings
      </TabsTrigger>
    </TabsList>
  );
};

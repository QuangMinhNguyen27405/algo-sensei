import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { TabsContent } from "@/components/ui/tabs";
import { Calendar, Mail } from "lucide-react";

export const Profile = () => {
  return (
    <TabsContent value="profile" className="flex-1 overflow-hidden">
      <ScrollArea className="h-full">
        <div className="space-y-8 p-4">
          {/* Profile Section */}
          <div className="text-center space-y-4">
            <Avatar className="h-20 w-20 mx-auto ring-2 ring-offset-2 ring-primary/10">
              <AvatarImage
                src="https://pbs.twimg.com/profile_images/1593304942210478080/TUYae5z7_400x400.jpg"
                alt="User Avatar"
              />
              <AvatarFallback className="text-lg font-semibold">
                SC
              </AvatarFallback>
            </Avatar>
            <div className="space-y-2">
              <h2 className="text-xl font-semibold">Shadcn</h2>
              <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
                <Mail className="h-4 w-4" />
                <span>shadcn@example.com</span>
              </div>
              <Badge variant="secondary" className="font-medium">
                Premium User
              </Badge>
            </div>
          </div>

          <Separator />

          {/* Account Details */}
          <div className="space-y-4">
            <h3 className="text-base font-semibold flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Account Details
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between py-2">
                <span className="text-sm text-muted-foreground">
                  Member Since
                </span>
                <span className="text-sm font-medium">July 2025</span>
              </div>
              <div className="flex items-center justify-between py-2">
                <span className="text-sm text-muted-foreground">
                  Last Login
                </span>
                <span className="text-sm font-medium">Today</span>
              </div>
              <div className="flex items-center justify-between py-2">
                <span className="text-sm text-muted-foreground">Status</span>
                <Badge
                  variant="outline"
                  className="text-green-600 border-green-600">
                  Active
                </Badge>
              </div>
            </div>
          </div>

          <Separator />

          {/* Actions */}
          <div className="space-y-3">
            <Button className="w-full">Edit Profile</Button>
            <Button variant="outline" className="w-full">
              Change Password
            </Button>
          </div>
        </div>
      </ScrollArea>
    </TabsContent>
  );
};

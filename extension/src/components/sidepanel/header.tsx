import { Heart } from "lucide-react";

export const Header = () => {
  return (
    <div className="border-b px-4 py-3">
      <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
          <Heart className="h-5 w-5 text-primary-foreground" />
        </div>
        <div>
          <h1 className="font-semibold text-lg">Sidepanel Template</h1>
          <p className="text-sm text-muted-foreground">
            WXT + Tailwind CSS 4.0 + shadcn/ui
          </p>
        </div>
      </div>
    </div>
  );
};

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import {
  useProblem,
  useUpdateUserProblem,
  useUserProblem,
} from "@/hooks/use-problems";
import {
  Calendar,
  CheckCircle2,
  Clock,
  Loader2,
  NotebookPen,
  Save,
  Timer,
  Zap,
} from "lucide-react";
import { useEffect, useState } from "react";

const STATUS_OPTIONS = [
  { value: "not_started", label: "Not Started" },
  { value: "in_progress", label: "In Progress" },
  { value: "completed", label: "Completed" },
] as const;

const STATUS_STYLES: Record<string, string> = {
  not_started: "border-muted-foreground/40 text-muted-foreground",
  in_progress:
    "border-yellow-600 text-yellow-600 dark:border-yellow-400 dark:text-yellow-400",
  completed:
    "border-green-600 text-green-600 dark:border-green-400 dark:text-green-400",
};

const DIFFICULTY_COLORS: Record<string, string> = {
  EASY: "text-green-600 border-green-600 dark:text-green-400 dark:border-green-400",
  MEDIUM:
    "text-yellow-600 border-yellow-600 dark:text-yellow-400 dark:border-yellow-400",
  HARD: "text-red-600 border-red-600 dark:text-red-400 dark:border-red-400",
};

function formatTime(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  if (mins < 60) return `${mins}m`;
  const hrs = Math.floor(mins / 60);
  const remainMins = mins % 60;
  return remainMins > 0 ? `${hrs}h ${remainMins}m` : `${hrs}h`;
}

function formatTag(tag: string): string {
  return tag
    .replace(/_/g, " ")
    .replace(/-/g, "-")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

interface ProblemDetailProps {
  problemId: number;
  onBack: () => void;
}

export function ProblemDetail({ problemId }: ProblemDetailProps) {
  const { data: problem, isLoading: problemLoading } = useProblem(problemId);
  const { data: userProblem, isLoading: userProblemLoading } =
    useUserProblem(problemId);
  const updateMutation = useUpdateUserProblem();

  const [editStatus, setEditStatus] = useState("");
  const [editNotes, setEditNotes] = useState("");
  const [editCode, setEditCode] = useState("");
  const [editAttempts, setEditAttempts] = useState(0);
  const [editTimeSpent, setEditTimeSpent] = useState(0);
  const [hasChanges, setHasChanges] = useState(false);

  // Populate form when data loads
  useEffect(() => {
    if (userProblem) {
      setEditStatus(userProblem.status);
      setEditNotes(userProblem.notes ?? "");
      setEditCode(userProblem.user_code ?? "");
      setEditAttempts(userProblem.attempts);
      setEditTimeSpent(userProblem.time_spent_seconds);
      setHasChanges(false);
    }
  }, [userProblem]);

  const handleFieldChange = <T,>(setter: (v: T) => void, value: T) => {
    setter(value);
    setHasChanges(true);
  };

  const handleSave = () => {
    if (!userProblem) return;

    updateMutation.mutate({
      problemId,
      data: {
        status: editStatus,
        notes: editNotes || undefined,
        user_code: editCode || undefined,
        attempts: editAttempts,
        time_spent_seconds: editTimeSpent,
      },
    });
    setHasChanges(false);
  };

  if (problemLoading || userProblemLoading) {
    return (
      <ScrollArea className="h-full">
        <div className="space-y-4 p-4">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-32 w-full" />
        </div>
      </ScrollArea>
    );
  }

  if (!userProblem) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-sm text-muted-foreground">Problem not found.</p>
      </div>
    );
  }

  return (
    <ScrollArea className="h-full">
      <div className="space-y-4 p-4">
        {/* Problem Info */}
        <div className="space-y-2">
          <h3 className="text-base font-semibold leading-tight">
            #{problemId} {problem?.title ?? "Unknown Problem"}
          </h3>

          <div className="flex items-center gap-2 flex-wrap">
            {problem?.difficulty && (
              <Badge
                variant="outline"
                className={DIFFICULTY_COLORS[problem.difficulty]}
              >
                {problem.difficulty.charAt(0) +
                  problem.difficulty.slice(1).toLowerCase()}
              </Badge>
            )}
            <Badge variant="outline" className={STATUS_STYLES[editStatus]}>
              {editStatus === "completed" && (
                <CheckCircle2 className="h-3 w-3" />
              )}
              {editStatus === "in_progress" && <Loader2 className="h-3 w-3" />}
              {STATUS_OPTIONS.find((s) => s.value === editStatus)?.label}
            </Badge>
          </div>

          {/* Tags */}
          {problem?.tags && problem.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 pt-1">
              {problem.tags.map((tag) => (
                <Badge
                  key={tag}
                  variant="secondary"
                  className="text-[10px] px-1.5 py-0"
                >
                  {formatTag(tag)}
                </Badge>
              ))}
            </div>
          )}
        </div>

        <Separator />

        {/* Tracking Stats */}
        <div className="grid grid-cols-2 gap-2">
          <div className="flex items-center gap-2 rounded-md border p-2.5">
            <Zap className="h-4 w-4 text-orange-500" />
            <div>
              <p className="text-[10px] text-muted-foreground uppercase tracking-wide">
                Attempts
              </p>
              <p className="text-sm font-semibold">{editAttempts}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded-md border p-2.5">
            <Timer className="h-4 w-4 text-blue-500" />
            <div>
              <p className="text-[10px] text-muted-foreground uppercase tracking-wide">
                Time Spent
              </p>
              <p className="text-sm font-semibold">
                {formatTime(editTimeSpent)}
              </p>
            </div>
          </div>
          {userProblem.completion_date && (
            <div className="flex items-center gap-2 rounded-md border p-2.5 col-span-2">
              <Calendar className="h-4 w-4 text-green-500" />
              <div>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wide">
                  Completed
                </p>
                <p className="text-sm font-semibold">
                  {userProblem.completion_date}
                </p>
              </div>
            </div>
          )}
        </div>

        <Separator />

        {/* Status Update */}
        <Card className="gap-3 py-3">
          <CardHeader className="px-3 py-0">
            <CardTitle className="text-sm flex items-center gap-1.5">
              <Clock className="h-3.5 w-3.5" />
              Status
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0">
            <div className="flex gap-1.5">
              {STATUS_OPTIONS.map((opt) => (
                <Button
                  key={opt.value}
                  variant={editStatus === opt.value ? "default" : "outline"}
                  size="sm"
                  className="h-7 text-xs flex-1"
                  onClick={() => handleFieldChange(setEditStatus, opt.value)}
                >
                  {opt.label}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Attempts & Time Controls */}
        <Card className="gap-3 py-3">
          <CardHeader className="px-3 py-0">
            <CardTitle className="text-sm flex items-center gap-1.5">
              <Zap className="h-3.5 w-3.5" />
              Tracking
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 space-y-3">
            <div className="space-y-1">
              <Label className="text-xs">Attempts</Label>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="h-7 w-7 p-0"
                  disabled={editAttempts <= 0}
                  onClick={() =>
                    handleFieldChange(
                      setEditAttempts,
                      Math.max(0, editAttempts - 1),
                    )
                  }
                >
                  −
                </Button>
                <span className="text-sm font-medium w-8 text-center">
                  {editAttempts}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  className="h-7 w-7 p-0"
                  onClick={() =>
                    handleFieldChange(setEditAttempts, editAttempts + 1)
                  }
                >
                  +
                </Button>
              </div>
            </div>
            <div className="space-y-1">
              <Label className="text-xs">Time Spent (minutes)</Label>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="h-7 w-7 p-0"
                  disabled={editTimeSpent <= 0}
                  onClick={() =>
                    handleFieldChange(
                      setEditTimeSpent,
                      Math.max(0, editTimeSpent - 60),
                    )
                  }
                >
                  −
                </Button>
                <span className="text-sm font-medium w-12 text-center">
                  {Math.round(editTimeSpent / 60)}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  className="h-7 w-7 p-0"
                  onClick={() =>
                    handleFieldChange(setEditTimeSpent, editTimeSpent + 60)
                  }
                >
                  +
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Notes */}
        <Card className="gap-3 py-3">
          <CardHeader className="px-3 py-0">
            <CardTitle className="text-sm flex items-center gap-1.5">
              <NotebookPen className="h-3.5 w-3.5" />
              Notes
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0">
            <Textarea
              placeholder="Add your notes, approach, or key insights..."
              value={editNotes}
              onChange={(e) => handleFieldChange(setEditNotes, e.target.value)}
              className="min-h-20 text-xs resize-none"
            />
          </CardContent>
        </Card>

        {/* Code */}
        <Card className="gap-3 py-3">
          <CardHeader className="px-3 py-0">
            <CardTitle className="text-sm flex items-center gap-1.5">
              <code className="text-xs">&lt;/&gt;</code>
              Your Code
            </CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0">
            <Textarea
              placeholder="Paste your solution code here..."
              value={editCode}
              onChange={(e) => handleFieldChange(setEditCode, e.target.value)}
              className="min-h-28 text-xs font-mono resize-none"
            />
          </CardContent>
        </Card>

        {/* Save Button */}
        <Button
          className="w-full"
          disabled={!hasChanges || updateMutation.isPending}
          onClick={handleSave}
        >
          {updateMutation.isPending ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Saving...
            </>
          ) : (
            <>
              <Save className="h-4 w-4" />
              Save Changes
            </>
          )}
        </Button>

        {updateMutation.isError && (
          <p className="text-xs text-destructive text-center">
            Failed to save. Please try again.
          </p>
        )}

        {updateMutation.isSuccess && !hasChanges && (
          <p className="text-xs text-green-600 dark:text-green-400 text-center">
            Changes saved successfully!
          </p>
        )}
      </div>
    </ScrollArea>
  );
}

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { TabsContent } from "@/components/ui/tabs";
import {
  useProblem,
  useUserProblems,
  type UserProblem,
} from "@/hooks/use-problems";
import {
  ArrowLeft,
  CheckCircle2,
  Clock,
  Code2,
  Filter,
  Loader2,
  NotebookPen,
  Timer,
  Zap,
} from "lucide-react";
import { useState } from "react";
import { ProblemDetail } from "./problem-detail";

type StatusFilter = "all" | "not_started" | "in_progress" | "completed";

const STATUS_LABELS: Record<string, { label: string; color: string }> = {
  not_started: {
    label: "Not Started",
    color: "text-muted-foreground border-muted-foreground/40",
  },
  in_progress: {
    label: "In Progress",
    color:
      "text-yellow-600 border-yellow-600 dark:text-yellow-400 dark:border-yellow-400",
  },
  completed: {
    label: "Completed",
    color:
      "text-green-600 border-green-600 dark:text-green-400 dark:border-green-400",
  },
};

const DIFFICULTY_COLORS: Record<string, string> = {
  EASY: "text-green-600 dark:text-green-400",
  MEDIUM: "text-yellow-600 dark:text-yellow-400",
  HARD: "text-red-600 dark:text-red-400",
};

function formatTime(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  if (mins < 60) return `${mins}m`;
  const hrs = Math.floor(mins / 60);
  const remainMins = mins % 60;
  return remainMins > 0 ? `${hrs}h ${remainMins}m` : `${hrs}h`;
}

// ── Problem Card ─────────────────────────────────────────────────────────────

function ProblemCard({
  userProblem,
  onClick,
}: {
  userProblem: UserProblem;
  onClick: () => void;
}) {
  const statusInfo = STATUS_LABELS[userProblem.status];

  return (
    <Card
      className="cursor-pointer gap-3 py-3 transition-colors hover:bg-accent/50"
      onClick={onClick}
    >
      <CardContent className="px-4 py-0">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0 space-y-1.5">
            <ProblemTitle problemId={userProblem.problem_id} />

            <div className="flex items-center gap-2 flex-wrap">
              <Badge variant="outline" className={statusInfo.color}>
                {userProblem.status === "completed" && (
                  <CheckCircle2 className="h-3 w-3" />
                )}
                {userProblem.status === "in_progress" && (
                  <Loader2 className="h-3 w-3" />
                )}
                {statusInfo.label}
              </Badge>

              <ProblemDifficultyBadge problemId={userProblem.problem_id} />
            </div>
          </div>

          <div className="flex flex-col items-end gap-1 text-xs text-muted-foreground shrink-0">
            {userProblem.attempts > 0 && (
              <span className="flex items-center gap-1">
                <Zap className="h-3 w-3" />
                {userProblem.attempts}{" "}
                {userProblem.attempts === 1 ? "attempt" : "attempts"}
              </span>
            )}
            {userProblem.time_spent_seconds > 0 && (
              <span className="flex items-center gap-1">
                <Timer className="h-3 w-3" />
                {formatTime(userProblem.time_spent_seconds)}
              </span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function ProblemTitle({ problemId }: { problemId: number }) {
  const { data: problem, isLoading } = useProblem(problemId);

  if (isLoading) return <Skeleton className="h-4 w-32" />;

  return (
    <p className="text-sm font-medium leading-tight truncate">
      #{problemId} {problem?.title ?? "Unknown Problem"}
    </p>
  );
}

function ProblemDifficultyBadge({ problemId }: { problemId: number }) {
  const { data: problem, isLoading } = useProblem(problemId);

  if (isLoading) return <Skeleton className="h-5 w-12" />;
  if (!problem) return null;

  const diffColor = DIFFICULTY_COLORS[problem.difficulty] ?? "";

  return (
    <span className={`text-xs font-medium ${diffColor}`}>
      {problem.difficulty.charAt(0) + problem.difficulty.slice(1).toLowerCase()}
    </span>
  );
}

// ── Status Filter Bar ────────────────────────────────────────────────────────

function StatusFilterBar({
  current,
  onChange,
}: {
  current: StatusFilter;
  onChange: (f: StatusFilter) => void;
}) {
  const filters: { value: StatusFilter; label: string }[] = [
    { value: "all", label: "All" },
    { value: "in_progress", label: "In Progress" },
    { value: "completed", label: "Completed" },
    { value: "not_started", label: "Not Started" },
  ];

  return (
    <div className="flex items-center gap-1 px-4 pb-2">
      <Filter className="h-3.5 w-3.5 text-muted-foreground mr-1" />
      {filters.map((f) => (
        <Button
          key={f.value}
          variant={current === f.value ? "default" : "ghost"}
          size="sm"
          className="h-7 text-xs px-2.5"
          onClick={() => onChange(f.value)}
        >
          {f.label}
        </Button>
      ))}
    </div>
  );
}

// ── Stats Summary ────────────────────────────────────────────────────────────

function StatsSummary({ problems }: { problems: UserProblem[] }) {
  const completed = problems.filter((p) => p.status === "completed").length;
  const inProgress = problems.filter((p) => p.status === "in_progress").length;
  const totalTime = problems.reduce((s, p) => s + p.time_spent_seconds, 0);

  return (
    <div className="grid grid-cols-3 gap-2 px-4 pb-2">
      <div className="flex items-center gap-1.5 rounded-md border p-2">
        <CheckCircle2 className="h-3.5 w-3.5 text-green-600 dark:text-green-400" />
        <div>
          <p className="text-xs text-muted-foreground">Solved</p>
          <p className="text-sm font-semibold">{completed}</p>
        </div>
      </div>
      <div className="flex items-center gap-1.5 rounded-md border p-2">
        <Code2 className="h-3.5 w-3.5 text-yellow-600 dark:text-yellow-400" />
        <div>
          <p className="text-xs text-muted-foreground">Active</p>
          <p className="text-sm font-semibold">{inProgress}</p>
        </div>
      </div>
      <div className="flex items-center gap-1.5 rounded-md border p-2">
        <Clock className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" />
        <div>
          <p className="text-xs text-muted-foreground">Time</p>
          <p className="text-sm font-semibold">{formatTime(totalTime)}</p>
        </div>
      </div>
    </div>
  );
}

// ── Main Problems Tab ────────────────────────────────────────────────────────

export const Problems = () => {
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [selectedProblemId, setSelectedProblemId] = useState<number | null>(
    null,
  );

  const queryFilter =
    statusFilter === "all" ? undefined : { status: statusFilter };
  const { data: userProblems, isLoading, error } = useUserProblems(queryFilter);

  // Detail view
  if (selectedProblemId !== null) {
    return (
      <TabsContent value="problems" className="flex-1 overflow-hidden">
        <div className="flex items-center gap-2 px-4 py-3 border-b">
          <Button
            variant="ghost"
            size="sm"
            className="h-7 w-7 p-0"
            onClick={() => setSelectedProblemId(null)}
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <h2 className="text-sm font-semibold">Problem Details</h2>
        </div>
        <ProblemDetail
          problemId={selectedProblemId}
          onBack={() => setSelectedProblemId(null)}
        />
      </TabsContent>
    );
  }

  // List view
  return (
    <TabsContent value="problems" className="flex-1 overflow-hidden">
      <ScrollArea className="h-full">
        <div className="space-y-2 pt-4">
          {/* Header */}
          <div className="px-4 space-y-1">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <NotebookPen className="h-5 w-5" />
              My Problems
            </h2>
            <p className="text-xs text-muted-foreground">
              Track your progress across LeetCode problems
            </p>
          </div>

          <Separator />

          {/* Stats */}
          {userProblems && userProblems.length > 0 && (
            <StatsSummary problems={userProblems} />
          )}

          {/* Filter */}
          <StatusFilterBar current={statusFilter} onChange={setStatusFilter} />

          <Separator />

          {/* List */}
          <div className="px-4 pb-4 space-y-2">
            {isLoading && (
              <div className="space-y-2">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-20 w-full rounded-xl" />
                ))}
              </div>
            )}

            {error && (
              <div className="text-center py-8">
                <p className="text-sm text-destructive">
                  Failed to load problems. Please sign in and try again.
                </p>
              </div>
            )}

            {!isLoading && !error && userProblems?.length === 0 && (
              <div className="text-center py-8 space-y-2">
                <Code2 className="h-10 w-10 mx-auto text-muted-foreground/50" />
                <p className="text-sm text-muted-foreground">
                  {statusFilter === "all"
                    ? "No problems tracked yet. Start solving on LeetCode!"
                    : `No ${STATUS_LABELS[statusFilter]?.label.toLowerCase()} problems.`}
                </p>
              </div>
            )}

            {userProblems?.map((up) => (
              <ProblemCard
                key={up.id}
                userProblem={up}
                onClick={() => setSelectedProblemId(up.problem_id)}
              />
            ))}
          </div>
        </div>
      </ScrollArea>
    </TabsContent>
  );
};

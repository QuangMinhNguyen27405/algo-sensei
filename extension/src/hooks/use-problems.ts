import { request } from "@/utils/api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { z } from "zod";

// ── Zod Schemas ──────────────────────────────────────────────────────────────

const ProblemResponseSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string().nullable().optional(),
  difficulty: z.enum(["EASY", "MEDIUM", "HARD"]),
  test_cases: z.string().nullable().optional(),
  tags: z.array(z.string()).nullable().optional(),
});

const UserProblemResponseSchema = z.object({
  id: z.number(),
  user_id: z.number(),
  problem_id: z.number(),
  status: z.enum(["not_started", "in_progress", "completed"]),
  user_code: z.string().nullable().optional(),
  notes: z.string().nullable().optional(),
  attempts: z.number(),
  time_spent_seconds: z.number(),
  completion_date: z.string().nullable().optional(),
});

export type Problem = z.infer<typeof ProblemResponseSchema>;
export type UserProblem = z.infer<typeof UserProblemResponseSchema>;

const ProblemListSchema = z.array(ProblemResponseSchema);
const UserProblemListSchema = z.array(UserProblemResponseSchema);

// ── Query Keys ───────────────────────────────────────────────────────────────

export const problemKeys = {
  all: ["problems"] as const,
  list: (filters?: { difficulty?: string }) =>
    [...problemKeys.all, "list", filters] as const,
  detail: (id: number) => [...problemKeys.all, "detail", id] as const,
  userProblems: ["user-problems"] as const,
  userProblemList: (filters?: { status?: string }) =>
    [...problemKeys.userProblems, "list", filters] as const,
  userProblemDetail: (problemId: number) =>
    [...problemKeys.userProblems, "detail", problemId] as const,
};

// ── Problem Queries (public) ─────────────────────────────────────────────────

export function useProblems(filters?: {
  difficulty?: string;
  skip?: number;
  limit?: number;
}) {
  return useQuery({
    queryKey: problemKeys.list(filters),
    queryFn: () =>
      request({
        method: "GET",
        url: "/problems/",
        data: {
          ...(filters?.difficulty && { difficulty: filters.difficulty }),
          ...(filters?.skip != null && { skip: filters.skip }),
          ...(filters?.limit != null && { limit: filters.limit }),
        },
        schema: ProblemListSchema,
      }),
  });
}

export function useProblem(id: number) {
  return useQuery({
    queryKey: problemKeys.detail(id),
    queryFn: () =>
      request({
        method: "GET",
        url: `/problems/${id}`,
        schema: ProblemResponseSchema,
      }),
    enabled: id > 0,
  });
}

// ── UserProblem Queries (authenticated) ──────────────────────────────────────

export function useUserProblems(filters?: { status?: string }) {
  return useQuery({
    queryKey: problemKeys.userProblemList(filters),
    queryFn: () =>
      request({
        method: "GET",
        url: "/problems/user/me",
        data: {
          ...(filters?.status && { problem_status: filters.status }),
        },
        schema: UserProblemListSchema,
        options: { requireAuth: true },
      }),
  });
}

export function useUserProblem(problemId: number) {
  return useQuery({
    queryKey: problemKeys.userProblemDetail(problemId),
    queryFn: () =>
      request({
        method: "GET",
        url: `/problems/user/me/${problemId}`,
        schema: UserProblemResponseSchema,
        options: { requireAuth: true },
      }),
    enabled: problemId > 0,
  });
}

// ── UserProblem Mutations ────────────────────────────────────────────────────

interface CreateUserProblemInput {
  problem_id: number;
  status?: string;
  user_code?: string;
  notes?: string;
}

export function useCreateUserProblem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: CreateUserProblemInput) =>
      request({
        method: "POST",
        url: "/problems/user",
        data: input,
        schema: UserProblemResponseSchema,
        options: { requireAuth: true },
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: problemKeys.userProblems });
    },
  });
}

interface UpdateUserProblemInput {
  problemId: number;
  data: {
    status?: string;
    user_code?: string;
    notes?: string;
    attempts?: number;
    time_spent_seconds?: number;
  };
}

export function useUpdateUserProblem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ problemId, data }: UpdateUserProblemInput) =>
      request({
        method: "PUT",
        url: `/problems/user/me/${problemId}`,
        data,
        schema: UserProblemResponseSchema,
        options: { requireAuth: true },
      }),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: problemKeys.userProblems });
      queryClient.invalidateQueries({
        queryKey: problemKeys.userProblemDetail(variables.problemId),
      });
    },
  });
}

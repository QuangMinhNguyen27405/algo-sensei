import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

interface GetCodeParams {
  user_id: string;
  session_id: string;
  problem_description: string;
  code: string;
  language: string;
}

export const useGetHints = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      user_id,
      session_id,
      problem_description,
      code,
      language,
    }: GetCodeParams) => {
      return axios.post("http://127.0.0.1:8000/agent/get-hints", {
        user_id,
        session_id,
        problem_description,
        code,
        language,
      }).then(res => res.data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["hints"] });
    },
  });
};

export const useGetCodeComplexity = () => {
  return useMutation({
    mutationFn: ({
      user_id,
      session_id,
      problem_description,
      code,
      language,
    }: GetCodeParams) => {
      return axios.post("http://127.0.0.1:8000/agent/get-hints", {
        user_id,
        session_id,
        problem_description,
        code,
        language,
      }).then(res => res.data);
    },
  });
};

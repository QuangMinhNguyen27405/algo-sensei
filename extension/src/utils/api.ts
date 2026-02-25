import axios from "axios";

import { EnvConfig } from "@/config/env";

const api = axios.create({
  baseURL: `${EnvConfig.get().VITE_API_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
});

interface RequestBaseArgs<T> {
  method: "GET" | "POST" | "DELETE" | "PUT" | "PATCH";
  url: string;
  data?: object;
  schema: { parse: (data: unknown) => T };
}

// Define an interface that defines overloads for the request function
interface IRequest {
  <T extends { data: object }>(
    args: RequestBaseArgs<T> & {
      options: { includeOnlyDataField: true; requireAuth?: boolean };
    },
  ): Promise<T["data"]>;

  <T>(
    args: RequestBaseArgs<T> & {
      options?: {
        includeOnlyDataField?: false | undefined;
        requireAuth?: boolean;
      };
    },
  ): Promise<T>;
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status;

      if (status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
      }
    }
    return Promise.reject(error);
  },
);

export const request: IRequest = async <T>({
  method,
  url,
  data = {},
  schema,
  options = {},
}: {
  method: "GET" | "POST" | "DELETE" | "PUT" | "PATCH";
  url: string;
  data?: object;
  schema: { parse: (data: unknown) => T };
  options?: { includeOnlyDataField?: boolean; requireAuth?: boolean };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
}): Promise<any> => {
  const { includeOnlyDataField = false } = options;
  const response = await api.request({
    method,
    url,
    ...(method === "GET" ? { params: data } : { data }),
    headers: {
      ...api.defaults.headers.common,
      ...(options?.requireAuth
        ? { Authorization: `Bearer ${localStorage.getItem("token")}` }
        : {}),
    },
  });
  const parsedData = schema.parse(response.data);

  return includeOnlyDataField &&
    parsedData != null &&
    typeof parsedData === "object" &&
    "data" in parsedData
    ? (parsedData as { data: unknown }).data
    : parsedData;
};

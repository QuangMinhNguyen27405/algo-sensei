import { z, ZodObject, type ZodRawShape } from "zod";

export const EnvConfig = {
  get: () =>
    parseEnvConfig({
      env: import.meta.env,
      schema: z.object({
        VITE_API_URL: z.string().url("Invalid URL"),
      }),
    }),
};

export const parseEnvConfig = <T extends ZodObject<ZodRawShape>>({
  env,
  schema,
}: {
  env: Record<string, string | undefined>;
  schema: T;
}): z.infer<T> => {
  const envs = schema.safeParse(env);
  if (!envs.success) {
    const issues = envs.error.issues
      .map((issue) => `${String(issue.path[0])}: ${issue.message}`)
      .join(", ");
    throw new Error(
      `Environment variables are not set correctly. Please check your .env file.\n Problems with: ${issues}`
    );
  }
  return envs.data;
};

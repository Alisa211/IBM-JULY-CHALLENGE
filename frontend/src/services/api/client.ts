const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

type RequestOptions = {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
};

export async function apiClient<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = 'GET', body, headers = {} } = options;

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

/** Simulates API delay for mock data */
export function simulateDelay<T>(data: T, ms = 800): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(data), ms));
}

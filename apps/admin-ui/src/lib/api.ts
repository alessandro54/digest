import { PUBLIC_API_BASE as BASE_FROM_ENV } from '$env/static/public';

const BASE = BASE_FROM_ENV || 'http://localhost:8000/v1';

export async function api<T = unknown>(path: string, init?: RequestInit): Promise<T> {
	const res = await fetch(`${BASE}${path}`, {
		...init,
		headers: {
			'content-type': 'application/json',
			...(init?.headers || {})
		}
	});
	if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
	// No content
	if (res.status === 204) return undefined as T;
	return (await res.json()) as T;
}

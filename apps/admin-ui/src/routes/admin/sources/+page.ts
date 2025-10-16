import type { PageLoad } from './$types';
import { api } from '$lib/api';
import type { Source } from '$lib/types';

export const load: PageLoad = async () => {
	const sources = await api<Source[]>('/sources/'); // GET /v1/sources
	return { sources };
};

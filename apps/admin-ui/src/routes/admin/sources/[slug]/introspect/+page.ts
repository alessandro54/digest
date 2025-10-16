import type { PageLoad } from './$types';
import { api } from '$lib/api';

export const load: PageLoad = async ({ params }) => {
	const introspection = await api(`/sources/${params.slug}/introspect/`, { method: 'POST' });
	return { introspection };
};

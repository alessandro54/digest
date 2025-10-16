export type Source = {
	id: number;
	slug: string;
	feed_url: string;
	kind: string;
	enabled: boolean;
	cadence_minutes: number;
	timeout_sec: number;
	max_retries: number;
	priority: number;
	last_run_at: string | null;
	created_at: string;
	updated_at: string;
	notes: string | null;
};

export type SourceCreate = {
	slug: string;
	feed_url: string;
	kind?: string;
	enabled?: boolean;
	cadence_minutes?: number;
	timeout_sec?: number;
	max_retries?: number;
	priority?: number;
	notes?: string | null;
};

export type SourceUpdate = Partial<Omit<Source, 'id' | 'created_at' | 'updated_at' | 'slug'>> & {
	slug?: never;
};

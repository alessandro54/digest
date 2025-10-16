<script lang="ts">
	// Accept whatever the page passes, but normalize to safe defaults
	export let data:
		| {
				slug: string;
				feed_url: string;
				status: number | null;
				items: number;
				schema: Record<string, string>;
				namespaces: string[];
				samples: Array<{
					schema: Record<string, string>;
					preview: Record<string, string | null>;
				}>;
		  }
		| undefined;

	// Safe normalized object so we never call Object.keys on undefined
	const d = {
		slug: data?.slug ?? '',
		feed_url: data?.feed_url ?? '',
		status: data?.status ?? null,
		items: data?.items ?? 0,
		schema: data?.schema ?? {},
		namespaces: data?.namespaces ?? [],
		samples: data?.samples ?? []
	};

	const entries = (obj: Record<string, string> | undefined) => Object.entries(obj ?? {});
</script>

<div class="space-y-4">
	<div>
		<h1 class="text-xl font-semibold">Introspect: {d.slug}</h1>
		<p class="text-sm opacity-80">URL: {d.feed_url}</p>
		<p class="text-sm opacity-80">HTTP status: {d.status ?? 'n/a'} · Items: {d.items}</p>
		{#if d.namespaces.length}
			<p class="mt-1 text-sm">
				Namespaces: <span class="opacity-80">{d.namespaces.join(', ')}</span>
			</p>
		{/if}
	</div>

	<section>
		<h2 class="mb-2 font-semibold">Merged schema (first 3 entries)</h2>
		{#if Object.keys(d.schema).length === 0}
			<div class="text-sm opacity-70">No items in feed.</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="min-w-[420px] border border-slate-200 text-sm">
					<thead class="bg-slate-50">
						<tr>
							<th class="border-b border-slate-200 px-3 py-2 text-left">Key</th>
							<th class="border-b border-slate-200 px-3 py-2 text-left">Type</th>
						</tr>
					</thead>
					<tbody>
						{#each entries(d.schema) as [k, v]}
							<tr class="odd:bg-white even:bg-slate-50/30">
								<td class="border-b border-slate-100 px-3 py-2 font-mono">{k}</td>
								<td class="border-b border-slate-100 px-3 py-2">{v}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</section>

	<section>
		<h2 class="mb-2 font-semibold">Samples</h2>
		{#each d.samples as s, i}
			<div class="mb-3 rounded-lg border border-slate-200 p-3">
				<h3 class="mb-2 font-semibold">Entry #{i + 1}</h3>
				<div class="space-y-1 text-sm">
					<div><span class="font-medium">title:</span> {s.preview.title}</div>
					<div class="truncate">
						<span class="font-medium">link:</span>
						<a class="underline" href={s.preview.link ?? '#'} target="_blank" rel="noreferrer"
							>{s.preview.link}</a
						>
					</div>
					<div><span class="font-medium">author:</span> {s.preview.author}</div>
					<div><span class="font-medium">published:</span> {s.preview.published}</div>
					<details class="mt-1">
						<summary class="cursor-pointer underline">summary (raw HTML)</summary>
						<div class="prose prose-sm mt-2 max-w-none border-t pt-2">
							{@html s.preview.summary ?? ''}
						</div>
					</details>
				</div>

				<details class="mt-3">
					<summary class="cursor-pointer underline">Entry schema</summary>
					<div class="mt-2 overflow-x-auto">
						<table class="min-w-[420px] border border-slate-200 text-sm">
							<thead class="bg-slate-50">
								<tr>
									<th class="border-b border-slate-200 px-3 py-2 text-left">Key</th>
									<th class="border-b border-slate-200 px-3 py-2 text-left">Type</th>
								</tr>
							</thead>
							<tbody>
								{#each entries(s.schema) as [k, v]}
									<tr class="odd:bg-white even:bg-slate-50/30">
										<td class="border-b border-slate-100 px-3 py-2 font-mono">{k}</td>
										<td class="border-b border-slate-100 px-3 py-2">{v}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</details>
			</div>
		{/each}
	</section>
</div>

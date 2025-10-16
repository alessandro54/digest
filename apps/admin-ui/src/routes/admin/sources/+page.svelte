<script lang="ts">
	import type { Source } from '$lib/types';
	import { api } from '$lib/api';
	export let data: { sources: Source[] };

	async function remove(slug: string) {
		if (!confirm(`Delete source "${slug}"?`)) return;
		await api(`/sources/${slug}`, { method: 'DELETE' }); // 204
		// refresh client-side
		location.reload();
	}
</script>

<h1 class="mb-3 text-xl font-semibold text-rose-400">Sources</h1>

<a href="/admin/sources/new" class="underline">+ New source</a>

<table class="mt-4" border="1" cellpadding="6">
	<thead>
		<tr>
			<th>Slug</th>
			<th>Kind</th>
			<th>Enabled</th>
			<th>Cadence</th>
			<th>Priority</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
		{#each data.sources as s, i}
			<tr class={i % 2 === 0 ? 'bg-gray-100' : ''}>
				<td>{s.slug}</td>
				<td>{s.kind}</td>
				<td>{s.enabled ? 'yes' : 'no'}</td>
				<td>{s.cadence_minutes}m</td>
				<td>{s.priority}</td>
				<td>
					<a href={`/admin/sources/${s.slug}`} class="underline">edit</a>
					&nbsp;|&nbsp;
					<a href={`/admin/sources/${s.slug}/introspect`} class="underline">introspect</a>
					&nbsp;|&nbsp;
					<button on:click={() => remove(s.slug)}>delete</button>
				</td>
			</tr>
		{/each}
	</tbody>
</table>

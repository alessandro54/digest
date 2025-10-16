<script lang="ts">
	import { api } from '$lib/api';
	import type { SourceCreate } from '$lib/types';

	let form: SourceCreate = {
		slug: '',
		feed_url: '',
		kind: 'tech',
		enabled: true,
		cadence_minutes: 60,
		timeout_sec: 20,
		max_retries: 3,
		priority: 0,
		notes: ''
	};
	let error = '';

	async function submit() {
		error = '';
		try {
			await api('/sources/', {
				method: 'POST',
				body: JSON.stringify(form)
			});
			window.location.href = '/admin/sources';
		} catch (e: any) {
			error = e?.message || 'Failed to create';
		}
	}
</script>

<h1 class="mb-3 text-xl font-semibold">New source</h1>
{#if error}<p style="color:red">{error}</p>{/if}

<div style="display:grid; gap:.5rem; max-width:560px">
	<label>Slug <input bind:value={form.slug} required /></label>
	<label>Feed URL <input bind:value={form.feed_url} required /></label>
	<label>Kind <input bind:value={form.kind} /></label>
	<label>Enabled <input type="checkbox" bind:checked={form.enabled} /></label>
	<label>Cadence (min) <input type="number" bind:value={form.cadence_minutes} /></label>
	<label>Timeout (sec) <input type="number" bind:value={form.timeout_sec} /></label>
	<label>Max retries <input type="number" bind:value={form.max_retries} /></label>
	<label>Priority <input type="number" bind:value={form.priority} /></label>
	<label>Notes <textarea bind:value={form.notes} rows="3" /></label>
	<div style="display:flex; gap:.5rem; margin-top:.5rem">
		<button on:click|preventDefault={submit}>Create</button>
		<a href="/admin/sources">Cancel</a>
	</div>
</div>

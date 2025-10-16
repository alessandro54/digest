<script lang="ts">
	import { browser } from '$app/environment';
	import IntrospectView from '$lib/components/IntrospectView.svelte';
	export let data: { introspection: Parameters<typeof IntrospectView>[0]['data'] };

	function nav_back() {
		if (browser) window.history.back();
	}
</script>

<section class="p-4">
	<button
		class="cursor-pointer rounded-md bg-indigo-300 px-2 hover:bg-indigo-500"
		on:click={nav_back}
	>
		Back
	</button>
	<IntrospectView data={data.introspection} />
</section>

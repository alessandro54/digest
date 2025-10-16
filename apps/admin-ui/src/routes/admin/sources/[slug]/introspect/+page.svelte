<script lang="ts">
	import IntrospectView from '$lib/components/IntrospectView.svelte';
	export let data: { introspection: Parameters<typeof IntrospectView>[0]['data'] };
</script>

<IntrospectView data={data.introspection} />

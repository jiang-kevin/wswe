<script lang="ts">
	import RestaurantCard from '$lib/RestaurantCard.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<div>
    {#each data.restaurants as r}
        <RestaurantCard {...r}/>
    {/each}
</div>
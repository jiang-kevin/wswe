<script lang="ts">
    interface Restaurant {
        name: string;
        description: string;
        price: number;
        address: string;
    }
    let r: Restaurant = $props();
</script>

<div>
    {r.name}
</div>
<div>
    {r.description}
</div>
<div>
    {r.price}
</div>
<div>
    {r.address}
</div>
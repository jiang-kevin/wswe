<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<div>
    <form method="POST">
		<label for="name">
			Name
			<input type="text" id="name" name="name">
		</label>
		<br>
		<label for="description">
			Description
			<input type="text" id="description" name="description">
		</label>
		<br>
		<label for="name">
			Price
			<input type="range" min=1 max=5 id="price" name="price">
		</label>
		<br>
		<label for="name">
			Address
			<input type="text" id="address" name="address">
		</label>
		<br><br>
		<button name="submit">Submit</button>
	</form>
</div>
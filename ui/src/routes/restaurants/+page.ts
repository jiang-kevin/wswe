import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch(`http://localhost:8000/api/v1/restaurants`);
	const restaurants = await res.json();

	return { restaurants };
};
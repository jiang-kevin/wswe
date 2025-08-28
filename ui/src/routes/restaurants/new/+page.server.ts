import type { Actions } from "./$types"

export const actions = {
    default: async ({ request, fetch }) => {
        const data = await request.formData();
        const payload = {
            name: data.get("name"),
            description: data.get("description"),
            price: data.get("price"),
            address: data.get("address")
        }
        console.log(JSON.stringify(payload))
        const res = await fetch(`http://localhost:8000/api/v1/restaurants`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        console.log(await res.text());
    }
} satisfies Actions;
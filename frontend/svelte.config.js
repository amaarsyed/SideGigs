import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter(),
		prerender: {
			// Ignore not-found links discovered during crawl so build doesn't fail
			handleHttpError: ({ status }) => {
				if (status === 404) return;
				throw new Error(String(status));
			}
		}
	}
};

export default config;

import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      TMDB_API_KEY: envField.string({
        context: 'server',
        access: 'secret',
        optional: true,
      }),
    }
  }
});

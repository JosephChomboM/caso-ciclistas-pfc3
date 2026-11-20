import { mkdirSync, writeFileSync } from 'node:fs';
mkdirSync('public', { recursive: true });
writeFileSync('public/version.json', JSON.stringify({
  commit: process.env.RENDER_GIT_COMMIT || process.env.GITHUB_SHA || 'development',
}));

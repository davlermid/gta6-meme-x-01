import { readFileSync, writeFileSync, mkdirSync, existsSync, cpSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR || '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || '/output';

try {
    const postPath = join(BOT_DIR, 'POST.json');
    let raw: string;
    try {
        raw = readFileSync(postPath, 'utf-8');
    } catch {
        console.error('Cannot read POST.json');
        process.exit(1);
    }

    let data: unknown;
    try {
        data = JSON.parse(raw);
    } catch {
        console.error('Invalid JSON in POST.json');
        process.exit(1);
    }

    if (
        typeof data !== 'object' ||
        data === null ||
        !('url' in data) ||
        typeof (data as Record<string, unknown>).url !== 'string' ||
        (data as Record<string, unknown>).url.length === 0
    ) {
        console.error('POST.json must contain a non-empty "url" string');
        process.exit(1);
    }

    try {
        mkdirSync(OUTPUT_DIR, { recursive: true });
    } catch {
        console.error('Cannot create output directory');
        process.exit(1);
    }

    const outPath = join(OUTPUT_DIR, 'POST.json');
    try {
        writeFileSync(outPath, raw);
    } catch {
        console.error('Cannot write POST.json to output directory');
        process.exit(1);
    }

    process.exit(0);
} catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(msg);
    process.exit(1);
}
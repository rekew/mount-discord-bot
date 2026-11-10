import { existsSync, mkdirSync, readdirSync, renameSync, statSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

const IMAGES_DIR = './images';
const ORIGINALS_DIR = './images/original';
const TARGET_WIDTH = 1100;
const QUALITY = 90;

const isPng = (name) => /^\d+\.\d+\.png$/i.test(name);

mkdirSync(ORIGINALS_DIR, { recursive: true });

for (const file of readdirSync(IMAGES_DIR).filter(isPng)) {
    const src = path.join(IMAGES_DIR, file);
    const dest = path.join(ORIGINALS_DIR, file);
    if (!existsSync(dest)) renameSync(src, dest);
}

const originals = readdirSync(ORIGINALS_DIR).filter(isPng).sort();
if (!originals.length) {
    console.log('no png originals found');
    process.exit(0);
}

const mb = (bytes) => (bytes / 1024 / 1024).toFixed(2) + 'MB';
let totalBefore = 0;
let totalAfter = 0;

for (const file of originals) {
    const input = path.join(ORIGINALS_DIR, file);
    const output = path.join(IMAGES_DIR, file.replace(/\.png$/i, '.webp'));

    const result = spawnSync('cwebp', [
        '-q', String(QUALITY),
        '-m', '6',
        '-sharp_yuv',
        '-metadata', 'none',
        '-resize', String(TARGET_WIDTH), '0',
        '-resize_mode', 'down_only',
        input,
        '-o', output,
    ], { encoding: 'utf8' });

    if (result.status !== 0) {
        console.error(`failed: ${file}\n${result.stderr || result.stdout}`);
        continue;
    }

    const before = statSync(input).size;
    const after = statSync(output).size;
    totalBefore += before;
    totalAfter += after;

    const saved = (100 - (after / before) * 100).toFixed(1);
    console.log(`${file} ${mb(before)} -> ${mb(after)} (-${saved}%)`);
}

const totalSaved = totalBefore ? (100 - (totalAfter / totalBefore) * 100).toFixed(1) : '0';
console.log(`\ntotal ${mb(totalBefore)} -> ${mb(totalAfter)} (-${totalSaved}%)`);

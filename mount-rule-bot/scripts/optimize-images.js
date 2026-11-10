/**
 * Convert original rule images into optimized WebP files.
 * @module scripts/optimize-images
 */

// Node.js modules
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readdirSync, renameSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** Absolute path to the optimized rule images. */
const IMAGES_DIR = fileURLToPath(new URL('../images/', import.meta.url));

/** Absolute path to the repository-original PNG images. */
const ORIGINALS_DIR = path.join(IMAGES_DIR, 'original');

const TARGET_WIDTH = 1100;
const QUALITY = 90;

/**
 * Check whether a file is a rule image in PNG format.
 * @param {string} name File name to test.
 * @returns {boolean} `true` for names such as `1.1.png`.
 */
const isPng = (name) => /^\d+\.\d+\.png$/i.test(name);

/**
 * Format a byte count as megabytes.
 * @param {number} bytes Byte count.
 * @returns {string} Formatted size in megabytes.
 */
const toMegabytes = (bytes) => `${(bytes / 1024 / 1024).toFixed(2)}MB`;

/**
 * Move PNG files from the images directory into the originals directory.
 * @returns {void}
 */
function movePngsToOriginals() {
    mkdirSync(ORIGINALS_DIR, { recursive: true });

    for (const file of readdirSync(IMAGES_DIR).filter(isPng)) {
        const source = path.join(IMAGES_DIR, file);
        const destination = path.join(ORIGINALS_DIR, file);

        if (!existsSync(destination)) {
            renameSync(source, destination);
        }
    }
}

/**
 * Convert a single original image and accumulate size statistics.
 * @param {string} file PNG file name.
 * @param {{ before: number, after: number, failed: number }} totals Running totals.
 * @returns {void}
 */
function convertImage(file, totals) {
    const input = path.join(ORIGINALS_DIR, file);
    const output = path.join(IMAGES_DIR, file.replace(/\.png$/i, '.webp'));

    const result = spawnSync(
        'cwebp',
        [
            '-q',
            String(QUALITY),
            '-m',
            '6',
            '-sharp_yuv',
            '-metadata',
            'none',
            '-resize',
            String(TARGET_WIDTH),
            '0',
            '-resize_mode',
            'down_only',
            input,
            '-o',
            output,
        ],
        { encoding: 'utf8' },
    );

    if (result.status !== 0) {
        console.error(`failed: ${file}\n${result.stderr || result.stdout}`);
        totals.failed += 1;
        return;
    }

    const before = statSync(input).size;
    const after = statSync(output).size;
    totals.before += before;
    totals.after += after;

    const saved = (100 - (after / before) * 100).toFixed(1);
    console.log(`${file} ${toMegabytes(before)} -> ${toMegabytes(after)} (-${saved}%)`);
}

/**
 * Optimize every original rule image and report the total size reduction.
 * @returns {void}
 */
export function runOptimizeImages() {
    movePngsToOriginals();

    const originals = readdirSync(ORIGINALS_DIR).filter(isPng).sort();

    if (!originals.length) {
        console.log('no png originals found');
        return;
    }

    const totals = { before: 0, after: 0, failed: 0 };

    for (const file of originals) {
        convertImage(file, totals);
    }

    const saved = totals.before ? (100 - (totals.after / totals.before) * 100).toFixed(1) : '0';
    console.log(
        `\ntotal ${toMegabytes(totals.before)} -> ${toMegabytes(totals.after)} (-${saved}%)`,
    );

    if (totals.failed > 0) {
        process.exitCode = 1;
    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    runOptimizeImages();
}

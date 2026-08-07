'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const ASSETS = path.join(ROOT, 'assets');

function files(relativeDir, extension) {
    return fs.readdirSync(path.join(ASSETS, relativeDir))
        .filter(file => file.endsWith(extension))
        .sort();
}

function assertImage(relativePath) {
    const file = path.join(ASSETS, relativePath);
    assert.ok(fs.existsSync(file), `missing assets/${relativePath}`);
    const data = fs.readFileSync(file);
    assert.ok(data.length >= 12, `empty or truncated assets/${relativePath}`);
    if (relativePath.endsWith('.webp')) {
        assert.strictEqual(data.subarray(0, 4).toString('ascii'), 'RIFF', `invalid WebP: assets/${relativePath}`);
        assert.strictEqual(data.subarray(8, 12).toString('ascii'), 'WEBP', `invalid WebP: assets/${relativePath}`);
    } else if (relativePath.endsWith('.png')) {
        assert.deepStrictEqual([...data.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10], `invalid PNG: assets/${relativePath}`);
    } else if (relativePath.endsWith('.ico')) {
        assert.deepStrictEqual([...data.subarray(0, 4)], [0, 0, 1, 0], `invalid ICO: assets/${relativePath}`);
    }
}

const families = [
    ['avatars', '.webp', 30],
    ['buildings/companies', '.webp', 193],
    ['buildings/companies/thumb', '.webp', 193],
    ['buildings/walls', '.webp', 16],
    ['buildings/walls_lit', '.webp', 96],
    ['tutorial', '.png', 9],
    ['tutorial', '.webp', 9],
    ['creatures', '.webp', 25],
];

for (const [dir, extension, expected] of families) {
    const familyFiles = files(dir, extension);
    assert.strictEqual(familyFiles.length, expected, `${dir} should contain ${expected} ${extension} files`);
    for (const file of familyFiles) assertImage(`${dir}/${file}`);
}

// Derived variants must stay 1:1 with their sources — the game builds a thumb URL
// from the company id alone, so a missing thumb is a broken card, not a fallback.
// (scripts/genDerivedAssets.py regenerates both families.)
const companyIds = files('buildings/companies', '.webp');
assert.deepStrictEqual(
    files('buildings/companies/thumb', '.webp'),
    companyIds,
    'every company image needs a matching thumb — run scripts/genDerivedAssets.py',
);
assert.deepStrictEqual(
    files('tutorial', '.webp'),
    files('tutorial', '.png').map(file => file.replace(/\.png$/, '.webp')),
    'every tutorial guide PNG needs a matching WebP — run scripts/genDerivedAssets.py',
);

// A thumb exists to be small. If one ever comes out heavier than a modest budget the
// generator has regressed (wrong width, wrong quality, or a source that is not 2:1).
for (const file of companyIds) {
    const bytes = fs.statSync(path.join(ASSETS, 'buildings/companies/thumb', file)).size;
    assert.ok(bytes < 120 * 1024, `thumb too large (${Math.round(bytes / 1024)} KB): ${file}`);
}

for (const file of [
    'branding/apple-touch-icon.png',
    'branding/editor-showcase.png',
    'branding/favicon-16x16.png',
    'branding/favicon-32x32.png',
    'branding/favicon.ico',
    'branding/mint-street-logo.png',
]) assertImage(file);

console.log('✓ CDN assets: 577 valid images (incl. 193 company thumbs + 9 tutorial WebP)');

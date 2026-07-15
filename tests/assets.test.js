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
    ['buildings/walls', '.webp', 16],
    ['buildings/walls_lit', '.webp', 96],
    ['tutorial', '.png', 9],
];

for (const [dir, extension, expected] of families) {
    const familyFiles = files(dir, extension);
    assert.strictEqual(familyFiles.length, expected, `${dir} should contain ${expected} ${extension} files`);
    for (const file of familyFiles) assertImage(`${dir}/${file}`);
}

for (const file of [
    'branding/apple-touch-icon.png',
    'branding/editor-showcase.png',
    'branding/favicon-16x16.png',
    'branding/favicon-32x32.png',
    'branding/favicon.ico',
    'branding/mint-street-logo.png',
]) assertImage(file);

console.log('✓ CDN assets: 350 valid images');

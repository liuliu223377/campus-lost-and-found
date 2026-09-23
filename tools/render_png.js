// 把 prototype/svg/*.svg 渲染成 PNG（可选步骤，用于：博客配图 / 导入只支持图片的原型工具）
// 用法: node tools/render_png.js
const fs = require('fs');
const path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const BASE = path.join(__dirname, '..');
const SRC = path.join(BASE, 'prototype', 'svg');
const OUT = path.join(BASE, 'prototype', 'png');
const SCALE = 2; // 2 倍图，博客上更清晰

if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

for (const f of fs.readdirSync(SRC).filter((n) => n.endsWith('.svg'))) {
  const svg = fs.readFileSync(path.join(SRC, f), 'utf8');
  const r = new Resvg(svg, {
    fitTo: { mode: 'zoom', value: SCALE },
    font: { loadSystemFonts: true, defaultFontFamily: 'Microsoft YaHei' },
  });
  const png = r.render().asPng();
  fs.writeFileSync(path.join(OUT, f.replace(/\.svg$/, '.png')), png);
  console.log('rendered:', f.replace(/\.svg$/, '.png'));
}
console.log('done ->', OUT);

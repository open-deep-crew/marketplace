const fs = require('fs');

// Fix acpx kiro agent command
const acpxPath = 'C:/Users/y2830/AppData/Roaming/npm/node_modules/acpx/dist/cli.js';
let acpxContent = fs.readFileSync(acpxPath, 'utf8');
acpxContent = acpxContent.replace('kiro: "kiro-cli acp"', 'kiro: "kiro acp"');
fs.writeFileSync(acpxPath, acpxContent, 'utf8');
console.log('acpx kiro fix done');

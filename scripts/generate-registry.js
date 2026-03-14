#!/usr/bin/env node

/**
 * Registry Generator for Claude Code Marketplaces
 *
 * 数据来源：
 * 1. marketplace.json - plugin 完整配置 + atom 引用关系
 * 2. atoms/ 目录文件扫描 - 所有实际存在的 atoms
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const MARKETPLACE_PATH = path.join(ROOT_DIR, '.claude-plugin/marketplace.json');
const ATOMS_DIR = path.join(ROOT_DIR, 'atoms');
const OUTPUT_DIR = path.join(ROOT_DIR, 'public/generated');
const OUTPUT_PATH = path.join(OUTPUT_DIR, 'registry.json');
const ATOMS_DEST = path.join(ROOT_DIR, 'public/atoms');

// ─── 文件系统扫描 ────────────────────────────────────────────────────────────

/**
 * 递归复制目录
 */
function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    entry.isDirectory() ? copyDirectory(srcPath, destPath) : fs.copyFileSync(srcPath, destPath);
  }
}

/**
 * 扫描 atoms/ 目录，返回所有 atom 的基础信息
 * - commands/: 每个 .md 文件是一个 command atom
 * - agents/:   每个 .md 文件是一个 agent atom
 * - skills/:   每个子目录（含 SKILL.md）是一个 skill atom
 * - hooks/:    每个 .sh 文件是一个 hook atom
 * - mcps/:     每个 mcp.json 中的 server key 是一个 mcp atom
 *
 * @returns {Map<string, object>} key = 相对路径（如 atoms/commands/bugfix-expert.md）或 mcp server name
 */
function scanAtomsDir(atomsDir) {
  const atomsMap = new Map();

  const subDirs = {
    commands: 'command',
    agents: 'agent',
    hooks: 'hook',
  };

  // commands / agents / hooks：扫描文件
  for (const [dir, type] of Object.entries(subDirs)) {
    const dirPath = path.join(atomsDir, dir);
    if (!fs.existsSync(dirPath)) continue;

    for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
      if (!entry.isFile()) continue;
      if (!/\.(md|sh)$/.test(entry.name)) continue;

      const relPath = `atoms/${dir}/${entry.name}`;
      const name = entry.name.replace(/\.(md|sh)$/, '');
      atomsMap.set(relPath, { type, name, path: relPath, usedBy: [] });
    }
  }

  // skills：扫描子目录，要求含 SKILL.md
  const skillsDir = path.join(atomsDir, 'skills');
  if (fs.existsSync(skillsDir)) {
    for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const skillMdPath = path.join(skillsDir, entry.name, 'SKILL.md');
      if (!fs.existsSync(skillMdPath)) continue;

      const relPath = `atoms/skills/${entry.name}/SKILL.md`;
      atomsMap.set(relPath, { type: 'skill', name: entry.name, path: relPath, usedBy: [] });
    }
  }

  // mcps：解析 mcp.json 中的每个 server
  const mcpsDir = path.join(atomsDir, 'mcps');
  if (fs.existsSync(mcpsDir)) {
    for (const entry of fs.readdirSync(mcpsDir, { withFileTypes: true })) {
      if (!entry.isFile() || !/\.json$/.test(entry.name)) continue;
      
      const mcpJsonPath = path.join(mcpsDir, entry.name);
      try {
        const mcpConfig = JSON.parse(fs.readFileSync(mcpJsonPath, 'utf-8'));
        const servers = mcpConfig.mcpServers || {};
        
        for (const serverName of Object.keys(servers)) {
          const relPath = `atoms/mcps/${entry.name}`;
          // 使用 serverName 作为 key，这样可以通过 plugin 的 mcpServers 引用
          atomsMap.set(serverName, { 
            type: 'mcp', 
            name: serverName, 
            path: relPath, 
            usedBy: [] 
          });
        }
      } catch (error) {
        console.warn(`   ⚠ Failed to parse ${mcpJsonPath}: ${error.message}`);
      }
    }
  }

  return atomsMap;
}

// ─── marketplace.json 解析 ───────────────────────────────────────────────────

function resolveEnvVars(str) {
  return str ? str.replace(/\$\{CLAUDE_PLUGIN_ROOT\}\/?/g, '') : str;
}

function normalizeSkillPath(p) {
  if (p.endsWith('SKILL.md') || p.endsWith('skill.md')) return p;
  return `${p.replace(/\/$/, '')}/SKILL.md`;
}

/**
 * 从 hooks 配置中提取所有 hook 文件路径
 */
function extractHookPaths(hooksConfig) {
  if (!hooksConfig || typeof hooksConfig !== 'object') return [];
  const paths = [];
  for (const eventHooks of Object.values(hooksConfig)) {
    if (!Array.isArray(eventHooks)) continue;
    for (const matcher of eventHooks) {
      if (!Array.isArray(matcher.hooks)) continue;
      for (const hook of matcher.hooks) {
        if (hook.type === 'command' && hook.command) {
          paths.push(resolveEnvVars(hook.command));
        }
      }
    }
  }
  return paths;
}

/**
 * 从 plugin 配置中提取所有引用的 atom 路径（统一为相对路径）
 */
function extractPluginAtomPaths(plugin) {
  const paths = [];

  const normalize = (p) => resolveEnvVars(p).replace(/^\.\//, '');

  for (const p of plugin.commands || []) paths.push(normalize(p));
  for (const p of plugin.agents || []) paths.push(normalize(p));
  for (const p of plugin.skills || []) paths.push(normalizeSkillPath(normalize(p)));
  for (const p of extractHookPaths(plugin.hooks)) paths.push(normalize(p));
  
  // 添加 mcpServers 的引用（直接使用 server name 作为 key）
  if (plugin.mcpServers && typeof plugin.mcpServers === 'object') {
    for (const serverName of Object.keys(plugin.mcpServers)) {
      paths.push(serverName);
    }
  }

  return paths;
}

// ─── 主流程 ──────────────────────────────────────────────────────────────────

function generateRegistry() {
  console.log('🚀 Starting registry generation...\n');

  // 1. 读取 marketplace.json
  console.log('📖 Reading marketplace.json...');
  if (!fs.existsSync(MARKETPLACE_PATH)) {
    console.error(`❌ marketplace.json not found at ${MARKETPLACE_PATH}`);
    process.exit(1);
  }
  const marketplace = JSON.parse(fs.readFileSync(MARKETPLACE_PATH, 'utf-8'));
  const plugins = marketplace.plugins || [];
  console.log(`   ✓ Found ${plugins.length} plugins\n`);

  // 2. 扫描 atoms/ 目录
  console.log('🔍 Scanning atoms directory...');
  const atomsMap = scanAtomsDir(ATOMS_DIR);
  console.log(`   ✓ Found ${atomsMap.size} atoms on disk\n`);

  // 3. 根据 marketplace.json 的引用关系，填充 usedBy
  console.log('🔗 Resolving plugin → atom references...');
  for (const plugin of plugins) {
    const atomPaths = extractPluginAtomPaths(plugin);
    for (const atomPath of atomPaths) {
      if (atomsMap.has(atomPath)) {
        const atom = atomsMap.get(atomPath);
        if (!atom.usedBy.includes(plugin.name)) {
          atom.usedBy.push(plugin.name);
        }
      } else {
        console.warn(`   ⚠ [${plugin.name}] references missing atom: ${atomPath}`);
      }
    }
  }
  console.log('   ✓ References resolved\n');

  // 4. 按类型分组 atoms
  const grouped = { commands: [], agents: [], skills: [], hooks: [], mcps: [] };
  for (const atom of atomsMap.values()) {
    const key = atom.type === 'command' ? 'commands'
      : atom.type === 'agent' ? 'agents'
      : atom.type === 'skill' ? 'skills'
      : atom.type === 'mcp' ? 'mcps'
      : 'hooks';
    grouped[key].push(atom);
  }
  for (const arr of Object.values(grouped)) arr.sort((a, b) => a.name.localeCompare(b.name));

  // 5. 统计
  const stats = {
    totalAtoms: atomsMap.size,
    totalPlugins: plugins.length,
    byType: {
      commands: grouped.commands.length,
      agents: grouped.agents.length,
      skills: grouped.skills.length,
      hooks: grouped.hooks.length,
      mcps: grouped.mcps.length,
    },
  };

  // 6. plugins 保留 marketplace.json 中的所有字段
  const pluginSummaries = plugins.map(plugin => ({
    ...plugin,
    // 追加 atomsCount 统计（不覆盖原有字段）
    atomsCount: {
      commands: (plugin.commands || []).length,
      agents: (plugin.agents || []).length,
      skills: (plugin.skills || []).length,
      hooks: extractHookPaths(plugin.hooks).length,
      mcps: plugin.mcpServers ? Object.keys(plugin.mcpServers).length : 0,
    },
  }));

  // 7. 构建 registry
  const registry = {
    metadata: {
      generatedAt: new Date().toISOString(),
      version: marketplace.version || '1.0.0',
      marketplace: marketplace.name || 'claude-code-marketplaces',
    },
    stats,
    atoms: grouped,
    plugins: pluginSummaries,
  };

  // 8. 写入 registry.json
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(registry, null, 2), 'utf-8');
  console.log(`💾 Registry written to: ${OUTPUT_PATH}\n`);

  // 9. 同步 atoms 到 public/atoms
  console.log('📁 Copying atoms to public/atoms...');
  if (fs.existsSync(ATOMS_DIR)) {
    if (fs.existsSync(ATOMS_DEST)) fs.rmSync(ATOMS_DEST, { recursive: true, force: true });
    copyDirectory(ATOMS_DIR, ATOMS_DEST);
    console.log(`   ✓ Copied to: ${ATOMS_DEST}\n`);
  } else {
    console.warn(`   ⚠ atoms directory not found: ${ATOMS_DIR}\n`);
  }

  console.log('✅ Done!\n');
  console.log(`   Plugins: ${stats.totalPlugins}  |  Atoms: ${stats.totalAtoms}`);
  console.log(`   commands=${stats.byType.commands} agents=${stats.byType.agents} skills=${stats.byType.skills} hooks=${stats.byType.hooks} mcps=${stats.byType.mcps}\n`);
}

try {
  generateRegistry();
} catch (error) {
  console.error('\n❌ Error:', error.message);
  console.error(error.stack);
  process.exit(1);
}

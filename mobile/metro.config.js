/* Expo's defaults, plus the one thing this app needs that a plain project does not:
 * `@aruvi/shared` is a symlink to ../packages/shared (a `file:` dependency — mobile/ is NOT an
 * npm workspace, see the root package.json), so Metro must watch that folder for edits and hot
 * reloads. Extending, not replacing, the defaults keeps expo-doctor's Metro check green.
 *
 * Resolution is pinned to THIS app's node_modules (no hierarchical lookup up to the repo
 * root): the root holds the web's React 18, and a native module resolving React from there
 * would give the app two Reacts. The shared package imports nothing, so it needs no lookup. */
const { getDefaultConfig } = require("expo/metro-config");
const path = require("path");
const config = getDefaultConfig(__dirname);
config.watchFolders = [...(config.watchFolders || []), path.resolve(__dirname, "../packages/shared")];
config.resolver.nodeModulesPaths = [path.resolve(__dirname, "node_modules")];
config.resolver.disableHierarchicalLookup = true;
module.exports = config;

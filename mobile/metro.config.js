/* Expo's default Metro config already understands the npm workspace at the repo root (SDK 52+
 * derives watchFolders and node_modules paths from it) and resolves package.json `exports`,
 * which is how `@aruvi/shared/format` reaches packages/shared/src/format.js. Spelled out here
 * only so a future SDK change has one place to look. */
const { getDefaultConfig } = require("expo/metro-config");
const path = require("path");
const root = path.resolve(__dirname, "..");
const config = getDefaultConfig(__dirname);
config.watchFolders = [root];
config.resolver.nodeModulesPaths = [path.join(__dirname, "node_modules"), path.join(root, "node_modules")];
module.exports = config;

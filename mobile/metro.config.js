/* Expo's defaults, plus the one thing this app needs that a plain project does not:
 * `@aruvi/shared` is a symlink to ../packages/shared (a `file:` dependency — mobile/ is NOT an
 * npm workspace, see the root package.json), so Metro must watch that folder for edits and hot
 * reloads. Extending, not replacing, the defaults keeps expo-doctor's Metro check green.
 * No resolver overrides: the repo root holds none of the phone's packages (that was the point
 * of leaving the workspace), and the shared package imports nothing, so ordinary lookup from
 * mobile/node_modules is already the right answer. */
const { getDefaultConfig } = require("expo/metro-config");
const path = require("path");
const config = getDefaultConfig(__dirname);
config.watchFolders = [...(config.watchFolders || []), path.resolve(__dirname, "../packages/shared")];
module.exports = config;

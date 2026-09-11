/* ───────── the storage shim (Track D step 1, 2026-09-11) ─────────
 *
 * Every client cache in this package — section state, section history, the Ask Meyy bank,
 * the signed-in user id — was written against the browser's localStorage as a SYNCHRONOUS
 * optimistic cache in front of the server (sectionState.js's header says why: readHistory /
 * readLocalSection run during render and can never become promises). The phone keeps that
 * contract with MMKV, which is synchronous too; AsyncStorage would break it.
 *
 * So this module is the one seam: a tiny synchronous key/value interface, and `setStorage`
 * to install the platform's implementation once at boot —
 *   web    → `webStorage()` below (localStorage), from web/app/lib/shared-setup.js
 *   phone  → an MMKV adapter, from the Expo app's boot module
 * Until one is installed, an in-memory map stands in, so node tests and SSR passes work
 * without any platform at all (nothing is cached across a reload there — the server is the
 * authority regardless, which is the whole design of these caches).
 *
 * The interface is deliberately localStorage's minus the index API: `keys()` replaces the
 * `length`/`key(i)` pair, which MMKV never had. Calls may throw exactly as localStorage may
 * (private mode, quota) — every caller already guards with try/catch. */

const memory = new Map();
const memoryStorage = {
  getItem: (k) => (memory.has(k) ? memory.get(k) : null),
  setItem: (k, v) => { memory.set(k, String(v)); },
  removeItem: (k) => { memory.delete(k); },
  keys: () => Array.from(memory.keys()),
};

let impl = memoryStorage;

/* Install the platform's storage: { getItem, setItem, removeItem, keys } — all synchronous. */
export function setStorage(s) {
  impl = s || memoryStorage;
}

/* Where the current storage came from — "memory" until setStorage ran. Read by callers that
 * want to warn in dev when a screen mounted before boot installed the real one. */
export const storage = {
  getItem: (k) => impl.getItem(k),
  setItem: (k, v) => impl.setItem(k, v),
  removeItem: (k) => impl.removeItem(k),
  keys: () => impl.keys(),
  isMemory: () => impl === memoryStorage,
};

/* The browser adapter. Returns null outside a browser (SSR), which setStorage treats as
 * "keep the memory fallback". */
export function webStorage() {
  if (typeof window === "undefined" || !window.localStorage) return null;
  const ls = window.localStorage;
  return {
    getItem: (k) => ls.getItem(k),
    setItem: (k, v) => ls.setItem(k, v),
    removeItem: (k) => ls.removeItem(k),
    keys: () => {
      const out = [];
      for (let i = 0; i < ls.length; i += 1) { const k = ls.key(i); if (k != null) out.push(k); }
      return out;
    },
  };
}

/* Remove every key starting with one of `prefixes`. Returns the count. Shared by the
 * clear-on-sign-out paths (sectionState, sectionHistory, bank) so the phone's "sign-out must
 * clear every per-teacher cache" rule (live walk, 2026-09-11) has one implementation. */
export function removeByPrefix(prefixes) {
  let removed = 0;
  try {
    const doomed = storage.keys().filter((k) => prefixes.some((p) => k.startsWith(p)));
    doomed.forEach((k) => { storage.removeItem(k); removed += 1; });
  } catch { /* private mode / storage disabled — the server is the authority regardless */ }
  return removed;
}

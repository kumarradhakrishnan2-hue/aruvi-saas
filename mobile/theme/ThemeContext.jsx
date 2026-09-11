/* Theme = the OS scheme + the teacher's in-app override (Auto/Light/Dark), the same three-way
 * the web keeps in localStorage under `aruvi-theme`. Stored through the shared storage shim so
 * the key survives sign-out (it is a device preference, not a teacher cache — clearTeacherCaches
 * does not name it). `t` is the resolved token set for the effective scheme. */
import { createContext, useContext, useMemo, useState } from "react";
import { useColorScheme } from "react-native";
import { storage } from "@aruvi/shared/storage";
import { light, dark } from "./tokens";

const KEY = "aruvi-theme";
const ThemeCtx = createContext({ t: light, scheme: "light", pref: "system", setPref: () => {} });

export function ThemeProvider({ children }) {
  const os = useColorScheme() || "light";
  const [pref, setPrefState] = useState(() => { try { return storage.getItem(KEY) || "system"; } catch { return "system"; } });
  const setPref = (p) => { setPrefState(p); try { storage.setItem(KEY, p); } catch {} };
  const scheme = pref === "system" ? os : pref;
  const value = useMemo(() => ({ t: scheme === "dark" ? dark : light, scheme, pref, setPref }), [scheme, pref]);
  return <ThemeCtx.Provider value={value}>{children}</ThemeCtx.Provider>;
}

export const useTheme = () => useContext(ThemeCtx);

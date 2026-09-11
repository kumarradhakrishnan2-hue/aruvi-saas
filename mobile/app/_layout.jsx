/* Root layout: boot the shared package FIRST (module order — lib/boot installs storage, API,
 * Supabase before any screen module evaluates), load the three faces, hold the splash until
 * they are in, then the theme and a plain stack. Screens decide where to go (app/index.jsx). */
import "../lib/boot";
import { useEffect } from "react";
import { Stack } from "expo-router";
import { useFonts } from "expo-font";
import * as SplashScreen from "expo-splash-screen";
import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { ThemeProvider, useTheme } from "../theme/ThemeContext";
import { FONT_MAP } from "../theme/fonts";

SplashScreen.preventAutoHideAsync().catch(() => {});

function Shell() {
  const { t, scheme } = useTheme();
  return (
    <>
      {/* the bar is pine in both themes, so the status bar is always light-on-dark */}
      <StatusBar style="light" backgroundColor={t.bar_fill} />
      <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: t.paper }, animation: "fade" }} />
    </>
  );
}

export default function RootLayout() {
  const [loaded, error] = useFonts(FONT_MAP);
  useEffect(() => { if (loaded || error) SplashScreen.hideAsync().catch(() => {}); }, [loaded, error]);
  if (!loaded && !error) return null;
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <Shell />
      </ThemeProvider>
    </SafeAreaProvider>
  );
}

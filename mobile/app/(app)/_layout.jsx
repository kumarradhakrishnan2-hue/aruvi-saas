/* The signed-in shell. Step 2 holds one screen; step 3 puts LessonView here and step 4 the two
 * tabs (My Classes / My Lessons — no sidebar, no hamburger, CLAUDE.md §4). Redirects to the
 * front door when there is no user, so a deep link cannot land inside without an identity. */
import { Redirect, Stack } from "expo-router";
import { getUser } from "@aruvi/shared/format";
import { useTheme } from "../../theme/ThemeContext";

export default function AppLayout() {
  const { t } = useTheme();
  if (!getUser()) return <Redirect href="/login" />;
  return <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: t.paper } }} />;
}

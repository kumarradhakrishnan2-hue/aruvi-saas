/* The gate. getUser() is synchronous from the storage shim, so this renders nothing and
 * redirects at once — no flash of the front door for a signed-in teacher. */
import { Redirect } from "expo-router";
import { getUser } from "@aruvi/shared/format";

export default function Index() {
  return <Redirect href={getUser() ? "/(app)" : "/login"} />;
}

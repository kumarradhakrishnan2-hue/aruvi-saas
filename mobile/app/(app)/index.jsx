/* Step 2's proof screen: the bearer reaches the API. Shows who is signed in, what /entitlement
 * and /readiness say about her (a missing value is an em-dash, never a guess — CLAUDE.md §4),
 * the theme switch, and Sign out. Replaced by My Classes in step 4; nothing here is product.
 * A LOADING state is shown until both calls return — the live walk's first finding (a false
 * "Pick a chapter" flashed on a real network) is designed in from the first screen. */
import { useEffect, useState } from "react";
import { View, Text, ScrollView, ActivityIndicator, Pressable, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import { getUser, getJSON, fetchEntitlement } from "@aruvi/shared/format";
import { signOutAuth } from "@aruvi/shared/auth";
import { clearTeacherCaches } from "@aruvi/shared/signout";
import { API } from "@aruvi/shared/config";
import Bar from "../../components/Bar";
import { Button } from "../../components/ui";
import { useTheme } from "../../theme/ThemeContext";
import { type } from "../../theme/type";

const dash = (v) => (v === null || v === undefined || v === "" ? "—" : String(v));

export default function Home() {
  const { t, pref, setPref } = useTheme();
  const router = useRouter();
  const user = getUser();
  const [state, setState] = useState({ loading: true, ent: null, readiness: null, err: "" });

  useEffect(() => {
    let alive = true;
    (async () => {
      const ent = await fetchEntitlement();
      let readiness = null, err = "";
      try { readiness = (await getJSON("/readiness"))?.readiness || null; }
      catch (e) { if (String(e.message) === "401") err = "Your sign-in has expired — please sign in again."; else if (String(e.message) !== "404") err = "Couldn't reach Meyy right now."; }
      if (alive) setState({ loading: false, ent, readiness, err });
    })();
    return () => { alive = false; };
  }, []);

  const signOut = async () => {
    await signOutAuth();
    clearTeacherCaches(["setup_check_pending_", "mylessons_subject_", "mylessons_class_", "allocations_"]);
    router.replace("/login");
  };

  const subjects = state.readiness?.subjects || [];
  return (
    <View style={{ flex: 1, backgroundColor: t.paper }}>
      <Bar />
      <ScrollView contentContainerStyle={s.body}>
        <Text style={[type.label, { color: t.ink_soft }]}>Signed in as</Text>
        <Text style={[type.title, { color: t.ink, marginTop: 4 }]}>{user}</Text>
        <Text style={[type.small, { color: t.ink_soft, marginTop: 4 }]}>{API}</Text>

        {state.loading ? (
          <View style={s.loading}><ActivityIndicator color={t.pine} /><Text style={[type.small, { color: t.ink_soft, marginLeft: 10 }]}>Fetching your record…</Text></View>
        ) : (
          <>
            {state.err ? <Text style={[type.body, { color: t.danger, marginTop: 18 }]}>{state.err}</Text> : null}
            <View style={[s.card, { backgroundColor: t.card_doc, borderColor: t.card_doc_edge }]}>
              <Text style={[type.label, { color: t.ink_soft }]}>Plan</Text>
              <Text style={[type.body, { color: t.ink }]}>
                {state.ent ? `${dash(state.ent.status)}${state.ent.enforced ? ` · ${dash(state.ent.trial_chapters_used)} of ${dash(state.ent.trial_chapter_cap)} trial chapters used` : ""}` : "—"}
              </Text>
            </View>
            <View style={[s.card, { backgroundColor: t.card_doc, borderColor: t.card_doc_edge }]}>
              <Text style={[type.label, { color: t.ink_soft }]}>Teaching profile</Text>
              {subjects.length ? subjects.map((sub, i) => (
                <Text key={i} style={[type.body, { color: t.ink }]}>
                  {dash(sub.name)} · {(sub.grades || []).map((g) => `Class ${g.grade ? g.grade.toUpperCase() : "—"}`).join(", ") || "—"}
                </Text>
              )) : <Text style={[type.body, { color: t.ink_soft }]}>No profile yet — first run comes in step 5.</Text>}
            </View>
          </>
        )}

        <Text style={[type.label, { color: t.ink_soft, marginTop: 28 }]}>Theme</Text>
        <View style={s.segs}>
          {[["system", "Auto"], ["light", "Light"], ["dark", "Dark"]].map(([v, label]) => (
            <Pressable key={v} onPress={() => setPref(v)} accessibilityRole="button" accessibilityState={{ selected: pref === v }}
              style={[s.seg, { borderColor: t.edge, backgroundColor: pref === v ? t.tint_pine : t.paper_2 }]}>
              <Text style={[type.small, { color: pref === v ? t.pine : t.ink }]}>{label}</Text>
            </Pressable>
          ))}
        </View>
        <Button kind="link" title="Sign out" onPress={signOut} style={{ marginTop: 28, alignSelf: "flex-start" }} />
      </ScrollView>
    </View>
  );
}

const s = StyleSheet.create({
  body: { paddingHorizontal: 20, paddingVertical: 22, paddingBottom: 40 },
  loading: { flexDirection: "row", alignItems: "center", marginTop: 24 },
  card: { borderWidth: 1, borderRadius: 10, padding: 14, marginTop: 14, gap: 4 },
  segs: { flexDirection: "row", gap: 8, marginTop: 8 },
  seg: { flex: 1, borderWidth: 1, borderRadius: 8, paddingVertical: 10, alignItems: "center" },
});

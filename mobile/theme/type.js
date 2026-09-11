/* Text roles, once. Sizes are the web's phone-width values (globals.css @media ≤600px). */
import { display, body, mono } from "./fonts";

export const type = {
  headline: { fontFamily: display(600), fontSize: 26, lineHeight: 32 },   // .ob-headline
  title:    { fontFamily: display(500), fontSize: 22, lineHeight: 28 },   // .ob-title
  h2:       { fontFamily: display(500), fontSize: 18, lineHeight: 24 },
  body:     { fontFamily: body(400), fontSize: 17, lineHeight: 25 },
  bodyStrong: { fontFamily: body(600), fontSize: 17, lineHeight: 25 },
  bodyItalic: { fontFamily: body(400, true), fontSize: 17, lineHeight: 25 },
  small:    { fontFamily: body(400), fontSize: 14, lineHeight: 20 },
  label:    { fontFamily: mono(500), fontSize: 12, lineHeight: 16, letterSpacing: 0.6, textTransform: "uppercase" },
  mono:     { fontFamily: mono(400), fontSize: 15, lineHeight: 22 },
  button:   { fontFamily: body(600), fontSize: 17, lineHeight: 22 },
};

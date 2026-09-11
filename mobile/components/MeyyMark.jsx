/* The MEYY wordmark — the same path data as web/app/components/MeyyMark.jsx (viewBox trimmed
 * to the ink, 12.5 0 413 110), drawn with react-native-svg. `color` is the stroke; `dot` the
 * two dots' fill (the brand's #d63a2f goes muddy on pine, so the bar passes #e0705f, as the
 * web's CSS does). Height sets the size; width follows the 413:110 ratio. */
import Svg, { Path, Circle, Text as SvgText } from "react-native-svg";

export default function MeyyMark({ height = 22, color = "#1f2a24", dot = "#d63a2f", label = "MEYY" }) {
  const width = Math.round((height * 413) / 110);
  return (
    <Svg width={width} height={height} viewBox="12.5 0 413 110" accessibilityRole="image" accessibilityLabel={label}
      fill="none" stroke={color} strokeWidth={15} strokeLinecap="round" strokeLinejoin="round">
      <Path d="M20 95V22L62 66L104 22V95" />
      <Path d="M148 22h64M148 58h64M148 94h64" />
      <Path d="M268 95V60L240 26M268 60l28-34M350 95V60L322 26M350 60l28-34" />
      <Circle cx={268} cy={9} r={9} fill={dot} stroke="none" />
      <Circle cx={350} cy={9} r={9} fill={dot} stroke="none" />
      <Circle cx={409} cy={30} r={15} strokeWidth={2.5} />
      <SvgText x={409} y={34.7} textAnchor="middle" fontFamily="Helvetica" fontWeight="700" fontSize={13} fill={color} stroke="none">TM</SvgText>
    </Svg>
  );
}

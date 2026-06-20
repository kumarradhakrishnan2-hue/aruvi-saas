import "./globals.css";

export const metadata = {
  title: "Aruvi",
  description: "NCF-aligned lesson plans & assessments",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

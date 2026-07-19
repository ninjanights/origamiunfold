import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { LocaleProvider } from "@/components/LocaleProvider";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className="flex min-h-screen flex-col">
        <LocaleProvider>
          <Header />

          <main className="mx-auto w-full max-w-7xl flex-1 px-6">{children}</main>

          <Footer />
        </LocaleProvider>
      </body>
    </html>
  );
}

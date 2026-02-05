import type { Metadata } from "next";
import { Poppins} from "next/font/google";
import "./globals.css";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { VaultProvider } from "@/lib/contexts/vaultcontext";

const geistSans = Poppins({
  variable: "--font-poppins",
  subsets: ["latin"],
  weight: ["400", "700"],
});

export const metadata: Metadata = {
  title: "Secret Dome",
  description: "Secret Dome a Website for storing secrets securely and privately.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
      suppressHydrationWarning
        className={`${geistSans.className} antialiased`}
      >
        <GoogleOAuthProvider clientId={`${process.env.GOOGLE_CLIENT_ID}`}>
          <VaultProvider>
          {children}
          </VaultProvider>
        </GoogleOAuthProvider>

        </body>
    </html>
  );
}

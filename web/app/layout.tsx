import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import ChatProvider from "../business/hooks/provider/chat-provider";
import "@mantine/core/styles.css";
import { MantineProvider } from "@mantine/core";
import ChatHeader from "@/components/ChatHeader";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Fingaroo",
  description: "AI와 대화하는 채팅 인터페이스",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="kor">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <MantineProvider>
          <ChatProvider>
            <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 overflow-y-hidden">
              <ChatHeader />
              <div className="flex flex-1 w-full overflow-y-auto overflow-x-hidden">
                {children}
              </div>
            </div>
          </ChatProvider>
        </MantineProvider>
      </body>
    </html>
  );
}

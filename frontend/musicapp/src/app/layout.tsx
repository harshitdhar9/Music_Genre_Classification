// app/layout.tsx
import "./globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "SoundSage",
  description: "Understand and generate music with AI",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-white font-sans min-h-screen flex flex-col">
        <header className="w-full px-6 py-4 border-b border-gray-800 shadow-md">
          <h1 className="text-2xl font-bold text-purple-400">SoundSage</h1>
          <p className="text-sm text-gray-400">Understand and generate music with AI</p>
        </header>

        <main className="flex-1 w-full max-w-4xl mx-auto px-6 py-10">
          {children}
        </main>

        <footer className="w-full py-4 text-center text-gray-600 border-t border-gray-800 text-sm">
          Made with ❤️ by You | <a href="https://github.com/yourgithub" className="underline hover:text-white">GitHub</a>
        </footer>
      </body>
    </html>
  );
}

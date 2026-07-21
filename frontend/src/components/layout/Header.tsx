"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { useLocale } from "@/components/LocaleProvider";

export default function Header() {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const { locale, toggleLocale } = useLocale();

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    const nextTheme = savedTheme === "dark" ? "dark" : "light";

    setTheme(nextTheme);
    document.documentElement.classList.toggle("dark", nextTheme === "dark");
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    document.documentElement.classList.toggle("dark", nextTheme === "dark");
    localStorage.setItem("theme", nextTheme);
  };

  return (
    <header className="py-2.5">
      <div className="mx-auto flex max-w-7xl items-center px-4 sm:px-6">
        {/* Left */}
        <div className="flex flex-1 items-center gap-2.5">
          <Image src="/fox.png" alt="Fox" width={25} height={25} />
          <Link
            href="/"
            className="whitespace-nowrap text-base font-bold tracking-tight text-neutral-800 transition hover:text-neutral-600 dark:text-neutral-100 dark:hover:text-white sm:text-lg"
          >
            {locale === "ja" ? "おりがみ ひらく" : "Origami Unfold"}
          </Link>
        </div>

        {/* Center */}
        <nav className="flex items-center gap-3 sm:gap-6">
          <Link
            href="/"
            className="text-sm font-semibold text-neutral-500 transition-colors duration-200 hover:text-[#F87C63] dark:text-neutral-400 dark:hover:text-[#F87C63]"
          >
            {locale === "ja" ? "いえ" : "Home"}
          </Link>

          <Link
            href="/about"
            className="text-sm font-semibold text-neutral-500 transition-colors duration-200 hover:text-[#F87C63] dark:text-neutral-400 dark:hover:text-[#F87C63]"
          >
            {locale === "ja" ? "このあぷり" : "About"}
          </Link>

        </nav>

        {/* Right */}
        <div className="flex flex-1 justify-end">
          <div className="flex items-center gap-2.5 whitespace-nowrap">
            <span className="hidden text-[10px] font-normal text-neutral-500 dark:text-neutral-400 lg:inline">
              {locale === "ja" ? "もどらないで。こたえは すぐそこです。" : "Don't turn back, Your answer is just around the corner."}
            </span>
            <span className="hidden text-neutral-300 dark:text-neutral-600 lg:inline" aria-hidden="true">•</span>
            <button
              type="button"
              onClick={toggleTheme}
              className="flex size-7 items-center justify-center rounded-full text-neutral-500 transition hover:bg-[#F87C63]/30 hover:text-neutral-900 dark:text-neutral-400 dark:hover:bg-[#F87C63]/15 dark:hover:text-[#F87C63]"
              aria-label={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
            >
              {theme === "light" ? (
                <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="currentColor">
                  <path d="M6.34 6.34a8 8 0 1 0 11.32 11.32Z" />
                </svg>
              ) : (
                <svg aria-hidden="true" viewBox="0 0 24 24" className="size-4" fill="currentColor">
                  <circle cx="12" cy="12" r="6.5" />
                </svg>
              )}
            </button>
            <span className="text-neutral-300 dark:text-neutral-600" aria-hidden="true">•</span>
            <button
              type="button"
              onClick={toggleLocale}
              className="flex size-7 items-center justify-center rounded-full text-xs font-medium text-neutral-500 transition hover:bg-[#F87C63]/30 hover:text-neutral-900 dark:text-neutral-400 dark:hover:bg-[#F87C63]/15 dark:hover:text-[#F87C63]"
              aria-label={locale === "ja" ? "Switch to English" : "にほんごに きりかえる"}
            >
              {locale === "ja" ? "a" : "あ"}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

"use client";

import Link from "next/link";
import { useLocale } from "@/components/LocaleProvider";

export default function Footer() {
  const { locale } = useLocale();

  return (
    <footer className="py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-center overflow-x-auto px-6 text-xs font-medium text-neutral-500 scrollbar-none dark:text-neutral-500">
        <div className="flex shrink-0 items-center gap-2 whitespace-nowrap">
          <span className="font-semibold text-neutral-800 dark:text-neutral-200">{locale === "ja" ? "おりがみ ひらく" : "Origami Unfold"}</span>
          <span className="text-neutral-300 dark:text-neutral-700">•</span>
          <span>{locale === "ja" ? "おりめごとに おはなしが かくれています。" : "Every fold hides a story. Every question unfolds one."}</span>
          <span className="text-neutral-300 dark:text-neutral-700">•</span>
          <span>{locale === "ja" ? "2026ねんから" : "Since 2026"}</span>
          <span className="text-neutral-300 dark:text-neutral-700">•</span>
          <span>v1.0.0</span>
          <span className="text-neutral-300 dark:text-neutral-700">•</span>
          <Link
            href="https://github.com/ninjanights"
            target="_blank"
            aria-label="GitHub"
            className="transition hover:text-[#E6CDC5] dark:hover:text-[#E6CDC5]"
          >
            <svg aria-hidden="true" viewBox="0 0 24 24" className="size-3.5" fill="currentColor">
              <path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.18-3.37-1.18-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.04 1.53 1.04.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.56-1.11-4.56-4.95 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.6 9.6 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.85-2.34 4.69-4.57 4.94.36.31.68.91.68 1.84v2.73c0 .26.18.57.69.48A10 10 0 0 0 12 2Z" />
            </svg>
          </Link>
          <span className="text-neutral-300 dark:text-neutral-700">•</span>
          <Link href="/docs" className="transition hover:text-[#E6CDC5] dark:hover:text-[#E6CDC5]">{locale === "ja" ? "せつめい" : "Documentation"}</Link>
          <span className="text-neutral-300 dark:text-neutral-700">•</span>
          <Link href="/status" className="transition hover:text-[#E6CDC5] dark:hover:text-[#E6CDC5]">{locale === "ja" ? "じょうたい" : "Status"}</Link>
        </div>
      </div>
    </footer>
  );
}

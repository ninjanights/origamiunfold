"use client";

import { useLocale } from "@/components/LocaleProvider";

export default function DocumentationPage() {
  const { locale } = useLocale();

  return (
    <section className="flex h-full items-center justify-center">
      <h1 className="text-center text-3xl font-bold tracking-tight text-neutral-800 dark:text-neutral-100 sm:text-4xl">
        {locale === "ja" ? "どきゅめんと" : "documentation"}
      </h1>
    </section>
  );
}

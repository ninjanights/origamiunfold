"use client";

import { createContext, useContext, useEffect, useState } from "react";

type Locale = "en" | "ja";

interface LocaleContextValue {
  locale: Locale;
  toggleLocale: () => void;
}

const LocaleContext = createContext<LocaleContextValue | null>(null);

export function LocaleProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>("ja");

  useEffect(() => {
    const savedLocale = localStorage.getItem("locale");
    if (savedLocale === "en" || savedLocale === "ja") setLocale(savedLocale);
  }, []);

  const toggleLocale = () => {
    const nextLocale = locale === "ja" ? "en" : "ja";
    setLocale(nextLocale);
    localStorage.setItem("locale", nextLocale);
  };

  return <LocaleContext.Provider value={{ locale, toggleLocale }}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const context = useContext(LocaleContext);
  if (!context) throw new Error("useLocale must be used inside LocaleProvider.");
  return context;
}

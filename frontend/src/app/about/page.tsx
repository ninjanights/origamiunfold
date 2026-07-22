"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

import { useLocale } from "@/components/LocaleProvider";

const privacyFeatures = [
  "Temporary Workspace",
  "Isolated Processing Environment",
  "Session-Based Storage",
  "Backend Session Validation",
  "Secure Cookie Renewal",
  "Automatic Data Cleanup",
  "No Account Requirement",
  "No Model Training Usage",
  "Minimal Data Collection",
];

const capabilities = [
  "Multi-Format Support - PDF, DOCX, TXT, CSV, and Markdown processing.",
  "AI Document Chat - Ask questions and get context-aware answers.",
  "Semantic Search - Find information through meaning-based retrieval.",
  "RAG Pipeline - Retrieve relevant context and generate accurate responses.",
  "Document Summarization - Generate quick insights from large files.",
  "Session-Based Workspace - Temporary and isolated document processing.",
  "Privacy-First Architecture - Minimal data handling with automatic cleanup.",
];

const futurePlans = [
  "AI Knowledge Map - Visualize concepts and relationships across documents.",
  "Semantic Graph Explorer - Explore hidden connections between information.",
  "AI Research Agents - Automate deeper analysis and discovery.",
  "Multimodal Support - Understand text, images, tables, and charts.",
];

export default function AboutPage() {
  const { locale } = useLocale();

  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <section className="flex h-full items-center justify-center py-2 text-center">
      <div className="w-full max-w-6xl space-y-4 text-neutral-600 dark:text-neutral-300">
        <div className="flex items-center justify-center gap-3">
          <Image src="/fox.png" alt="Fox" width={48} height={48} />
          <div className="text-left">
            <h1 className="text-xl font-bold tracking-tight text-neutral-800 dark:text-neutral-100 sm:text-2xl">
              Origami Unfold
            </h1>
            <p className="text-[11px] leading-4 text-neutral-500 dark:text-neutral-400">
              Don&apos;t turn back, Your answer is just around the corner.
            </p>
          </div>
        </div>

        <div className="mx-auto max-w-3xl space-y-3 text-center text-[11px] leading-4">
          <div>
            <h2 className="mb-1 text-sm font-bold text-neutral-800 dark:text-neutral-100">
              The Story
            </h2>
            <p>
              Origami Unfold began as a personal experiment. I wanted to
              understand how AI truly retrieves, understands, and reasons over
              information - not as a black box, but from its foundations.
              Building the retrieval pipeline from scratch became my way of
              learning semantic search, vector embeddings, and
              Retrieval-Augmented Generation by understanding every layer
              instead of simply using it.
            </p>
            <p className="mt-2">
              Along the journey, I realized the project had become more than a
              learning experience. It solved a problem I kept facing myself:
              documents are rich with knowledge, yet exploring them still feels
              linear and frustrating. So I decided to open it to everyone.
            </p>
            <p className="mt-2">
              Today, Origami Unfold transforms uploaded documents into
              searchable knowledge spaces where users can ask questions,
              retrieve context-aware answers, and interact with information
              naturally. While Version One focuses on conversational document
              intelligence, the long-term vision is much larger-transforming
              documents into interactive semantic landscapes where ideas can be
              explored instead of searched.
            </p>
          </div>

          <div>
            <h2 className="mb-1 text-sm font-bold text-neutral-800 dark:text-neutral-100">
              Our Philosophy
            </h2>
            <p>
              Things are connected with vibe, tone, aura, and aesthetic.
              Everything responds to alteration-that&apos;s how they get
              recalled when we remember, like dominoes. Things share a common
              space, evolve together with divergence, and that shared space is
              where meaning comes from.
            </p>
          </div>
        </div>

        <div className="relative flex justify-center">
          <div className="flex divide-x divide-neutral-200 text-left text-[10px] leading-4 dark:divide-neutral-800">
            <div className="flex flex-col items-center px-4 text-center sm:px-6">
              <h2 className="mb-1 text-xs font-bold text-neutral-800 dark:text-neutral-100">
                Privacy
              </h2>
              <ul className="text-center space-y-0.5">
                {privacyFeatures.map((feature) => (
                  <li key={feature}>{feature}</li>
                ))}
              </ul>
            </div>

            <div className="flex flex-col items-center px-4 text-center sm:px-6">
              <h2 className="mb-1 text-xs font-bold text-neutral-800 dark:text-neutral-100">
                Currently
              </h2>
              <ul className="space-y-0.5 text-center">
                {capabilities.map((capability) => (
                  <li key={capability}>{capability}</li>
                ))}
              </ul>

              <h2 className="mb-1 mt-3 text-xs font-bold text-neutral-800 dark:text-neutral-100">
                We coming up with
              </h2>
              <ul className="space-y-0.5 text-center text-neutral-400 dark:text-neutral-500">
                {futurePlans.map((plan) => (
                  <li key={plan}>{plan}</li>
                ))}
              </ul>
            </div>

            <div className="flex flex-col items-center gap-1.5 px-4 text-center sm:px-6">
              <div className="flex items-center gap-2">
                <Link
                  href="https://github.com/ninjanights"
                  target="_blank"
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-neutral-600 transition hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-100"
                >
                  <svg
                    aria-hidden="true"
                    viewBox="0 0 24 24"
                    className="size-3.5"
                    fill="currentColor"
                  >
                    <path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.18-3.37-1.18-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.04 1.53 1.04.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.56-1.11-4.56-4.95 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.6 9.6 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.85-2.34 4.69-4.57 4.94.36.31.68.91.68 1.84v2.73c0 .26.18.57.69.48A10 10 0 0 0 12 2Z" />
                  </svg>
                  ninjanights
                </Link>

                <span className="text-neutral-300 dark:text-neutral-700">
                  •
                </span>
                <Link
                  href="https://open.spotify.com/user/wxptrsmiblc51satoitf9jc2p?si=6a9b18cf2cdd4fa5"
                  target="_blank"
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-neutral-600 transition hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-100"
                >
                  <svg
                    aria-hidden="true"
                    viewBox="0 0 24 24"
                    className="size-3.5 text-neutral-600 dark:text-neutral-400"
                    fill="currentColor"
                  >
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2Zm4.59 14.41a.62.62 0 0 1-.86.21c-2.36-1.44-5.33-1.77-8.83-.97a.622.622 0 1 1-.28-1.21c3.83-.88 7.12-.5 9.76 1.11.3.18.39.57.21.86Zm1.22-2.72a.78.78 0 0 1-1.07.26c-2.7-1.66-6.82-2.14-10.02-1.17a.78.78 0 1 1-.45-1.49c3.65-1.11 8.19-.57 11.28 1.33.37.23.48.72.26 1.07Zm.11-2.83c-3.24-1.92-8.59-2.1-11.69-1.16a.936.936 0 1 1-.54-1.79c3.56-1.08 9.46-.87 13.19 1.34a.935.935 0 1 1-.96 1.61Z" />
                  </svg>
                </Link>
              </div>

              <p className="mt-2 text-neutral-500 dark:text-neutral-400">
                Kanchrapara, Kolkata, IN
              </p>
              <p className="text-neutral-400 dark:text-neutral-500">v1.0.0</p>
            </div>
          </div>

          <span className="sr-only" suppressHydrationWarning>
            {mounted && locale === "ja"
              ? "おりがみ ひらく について"
              : "About Origami Unfold"}
          </span>
        </div>
      </div>
    </section>
  );
}

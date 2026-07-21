"use client";

import { useLocale } from "@/components/LocaleProvider";

const pipeline = [
  "Upload",
  "Extraction",
  "Cleaning",
  "Chunking",
  "Embeddings",
  "Vector Index",
  "Semantic Retrieval",
  "Context Assembly",
  "LLM Response",
];

const ingestion = [
  "PDF",
  "DOCX",
  "TXT",
  "CSV",
  "Markdown",
];

const architecture = [
  "Python",
  "Django",
  "Sentence Transformers",
  "FAISS Vector Database",
  "NumPy",
  "Pandas",
  "PyMuPDF",
  "python-docx",
];

const intelligence = [
  "Semantic Search",
  "Retrieval-Augmented Generation",
  "Context Window Optimization",
  "Recursive Chunking",
  "Embedding Similarity",
  "Prompt Assembly",
];

export default function DocumentationPage() {
  const { locale } = useLocale();

  return (
    <section className="flex h-full justify-center overflow-y-auto px-2 py-2">
      <div className="w-full max-w-4xl space-y-5">

        {/* Title */}

        <div className="text-center">
          <h1 className="text-2xl font-bold tracking-tight text-neutral-900 dark:text-neutral-100">
            {locale === "ja" ? "どきゅめんと" : "Documentation"}
          </h1>

          <p className="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
            Understanding the architecture behind Origami Unfold.
          </p>
        </div>

        {/* Intro */}

        <div className="mx-auto max-w-3xl text-center text-[11px] leading-4 text-neutral-600 dark:text-neutral-400">
          <p>
            Origami Unfold follows a Retrieval-Augmented Generation architecture
            built from the ground up. Every uploaded document passes through an
            ingestion pipeline that extracts content, prepares semantic
            embeddings, retrieves relevant context, and generates grounded
            responses instead of relying purely on model memory.
          </p>
        </div>

        {/* Pipeline */}

        <div className="text-center text-[11px] leading-4">
          <h2 className="mb-1.5 text-xs font-bold text-neutral-800 dark:text-neutral-100">
            Processing Pipeline
          </h2>

          <div className="flex flex-wrap items-center justify-center gap-x-0.5 gap-y-1">
            <span>A File</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Extraction</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Cleaning</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Chunking</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Embeddings</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Vector Index</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Retrieval</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>Context</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>
            <span>LLM</span>

            <span className="px-1 text-neutral-400 dark:text-neutral-600">then</span>

            <code className="px-1 py-0.5 text-[10px] dark:bg-neutral-900">
              [[0.18, -1.02, 0.44, ...]]
            </code>
          </div>
        </div>

        {/* Three Columns */}

        <div className="grid divide-y divide-neutral-200 border-neutral-200 text-[11px] leading-4 dark:divide-neutral-800 md:grid-cols-3 md:divide-x md:divide-y-0">

          {/* Supported */}

          <div className="p-2 text-center">
            <h2 className="mb-1.5 text-xs font-bold">
              Ingestion
            </h2>

            <ul className="space-y-0.5">
              {ingestion.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          {/* AI */}

          <div className="p-2 text-center">
            <h2 className="mb-1.5 text-xs font-bold">
              Intelligence
            </h2>

            <ul className="space-y-0.5">
              {intelligence.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          {/* Stack */}

          <div className="p-2 text-center">
            <h2 className="mb-1.5 text-xs font-bold">
              Architecture
            </h2>

            <ul className="space-y-0.5">
              {architecture.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

        </div>

        {/* Engine */}

        <div className="mx-auto max-w-3xl space-y-1.5 text-center text-[11px] leading-4">
          <h2 className="text-sm font-bold text-neutral-900 dark:text-neutral-100">
            The Engine
          </h2>

          <p>
            Documents are parsed into structured text before passing through a
            recursive chunking strategy. Each chunk is transformed into vector
            embeddings using sentence transformer models and indexed inside a
            vector database for similarity search.
          </p>

          <p>
            User questions are embedded using the same model, allowing semantic
            retrieval to identify the most relevant chunks. Retrieved context is
            assembled into a prompt and forwarded to the language model,
            producing responses grounded in the uploaded document rather than
            hallucinated knowledge.
          </p>
        </div>

        {/* Principles */}

        <div className="rounded-lg l-200 p-2 text-center text-[11px] leading-4">
          <h2 className="mb-1 text-sm font-bold">
            Design Principles
          </h2>

          <p>
            Retrieval before generation. Privacy before persistence.
            Simplicity before complexity. Every component exists to improve
            answer quality while keeping document processing isolated,
            transparent, and reproducible.
          </p>
        </div>

      </div>
    </section>
  );
}
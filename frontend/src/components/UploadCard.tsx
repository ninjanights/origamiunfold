"use client";

import { useState } from "react";
import { useUpload } from "@/hooks/useUpload";
import { useLocale } from "@/components/LocaleProvider";

interface UploadCardProps {
  onUploadComplete: () => Promise<void>;
}

export default function UploadCard({ onUploadComplete }: UploadCardProps) {
  const [file, setFile] = useState<File | null>(null);
  const { locale } = useLocale();

  const { upload, loading } = useUpload();

  const handleUpload = async () => {
    if (!file) return;

    const response = await upload(file);
    console.log(response);
    if (response) {
      await onUploadComplete();
      setFile(null);
    }
  };

  return (
    <section className="mx-auto w-full max-w-xl text-center">
      <div className="space-y-5">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-neutral-800 dark:text-neutral-100">
            {locale === "ja" ? "ぶんしょを おくる" : "Upload your document"}
          </h1>

          <p className="mx-auto max-w-md text-sm font-medium leading-6 text-neutral-500 dark:text-neutral-400">
            {locale === "ja" ? "PDF、DOCX、TXT、CSVを おくると、ぶんしょと おはなしできます。" : "Upload a PDF, DOCX, TXT or CSV to start chatting with your documents."}
          </p>
        </div>

        <label
          htmlFor="file-upload"
          className="flex cursor-pointer flex-col items-center justify-center rounded-full border-2 border-dashed border-[#E6CDC5] bg-transparent px-10 py-9 transition hover:border-[#E6CDC5] dark:border-[#E6CDC5]/50 dark:hover:border-[#E6CDC5]"
        >
          <span className="text-base font-bold text-neutral-800 dark:text-neutral-100">
            {file ? file.name : locale === "ja" ? "ぶんしょを えらぶ" : "Choose a document"}
          </span>

          <span className="mt-1.5 text-sm font-medium text-neutral-500 dark:text-neutral-400">
            {locale === "ja" ? "ここを おして ふぁいるを えらぶ" : "Click here to browse your files"}
          </span>

          <input
            id="file-upload"
            type="file"
            className="hidden"
            onChange={(e) => {
              const selectedFile = e.target.files?.[0];

              if (selectedFile) {
                setFile(selectedFile);
              }
            }}
          />
        </label>

        <div className="flex justify-center">
          <button
            disabled={!file || loading}
            onClick={handleUpload}
            className="rounded-full bg-[#E6CDC5] px-6 py-2.5 text-sm font-bold text-neutral-900 transition hover:bg-[#E6CDC5]/80 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-[#E6CDC5] dark:text-neutral-950 dark:hover:bg-[#E6CDC5]/80"
          >
            {loading ? (locale === "ja" ? "おくっています..." : "Uploading...") : locale === "ja" ? "ぶんしょを おくる" : "Upload Document"}
          </button>
        </div>
      </div>
    </section>
  );
}

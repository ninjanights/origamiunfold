"use client";

import { useEffect, useState } from "react";
import { useUpload } from "@/hooks/useUpload";
import { useLocale } from "@/components/LocaleProvider";

interface UploadCardProps {
  onUploadComplete: () => Promise<void>;
  uploadLimitReached: boolean;
}

export default function UploadCard({
  onUploadComplete,
  uploadLimitReached,
}: UploadCardProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isMounted, setIsMounted] = useState(false);

  const { locale } = useLocale();
  const { upload, loading } = useUpload();

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleUpload = async () => {
    if (!file || uploadLimitReached) return;

    const response = await upload(file);

    if (response) {
      await onUploadComplete();
      setFile(null);
    }
  };

  if (!isMounted) return null;

  return (
    <section className="flex h-full items-center justify-center py-3">
      <div className="mx-auto w-full max-w-xl space-y-5">
        <label
          htmlFor="file-upload"
          className={`flex flex-col items-center justify-center rounded-full
          border-2 border-dashed border-[#ADD7B9] bg-transparent px-8 py-7 transition
          hover:border-[#ADD7B9]
          dark:border-[#ADD7B9]/50 dark:hover:border-[#ADD7B9] ${uploadLimitReached ? "cursor-not-allowed opacity-50" : "cursor-pointer"}`}
        >
          <span className="text-base font-bold text-neutral-800 dark:text-neutral-100">
            {uploadLimitReached
              ? locale === "ja"
                ? "ぶんしょの じょうげんです"
                : "Document limit reached"
              : file
                ? file.name
                : locale === "ja"
                  ? "ぶんしょを えらぶ"
                  : "Choose a document"}
          </span>

          <span className="mt-1.5 text-sm font-medium text-neutral-500 dark:text-neutral-400">
            {uploadLimitReached
              ? locale === "ja"
                ? "ぶんしょは 21こまで おくれます。"
                : "You can upload up to 21 documents."
              : locale === "ja"
                ? "ここを おして ふぁいるを えらぶ"
                : "Click here to browse your files"}
          </span>

          <input
            id="file-upload"
            type="file"
            className="hidden"
            disabled={uploadLimitReached}
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
            disabled={!file || loading || uploadLimitReached}
            onClick={handleUpload}
            className="rounded-full bg-[#ADD7B9] px-6 py-2.5 text-sm font-bold
            text-neutral-900 transition hover:bg-[#ADD7B9]/80
           disabled:opacity-50
            dark:bg-[#ADD7B9] dark:text-neutral-950
            dark:hover:bg-[#ADD7B9]/80"
          >
            {loading
              ? locale === "ja"
                ? "おくっています..."
                : "Uploading..."
              : locale === "ja"
                ? "ぶんしょを おくる"
                : "Upload Document"}
          </button>
        </div>
      </div>
    </section>
  );
}

"use client";

import { useEffect, useRef, useState } from "react";
import UploadCard from "@/components/UploadCard";
import { useFiles } from "@/hooks/useFiles";
import type { WorkspaceFile } from "@/types/upload";
import { useLocale } from "@/components/LocaleProvider";

function FileIcon({ extension }: { extension: string }) {
  const label = extension.replace(".", "").toUpperCase();
  const color = "text-[#E6CDC5]";

  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className={`size-5 shrink-0 ${color}`} fill="none" stroke="currentColor" strokeWidth="1.7">
      <path d="M6.5 3.5h7l4 4v13h-11Z" />
      <path d="M13.5 3.5v4h4" />
      <text x="12" y="17" fill="currentColor" stroke="none" textAnchor="middle" fontSize="5" fontWeight="700">
        {label || "FILE"}
      </text>
    </svg>
  );
}

function FileCapsule({ file }: { file: WorkspaceFile }) {
  return (
    <div className="flex max-w-44 items-center gap-1.5 rounded-full bg-neutral-100 py-1.5 pl-2 pr-3 text-xs dark:bg-neutral-800">
      <FileIcon extension={file.extension} />
      <span className="truncate font-medium text-neutral-700 dark:text-neutral-200">{file.filename}</span>
      <span className="text-[10px] text-neutral-400">{Math.max(1, Math.ceil(file.size / 1024))} KB</span>
    </div>
  );
}

export default function WorkspaceUpload() {
  const { files, loading, refreshFiles } = useFiles();
  const { locale } = useLocale();
  const [uploadOpen, setUploadOpen] = useState(true);
  const isInitialLoad = useRef(true);

  useEffect(() => {
    if (!loading && isInitialLoad.current) {
      setUploadOpen(files.length === 0);
      isInitialLoad.current = false;
    }
  }, [files.length, loading]);

  const displayedFiles = files.slice(0, 3);
  const remainingFiles = files.length - displayedFiles.length;

  return (
    <section className="flex h-full items-center justify-center py-6">
      <div className="w-full">
        {files.length > 0 && !loading && (
          <div className={`mb-5 flex items-center gap-2 ${uploadOpen ? "justify-between" : "justify-center"}`}>
            <div className="flex min-w-0 items-center gap-2 overflow-x-auto scrollbar-none">
              {displayedFiles.map((file) => <FileCapsule key={file.filename} file={file} />)}
              {remainingFiles > 0 && <span className="shrink-0 text-xs font-semibold text-neutral-400">+{remainingFiles}</span>}
            </div>
            <button
              type="button"
              onClick={() => setUploadOpen((isOpen) => !isOpen)}
              className="flex size-8 shrink-0 items-center justify-center rounded-full bg-[#E6CDC5]/30 text-neutral-700 transition hover:bg-[#E6CDC5]/50 dark:bg-[#E6CDC5]/15 dark:text-[#E6CDC5] dark:hover:bg-[#E6CDC5]/25"
              aria-label={uploadOpen ? (locale === "ja" ? "おくる がめんを とじる" : "Close upload form") : locale === "ja" ? "ほかの ぶんしょを おくる" : "Upload another document"}
            >
              {uploadOpen ? "×" : "+"}
            </button>
          </div>
        )}

        {uploadOpen && <UploadCard onUploadComplete={refreshFiles} />}
      </div>
    </section>
  );
}

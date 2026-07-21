"use client";

import { useState } from "react";

import { useLocale } from "@/components/LocaleProvider";
import type { WorkspaceFile } from "@/types/upload";

interface WorkspaceHeaderProps {
  files: WorkspaceFile[];

  selectionMode: boolean;
  selectedFiles: string[];

  onToggleFile: (filename: string) => void;
  onDelete: () => void;
  onCancel: () => void;
  onSelect: () => void;
  isPanelOpen: boolean;
  onTogglePanel: () => void;
}

interface FilePillProps {
  file: WorkspaceFile;
  selectionMode: boolean;
  selected: boolean;
  onClick: () => void;
}

function FilePill({ file, selectionMode, selected, onClick }: FilePillProps) {
  const extension = file.extension.replace(".", "").toUpperCase() || "FILE";
  const extensionColor = {
    PDF: "text-orange-300",
    CSV: "text-yellow-300",
    TXT: "text-teal-300",
    DOCX: "text-red-300",
  }[extension] ?? "text-green-300";

  const size =
    file.size < 1024 ? `${file.size} B` : `${Math.ceil(file.size / 1024)} KB`;

  return (
    <div
      onClick={selectionMode ? onClick : undefined}
      className={`flex max-w-52 items-center gap-1.5 rounded-full py-1.5 px-3 text-xs transition
        ${
          selected
            ? "bg-neutral-200 dark:bg-neutral-700"
            : "bg-neutral-100 dark:bg-neutral-800"
        }
        ${selectionMode ? "cursor-pointer" : ""}
      `}
    >
      <span className={`rounded-full text-[12px] font-bold ${extensionColor}`}>
        {extension}
      </span>

      <span className="truncate font-medium text-neutral-700 dark:text-neutral-200">
        {shortenFileName(file.filename)}
      </span>

      <span className="shrink-0 text-[10px] text-neutral-400">{size}</span>
    </div>
  );
}

export function shortenFileName(filename: string) {
  const dot = filename.lastIndexOf(".");

  const name = dot !== -1 ? filename.slice(0, dot) : filename;
  const ext = dot !== -1 ? filename.slice(dot + 1) : "";

  if (name.length <= 8) return filename;

  return `${name.slice(0, 5)}...${name.slice(-3)}.${ext}`;
}

export default function WorkspaceHeader({
  files,
  selectionMode,
  selectedFiles,
  onSelect,
  onToggleFile,
  onDelete,
  onCancel,
  isPanelOpen,
  onTogglePanel,
}: WorkspaceHeaderProps) {
  const { locale } = useLocale();
  const [showAllFiles, setShowAllFiles] = useState(false);

  const visibleFiles = files.slice(0, 3);
  const hiddenCount = files.length - visibleFiles.length;

  return (
    <div className="mb-4 text-center">
      {files.length > 0 && (
        <>
          {showAllFiles ? (
            <div className="mx-auto mb-3 flex max-w-6xl flex-wrap justify-center gap-2">
              {files.map((workspaceFile) => (
                <FilePill
                  key={workspaceFile.filename}
                  file={workspaceFile}
                  selectionMode={selectionMode}
                  selected={selectedFiles.includes(workspaceFile.filename)}
                  onClick={() => onToggleFile(workspaceFile.filename)}
                />
              ))}

              <button
                onClick={() => setShowAllFiles(false)}
                className="self-center text-xs font-medium text-neutral-500 hover:text-neutral-800 dark:text-neutral-400 dark:hover:text-neutral-100"
              >
                {locale === "ja" ? "すくなく みる" : "Show less"}
              </button>
            </div>
          ) : (
            <div className="mb-3 flex flex-wrap justify-center gap-2">
              {visibleFiles.map((workspaceFile) => (
                <div key={workspaceFile.filename}>
                <FilePill
                  file={workspaceFile}
                  selectionMode={selectionMode}
                  selected={selectedFiles.includes(workspaceFile.filename)}
                  onClick={() => onToggleFile(workspaceFile.filename)}
                />
                </div>
              ))}

              {hiddenCount > 0 && (
                <button
                  onClick={() => setShowAllFiles(true)}
                  className="flex items-center rounded-full bg-neutral-100 px-3 py-1.5 text-xs font-medium dark:bg-neutral-800"
                >
                  +{hiddenCount}
                </button>
              )}
            </div>
          )}

          <div className="mb-4 flex justify-center gap-2 overflow-x-auto pb-1 scrollbar-none">
            <button
              onClick={onSelect}
              className="flex h-9 whitespace-nowrap items-center gap-1.5 rounded-full bg-neutral-100 px-4 text-[12px] font-bold text-neutral-500 transition hover:bg-neutral-200 dark:bg-neutral-800 dark:text-neutral-200 dark:hover:bg-neutral-700"
            >
              {selectionMode
                ? locale === "ja"
                  ? `${selectedFiles.length} こ えらんだ`
                  : `${selectedFiles.length} selected`
                : locale === "ja"
                  ? "えらぶ"
                  : "Select"}
            </button>

            <button
              disabled={selectedFiles.length === 0}
              onClick={onDelete}
              className={`flex h-9 whitespace-nowrap items-center gap-1.5 rounded-full px-4 text-[12px] font-bold transition disabled:opacity-50 ${
                selectedFiles.length > 0
                  ? "bg-neutral-100 text-red-400 hover:bg-neutral-200 dark:bg-neutral-800 dark:text-red-400 dark:hover:bg-neutral-700"
                  : "bg-neutral-100 text-neutral-500 hover:bg-neutral-200 dark:bg-neutral-800 dark:text-neutral-200 dark:hover:bg-neutral-700"
              }`}
            >
              {locale === "ja" ? "さくじょ" : "Delete"}
            </button>

            <button
              disabled={!selectionMode}
              onClick={onCancel}
              className="flex h-9 items-center gap-1.5 rounded-full bg-neutral-100 px-4 text-[12px] font-bold text-neutral-500 transition hover:bg-neutral-200 disabled:opacity-50 dark:bg-neutral-800 dark:text-neutral-200 dark:hover:bg-neutral-700"
            >
              {locale === "ja" ? "やめる" : "Cancel"}
            </button>

            <button
              onClick={onTogglePanel}
              className="flex h-9 items-center gap-1.5 rounded-full bg-neutral-100 px-4 text-[12px] font-bold text-neutral-500 transition hover:bg-neutral-200 dark:bg-neutral-800 dark:text-neutral-200 dark:hover:bg-neutral-700"
            >
              {isPanelOpen
                ? locale === "ja"
                  ? "ふぁいるを おくる"
                  : "Upload a File"
                : locale === "ja"
                  ? "しつもん まど"
                  : "Ask Window"}
            </button>
          </div>
        </>
      )}

      <h1 className="text-2xl font-bold tracking-tight text-neutral-800 dark:text-neutral-100 sm:text-3xl">
        {isPanelOpen
          ? locale === "ja"
            ? "しつもんする"
            : "Ask your question"
          : locale === "ja"
            ? "ぶんしょを おくる"
            : "Upload your document"}
      </h1>

      {!isPanelOpen && (
        <p className="mx-auto mt-1 max-w-md text-sm font-medium leading-5 text-neutral-500 dark:text-neutral-400">
          {locale === "ja"
            ? "PDF、DOCX、TXT、CSVを おくると、ぶんしょと おはなしできます。"
            : "Upload a PDF, DOCX, TXT or CSV to start chatting with your documents."}
        </p>
      )}
    </div>
  );
}

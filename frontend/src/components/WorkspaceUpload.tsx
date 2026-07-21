"use client";

import { useState } from "react";

import UploadCard from "@/components/UploadCard";
import WorkspaceHeader from "@/components/WorkspaceHeader";
import Panel from "@/components/Panel";

import { useFiles } from "@/hooks/useFiles";
import { deleteFiles } from "@/services/api";

export default function WorkspaceUpload() {
  const { files, loading, refreshFiles } = useFiles();

  const [selectionMode, setSelectionMode] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const workspaceFiles = loading ? [] : files;
  const toggleFile = (filename: string) => {
    setSelectedFiles((current) =>
      current.includes(filename)
        ? current.filter((f) => f !== filename)
        : [...current, filename],
    );
  };

  const cancelSelection = () => {
    setSelectionMode(false);
    setSelectedFiles([]);
  };

  const handleDelete = async () => {
    if (selectedFiles.length === 0) return;

    try {
      await deleteFiles(selectedFiles);

      await refreshFiles();

      setSelectedFiles([]);
      setSelectionMode(false);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <section className="flex h-full items-center justify-center py-3">
      <div className="w-full">
        <WorkspaceHeader
          files={workspaceFiles}
          selectionMode={selectionMode}
          selectedFiles={selectedFiles}
          onToggleFile={toggleFile}
          onDelete={handleDelete}
          onCancel={cancelSelection}
          onSelect={() => setSelectionMode(true)}
          isPanelOpen={isPanelOpen}
          onTogglePanel={() => setIsPanelOpen((current) => !current)}
        />

        {isPanelOpen ? (
          <Panel />
        ) : (
          <UploadCard
            onUploadComplete={refreshFiles}
            uploadLimitReached={workspaceFiles.length >= 21}
          />
        )}
      </div>
    </section>
  );
}

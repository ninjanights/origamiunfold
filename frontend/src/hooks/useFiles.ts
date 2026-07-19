"use client";

import { useCallback, useEffect, useState } from "react";
import { getFiles } from "@/services/api";
import type { WorkspaceFile } from "@/types/upload";

export function useFiles() {
  const [files, setFiles] = useState<WorkspaceFile[]>([]);
  const [loading, setLoading] = useState(true);

  const refreshFiles = useCallback(async () => {
    try {
      setLoading(true);
      const workspaceFiles = await getFiles();
      setFiles(workspaceFiles);
    } catch (error) {
      console.error(error);
      setFiles([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refreshFiles();
  }, [refreshFiles]);

  return { files, loading, refreshFiles };
}

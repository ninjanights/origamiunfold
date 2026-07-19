"use client";

import { useState } from "react";
import { uploadFile } from "@/services/api";

export function useUpload() {
  const [loading, setLoading] = useState(false);

  const upload = async (file: File) => {
    try {
      setLoading(true);

      const response = await uploadFile(file);

      return response;
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return {
    upload,
    loading,
  };
}

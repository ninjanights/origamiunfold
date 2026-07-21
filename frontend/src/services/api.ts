import api from "./axios";
import type { UploadResponse, WorkspaceFile } from "@/types/upload";
import type { AskRequest, AskResponse } from "@/types/chat";
import type { BackendStatus } from "@/types/status";


export async function getBackendStatus(): Promise<BackendStatus> {
  const response = await api.get("/health/");
  return response.data;
}


export async function uploadFile(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post<UploadResponse>(`/upload/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function getFiles(): Promise<WorkspaceFile[]> {
  const response = await api.get<WorkspaceFile[]>(`/files/`);
  return response.data;
}

export async function loadDemo(): Promise<{ message: string }> {
  const response = await api.post("/demo/load/");
  return response.data;
}

export async function ask(payload: AskRequest): Promise<AskResponse> {
  const response = await api.post<AskResponse>(`/chat/`, payload);
  return response.data;
}

export async function deleteFiles(
  files: string[],
): Promise<{ message: string }> {
  const response = await api.delete("/files/delete/", {
    data: { files },
  });
  return response.data;
}

export async function deleteAllFiles(): Promise<{ message: string }> {
  const response = await api.delete("/files/delete-all/");

  return response.data;
}

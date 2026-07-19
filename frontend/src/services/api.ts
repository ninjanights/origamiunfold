import api from "./axios";
import type { UploadResponse, WorkspaceFile } from "@/types/upload";
import type { AskRequest, AskResponse } from "@/types/chat";

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

export async function ask(payload: AskRequest): Promise<AskResponse> {
  const response = await api.post<AskResponse>(`/chat/`, payload);

  return response.data;
}

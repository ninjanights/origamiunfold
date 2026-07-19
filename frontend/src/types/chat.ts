export interface Source {
    file: string;
    page: number;
    chunk: number;
}

export interface AskRequest {
    question: string;
}

export interface AskResponse {
    answer: string;
    sources: Source[];
}
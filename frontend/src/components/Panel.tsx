"use client";

import { useEffect, useMemo, useState } from "react";

import { ask } from "@/services/api";
import { useConversation } from "@/hooks/useConversation";
import { useLocale } from "@/components/LocaleProvider";

const ROWS_PER_PAGE = 5;

function preview(text: string, words: number) {
  const parts = text.trim().split(/\s+/);
  return parts.length > words ? `${parts.slice(0, words).join(" ")}...` : text;
}

function visiblePages(totalPages: number, activePage: number) {
  if (totalPages <= 7) return Array.from({ length: totalPages }, (_, index) => index + 1);

  if (activePage <= 4) return [1, 2, 3, 4, 5, "…", totalPages];
  if (activePage >= totalPages - 3) return [1, "…", totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages];

  return [1, "…", activePage - 1, activePage, activePage + 1, "…", totalPages];
}

export default function Panel() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [activePage, setActivePage] = useState(1);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [failedQuestionId, setFailedQuestionId] = useState<string | null>(null);
  const { messages, addUserMessage, addAssistantMessage, deleteConversation } = useConversation();
  const { locale } = useLocale();

  const conversations = useMemo(
    () =>
      messages.reduce<
        { question: (typeof messages)[number]; answer?: (typeof messages)[number] }[]
      >((rows, message) => {
        if (message.role === "You") {
          rows.push({ question: message });
        } else if (rows.length > 0) {
          rows[rows.length - 1].answer = message;
        }
        return rows;
      }, []),
    [messages],
  );

  const totalPages = Math.max(1, Math.ceil(conversations.length / ROWS_PER_PAGE));
  const pageRows = conversations.slice(
    (activePage - 1) * ROWS_PER_PAGE,
    activePage * ROWS_PER_PAGE,
  );
  const pageNumbers = visiblePages(totalPages, activePage);

  useEffect(() => {
    setTimeout(() => setActivePage(totalPages), 0);
  }, [conversations.length, totalPages]);

  const requestAnswer = async (questionText: string, questionId?: string) => {
    setLoading(true);
    setFailedQuestionId(null);

    try {
      const response = await ask({ question: questionText });
      addAssistantMessage(response.answer, response.sources);
    } catch (error) {
      console.error(error);
      if (questionId) setFailedQuestionId(questionId);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    const questionId = crypto.randomUUID();
    addUserMessage(trimmed, questionId);
    setQuestion("");
    await requestAnswer(trimmed, questionId);
  };

  const handleRefresh = async (questionText: string, questionId: string) => {
    if (loading) return;
    await requestAnswer(questionText, questionId);
  };

  return (
    <section className="flex h-full items-center justify-center py-3">
      <div className="mx-auto flex min-h-[24rem] w-full max-w-5xl gap-3">
        <div className="flex min-w-0 flex-1 flex-col rounded-[2rem] border-2 border-dashed border-[#ADD7B9] bg-transparent px-5 py-5 dark:border-[#ADD7B9]/50 sm:px-7">
          <div className="flex items-center justify-between pb-4 text-sm font-bold">
            <span className="text-neutral-500 dark:text-neutral-400">_fox</span>
            <span className="text-neutral-500 dark:text-neutral-400">{locale === "ja" ? "{すべて}" : "{Everything}"}</span>
          </div>

          <div className="flex-1 space-y-2 py-4">
            {pageRows
              .filter(({ question: conversationQuestion }) => !expandedId || expandedId === conversationQuestion.id)
              .map(({ question: conversationQuestion, answer }) => {
              const isLatest =
                conversationQuestion.id ===
                conversations[conversations.length - 1]?.question.id;
              const isExpanded = expandedId === conversationQuestion.id || isLatest;
              const isFailed = failedQuestionId === conversationQuestion.id;

              return (
                <article
                  key={conversationQuestion.id}
                  className={`rounded-2xl border border-neutral-200 px-4 py-3 dark:border-neutral-800 ${isExpanded ? "space-y-4 bg-neutral-200 dark:bg-neutral-800" : ""}`}
                >
                  {isExpanded ? (
                    <>
                      <p className="text-sm font-semibold leading-6 text-neutral-800 dark:text-neutral-100">{conversationQuestion.content}</p>
                      <p className="text-sm leading-6 text-neutral-700 dark:text-neutral-200">
                        {answer?.content ?? (isFailed ? locale === "ja" ? "こたえを みつけられません。" : "Unable to get an answer." : locale === "ja" ? "かんがえています..." : "Thinking...")}
                      </p>
                      {answer?.sources && answer.sources.length > 0 && (
                        <div className="flex flex-wrap gap-x-3 gap-y-1 pt-1 text-xs text-neutral-500 dark:text-neutral-400">
                          {answer.sources.map((source, index) => (
                            <span key={`${source.file}-${source.page}-${source.chunk}-${index}`}>
                              {source.file} · {locale === "ja" ? "ぺーじ" : "Page"} {source.page}
                            </span>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="space-y-1 text-sm">
                      <p className="font-semibold text-neutral-800 dark:text-neutral-100">{preview(conversationQuestion.content, 5)}</p>
                      <div className="flex items-start justify-between gap-3">
                        <p className="text-neutral-600 dark:text-neutral-300">{preview(answer?.content ?? (locale === "ja" ? "かんがえています..." : "Thinking..."), 20)}</p>
                        <button
                          onClick={() => setExpandedId(conversationQuestion.id)}
                          className="shrink-0 text-xs font-bold text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-100"
                        >
                          {locale === "ja" ? "ひらく" : "Expand"}
                        </button>
                      </div>
                    </div>
                  )}

                  <div className={isExpanded ? "flex justify-end gap-4" : "hidden"}>
                    {isFailed && (
                      <button
                        onClick={() => handleRefresh(conversationQuestion.content, conversationQuestion.id)}
                        className="text-xs font-bold text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-100"
                      >
                        {locale === "ja" ? "もういちど" : "Refresh"}
                      </button>
                    )}
                    <button
                      onClick={() => {
                        deleteConversation(conversationQuestion.id);
                        setExpandedId(null);
                        setFailedQuestionId(null);
                      }}
                      className="text-xs font-bold text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-100"
                    >
                      {locale === "ja" ? "さくじょ" : "Delete"}
                    </button>
                    {expandedId && (
                      <button
                        onClick={() => setExpandedId(null)}
                        className="text-xs font-bold text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-neutral-100"
                      >
                        {locale === "ja" ? "とじる" : "Collapse"}
                      </button>
                    )}
                  </div>
                </article>
              );
            })}

            {conversations.length === 0 && (
              <p className="pt-8 text-center text-sm text-neutral-400">{locale === "ja" ? "しつもんして はじめよう。" : "Ask a question to start your conversation."}</p>
            )}

            {loading && <div className="text-sm text-neutral-400">{locale === "ja" ? "かんがえています..." : "Thinking..."}</div>}
          </div>

          <div className="mt-6 flex gap-3">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleAsk();
            }}
            placeholder={locale === "ja" ? "ぶんしょに しつもん..." : "Ask your document..."}
            className="flex-1 rounded-full bg-neutral-200 px-5 py-3 outline-none dark:bg-neutral-800"
          />

          <button
            onClick={handleAsk}
            disabled={loading}
            className="grid size-12 place-items-center rounded-full text-neutral-700 transition hover:text-neutral-950 disabled:opacity-50 dark:text-neutral-300 dark:hover:text-neutral-100"
            aria-label={locale === "ja" ? "しつもんを おくる" : "Send question"}
          >
            <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
          </div>
        </div>

        <nav className="flex w-5 flex-col items-center gap-2 pt-16 text-xs font-bold text-neutral-400" aria-label={locale === "ja" ? "かいわの ぺーじ" : "Conversation pages"}>
          <button
            onClick={() => setActivePage((page) => page - 1)}
            disabled={activePage === 1}
            className="text-neutral-500 disabled:opacity-30 dark:text-neutral-400"
            aria-label={locale === "ja" ? "まえの ぺーじ" : "Previous page"}
          >
            <svg viewBox="0 0 24 24" className="size-4 -rotate-90" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
          {pageNumbers.map((page, index) =>
            page === "…" ? (
              <span key={`ellipsis-${index}`}>…</span>
            ) : (
            <button
              key={page}
              onClick={() => {
                setExpandedId(null);
                setActivePage(Number(page));
              }}
              className={page === activePage ? "text-neutral-900 dark:text-neutral-100" : "hover:text-neutral-700 dark:hover:text-neutral-200"}
              aria-label={locale === "ja" ? `${page} ぺーじ` : `Page ${page}`}
            >
              {page}
            </button>
            ),
          )}
          <button
            onClick={() => setActivePage((page) => page + 1)}
            disabled={activePage === totalPages}
            className="text-neutral-500 disabled:opacity-30 dark:text-neutral-400"
            aria-label={locale === "ja" ? "つぎの ぺーじ" : "Next page"}
          >
            <svg viewBox="0 0 24 24" className="size-4 rotate-90" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
        </nav>
      </div>
    </section>
  );
}

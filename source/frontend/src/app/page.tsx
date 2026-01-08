"use client";

import { useEffect, useMemo, useState } from "react";

import layout from "./page.module.css";
import controls from "./controls.module.css";

import Header from "../components/Header";
import ChatBox from "../components/ChatBox";
import type { Msg } from "../components/MessageBubble";
import { getOrCreateSessionId } from "../lib/session";
import { postChat, postReset } from "../lib/api";

export default function Page() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

  const [sessionId, setSessionId] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setSessionId(getOrCreateSessionId());
  }, []);

  const canSend = useMemo(
    () => input.trim().length > 0 && !loading,
    [input, loading]
  );

  async function send() {
    const text = input.trim();
    if (!text) return;

    setMessages((m) => [...m, { role: "user", content: text }]);
    setInput("");
    setLoading(true);

    try {
      const data = await postChat(apiBase, sessionId, text);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: data.reply, trace_id: data.trace_id },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function clear() {
    await postReset(apiBase, sessionId);
    setMessages([]);
  }

  return (
    <main className={layout.container}>
      <Header title="Artefact Assistant | Data & AI to drive impact" />

      <div className={controls.topBar}>
        <button
          onClick={clear}
          disabled={loading}
          className={controls.clearBtn}
        >
          Clear conversation
        </button>
        <span className={controls.session}>Session: {sessionId}</span>
      </div>

      <ChatBox messages={messages} loading={loading} />

      <div className={controls.inputBar}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
          className={controls.input}
          onKeyDown={(e) => {
            if (e.key === "Enter" && canSend) send();
          }}
        />
        <button onClick={send} disabled={!canSend} className={controls.sendBtn}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </main>
  );
}

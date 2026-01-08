import { useEffect, useRef } from "react";
import chat from "../app/chat.module.css";
import MessageBubble, { Msg } from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

type Props = {
  messages: Msg[];
  loading: boolean;
};

export default function ChatBox({ messages, loading }: Props) {
  const chatRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, loading]);

  return (
    <div ref={chatRef} className={chat.chatBox}>
      {messages.map((m, idx) => (
        <MessageBubble key={idx} msg={m} />
      ))}

      {loading && <TypingIndicator />}

      {messages.length === 0 && (
        <div className={chat.empty}>
          Try: “What is 128 times 46?”, “Convert 1 USD to BRL”, “How much is 0.1 BTC in BRL?”
        </div>
      )}
    </div>
  );
}

import chat from "../app/chat.module.css";

export type Msg = {
  role: "user" | "assistant";
  content: string;
  trace_id?: string;
};

type Props = { msg: Msg };

export default function MessageBubble({ msg }: Props) {
  return (
    <div
      className={`${chat.message} ${
        msg.role === "user" ? chat.user : chat.assistant
      }`}
    >
      <div className={chat.sender}>
        {msg.role === "user" ? "You" : "Artefact Assistant"}
      </div>

      <div className={msg.role === "user" ? chat.bubbleUser : chat.bubbleAssistant}>
        {msg.content}
      </div>

      {msg.role === "assistant" && msg.trace_id && (
        <div className={chat.trace}>trace_id: {msg.trace_id}</div>
      )}
    </div>
  );
}

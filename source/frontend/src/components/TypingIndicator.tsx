import chat from "../app/chat.module.css";

export default function TypingIndicator() {
  return (
    <div className={`${chat.message} ${chat.assistant}`}>
      <div className={chat.sender}>Artefact Assistant</div>
      <div className={chat.typing}>
        <span>.</span>
        <span>.</span>
        <span>.</span>
      </div>
    </div>
  );
}

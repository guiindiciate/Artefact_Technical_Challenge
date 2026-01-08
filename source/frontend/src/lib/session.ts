export function newSessionId() {
  return (crypto as any).randomUUID
    ? (crypto as any).randomUUID()
    : String(Date.now());
}

export function getOrCreateSessionId(): string {
  const saved = localStorage.getItem("session_id");
  const sid = saved || newSessionId();
  localStorage.setItem("session_id", sid);
  return sid;
}

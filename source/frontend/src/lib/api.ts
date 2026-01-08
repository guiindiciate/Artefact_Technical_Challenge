export async function postChat(apiBase: string, sessionId: string, message: string) {
  const r = await fetch(`${apiBase}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  return r.json();
}

export async function postReset(apiBase: string, sessionId: string) {
  await fetch(`${apiBase}/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
}

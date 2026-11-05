(() => {
  const direct = location.pathname.match(/^\/messages\/(\d+)$/);
  const group = location.pathname === "/mt-group";
  const list = document.querySelector(group ? ".group-chat .chat-messages" : ".chat-messages");
  if (!list || (!direct && !group)) return;
  const known = new Set(Array.from(list.querySelectorAll("[data-message-id]")).map(x => x.dataset.messageId));
  const endpoint = group ? "/api/v1/mt-group" : "/api/v1/messages/" + direct[1];
  let after = Math.max(0, ...Array.from(known).map(Number));
  async function poll() {
    try {
      const response = await fetch(endpoint + "?after=" + after, {credentials:"same-origin"});
      if (!response.ok) return;
      const payload = await response.json();
      for (const message of payload.messages || []) {
        if (known.has(String(message.id))) continue;
        const article = document.createElement("article");
        article.dataset.messageId = message.id;
        article.className = "chat-bubble " + (group ? "theirs" : (message.sender_id === Number(document.body.dataset.currentUserId) ? "mine" : "theirs"));
        if (group) {
          const author = document.createElement("strong"); author.textContent = message.username; article.append(author);
        }
        const body = document.createElement("p"); body.textContent = message.body;
        const time = document.createElement("small"); time.textContent = new Date(message.created_at).toLocaleString();
        article.append(body, time); list.append(article);
        known.add(String(message.id)); after = Math.max(after, message.id);
      }
      if ((payload.messages || []).length) list.scrollTop = list.scrollHeight;
    } catch (_) {}
  }
  window.setInterval(poll, 3000);
})();

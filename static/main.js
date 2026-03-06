const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const animationPrompt = document.getElementById("animation-prompt");
const animationLink = document.getElementById("animation-link");
const logoutBtn = document.getElementById("logout-btn");
const newSessionBtn = document.getElementById("new-session");

let conversationHistory = [];
let typingNode = null;

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderMarkdown(text) {
  let safe = escapeHtml(text);
  safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  safe = safe.replace(/`([^`]+)`/g, "<code>$1</code>");
  safe = safe.replace(/\n/g, "<br>");
  return safe;
}

function appendMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;
  messageDiv.innerHTML = `<p>${renderMarkdown(text)}</p>`;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showAnimationPrompt(question) {
  if (!animationPrompt || !animationLink) return;
  animationLink.href = `/animations?q=${encodeURIComponent(question)}`;
  animationPrompt.classList.remove("hidden");
}

function showTypingIndicator() {
  if (typingNode) return;
  typingNode = document.createElement("div");
  typingNode.className = "message bot-message typing-indicator";
  typingNode.innerHTML = "<p><span></span><span></span><span></span></p>";
  chatBox.appendChild(typingNode);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTypingIndicator() {
  if (!typingNode) return;
  typingNode.remove();
  typingNode = null;
}

if (chatForm) {
  chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage(question, "user");
    userInput.value = "";
    if (animationPrompt) animationPrompt.classList.add("hidden");
    showTypingIndicator();

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question, history: conversationHistory }),
      });
      const data = await response.json();
      hideTypingIndicator();
      appendMessage(data.reply || "I need a moment to respond.", "bot");
      conversationHistory = Array.isArray(data.history) ? data.history : conversationHistory;
      showAnimationPrompt(question);
    } catch (error) {
      hideTypingIndicator();
      appendMessage("Sorry, something went wrong. Try again.", "bot");
    }
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    await fetch("/logout", { method: "POST" });
    window.location.href = "/";
  });
}

if (newSessionBtn) {
  newSessionBtn.addEventListener("click", async () => {
    await fetch("/api/new_session", { method: "POST" });
    conversationHistory = [];
    window.location.reload();
  });
}

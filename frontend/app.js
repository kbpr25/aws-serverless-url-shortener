// Replace this with your actual API Gateway Invoke URL
const API_BASE = "https://1mamyoez59.execute-api.ap-south-1.amazonaws.com/dev";

// Utility: show message inside a div
function showMessage(elementId, message, isError = false) {
  const el = document.getElementById(elementId);
  el.innerHTML = `<p class="${isError ? "error" : ""}">${message}</p>`;
}

// Utility: pretty-print JSON inside a <pre>
function showJSON(elementId, data) {
  const el = document.getElementById(elementId);
  el.textContent = JSON.stringify(data, null, 2);
}

// Function: Create short URL
async function shortenUrl() {
  const longUrl = document.getElementById("longUrl").value.trim();

  if (!longUrl) {
    showMessage("shortResult", "❌ Please enter a valid URL", true);
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/shorten`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ longUrl })
    });

    if (!res.ok) {
      const error = await res.text();
      throw new Error(error);
    }

    const data = await res.json();
    const shortLink = `${API_BASE}/${data.shortId}`;

    showMessage(
      "shortResult",
      `✅ Short link created: <a href="${shortLink}" target="_blank">${shortLink}</a>`
    );
  } catch (err) {
    showMessage("shortResult", `❌ Error: ${err.message}`, true);
  }
}

// Function: Get stats for shortId
async function getStats() {
  const shortId = document.getElementById("shortId").value.trim();

  if (!shortId) {
    showMessage("statsResult", "❌ Please enter a shortId", true);
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/stats/${shortId}`);

    if (!res.ok) {
      const error = await res.text();
      throw new Error(error);
    }

    const data = await res.json();
    showJSON("statsOutput", data);
  } catch (err) {
    showMessage("statsResult", `❌ Error: ${err.message}`, true);
  }
}

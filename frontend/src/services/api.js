const API_URL = "https://lucidverify-backend.onrender.com";

export async function verifyNews(text) {
  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  });

  if (!response.ok) {
    throw new Error("Server error");
  }

  return await response.json();
}

// frontend/src/services/api.js

// 🔗 Your deployed backend URL (from Render)
const BASE_URL = "https://lucidverify-backend.onrender.com";

/**
 * Send text to backend and get prediction
 * @param {string} text
 * @returns {Promise<{label:string, confidence:number, source:string}>}
 */
export async function predictNews(text) {
  try {
    const response = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    // If backend crashes or wrong response
    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error("Prediction error:", error);

    return {
      label: "error",
      confidence: 0,
      source: "backend_unreachable"
    };
  }
}

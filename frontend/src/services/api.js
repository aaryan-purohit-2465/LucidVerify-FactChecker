fetch(`{https://lucidverify-backend.onrender.com}/predict`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    text: userInput
  })
})

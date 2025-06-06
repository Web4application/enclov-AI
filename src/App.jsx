import React, { useState } from 'react'
import './App.css'

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")

  const sendMessage = async () => {
    if (!input.trim()) return

    setMessages([...messages, { role: 'user', content: input }])
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    })

    const data = await response.json()
    setMessages(prev => [...prev, { role: 'ai', content: data.response }])
    setInput("")
  }

  return (
    <div className="chat-container">
      <h1>Enclov AI</h1>
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role}>{msg.content}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === "Enter" && sendMessage()}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  )
}

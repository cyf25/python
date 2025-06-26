import React from "react";
import ChatBox from "./ChatBox";
import "antd/dist/reset.css";

function App() {
  return (
    <div style={{ background: "#f7f8fa", minHeight: "100vh" }}>
      <div style={{
        width: 700, maxWidth: "95vw", margin: "0 auto", paddingTop: 40
      }}>
        <h1 style={{ fontWeight: 700, fontSize: 32, marginBottom: 24 }}>
          🛒 电商智能客服助手 (RAG + DeepSeek)
        </h1>
        <ChatBox />
      </div>
    </div>
  );
}

export default App; 
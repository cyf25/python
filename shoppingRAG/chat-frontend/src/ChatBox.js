import React, { useRef, useState, useEffect } from "react";
import { Input, Button, List, Avatar, message as antdMsg, Typography } from "antd";
import { UserOutlined, RobotOutlined } from "@ant-design/icons";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const API_URL = "http://localhost:8000/rag/chat";

function ChatBox() {
  const [input, setInput] = useState("");
  const [chatList, setChatList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => localStorage.getItem("session_id") || "");
  const listRef = useRef(null);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [chatList]);

  const sendMsg = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userMsg = { role: "user", content: input };
    setChatList((prev) => [...prev, userMsg]);
    try {
      const resp = await axios.post(API_URL, {
        question: input,
        session_id: sessionId || undefined
      });
      setSessionId(resp.data.session_id);
      localStorage.setItem("session_id", resp.data.session_id);
      setChatList((prev) => [
        ...prev,
        { role: "assistant", content: resp.data.answer }
      ]);
      setInput("");
    } catch (e) {
      antdMsg.error("请求失败");
    }
    setLoading(false);
  };

  const handleInputKeyDown = (e) => {
    if (e.key === "Enter" && !loading) {
      sendMsg();
    }
  };

  return (
    <div style={{
      position: "relative", minHeight: 600, background: "#fff",
      borderRadius: 20, boxShadow: "0 4px 32px rgba(0,0,0,0.10)",
      paddingBottom: 100, marginBottom: 32, width: 900, maxWidth: "98vw", marginLeft: "auto", marginRight: "auto"
    }}>
      <div
        ref={listRef}
        style={{
          maxHeight: 600, overflowY: "auto", padding: 36, paddingBottom: 0
        }}
      >
        <List
          dataSource={chatList}
          renderItem={(item, idx) => (
            <List.Item
              style={{
                border: "none", padding: 0, marginBottom: 24,
                justifyContent: item.role === "user" ? "flex-end" : "flex-start"
              }}
            >
              {item.role === "assistant" && (
                <Avatar
                  icon={<RobotOutlined />}
                  style={{ background: "#409eff", marginRight: 12 }}
                />
              )}
              <div
                style={{
                  background: item.role === "user" ? "#e6f7ff" : "#f5f5f5",
                  color: "#222", borderRadius: 18, padding: "14px 24px",
                  maxWidth: 600, wordBreak: "break-all", fontSize: 17, lineHeight: 1.8,
                  boxShadow: item.role === "assistant" ? "0 2px 8px #e6f7ff" : "0 2px 8px #f5f5f5"
                }}
              >
                {item.role === "assistant"
                  ? <ReactMarkdown>{item.content}</ReactMarkdown>
                  : <Typography.Text>{item.content}</Typography.Text>
                }
              </div>
              {item.role === "user" && (
                <Avatar
                  icon={<UserOutlined />}
                  style={{ background: "#87d068", marginLeft: 12 }}
                />
              )}
            </List.Item>
          )}
        />
      </div>
      <div
        style={{
          position: "absolute", left: 0, right: 0, bottom: 0,
          padding: 24, background: "#fff", borderRadius: "0 0 20px 20px",
          boxShadow: "0 -2px 12px rgba(0,0,0,0.04)"
        }}
      >
        <Input
          size="large"
          placeholder="请输入您的问题…"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleInputKeyDown}
          style={{ width: "calc(100% - 120px)", marginRight: 16, borderRadius: 28, fontSize: 18, height: 48 }}
          disabled={loading}
        />
        <Button
          type="primary"
          size="large"
          style={{ borderRadius: 28, width: 100, fontSize: 18, height: 48 }}
          onClick={sendMsg}
          loading={loading}
        >
          发送
        </Button>
      </div>
    </div>
  );
}

export default ChatBox; 
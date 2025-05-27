import { useEffect, useState } from "react";
import { ChatModule } from "@mlc-ai/web-llm";

export const useWebLLM = () => {
  const [chat, setChat] = useState<ChatModule | null>(null);
  const [reply, setReply] = useState<string>("");

  useEffect(() => {
    const loadModel = async () => {
      const chatModule = new ChatModule();
      await chatModule.reload("Llama-3-8B-Instruct-q4f32_1");
      setChat(chatModule);
    };
    loadModel();
  }, []);

  const ask = async (prompt: string) => {
    if (chat) {
      await chat.resetChat();
      await chat.generate(prompt, (chunk: string) => {
        setReply(prev => prev + chunk);
      });
    }
  };

  return { reply, ask };
};

import { useState } from 'react';
import { ChatContainer, type UiMessage } from './components/ChatContainer';
import { InputArea } from './components/InputArea';
import { sendMessage } from './api/client';
import { Sprout } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid';

function App() {
  const [messages, setMessages] = useState<UiMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());

  const handleSend = async (text: string) => {
    // Add user message
    const userMsg: UiMessage = {
      id: uuidv4(),
      role: 'user',
      content: text
    };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await sendMessage(text, sessionId);

      const botMsg: UiMessage = {
        id: uuidv4(),
        role: 'bot',
        content: response.response,
        type: response.response_type,
        remedies: response.remedies_json,
        when_to_seek_help: response.when_to_seek_help
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      // Add error message
      const errorMsg: UiMessage = {
        id: uuidv4(),
        role: 'bot',
        content: "I'm having trouble connecting to the server. Please make sure the backend is running."
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-herba-50 font-sans text-slate-800">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-herba-100 py-3 px-4 shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="bg-herba-100 p-2 rounded-xl text-herba-600">
            <Sprout size={24} />
          </div>
          <div>
            <h1 className="font-bold text-xl text-herba-900 tracking-tight">Herba</h1>
            <p className="text-xs text-herba-500 font-medium">Your Health Companion</p>
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-hidden relative flex flex-col max-w-4xl mx-auto w-full bg-white md:border-2 md:border-herba-400 shadow-xl md:my-4 md:rounded-2xl">
        <ChatContainer messages={messages} isLoading={isLoading} />
        <InputArea onSend={handleSend} isLoading={isLoading} />
      </main>
    </div>
  );
}

export default App;

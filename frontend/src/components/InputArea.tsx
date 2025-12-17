import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Mic, MicOff } from 'lucide-react';
import { cn } from '../lib/utils';

// Web Speech API Import Hack
declare global {
    interface Window {
        webkitSpeechRecognition: any;
    }
}

interface InputAreaProps {
    onSend: (message: string) => void;
    isLoading: boolean;
}

export const InputArea: React.FC<InputAreaProps> = ({ onSend, isLoading }) => {
    const [input, setInput] = useState('');
    const [isListening, setIsListening] = useState(false);
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const recognitionRef = useRef<any>(null);

    useEffect(() => {
        // Initialize Speech Recognition if available
        if ('webkitSpeechRecognition' in window) {
            const recognition = new window.webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                setInput(prev => prev + (prev ? ' ' : '') + transcript);
                setIsListening(false);
            };

            recognition.onerror = () => {
                setIsListening(false);
            };

            recognition.onend = () => {
                setIsListening(false);
            };

            recognitionRef.current = recognition;
        }
    }, []);

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
        }
    }, [input]);

    const toggleListening = () => {
        if (!recognitionRef.current) {
            alert("Voice input is not supported in this browser.");
            return;
        }

        if (isListening) {
            recognitionRef.current.stop();
            setIsListening(false);
        } else {
            recognitionRef.current.start();
            setIsListening(true);
        }
    };

    const handleSubmit = (e?: React.FormEvent) => {
        e?.preventDefault();
        if (input.trim() && !isLoading) {
            onSend(input);
            setInput('');
            if (textareaRef.current) textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-gray-100 flex gap-2 sticky bottom-0">
            <div className="relative flex-1">
                <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={isListening ? "Listening..." : "Describe your symptoms or ask a question..."}
                    rows={1}
                    className={cn(
                        "w-full resize-none rounded-xl border px-4 py-3 pr-12 text-sm focus:outline-none focus:ring-1 max-h-32 scrollbar-hide transition-colors",
                        isListening
                            ? "border-herba-500 bg-herba-50 ring-herba-500"
                            : "border-gray-200 bg-gray-50 focus:border-herba-500 focus:ring-herba-500"
                    )}
                    disabled={isLoading}
                />

                {/* Loading Spinner */}
                {isLoading && (
                    <div className="absolute right-3 top-3">
                        <Loader2 className="animate-spin text-herba-600" size={20} />
                    </div>
                )}
            </div>

            {/* Voice Button */}
            <button
                type="button"
                onClick={toggleListening}
                disabled={isLoading}
                className={cn(
                    "rounded-xl px-3 py-2 flex items-center justify-center transition-all bg-gray-100 hover:bg-gray-200 text-gray-600",
                    isListening && "bg-red-100 text-red-600 hover:bg-red-200 animate-pulse"
                )}
                title="Voice Input"
            >
                {isListening ? <MicOff size={20} /> : <Mic size={20} />}
            </button>

            {/* Send Button */}
            <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className={cn(
                    "rounded-xl px-4 py-2 flex items-center justify-center transition-all",
                    input.trim() && !isLoading
                        ? "bg-herba-600 text-white hover:bg-herba-700 shadow-md transform hover:scale-105"
                        : "bg-gray-100 text-gray-400 cursor-not-allowed"
                )}
            >
                <Send size={20} />
            </button>
        </form>
    );
};

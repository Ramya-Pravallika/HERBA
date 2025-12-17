import React, { useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { RemedyCard } from './RemedyCard';
import type { Remedy } from '../types';
import { Loader2 } from 'lucide-react';

export interface UiMessage {
    id: string;
    role: 'user' | 'bot';
    content: string;
    remedies?: Remedy[];
    type?: 'normal' | 'provide_remedies' | 'red_flag_emergency';
    when_to_seek_help?: string[];
}

interface ChatContainerProps {
    messages: UiMessage[];
    isLoading: boolean;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({ messages, isLoading }) => {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center text-gray-500 space-y-4">
                    <div className="w-16 h-16 bg-herba-100 rounded-full flex items-center justify-center mb-2">
                        <span className="text-3xl">🌿</span>
                    </div>
                    <h2 className="text-xl font-semibold text-herba-800">Welcome to Herba</h2>
                    <p className="max-w-md">I'm your personal health companion. Describe your symptoms, and I'll suggest natural home remedies.</p>
                </div>
            )}

            {messages.map((msg) => (
                <React.Fragment key={msg.id}>
                    {/* Text Content */}
                    {msg.content && (
                        <MessageBubble
                            content={msg.content}
                            isUser={msg.role === 'user'}
                        />
                    )}

                    {/* Remedies (only for bot) */}
                    {msg.role === 'bot' && msg.remedies && msg.remedies.length > 0 && (
                        <div className="pl-12 max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            {msg.remedies.map((remedy, idx) => (
                                <RemedyCard key={idx} remedy={remedy} index={idx} />
                            ))}
                        </div>
                    )}

                    {/* Red Flag Warning */}
                    {msg.type === 'red_flag_emergency' && (
                        <div className="pl-12 mb-4">
                            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg">
                                <p className="font-bold text-red-700">EMERGENCY ALERT</p>
                                <p className="text-red-800">Please seek immediate medical attention.</p>
                            </div>
                        </div>
                    )}

                    {/* When to seek help */}
                    {msg.when_to_seek_help && msg.when_to_seek_help.length > 0 && (
                        <div className="pl-12 mb-4">
                            <div className="bg-teal-50 border border-teal-100 rounded-xl p-4">
                                <h4 className="font-semibold text-teal-800 mb-2 flex items-center gap-2">
                                    ⚕️ When to Seek Medical Help
                                </h4>
                                <ul className="list-disc list-inside space-y-1 text-sm text-teal-900">
                                    {msg.when_to_seek_help.map((item, i) => (
                                        <li key={i}>{item}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </React.Fragment>
            ))}

            {isLoading && (
                <div className="flex justify-start w-full animate-pulse">
                    <div className="flex items-center gap-2 bg-gray-50 rounded-2xl p-4 ml-12">
                        <Loader2 className="animate-spin text-herba-400" size={16} />
                        <span className="text-xs text-gray-500">Thinking...</span>
                    </div>
                </div>
            )}

            <div ref={bottomRef} className="h-1" />
        </div>
    );
};

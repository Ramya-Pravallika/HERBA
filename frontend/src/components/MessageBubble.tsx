import React from 'react';
import ReactMarkdown from 'react-markdown';
import { cn } from '../lib/utils';
import { User, Bot } from 'lucide-react';

interface MessageBubbleProps {
    content: string;
    isUser: boolean;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ content, isUser }) => {
    return (
        <div className={cn("flex w-full mb-4", isUser ? "justify-end" : "justify-start")}>
            <div className={cn("flex max-w-[80%] md:max-w-[70%]", isUser ? "flex-row-reverse" : "flex-row")}>

                {/* Avatar */}
                <div className={cn(
                    "flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center mx-2",
                    isUser ? "bg-herba-600 text-white" : "bg-teal-600 text-white"
                )}>
                    {isUser ? <User size={18} /> : <Bot size={18} />}
                </div>

                {/* Bubble */}
                <div className={cn(
                    "p-4 rounded-2xl shadow-sm text-sm md:text-base",
                    isUser
                        ? "bg-herba-600 text-white rounded-br-none"
                        : "bg-white text-gray-800 border border-gray-100 rounded-bl-none"
                )}>
                    <div className="prose prose-sm max-w-none dark:prose-invert prose-p:my-1 prose-headings:my-2 prose-strong:text-inherit">
                        <ReactMarkdown
                            components={{
                                // Custom link styling
                                a: ({ node, ...props }) => <a {...props} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer" />
                            }}
                        >
                            {content}
                        </ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
};

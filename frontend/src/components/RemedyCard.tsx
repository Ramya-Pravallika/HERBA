import React, { useState } from 'react';
import { ChevronDown, ChevronUp, AlertTriangle } from 'lucide-react';
import type { Remedy } from '../types';
import { motion, AnimatePresence } from 'framer-motion';

interface RemedyCardProps {
    remedy: Remedy;
    index: number;
}

export const RemedyCard: React.FC<RemedyCardProps> = ({ remedy, index }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-xl border border-herba-200 shadow-sm overflow-hidden mb-3 hover:shadow-md transition-shadow"
        >
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between p-4 text-left hover:bg-herba-50 transition-colors"
            >
                <div>
                    <h3 className="font-semibold text-herba-800 text-lg">{remedy.name}</h3>
                    <p className="text-sm text-gray-600 line-clamp-1">{remedy.rationale}</p>
                </div>
                {isExpanded ? <ChevronUp className="text-herba-500" /> : <ChevronDown className="text-herba-500" />}
            </button>

            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                    >
                        <div className="p-4 pt-0 bg-herba-50/50">
                            <div className="mb-4">
                                <h4 className="font-medium text-herba-700 mb-2">Instructions</h4>
                                <ol className="list-decimal list-inside space-y-1 text-sm text-gray-700">
                                    {remedy.steps.map((step, i) => (
                                        <li key={i} className="pl-1">{step}</li>
                                    ))}
                                </ol>
                            </div>

                            {remedy.precautions && remedy.precautions.length > 0 && (
                                <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 flex gap-2">
                                    <AlertTriangle className="text-amber-500 flex-shrink-0" size={18} />
                                    <div className="text-sm text-amber-800">
                                        <span className="font-medium">Precautions:</span> {remedy.precautions.join(', ')}
                                    </div>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
};

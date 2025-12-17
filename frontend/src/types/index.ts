export interface Remedy {
    name: string;
    rationale: string;
    steps: string[];
    precautions: string[];
}

export interface ChatRequest {
    message: string;
    session_id?: string;
    conversation_history?: Array<{ role: string; content: string }>;
}

export interface ChatResponse {
    response: string;
    session_id: string;
    response_type: 'normal' | 'provide_remedies' | 'red_flag_emergency';
    needs_confirmation: boolean;
    red_flag: boolean;
    remedies_json?: Remedy[];
    when_to_seek_help?: string[];
    context?: any;
}

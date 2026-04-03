'use client';

import { useState, useRef, useEffect } from 'react';
import { PLATFORMS, PLATFORM_LIST } from '@/lib/constants';

const SUGGESTED_PROMPTS = {
  harley: [
    'What does DTC P0131 mean on my Harley?',
    'My Street Glide won\'t start — clicking noise',
    'Oil change interval for a 2020 Road King',
    'What causes the check engine light on a Sportster?',
  ],
  auto: [
    'What does P0420 mean on my car?',
    'My check engine light is flashing — is it safe to drive?',
    'How often should I change transmission fluid?',
    'What do different colored fluids under my car mean?',
  ],
  trucking: [
    'How many hours can I drive before my 10-hour break?',
    'What are the DOT pre-trip inspection requirements?',
    'How to calculate my cost per mile as an owner-operator?',
    'When do I need to file IFTA?',
  ],
  ebike: [
    'My Bosch e-bike shows error 503 — what does it mean?',
    'How to check battery health on my e-bike?',
    'Can I ride a Class 3 e-bike on bike paths in California?',
    'My range dropped from 50 to 30 miles — why?',
  ],
  scooter: [
    'Error E15 on my Ninebot — what should I do?',
    'How often should I change scooter tires?',
    'Best way to maintain battery life on my electric scooter?',
    'My scooter loses power going uphill — normal?',
  ],
};

export default function AIChatPage() {
  const [platform, setPlatform] = useState('harley');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [queryCount, setQueryCount] = useState(0);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const userMessage = text || input.trim();
    if (!userMessage || loading) return;

    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const res = await fetch('/api/ai-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          platform,
          history: messages.slice(-10),
        }),
      });

      const data = await res.json();

      if (res.ok) {
        setMessages((prev) => [...prev, { role: 'assistant', content: data.reply, platform }]);
        setQueryCount((c) => c + 1);
      } else {
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: data.error || 'Something went wrong. Please try again.', isError: true },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Network error. Please check your connection and try again.', isError: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  const platformColor = PLATFORMS[platform]?.color || '#E8720E';

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
            <span className="text-border">|</span>
            <h1 className="font-bold text-lg">🤖 AI Diagnostic Chat</h1>
          </div>
          <div className="flex items-center gap-2 text-sm text-text-muted">
            <span>{queryCount} queries today</span>
          </div>
        </div>
      </header>

      {/* Platform selector */}
      <div className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex flex-wrap gap-2">
          {PLATFORM_LIST.map((p) => (
            <button
              key={p.id}
              onClick={() => setPlatform(p.id)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                platform === p.id
                  ? 'text-white'
                  : 'bg-surface text-text-muted border border-border hover:text-text-primary'
              }`}
              style={platform === p.id ? { backgroundColor: p.color } : {}}
            >
              {p.icon} {p.shortName}
            </button>
          ))}
        </div>
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto p-4">
          {messages.length === 0 ? (
            /* Empty state with suggested prompts */
            <div className="py-16 text-center">
              <div
                className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl"
                style={{ backgroundColor: platformColor + '20' }}
              >
                {PLATFORMS[platform]?.icon}
              </div>
              <h2 className="text-xl font-bold mb-2">
                {PLATFORMS[platform]?.name} Expert
              </h2>
              <p className="text-text-muted mb-8 max-w-md mx-auto">
                Ask me anything about your {PLATFORMS[platform]?.shortName.toLowerCase()}.
                I can help with diagnostics, maintenance, codes, and more.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-xl mx-auto">
                {SUGGESTED_PROMPTS[platform]?.map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(prompt)}
                    className="mc-card-hover p-3 text-left text-sm text-text-secondary hover:text-text-primary"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            /* Messages */
            <div className="space-y-4">
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      msg.role === 'user'
                        ? 'bg-harley text-white rounded-br-md'
                        : msg.isError
                        ? 'bg-danger/10 text-danger border border-danger/20 rounded-bl-md'
                        : 'bg-surface border border-border rounded-bl-md'
                    }`}
                  >
                    {msg.role === 'assistant' && !msg.isError && (
                      <div className="flex items-center gap-1.5 mb-1.5">
                        <span className="text-xs">{PLATFORMS[msg.platform || platform]?.icon}</span>
                        <span className="text-xs font-medium" style={{ color: PLATFORMS[msg.platform || platform]?.color }}>
                          {PLATFORMS[msg.platform || platform]?.shortName} Expert
                        </span>
                      </div>
                    )}
                    <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              ))}

              {/* Typing indicator */}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-surface border border-border rounded-2xl rounded-bl-md px-4 py-3">
                    <div className="flex items-center gap-1.5 mb-1.5">
                      <span className="text-xs">{PLATFORMS[platform]?.icon}</span>
                      <span className="text-xs font-medium" style={{ color: platformColor }}>
                        {PLATFORMS[platform]?.shortName} Expert
                      </span>
                    </div>
                    <div className="flex gap-1">
                      <span className="w-2 h-2 rounded-full bg-text-muted animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 rounded-full bg-text-muted animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 rounded-full bg-text-muted animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-border p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask about your ${PLATFORMS[platform]?.shortName.toLowerCase()}...`}
            className="mc-input flex-1"
            maxLength={2000}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="mc-btn-primary px-6"
          >
            {loading ? '...' : 'Send'}
          </button>
        </form>
        <p className="text-text-faint text-xs text-center mt-2 max-w-4xl mx-auto">
          AI responses are informational only. Always consult a qualified mechanic for safety-critical repairs.
        </p>
      </div>
    </div>
  );
}

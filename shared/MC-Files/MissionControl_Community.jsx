'use client';

import { useState } from 'react';
import { PLATFORMS, PLATFORM_LIST } from '@/lib/constants';
import { PlatformBadge, TierBadge } from '@/components/PlatformBadge';

const MOCK_THREADS = [
  { id: '1', title: 'P0131 on 2019 Street Glide — O2 sensor or exhaust leak?', content: 'Getting P0131 code intermittently. Bike runs fine but check engine light keeps coming back after clearing. 22k miles, stock exhaust.', platform: 'harley', author: 'RoadKing_Mike', tier: 'premium', replies: 12, upvotes: 24, time: '2 hours ago', pinned: true },
  { id: '2', title: 'Best way to track fuel economy across multiple vehicles?', content: 'I have a truck and a car. Looking for a simple way to log fill-ups and compare MPG over time.', platform: 'auto', author: 'GearHead42', tier: 'free', replies: 8, upvotes: 15, time: '4 hours ago' },
  { id: '3', title: 'HOS 30-minute break question — does it reset the 8-hour clock?', content: 'New CDL driver here. If I take my 30-minute break at hour 6, does my 8-hour clock restart or just pause?', platform: 'trucking', author: 'TruckerTom', tier: 'pro', replies: 21, upvotes: 31, time: '6 hours ago' },
  { id: '4', title: 'Bosch CX motor making clicking noise after firmware update', content: 'Updated my Bosch CX to the latest firmware and now there\'s a clicking noise at low cadence. Anyone else?', platform: 'ebike', author: 'PedalPower', tier: 'premium', replies: 5, upvotes: 9, time: '8 hours ago' },
  { id: '5', title: 'Ninebot Max — tire pressure for best range?', content: 'What PSI are you running on the Ninebot Max? I want to maximize range for my commute.', platform: 'scooter', author: 'ScootCommuter', tier: 'free', replies: 14, upvotes: 18, time: '1 day ago' },
  { id: '6', title: 'Milwaukee-Eight vs Twin Cam — reliability comparison', content: 'Thinking about upgrading from my 2016 (TC) to a 2022 (M8). Anyone have experience with both? Reliability differences?', platform: 'harley', author: 'V_Twin_Life', tier: 'pro', replies: 33, upvotes: 47, time: '1 day ago' },
  { id: '7', title: 'DIY e-bike build — Bafang BBSHD vs BBS02 for commuting', content: 'Building my first e-bike for a 15-mile round trip commute. Is the BBSHD overkill? Budget is around $1500 total.', platform: 'ebike', author: 'DIY_Rider', tier: 'free', replies: 19, upvotes: 22, time: '2 days ago' },
  { id: '8', title: 'Owner-operator fuel surcharge — how to calculate fairly', content: 'Starting my own authority next month. How are you guys calculating fuel surcharges for your customers?', platform: 'trucking', author: 'OwnBoss_Haul', tier: 'premium', replies: 7, upvotes: 11, time: '3 days ago' },
];

export default function CommunityPage() {
  const [threads, setThreads] = useState(MOCK_THREADS);
  const [platformFilter, setPlatformFilter] = useState('all');
  const [showNewThread, setShowNewThread] = useState(false);
  const [votedThreads, setVotedThreads] = useState(new Set());

  const filtered = threads.filter((t) => platformFilter === 'all' || t.platform === platformFilter);

  const toggleUpvote = (id) => {
    setVotedThreads((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
        setThreads((t) => t.map((thread) => thread.id === id ? { ...thread, upvotes: thread.upvotes - 1 } : thread));
      } else {
        next.add(id);
        setThreads((t) => t.map((thread) => thread.id === id ? { ...thread, upvotes: thread.upvotes + 1 } : thread));
      }
      return next;
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a href="/dashboard" className="text-text-muted hover:text-text-primary text-sm">← Dashboard</a>
            <span className="text-border">|</span>
            <h1 className="font-bold text-lg">💬 Community</h1>
          </div>
          <button onClick={() => setShowNewThread(!showNewThread)} className="mc-btn-primary text-sm">
            + New Thread
          </button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Platform filter */}
        <div className="flex gap-2 flex-wrap mb-6">
          <button onClick={() => setPlatformFilter('all')} className={`px-3 py-1.5 rounded-full text-xs font-medium ${platformFilter === 'all' ? 'bg-text-primary text-background' : 'bg-surface text-text-muted border border-border'}`}>All</button>
          {PLATFORM_LIST.map((p) => (
            <button key={p.id} onClick={() => setPlatformFilter(p.id)} className={`px-3 py-1.5 rounded-full text-xs font-medium ${platformFilter === p.id ? 'text-white' : 'bg-surface text-text-muted border border-border'}`} style={platformFilter === p.id ? { backgroundColor: p.color } : {}}>
              {p.icon} {p.shortName}
            </button>
          ))}
        </div>

        {/* New thread form */}
        {showNewThread && (
          <div className="mc-card p-6 mb-6 animate-slide-down">
            <h3 className="font-bold mb-4">New Thread</h3>
            <div className="space-y-4">
              <input type="text" placeholder="Thread title..." className="mc-input" />
              <textarea placeholder="What's on your mind?" className="mc-input h-24 resize-none" />
              <div className="flex items-center gap-3">
                <select className="mc-input w-auto">
                  <option value="">Select platform</option>
                  {PLATFORM_LIST.map((p) => (<option key={p.id} value={p.id}>{p.icon} {p.name}</option>))}
                </select>
                <button className="mc-btn-primary">Post Thread</button>
                <button onClick={() => setShowNewThread(false)} className="mc-btn-ghost">Cancel</button>
              </div>
            </div>
          </div>
        )}

        {/* Threads */}
        <div className="space-y-3">
          {filtered.map((thread) => (
            <div key={thread.id} className={`mc-card-hover p-4 flex gap-4 ${thread.pinned ? 'border-harley/30' : ''}`}>
              {/* Upvote */}
              <div className="flex flex-col items-center gap-1">
                <button
                  onClick={() => toggleUpvote(thread.id)}
                  className={`text-lg transition-colors ${votedThreads.has(thread.id) ? 'text-harley' : 'text-text-faint hover:text-text-muted'}`}
                >
                  ▲
                </button>
                <span className={`text-sm font-bold ${votedThreads.has(thread.id) ? 'text-harley' : 'text-text-muted'}`}>
                  {thread.upvotes}
                </span>
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap mb-1">
                  {thread.pinned && <span className="text-xs text-harley font-bold">📌 PINNED</span>}
                  <PlatformBadge platform={thread.platform} size="sm" />
                </div>
                <h3 className="font-semibold mb-1 hover:text-harley cursor-pointer">{thread.title}</h3>
                <p className="text-text-muted text-sm line-clamp-2 mb-2">{thread.content}</p>
                <div className="flex items-center gap-3 text-xs text-text-dim">
                  <span className="flex items-center gap-1">
                    <span>{thread.author}</span>
                    <TierBadge tier={thread.tier} size="sm" />
                  </span>
                  <span>· {thread.replies} replies</span>
                  <span>· {thread.time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

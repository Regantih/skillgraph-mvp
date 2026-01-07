'use client';

import React, { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Activity, Shield } from 'lucide-react';

// UPDATE THIS WITH YOUR RENDER URL AFTER DEPLOYMENT
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AgentDashboard() {
    const [marketData, setMarketData] = useState<any>(null);

    // MOCK DATA FOR RADAR
    const VECTOR_DATA = [
        { skill: 'Python', confidence: 0.95, fullMark: 1 },
        { skill: 'System Arch', confidence: 0.85, fullMark: 1 },
        { skill: 'React/Next', confidence: 0.70, fullMark: 1 },
        { skill: 'AI/LLMs', confidence: 0.88, fullMark: 1 },
    ];

    useEffect(() => {
        // Check connection to Brain
        fetch(`${API_URL}/`)
            .then(res => res.json())
            .then(data => console.log("Brain Connected:", data))
            .catch(err => console.error("Brain Offline"));
    }, []);

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-8">
            <header className="mb-8 flex items-center gap-2">
                <Shield className="text-emerald-400" size={28} />
                <h1 className="text-2xl font-bold">AGENT COMMAND <span className="text-slate-500 text-sm">v.0.9.2</span></h1>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl max-w-2xl">
                <h2 className="text-lg font-semibold text-white mb-4">Verified Vector Signature</h2>
                <div className="h-[300px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={VECTOR_DATA}>
                            <PolarGrid stroke="#334155" />
                            <PolarAngleAxis dataKey="skill" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                            <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
                            <Radar name="Confidence" dataKey="confidence" stroke="#10b981" strokeWidth={3} fill="#10b981" fillOpacity={0.2} />
                        </RadarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

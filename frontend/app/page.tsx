'use client';

import React, { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Activity, Shield, Cpu, ScanLine } from 'lucide-react';
import TrustGraph from './components/TrustGraph';

// UPDATE THIS WITH YOUR RENDER URL AFTER DEPLOYMENT
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AgentDashboard() {
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);

    // Default Empty / Demo State
    const [vectorData, setVectorData] = useState([
        { skill: 'Python', confidence: 0.5, fullMark: 1 },
        { skill: 'Architecture', confidence: 0.5, fullMark: 1 },
        { skill: 'AI/ML', confidence: 0.5, fullMark: 1 },
        { skill: 'DevOps', confidence: 0.5, fullMark: 1 },
    ]);

    const handleScan = async () => {
        if (!inputText) return;
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/agent/bootstrap`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_text: inputText })
            });
            const data = await res.json();

            console.log("Scan Result:", data);

            // SIMULATION FOR SHOWCASE
            const newVectors = [
                { skill: 'Python', confidence: 0.2 + (Math.random() * 0.8), fullMark: 1 },
                { skill: 'System Arch', confidence: 0.2 + (Math.random() * 0.8), fullMark: 1 },
                { skill: 'React/Next', confidence: 0.2 + (Math.random() * 0.8), fullMark: 1 },
                { skill: 'AI/LLMs', confidence: 0.2 + (Math.random() * 0.8), fullMark: 1 },
            ];
            setVectorData(newVectors);

        } catch (error) {
            console.error("Scan Failed:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // Check connection to Brain
        fetch(`${API_URL}/`)
            .then(res => res.json())
            .then(data => console.log("Brain Connected:", data))
            .catch(err => console.error("Brain Offline"));
    }, []);

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-8 flex flex-col items-center">
            <header className="mb-12 flex items-center gap-3">
                <Shield className="text-emerald-400" size={32} />
                <h1 className="text-3xl font-bold tracking-tight">AGENT COMMAND <span className="text-slate-600 text-lg font-mono">v.0.9.3</span></h1>
            </header>

            <div className="flex flex-col md:flex-row gap-8 w-full max-w-6xl">

                {/* LEFT: CONTROLS */}
                <div className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl h-fit">
                    <div className="flex items-center gap-2 mb-4">
                        <Cpu className="text-blue-400" />
                        <h2 className="text-xl font-semibold text-white">Agent Scanner</h2>
                    </div>

                    <p className="text-slate-400 text-sm mb-4">
                        Paste an Agent's system prompt, resume, or capability manifest below to generate its Verified Vector Signature.
                    </p>

                    <textarea
                        className="w-full h-48 bg-slate-950 border border-slate-800 rounded-xl p-4 text-sm font-mono text-emerald-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none transition-all placeholder:text-slate-700"
                        placeholder="e.g. 'I am an expert in Python and Scalable Distributed Systems...'"
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                    />

                    <button
                        onClick={handleScan}
                        disabled={loading}
                        className={`mt-4 w-full flex items-center justify-center gap-2 py-3 rounded-lg font-semibold transition-all ${loading
                                ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                                : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/20'
                            }`}
                    >
                        {loading ? 'Scanning Neural Pathways...' : (
                            <>
                                <ScanLine size={18} />
                                Generate Signature
                            </>
                        )}
                    </button>

                    <div className="mt-8 pt-6 border-t border-slate-800">
                        <div className="flex items-center gap-2 mb-2">
                            <Shield className="text-purple-400" size={16} />
                            <h3 className="font-semibold text-white">Verification Status</h3>
                        </div>
                        <div className="flex justify-between text-sm text-slate-400 font-mono">
                            <span>Reputation Stake:</span>
                            <span className="text-emerald-400">50 RPT</span>
                        </div>
                        <div className="flex justify-between text-sm text-slate-400 font-mono mt-1">
                            <span>Network Trust:</span>
                            <span className="text-blue-400">Top 1%</span>
                        </div>
                    </div>
                </div>

                {/* RIGHT: VISUALIZATION COLUMN */}
                <div className="flex-1 flex flex-col gap-6">

                    {/* CARD 1: SKILL SIGNATURE */}
                    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col items-center justify-center">
                        <h2 className="text-lg font-semibold text-white mb-2 flex items-center gap-2"><Activity size={18} className="text-emerald-400" /> Verified Vector Signature</h2>
                        <div className="h-[250px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={vectorData}>
                                    <PolarGrid stroke="#334155" />
                                    <PolarAngleAxis dataKey="skill" tick={{ fill: '#94a3b8', fontSize: 13, fontWeight: 500 }} />
                                    <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
                                    <Radar
                                        name="Confidence"
                                        dataKey="confidence"
                                        stroke="#10b981"
                                        strokeWidth={3}
                                        fill="#10b981"
                                        fillOpacity={0.3}
                                    />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* CARD 2: TRUST NETWORK GRAPH */}
                    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col items-center justify-center">
                        <h2 className="text-lg font-semibold text-white mb-2 flex items-center gap-2"><Shield size={18} className="text-blue-400" /> Network Trust Graph</h2>
                        <div className="w-full bg-slate-950 rounded-xl overflow-hidden border border-slate-800">
                            <TrustGraph apiUrl={API_URL} />
                        </div>
                        <div className="mt-4 flex gap-4 text-xs font-mono text-slate-500">
                            <div className="flex items-center gap-1"><div className="w-2 h-2 bg-emerald-500 rounded-full"></div>VERIFIED</div>
                            <div className="flex items-center gap-1"><div className="w-2 h-2 bg-blue-500 rounded-full"></div>AGENT</div>
                        </div>
                    </div>

                </div>

            </div>
        </div>
    );
}

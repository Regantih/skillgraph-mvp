'use client';

import React, { useEffect, useState } from 'react';

interface Node {
    id: string;
    label: string;
    type: 'verifier' | 'agent';
    x?: number;
    y?: number;
}

interface Edge {
    source: string;
    target: string;
    label: string;
}

interface GraphData {
    nodes: Node[];
    edges: Edge[];
}

export default function TrustGraph({ apiUrl }: { apiUrl: string }) {
    const [data, setData] = useState<GraphData | null>(null);

    useEffect(() => {
        fetch(`${apiUrl}/trust/graph`)
            .then(res => res.json())
            .then((graphData: GraphData) => {
                // Simple deterministic layout for MVP
                // Place nodes in a circle
                const nodes = graphData.nodes.map((node, i) => {
                    const angle = (i / graphData.nodes.length) * 2 * Math.PI;
                    const r = 120; // Radius
                    return {
                        ...node,
                        x: 200 + r * Math.cos(angle),
                        y: 150 + r * Math.sin(angle)
                    };
                });
                setData({ nodes, edges: graphData.edges });
            })
            .catch(err => console.error("Failed to fetch graph", err));
    }, [apiUrl]);

    if (!data) return <div className="text-slate-500 animate-pulse">Loading Trust Network...</div>;

    return (
        <svg width="100%" height="300" viewBox="0 0 400 300" className="bg-slate-900 rounded-xl border border-slate-800">
            {/* Edges */}
            {data.edges.map((edge, i) => {
                const s = data.nodes.find(n => n.id === edge.source);
                const t = data.nodes.find(n => n.id === edge.target);
                if (!s || !t) return null;
                return (
                    <g key={i}>
                        <line x1={s.x} y1={s.y} x2={t.x} y2={t.y} stroke="#334155" strokeWidth="2" />
                        <text x={(s.x! + t.x!) / 2} y={(s.y! + t.y!) / 2} fill="#64748b" fontSize="10" textAnchor="middle">{edge.label}</text>
                    </g>
                );
            })}

            {/* Nodes */}
            {data.nodes.map((node, i) => (
                <g key={i}>
                    <circle
                        cx={node.x}
                        cy={node.y}
                        r={node.type === 'verifier' ? 12 : 8}
                        fill={node.type === 'verifier' ? '#10b981' : '#3b82f6'}
                        stroke="#1e293b"
                        strokeWidth="2"
                    />
                    <text x={node.x} y={node.y! + 25} fill="#e2e8f0" fontSize="12" textAnchor="middle">{node.label}</text>
                </g>
            ))}
        </svg>
    );
}

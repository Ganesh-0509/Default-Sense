import { useEffect, useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MiniMap } from "reactflow";
import "reactflow/dist/style.css";
import { Share2, Loader2, AlertTriangle } from "lucide-react";
import RiskBadge from "../components/RiskBadge";
import { getCustomers } from "../services/dataService";
import { getCustomerGraph, getCustomerRisk, getGraphStatus } from "../services/graphService";
import { errorMessage } from "../services/api";

// Node fill by Neo4j label. Connected defaulters override to red.
const LABEL_COLORS = {
  Customer: "#2563eb",
  Employer: "#7c3aed",
  Industry: "#d97706",
  Region: "#0d9488",
  EconomicEvent: "#ea580c",
};
const DEFAULTER_COLOR = "#dc2626";

const prettyRel = (t) =>
  (t || "").toLowerCase().replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

function buildFlow(graph, defaulterNames, selectedId) {
  const nodes = graph.nodes || [];
  const centerId =
    nodes.find((n) => n.label === "Customer" && n.properties?.customer_id === selectedId)?.id ||
    nodes.find((n) => n.label === "Customer")?.id;

  const others = nodes.filter((n) => n.id !== centerId);
  const R = 270;

  const flowNodes = nodes.map((n) => {
    const isCenter = n.id === centerId;
    let position = { x: 0, y: 0 };
    if (!isCenter) {
      const idx = others.findIndex((o) => o.id === n.id);
      const angle = (2 * Math.PI * idx) / Math.max(others.length, 1);
      position = { x: Math.round(R * Math.cos(angle)), y: Math.round(R * Math.sin(angle)) };
    }
    const isDefaulter =
      n.label === "Customer" && !isCenter && defaulterNames.includes(n.name);
    const bg = isDefaulter ? DEFAULTER_COLOR : LABEL_COLORS[n.label] || "#475569";

    return {
      id: n.id,
      position,
      data: {
        label: (
          <div className="leading-tight">
            <div className="text-[9px] uppercase tracking-wide opacity-80">
              {isDefaulter ? "Defaulter" : n.label}
            </div>
            <div className="text-xs font-semibold">{n.name}</div>
          </div>
        ),
      },
      style: {
        background: bg,
        color: "#fff",
        border: isCenter ? "3px solid #bfdbfe" : "2px solid rgba(255,255,255,0.35)",
        borderRadius: 12,
        padding: "8px 10px",
        width: 150,
        textAlign: "center",
        boxShadow: isCenter ? "0 0 0 4px rgba(37,99,235,0.15)" : "none",
      },
    };
  });

  const flowEdges = (graph.edges || []).map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    label: prettyRel(e.type),
    animated: e.source === centerId || e.target === centerId,
    style: { stroke: "#94a3b8", strokeWidth: 1.5 },
    labelStyle: { fontSize: 10, fill: "#475569" },
    labelBgStyle: { fill: "#f8fafc", fillOpacity: 0.85 },
  }));

  return { flowNodes, flowEdges };
}

export default function KnowledgeGraph() {
  const [customers, setCustomers] = useState([]);
  const [selected, setSelected] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [graph, setGraph] = useState(null);
  const [risk, setRisk] = useState(null);
  const [engineDown, setEngineDown] = useState(false);

  useEffect(() => {
    getGraphStatus()
      .then((s) => setEngineDown(!s?.available))
      .catch(() => setEngineDown(true));
    getCustomers({ limit: 100 })
      .then((d) => {
        setCustomers(d.items || []);
        if (d.items?.length) setSelected(d.items[0].customer_id);
      })
      .catch((err) => setError(errorMessage(err, "Could not load customers.")));
  }, []);

  const loadGraph = async (customerId) => {
    if (!customerId) return;
    setError("");
    setLoading(true);
    setGraph(null);
    setRisk(null);
    try {
      const [g, r] = await Promise.all([
        getCustomerGraph(customerId),
        getCustomerRisk(customerId).catch(() => null),
      ]);
      setGraph(g);
      setRisk(r);
    } catch (err) {
      setError(errorMessage(err, "Could not load the relationship graph."));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selected) loadGraph(selected);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selected]);

  const { flowNodes, flowEdges } = useMemo(() => {
    if (!graph) return { flowNodes: [], flowEdges: [] };
    const defaulters = risk?.connected_defaulters || [];
    return buildFlow(graph, defaulters, selected);
  }, [graph, risk, selected]);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Knowledge Graph</h1>
      <p className="mt-1 text-sm text-slate-500">
        Relationship intelligence & risk propagation across employers, industries, regions and
        connected borrowers (Neo4j).
      </p>

      {engineDown && (
        <div className="mt-4 flex items-center gap-2 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          <AlertTriangle className="h-4 w-4" />
          The graph engine (Neo4j) is currently unreachable.
        </div>
      )}

      <div className="mt-6 flex flex-wrap items-end gap-3 rounded-xl border border-slate-200 bg-white p-5">
        <div className="flex-1 min-w-[220px]">
          <label className="mb-1 block text-sm font-medium text-slate-700">Customer</label>
          <select
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          >
            {customers.map((c) => (
              <option key={c.customer_id} value={c.customer_id}>
                {c.customer_name} ({c.employment_type || "—"})
              </option>
            ))}
          </select>
        </div>
        {loading && (
          <div className="flex items-center gap-2 pb-2 text-sm text-slate-500">
            <Loader2 className="h-4 w-4 animate-spin" /> Loading graph…
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* Graph canvas */}
        <div className="rounded-xl border border-slate-200 bg-white lg:col-span-2">
          <div className="flex items-center justify-between border-b border-slate-100 px-5 py-3">
            <h2 className="flex items-center gap-2 text-sm font-semibold text-slate-700">
              <Share2 className="h-4 w-4 text-brand-600" /> Relationship Network
            </h2>
            {graph && (
              <span className="text-xs text-slate-400">
                {graph.node_count} nodes · {graph.edge_count} links
              </span>
            )}
          </div>
          <div style={{ height: 520 }}>
            {flowNodes.length > 0 ? (
              <ReactFlow
                nodes={flowNodes}
                edges={flowEdges}
                fitView
                fitViewOptions={{ padding: 0.2 }}
                proOptions={{ hideAttribution: true }}
                nodesDraggable
                minZoom={0.2}
              >
                <Background color="#e2e8f0" gap={20} />
                <Controls showInteractive={false} />
                <MiniMap pannable zoomable nodeColor={(n) => n.style?.background || "#94a3b8"} />
              </ReactFlow>
            ) : (
              <div className="flex h-full items-center justify-center text-sm text-slate-400">
                {loading ? "Loading…" : "No relationship data for this customer."}
              </div>
            )}
          </div>
          {/* Legend */}
          <div className="flex flex-wrap gap-3 border-t border-slate-100 px-5 py-3 text-xs text-slate-500">
            {Object.entries(LABEL_COLORS).map(([label, color]) => (
              <span key={label} className="flex items-center gap-1.5">
                <span className="h-3 w-3 rounded-full" style={{ background: color }} /> {label}
              </span>
            ))}
            <span className="flex items-center gap-1.5">
              <span className="h-3 w-3 rounded-full" style={{ background: DEFAULTER_COLOR }} />{" "}
              Connected defaulter
            </span>
          </div>
        </div>

        {/* Risk panel */}
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="text-sm font-semibold text-slate-700">Relationship Risk</h2>
          {!risk ? (
            <p className="mt-8 text-center text-xs text-slate-400">
              Select a customer to see relationship-based risk.
            </p>
          ) : (
            <>
              <div className="mt-3 text-center">
                <div className="text-4xl font-bold text-slate-800">
                  {risk.relationship_risk_score}
                  <span className="text-lg text-slate-400">/100</span>
                </div>
                <div className="mt-2">
                  <RiskBadge level={risk.relationship_risk_level} />
                </div>
              </div>

              <dl className="mt-5 space-y-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-slate-500">Employer</dt>
                  <dd className="font-medium text-slate-700">{risk.employer || "—"}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Industry</dt>
                  <dd className="font-medium text-slate-700">
                    {risk.industry || "—"}
                    {risk.industry_risk ? ` (${risk.industry_risk})` : ""}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-slate-500">Region</dt>
                  <dd className="font-medium text-slate-700">{risk.region || "—"}</dd>
                </div>
              </dl>

              {risk.connected_defaulters?.length > 0 && (
                <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2">
                  <div className="text-xs font-semibold text-red-700">
                    {risk.connected_defaulters.length} connected defaulter
                    {risk.connected_defaulters.length > 1 ? "s" : ""}
                  </div>
                  <div className="mt-1 text-xs text-red-600">
                    {risk.connected_defaulters.join(", ")}
                  </div>
                </div>
              )}

              {risk.factors?.length > 0 && (
                <div className="mt-4">
                  <div className="text-xs font-semibold text-slate-600">Contributing factors</div>
                  <ul className="mt-2 space-y-1.5">
                    {risk.factors.map((f, i) => (
                      <li key={i} className="text-xs text-slate-500">
                        <span className="font-medium text-slate-700">{f.factor}:</span> {f.detail}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AskMode } from "./pages/AskMode";
import { ChartsDemo } from "./pages/ChartsDemo";
import { ComingSoon } from "./pages/ComingSoon";
import { Landing } from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/memory/ask" element={<AskMode />} />
        <Route
          path="/memory/watch"
          element={
            <ComingSoon
              title="Watch mode"
              crumbs={[{ label: "Lab memory" }, { label: "Watch" }]}
              blurb="A proactive sidebar that surfaces relevant past experiments while you write — your last runs with this catalyst, this solvent, this substrate."
            />
          }
        />
        <Route
          path="/memory/compare"
          element={
            <ComingSoon
              title="Compare mode"
              crumbs={[{ label: "Lab memory" }, { label: "Compare" }]}
              blurb="Side-by-side structured diff of 2–5 experiments. What changed in reagents, conditions, observations, results — line by line."
            />
          }
        />
        <Route path="/charts-demo" element={<ChartsDemo />} />
        <Route path="/ask" element={<AskMode />} />
        <Route
          path="/experiment/new"
          element={
            <ComingSoon
              title="Experiment editor"
              crumbs={[{ label: "Notebook" }, { label: "New experiment" }]}
              blurb="The block-based editor — reagent table, checkpoints, observation, data ingest, calculation, witness signature. Slash-command block insertion, drag handles, inline AI suggestions. Coming in v0.2."
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

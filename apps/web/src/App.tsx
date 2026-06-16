import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AskMode } from "./pages/AskMode";
import { ChartsDemo } from "./pages/ChartsDemo";
import { Landing } from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/ask" element={<AskMode />} />
        <Route path="/charts-demo" element={<ChartsDemo />} />
      </Routes>
    </BrowserRouter>
  );
}

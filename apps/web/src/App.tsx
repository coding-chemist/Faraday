import { BrowserRouter, Route, Routes } from "react-router-dom";

import { ChartsDemo } from "./pages/ChartsDemo";
import { Landing } from "./pages/Landing";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/charts-demo" element={<ChartsDemo />} />
      </Routes>
    </BrowserRouter>
  );
}

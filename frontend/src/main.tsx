import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";

const root = document.getElementById("root");
if (!root) {
  throw new Error('index.html must have an element with id="root"');
}

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

import { useEffect, useState } from "react";

type ApiStatus = "checking" | "ok" | "error";

export default function App() {
  const [status, setStatus] = useState<ApiStatus>("checking");

  useEffect(() => {
    async function checkApi() {
      try {
        const response = await fetch("/api/health");
        setStatus(response.ok ? "ok" : "error");
      } catch {
        setStatus("error");
      }
    }
    checkApi();
  }, []);

  return (
    <main>
      <h1>Career Copilot</h1>
      {status === "checking" && <p>Checking the API...</p>}
      {status === "ok" && <p>API: ok</p>}
      {status === "error" && <p>API: unreachable. Is just dev running?</p>}
    </main>
  );
}

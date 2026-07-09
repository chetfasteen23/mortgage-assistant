import { useEffect, useState } from "react";
import { api } from "../src/api/client";

type LenderFileStatusResponse = {
  has_file: boolean;
  filename?: string;
  uploaded_at?: string;
};

type LenderFileStatusProps = {
  refreshKey: number;
};

export function LenderFileStatus({ refreshKey }: LenderFileStatusProps) {
  const [status, setStatus] = useState<LenderFileStatusResponse | null>(null);

  async function loadStatus() {
    const response = await api.get("/lender-files/current");
    setStatus(response.data);
  }

  useEffect(() => {
    loadStatus();
  }, [refreshKey]);

  if (!status) {
    return <p>Checking lender file...</p>;
  }

  if (!status.has_file) {
    return <p>No lender sheet uploaded yet.</p>;
  }

  return (
    <div>
      <h2>Current lender sheet</h2>
      <p>
        <strong>{status.filename}</strong>
      </p>
      <p>Uploaded: {new Date(status.uploaded_at ?? "").toLocaleString()}</p>
    </div>
  );
}
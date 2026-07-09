import { useState } from "react";
import { api } from "../src/api/client";

type UploadLenderSheetProps = {
    onUploadSuccess: () => void;
  };

export function UploadLenderSheetProps({ onUploadSuccess }: UploadLenderSheetProps) {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  async function handleUpload(event: React.FormEvent) {
    event.preventDefault();

    if (!file) {
      setMessage("Please choose an Excel file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/uploads/lender-sheet", formData);
      setMessage(`Uploaded successfully. Created ${response.data.total_chunks_created} chunks.`);
      onUploadSuccess();
    } catch {
      setMessage("Upload failed. Make sure you are logged in.");
    }
  }

  return (
    <form onSubmit={handleUpload}>
      <h2>Upload Lender Sheet</h2>

      <input
        type="file"
        accept=".xlsx,.xls"
        onChange={(event) => setFile(event.target.files?.[0] ?? null)}
      />

      <button type="submit">Upload</button>

      <p>{message}</p>
    </form>
  );
}
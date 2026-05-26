import Webcam from "react-webcam";
import { useRef, useState } from "react";
import API from "../api";

export default function CameraCapture() {
  const webcamRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const scanFace = async () => {
    try {
      setLoading(true);
      setResult(null);

      const imageSrc = webcamRef.current.getScreenshot();
      const blob = await fetch(imageSrc).then(r => r.blob());

      const formData = new FormData();
      formData.append("file", blob, "face.jpg");

      // ✅ NEW SINGLE ENDPOINT (production logic)
      const res = await API.post("/face/scan", formData);

      setResult(res.data);
      alert(JSON.stringify(res.data));

    } catch (err) {
      console.log("SCAN ERROR:", err);
      alert("Face scan failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center" }}>

      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        style={{ width: 300, borderRadius: 10 }}
      />

      <br /><br />

      <button
        onClick={scanFace}
        disabled={loading}
        style={{
          padding: "10px 20px",
          background: loading ? "gray" : "green",
          color: "white",
          border: "none",
          borderRadius: 5,
          cursor: "pointer"
        }}
      >
        {loading ? "Scanning..." : "SCAN FACE (AUTO IN/OUT)"}
      </button>

      {result && (
        <div style={{ marginTop: 15 }}>
          <p><b>Result:</b></p>
          <p> {result.name}</p>
          <p> {result.status}</p>
        </div>
      )}

    </div>
  );
}
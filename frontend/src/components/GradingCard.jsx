export default function GradingCard({ grade, confidence }) {
  const colors = { A: "green", B: "blue", C: "orange", BS: "red" };

  return (
    <div style={{
      border: `2px solid ${colors[grade]}`,
      borderRadius: "10px",
      padding: "1rem",
      textAlign: "center",
      color: colors[grade]
    }}>
      <h2>Grade: {grade}</h2>
      <p>Confidence: {confidence}</p>
    </div>
  );
}

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "not configured";

export default function Page() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        background: "linear-gradient(135deg, #f3efe6, #e7f1ff)",
        fontFamily: "ui-serif, Georgia, Cambria, Times New Roman, Times, serif",
        color: "#172033",
        padding: "1.5rem",
      }}
    >
      <section
        style={{
          width: "min(720px, 100%)",
          background: "rgba(255, 255, 255, 0.88)",
          border: "1px solid #d9e3f0",
          borderRadius: "16px",
          padding: "1.25rem",
          boxShadow: "0 8px 24px rgba(23, 32, 51, 0.08)",
        }}
      >
        <h1 style={{ margin: 0, fontSize: "2rem", lineHeight: 1.2 }}>
          Yaocihuatl Dashboard
        </h1>
        <p style={{ marginTop: "0.75rem", marginBottom: 0 }}>
          Despliegue minimo de infraestructura para validacion de servicios.
        </p>
        <p style={{ marginTop: "0.75rem", marginBottom: 0 }}>
          Estado: <strong>running</strong>
        </p>
        <p
          style={{
            marginTop: "0.75rem",
            marginBottom: 0,
            overflowWrap: "anywhere",
          }}
        >
          Backend URL: <code>{apiUrl}</code>
        </p>
      </section>
    </main>
  );
}

import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Yaocihuatl Dashboard",
  description: "Base de despliegue para fase de infraestructura minima",
};

interface RootLayoutProps {
  children: ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="es-MX">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}

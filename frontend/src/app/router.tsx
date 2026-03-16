import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { AppShell } from "@/components/layout/app-shell";
import { HomePage } from "@/pages/home-page";
import { OverwatchPage } from "@/pages/overwatch-page";
import { ValorantPage } from "@/pages/valorant-page";
import { CS2Page } from "@/pages/cs2-page";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "overwatch", element: <OverwatchPage /> },
      { path: "valorant", element: <ValorantPage /> },
      { path: "cs2", element: <CS2Page /> },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}

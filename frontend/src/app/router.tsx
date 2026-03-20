import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { AppShell } from "@/components/layout/app-shell";
import { FortnitePage } from "@/pages/fortnite-page";
import { HomePage } from "@/pages/home-page";
import { LolPage } from "@/pages/lol-page";
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
      { path: "lol", element: <LolPage /> },
      { path: "fortnite", element: <FortnitePage /> },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}

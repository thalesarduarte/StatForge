import { NavLink, Outlet } from "react-router-dom";

import { gameModules } from "@/features/core/services/platform-service";

const links = [{ path: "/", name: "Dashboard" }, ...gameModules.map((module) => ({ path: module.path, name: module.name }))];

export function AppShell() {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
      <header className="mb-8 rounded-[30px] border border-white/70 bg-slate-950 px-6 py-5 text-white shadow-panel">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="font-display text-3xl font-bold tracking-tight">StatForge</p>
            <p className="mt-2 max-w-2xl text-sm text-slate-300">
              Plataforma modular para perfis, rankings, comparativos e ecossistemas competitivos multi-game.
            </p>
          </div>
          <nav className="flex flex-wrap gap-2">
            {links.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  [
                    "rounded-full px-4 py-2 text-sm font-medium transition",
                    isActive ? "bg-white text-slate-950" : "bg-white/10 text-white hover:bg-white/20",
                  ].join(" ")
                }
              >
                {link.name}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}

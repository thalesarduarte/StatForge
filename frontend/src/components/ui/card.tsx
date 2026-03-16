import { ReactNode } from "react";

import { cn } from "@/utils/cn";

type CardProps = {
  children: ReactNode;
  className?: string;
};

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn("rounded-[28px] border border-border bg-white/80 p-6 shadow-panel backdrop-blur", className)}>
      {children}
    </div>
  );
}

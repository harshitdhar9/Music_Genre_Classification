// components/input.tsx
import * as React from "react";
import { cn } from "../lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  icon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", icon, ...props }, ref) => {
    return (
      <div className="relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400">
            {icon}
          </div>
        )}
        <input
          className={cn(
            "flex h-10 w-full rounded-md border border-gray-700 bg-gray-800/70 px-3 py-2 text-sm text-white placeholder-gray-400 shadow-sm transition-colors",
            "focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500",
            "hover:border-gray-600",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            icon ? "pl-10" : "pl-3",
            className
          )}
          ref={ref}
          {...props}
        />
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
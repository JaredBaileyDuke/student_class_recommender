// Label component extends from shadcnui - https://ui.shadcn.com/docs/components/label
import React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";

// Local
import { cn } from "../util/cn";

const Label = React.forwardRef(({ className, ...props }, ref) => (
  <LabelPrimitive.Root
    ref={ref}
    className={cn(
      "flex justify-start items-center text-sm font-medium text-black dark:text-white leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
      className
    )}
    {...props}
  />
));
Label.displayName = LabelPrimitive.Root.displayName;

const LabelInputContainer = ({ children, className }) => {
  return (
    <div className={cn("flex flex-col space-y-2 w-full", className)}>
      {children}
    </div>
  );
};

export { Label, LabelInputContainer };

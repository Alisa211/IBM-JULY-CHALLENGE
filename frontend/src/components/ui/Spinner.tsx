import type { HTMLAttributes } from 'react';
import { cn } from '../../utils/cn';

export type SpinnerSize = 'sm' | 'md' | 'lg';

export interface SpinnerProps extends HTMLAttributes<HTMLDivElement> {
  size?: SpinnerSize;
}

const sizeStyles: Record<SpinnerSize, string> = {
  sm: 'w-4 h-4 border-2',
  md: 'w-6 h-6 border-2',
  lg: 'w-8 h-8 border-[3px]',
};

export function Spinner({ size = 'md', className, ...props }: SpinnerProps) {
  return (
    <div
      role="status"
      aria-label="Loading"
      className={cn(
        'rounded-full animate-spin',
        'border-primary-600 border-t-transparent',
        sizeStyles[size],
        className
      )}
      {...props}
    >
      <span className="sr-only">Loading…</span>
    </div>
  );
}

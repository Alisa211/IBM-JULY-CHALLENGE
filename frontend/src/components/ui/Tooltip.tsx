import { useState, type ReactNode } from 'react';
import { cn } from '../../utils/cn';

export type TooltipPosition = 'top' | 'bottom' | 'left' | 'right';

export interface TooltipProps {
  content: ReactNode;
  children: ReactNode;
  position?: TooltipPosition;
  className?: string;
}

const positionStyles: Record<TooltipPosition, string> = {
  top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
  bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
  left: 'right-full top-1/2 -translate-y-1/2 mr-2',
  right: 'left-full top-1/2 -translate-y-1/2 ml-2',
};

const arrowStyles: Record<TooltipPosition, string> = {
  top: 'top-full left-1/2 -translate-x-1/2 border-t-surface-900 dark:border-t-surface-700 border-x-transparent border-b-transparent',
  bottom: 'bottom-full left-1/2 -translate-x-1/2 border-b-surface-900 dark:border-b-surface-700 border-x-transparent border-t-transparent',
  left: 'left-full top-1/2 -translate-y-1/2 border-l-surface-900 dark:border-l-surface-700 border-y-transparent border-r-transparent',
  right: 'right-full top-1/2 -translate-y-1/2 border-r-surface-900 dark:border-r-surface-700 border-y-transparent border-l-transparent',
};

export function Tooltip({
  content,
  children,
  position = 'top',
  className,
}: TooltipProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div
      className="relative inline-flex"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
      onFocus={() => setVisible(true)}
      onBlur={() => setVisible(false)}
    >
      {children}
      {visible && (
        <div
          role="tooltip"
          className={cn(
            'absolute z-50 pointer-events-none',
            'px-2.5 py-1.5 text-xs font-medium rounded-lg whitespace-nowrap',
            'bg-surface-900 dark:bg-surface-700 text-white',
            'shadow-lg animate-fade-in',
            positionStyles[position],
            className
          )}
        >
          {content}
          {/* Arrow */}
          <span
            className={cn(
              'absolute w-0 h-0 border-4',
              arrowStyles[position]
            )}
          />
        </div>
      )}
    </div>
  );
}

import type { HTMLAttributes, ReactNode } from 'react';
import { cn } from '../../utils/cn';

export type CardPadding = 'none' | 'sm' | 'md' | 'lg';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  hover?: boolean;
  padding?: CardPadding;
}

const paddingStyles: Record<CardPadding, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-5',
  lg: 'p-7',
};

export function Card({
  children,
  hover = false,
  padding = 'md',
  className,
  ...props
}: CardProps) {
  return (
    <div
      className={cn(
        'bg-white dark:bg-surface-800',
        'rounded-xl border border-surface-200 dark:border-surface-700',
        'shadow-sm',
        hover &&
          'transition-all duration-300 ease-out hover:shadow-lg hover:-translate-y-0.5 cursor-pointer',
        paddingStyles[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

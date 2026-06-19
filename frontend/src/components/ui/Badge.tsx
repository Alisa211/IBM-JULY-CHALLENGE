import type { HTMLAttributes, ReactNode } from 'react';
import { cn } from '../../utils/cn';

export type BadgeVariant = 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger';
export type BadgeSize = 'sm' | 'md';

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  size?: BadgeSize;
  children: ReactNode;
  dot?: boolean;
}

const variantStyles: Record<BadgeVariant, string> = {
  default:
    'bg-surface-100 text-surface-700 dark:bg-surface-700 dark:text-surface-300',
  primary:
    'bg-primary-100 text-primary-700 dark:bg-primary-900/50 dark:text-primary-300',
  secondary:
    'bg-secondary-100 text-secondary-700 dark:bg-secondary-900/50 dark:text-secondary-300',
  success:
    'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300',
  warning:
    'bg-amber-100 text-amber-700 dark:bg-amber-900/50 dark:text-amber-300',
  danger:
    'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300',
};

const dotColors: Record<BadgeVariant, string> = {
  default: 'bg-surface-500',
  primary: 'bg-primary-500',
  secondary: 'bg-secondary-500',
  success: 'bg-green-500',
  warning: 'bg-amber-500',
  danger: 'bg-red-500',
};

const sizeStyles: Record<BadgeSize, string> = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-xs px-2.5 py-1',
};

export function Badge({
  variant = 'default',
  size = 'sm',
  dot = false,
  children,
  className,
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 font-medium rounded-full whitespace-nowrap',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {dot && (
        <span
          className={cn('w-1.5 h-1.5 rounded-full shrink-0', dotColors[variant])}
        />
      )}
      {children}
    </span>
  );
}

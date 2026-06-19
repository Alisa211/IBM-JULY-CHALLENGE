import { AlertTriangle, RefreshCw } from 'lucide-react';
import { cn } from '../../utils/cn';
import { Button } from './Button';

export interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({
  title = 'Something went wrong',
  message = 'An unexpected error occurred. Please try again.',
  onRetry,
  className,
}: ErrorStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center py-16 px-6 text-center',
        className
      )}
    >
      <div className="w-16 h-16 rounded-2xl bg-red-100 dark:bg-red-950/40 flex items-center justify-center mb-5">
        <AlertTriangle size={28} className="text-red-500" />
      </div>
      <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-100 mb-1.5">
        {title}
      </h3>
      <p className="text-sm text-surface-500 dark:text-surface-400 max-w-sm mb-6">
        {message}
      </p>
      {onRetry && (
        <Button
          variant="outline"
          size="md"
          onClick={onRetry}
          leftIcon={<RefreshCw size={16} />}
        >
          Try Again
        </Button>
      )}
    </div>
  );
}

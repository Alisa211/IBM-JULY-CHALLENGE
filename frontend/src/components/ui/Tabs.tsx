import {
  createContext,
  useContext,
  type ReactNode,
  type HTMLAttributes,
  type ButtonHTMLAttributes,
} from 'react';
import { cn } from '../../utils/cn';

/* ---------- Context ---------- */
interface TabsContextValue {
  value: string;
  onChange: (value: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs compound components must be used inside <Tabs>');
  return ctx;
}

/* ---------- Tabs (root) ---------- */
export interface TabsProps {
  value: string;
  onChange: (value: string) => void;
  children: ReactNode;
  className?: string;
}

export function Tabs({ value, onChange, children, className }: TabsProps) {
  return (
    <TabsContext.Provider value={{ value, onChange }}>
      <div className={cn('w-full', className)}>{children}</div>
    </TabsContext.Provider>
  );
}

/* ---------- TabList ---------- */
export interface TabListProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function TabList({ children, className, ...props }: TabListProps) {
  return (
    <div
      role="tablist"
      className={cn(
        'flex border-b border-surface-200 dark:border-surface-700 gap-1',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

/* ---------- Tab ---------- */
export interface TabProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  value: string;
  children: ReactNode;
}

export function Tab({ value, children, className, ...props }: TabProps) {
  const { value: selected, onChange } = useTabsContext();
  const isActive = selected === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => onChange(value)}
      className={cn(
        'relative px-4 py-2.5 text-sm font-medium transition-colors duration-200 cursor-pointer',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-t-lg',
        isActive
          ? 'text-primary-600 dark:text-primary-400'
          : 'text-surface-500 dark:text-surface-400 hover:text-surface-700 dark:hover:text-surface-300',
        className
      )}
      {...props}
    >
      {children}
      {/* Active underline */}
      <span
        className={cn(
          'absolute bottom-0 left-0 right-0 h-0.5 rounded-full transition-all duration-200',
          isActive
            ? 'bg-primary-600 dark:bg-primary-400 scale-x-100'
            : 'bg-transparent scale-x-0'
        )}
      />
    </button>
  );
}

/* ---------- TabPanel ---------- */
export interface TabPanelProps extends HTMLAttributes<HTMLDivElement> {
  value: string;
  children: ReactNode;
}

export function TabPanel({ value, children, className, ...props }: TabPanelProps) {
  const { value: selected } = useTabsContext();
  if (selected !== value) return null;

  return (
    <div
      role="tabpanel"
      className={cn('py-4 animate-fade-in', className)}
      {...props}
    >
      {children}
    </div>
  );
}

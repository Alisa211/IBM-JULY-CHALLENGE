import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Dna, 
  ScanSearch, 
  Lightbulb, 
  MessageSquareText, 
  Settings,
  X,
  Sun,
  Moon
} from 'lucide-react';
import { useUiStore } from '../../store/uiStore';
import { cn } from '../../utils/cn';
import { useEffect } from 'react';

const NAV_ITEMS = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Style DNA', path: '/style-dna', icon: Dna },
  { label: 'Sculpture Analyzer', path: '/sculpture', icon: ScanSearch },
  { label: 'Idea Generator', path: '/ideas', icon: Lightbulb },
  { label: 'Critique Mode', path: '/critique', icon: MessageSquareText },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export function MobileDrawer() {
  const { mobileDrawerOpen, toggleMobileDrawer, theme, toggleTheme } = useUiStore();

  useEffect(() => {
    if (mobileDrawerOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [mobileDrawerOpen]);

  if (!mobileDrawerOpen) return null;

  return (
    <>
      <div 
        className="fixed inset-0 bg-surface-900/50 backdrop-blur-sm z-40 md:hidden animate-fade-in"
        onClick={toggleMobileDrawer}
      />
      
      <div className={cn(
        "fixed inset-y-0 left-0 w-72 bg-white dark:bg-surface-900 z-50 md:hidden flex flex-col shadow-2xl",
        "animate-slide-in"
      )}>
        <div className="flex h-16 items-center justify-between px-4 border-b border-surface-200 dark:border-surface-700">
          <div className="flex items-center gap-3">
            <div className="flex shrink-0 items-center justify-center w-8 h-8 rounded-lg bg-gradient-primary text-white">
              <ScanSearch className="w-5 h-5" />
            </div>
            <span className="text-lg font-bold gradient-text">
              AI Creative
            </span>
          </div>
          <button 
            onClick={toggleMobileDrawer}
            className="p-2 text-surface-500 hover:bg-surface-100 dark:hover:bg-surface-800 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4 px-3 flex flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={toggleMobileDrawer}
              className={({ isActive }) => cn(
                "flex items-center gap-3 rounded-lg px-3 py-3 transition-colors",
                isActive 
                  ? "bg-primary-50 text-primary-600 dark:bg-primary-500/10 dark:text-primary-400 font-medium" 
                  : "text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800"
              )}
            >
              <item.icon className="w-5 h-5 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-surface-200 dark:border-surface-700">
          <button
            onClick={toggleTheme}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-3 text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800 transition-colors"
          >
            {theme === 'light' ? <Moon className="w-5 h-5 shrink-0" /> : <Sun className="w-5 h-5 shrink-0" />}
            <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
          </button>
        </div>
      </div>
    </>
  );
}

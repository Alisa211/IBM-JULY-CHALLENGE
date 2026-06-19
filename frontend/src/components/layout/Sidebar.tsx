import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Dna, 
  ScanSearch, 
  Lightbulb, 
  MessageSquareText, 
  Settings,
  Sun,
  Moon,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react';
import { useUiStore } from '../../store/uiStore';
import { cn } from '../../utils/cn';

const NAV_ITEMS = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Style DNA', path: '/style-dna', icon: Dna },
  { label: 'Sculpture Analyzer', path: '/sculpture', icon: ScanSearch },
  { label: 'Idea Generator', path: '/ideas', icon: Lightbulb },
  { label: 'Critique Mode', path: '/critique', icon: MessageSquareText },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, theme, toggleTheme } = useUiStore();

  return (
    <aside
      className={cn(
        "hidden md:flex flex-col fixed inset-y-0 left-0 z-50",
        "bg-white/80 dark:bg-surface-900/80 backdrop-blur-xl border-r border-surface-200 dark:border-surface-700",
        "transition-all duration-300",
        sidebarCollapsed ? "w-[72px]" : "w-64"
      )}
    >
      <div className="flex h-16 shrink-0 items-center px-4 border-b border-surface-200 dark:border-surface-700">
        <div className={cn("flex items-center gap-3 overflow-hidden", sidebarCollapsed ? "justify-center w-full" : "")}>
          <div className="flex shrink-0 items-center justify-center w-10 h-10 rounded-xl bg-gradient-primary text-white shadow-lg shadow-primary-500/20">
            <ScanSearch className="w-6 h-6" />
          </div>
          {!sidebarCollapsed && (
            <span className="text-lg font-bold gradient-text whitespace-nowrap">
              AI Creative
            </span>
          )}
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto py-4 px-3 flex flex-col gap-1">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => cn(
              "flex items-center gap-3 rounded-lg px-3 py-2.5 transition-colors group relative",
              isActive 
                ? "bg-primary-50 text-primary-600 dark:bg-primary-500/10 dark:text-primary-400 font-medium" 
                : "text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800"
            )}
            title={sidebarCollapsed ? item.label : undefined}
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-5 bg-accent-500 rounded-r-full" />
                )}
                <item.icon className={cn("w-5 h-5 shrink-0", isActive ? "text-primary-600 dark:text-primary-400" : "text-surface-400 group-hover:text-surface-600 dark:group-hover:text-surface-300")} />
                {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-surface-200 dark:border-surface-700 flex flex-col gap-2">
        <button
          onClick={toggleTheme}
          className={cn(
            "flex items-center gap-3 rounded-lg px-3 py-2 text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800 transition-colors",
            sidebarCollapsed && "justify-center"
          )}
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ? <Moon className="w-5 h-5 shrink-0" /> : <Sun className="w-5 h-5 shrink-0" />}
          {!sidebarCollapsed && <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>}
        </button>
        <button
          onClick={toggleSidebar}
          className={cn(
            "flex items-center gap-3 rounded-lg px-3 py-2 text-surface-600 hover:text-surface-900 hover:bg-surface-100 dark:text-surface-400 dark:hover:text-surface-100 dark:hover:bg-surface-800 transition-colors",
            sidebarCollapsed && "justify-center"
          )}
          title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {sidebarCollapsed ? <PanelLeftOpen className="w-5 h-5 shrink-0" /> : <PanelLeftClose className="w-5 h-5 shrink-0" />}
          {!sidebarCollapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  );
}

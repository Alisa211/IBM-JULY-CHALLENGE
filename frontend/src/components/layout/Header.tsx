import { useState, useRef, useEffect } from 'react';
import { Menu, Search, Bell, ChevronDown, Settings as SettingsIcon, LogOut } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useUiStore } from '../../store/uiStore';
import { useProjectStore } from '../../store/projectStore';
import { useUserStore } from '../../store/userStore';

export function Header() {
  const { toggleMobileDrawer } = useUiStore();
  const { currentProject } = useProjectStore();
  const { user } = useUserStore();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between px-4 sm:px-6 bg-white/80 dark:bg-surface-900/80 backdrop-blur-xl border-b border-surface-200 dark:border-surface-700">
      <div className="flex items-center gap-4">
        <button
          onClick={toggleMobileDrawer}
          className="md:hidden p-2 -ml-2 text-surface-500 hover:bg-surface-100 dark:hover:bg-surface-800 rounded-lg transition-colors"
          aria-label="Open menu"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="flex flex-col">
          <span className="text-xs font-medium text-surface-500 dark:text-surface-400 uppercase tracking-wider">
            Current Project
          </span>
          <span className="text-sm sm:text-base font-semibold text-surface-900 dark:text-white truncate max-w-[200px] sm:max-w-xs">
            {currentProject?.name || 'No Project Selected'}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-4">
        <div className="hidden sm:flex relative group">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-surface-400">
            <Search className="w-4 h-4" />
          </div>
          <input
            type="text"
            className="bg-surface-100 dark:bg-surface-800 border-transparent focus:border-primary-500 focus:bg-white dark:focus:bg-surface-900 focus:ring-1 focus:ring-primary-500 text-sm rounded-full block w-full pl-10 px-4 py-2 transition-all placeholder-surface-400 text-surface-900 dark:text-white"
            placeholder="Search resources..."
          />
        </div>

        <button className="relative p-2 text-surface-500 hover:bg-surface-100 dark:hover:bg-surface-800 rounded-full transition-colors">
            <Bell className="w-5 h-5 text-surface-600 dark:text-surface-300" />
            {/* <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full border-2 border-white dark:border-surface-900" /> */}
        </button>

        <div className="relative" ref={dropdownRef}>
          <button 
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center gap-2 hover:bg-surface-100 dark:hover:bg-surface-800 p-1 pr-2 rounded-full transition-colors"
          >
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center text-white font-medium text-sm">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <ChevronDown className={`w-4 h-4 text-surface-500 hidden sm:block transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-surface-800 rounded-xl shadow-lg border border-surface-200 dark:border-surface-700 py-1 animate-fade-in overflow-hidden">
              <div className="px-4 py-3 border-b border-surface-100 dark:border-surface-700">
                <p className="text-sm font-medium text-surface-900 dark:text-white truncate">{user?.name}</p>
                <p className="text-xs text-surface-500 truncate">{user?.email}</p>
              </div>
              <Link 
                to="/settings" 
                onClick={() => setDropdownOpen(false)}
                className="flex items-center gap-2 px-4 py-2 text-sm text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700 transition-colors"
              >
                <SettingsIcon className="w-4 h-4" />
                Settings
              </Link>
              <button 
                onClick={() => setDropdownOpen(false)}
                className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-left"
              >
                <LogOut className="w-4 h-4" />
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

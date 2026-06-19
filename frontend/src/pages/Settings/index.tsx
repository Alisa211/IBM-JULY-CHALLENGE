import { Sun, Moon } from 'lucide-react';
import { useUiStore } from '../../store/uiStore';
import { useUserStore } from '../../store/userStore';
import { Card } from '../../components/ui/Card';

export default function Settings() {
  const { theme, toggleTheme } = useUiStore();
  const { user, setUser } = useUserStore();

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold text-surface-900 dark:text-white mb-2">
          Settings
        </h1>
        <p className="text-surface-500 dark:text-surface-400">
          Manage your application preferences and profile.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-8">
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-surface-900 dark:text-white mb-4">Appearance</h3>
            <div className="flex items-center justify-between p-4 rounded-lg bg-surface-50 dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center gap-3">
                {theme === 'dark' ? <Moon className="text-primary-400" /> : <Sun className="text-primary-600" />}
                <div>
                  <h4 className="font-medium text-surface-900 dark:text-white">Theme Preference</h4>
                  <p className="text-xs text-surface-500">Current: {theme === 'dark' ? 'Dark' : 'Light'} Mode</p>
                </div>
              </div>
              <button 
                onClick={toggleTheme}
                className="px-4 py-2 bg-surface-200 hover:bg-surface-300 dark:bg-surface-700 dark:hover:bg-surface-600 text-surface-900 dark:text-white rounded-lg transition-colors text-sm font-medium"
              >
                Toggle Theme
              </button>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold text-surface-900 dark:text-white mb-4">Profile</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1">Name</label>
                <input 
                  type="text"
                  value={user?.name || ''}
                  onChange={(e) => user && setUser({ ...user, name: e.target.value })}
                  className="w-full p-3 bg-surface-50 dark:bg-surface-800 rounded-lg border border-surface-200 dark:border-surface-700 text-surface-900 dark:text-white font-medium focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1">Email</label>
                <input 
                  type="email"
                  value={user?.email || ''}
                  onChange={(e) => user && setUser({ ...user, email: e.target.value })}
                  className="w-full p-3 bg-surface-50 dark:bg-surface-800 rounded-lg border border-surface-200 dark:border-surface-700 text-surface-900 dark:text-white font-medium focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                />
              </div>
            </div>
          </Card>
        </div>

        <div>
          <Card className="p-6 bg-gradient-to-b from-primary-50 to-white dark:from-surface-800 dark:to-surface-900 border-primary-200 dark:border-primary-900">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg text-white font-bold text-xl">
                AI
              </div>
              <div>
                <h3 className="text-lg font-bold text-surface-900 dark:text-white">AI Creative Director</h3>
                <p className="text-sm font-medium text-primary-600 dark:text-primary-400">Version 1.0.0-alpha</p>
              </div>
            </div>
            
            <p className="text-sm text-surface-600 dark:text-surface-300 leading-relaxed mb-6">
              A comprehensive toolkit for structural and aesthetic analysis, concept generation, and multi-persona critique.
            </p>
            
            <div className="pt-4 border-t border-primary-200/50 dark:border-primary-900/30">
              <p className="text-xs text-surface-500">
                Built for internal evaluation and creative augmentation.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { MobileDrawer } from './MobileDrawer';
import { useUiStore } from '../../store/uiStore';
import { cn } from '../../utils/cn';

export function AppLayout() {
  const { sidebarCollapsed } = useUiStore();
  
  return (
    <div className="flex h-screen overflow-hidden bg-surface-50 dark:bg-surface-950 font-sans text-surface-900 dark:text-surface-50">
      <Sidebar />
      <MobileDrawer />
      
      <div 
        className={cn(
          "flex flex-col flex-1 overflow-hidden transition-all duration-300 relative",
          sidebarCollapsed ? "md:ml-[72px]" : "md:ml-64"
        )}
      >
        <Header />
        
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 w-full max-w-7xl mx-auto">
          <div className="animate-fade-in w-full">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}

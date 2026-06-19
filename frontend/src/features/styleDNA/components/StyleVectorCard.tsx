import { Card } from '../../../components/ui/Card';

export function StyleVectorCard() {
  return (
    <Card className="p-6 h-full border-t-4 border-t-primary-500 overflow-hidden relative">
      <div className="absolute top-0 right-0 w-64 h-64 bg-primary-500/10 rounded-full blur-3xl -mr-32 -mt-32 pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-accent-500/10 rounded-full blur-3xl -ml-32 -mb-32 pointer-events-none" />
      
      <div className="relative z-10 flex flex-col h-full">
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-surface-900 dark:text-white">Style Embedding Vector</h3>
          <p className="text-sm text-surface-500 dark:text-surface-400">AI-powered style visualization</p>
        </div>

        <div className="flex-1 flex items-center justify-center min-h-[300px]">
          <svg viewBox="0 0 200 200" className="w-full max-w-[280px] h-auto drop-shadow-xl">
            <defs>
              <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="var(--color-primary-500)" stopOpacity="0.8" />
                <stop offset="100%" stopColor="var(--color-accent-500)" stopOpacity="0.4" />
              </linearGradient>
              <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>
            {/* Background grid */}
            <circle cx="100" cy="100" r="80" fill="none" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" strokeDasharray="4 4" />
            <circle cx="100" cy="100" r="50" fill="none" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" strokeDasharray="4 4" />
            <circle cx="100" cy="100" r="20" fill="none" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" strokeDasharray="4 4" />
            
            {/* Axis lines */}
            <line x1="100" y1="20" x2="100" y2="180" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" />
            <line x1="20" y1="100" x2="180" y2="100" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" />
            <line x1="43" y1="43" x2="157" y2="157" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" />
            <line x1="43" y1="157" x2="157" y2="43" stroke="currentColor" className="text-surface-200 dark:text-surface-800" strokeWidth="1" />
            
            {/* Data Polygon */}
            <polygon 
              points="100,30 150,70 140,140 70,160 40,90" 
              fill="url(#polyGrad)" 
              stroke="var(--color-primary-500)" 
              strokeWidth="2"
              filter="url(#glow)"
              className="animate-pulse-slow origin-center"
            />
            
            {/* Data Points */}
            <circle cx="100" cy="30" r="4" fill="var(--color-primary-500)" />
            <circle cx="150" cy="70" r="4" fill="var(--color-primary-500)" />
            <circle cx="140" cy="140" r="4" fill="var(--color-primary-500)" />
            <circle cx="70" cy="160" r="4" fill="var(--color-primary-500)" />
            <circle cx="40" cy="90" r="4" fill="var(--color-primary-500)" />
          </svg>
        </div>
      </div>
    </Card>
  );
}

import { Sparkles } from 'lucide-react';
import { Button } from '../../../components/ui/Button';

interface GenerationControlsProps {
  onGenerate: () => void;
  isGenerating: boolean;
}

export function GenerationControls({ onGenerate, isGenerating }: GenerationControlsProps) {
  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-6 bg-surface-50 dark:bg-surface-800/50 rounded-xl border border-surface-200 dark:border-surface-700">
      <div>
        <h3 className="font-medium text-surface-900 dark:text-white">AI Generator</h3>
        <p className="text-sm text-surface-500 dark:text-surface-400">Produce 3 new concepts based on current brief</p>
      </div>
      
      <div className="relative group">
        {!isGenerating && (
          <div className="absolute -inset-0.5 bg-gradient-to-r from-primary-500 to-accent-500 rounded-lg blur opacity-30 group-hover:opacity-70 transition duration-1000 group-hover:duration-200 animate-pulse-slow"></div>
        )}
        <Button
          variant="primary"
          size="lg"
          className="relative w-full sm:w-auto"
          onClick={onGenerate}
          isLoading={isGenerating}
          leftIcon={<Sparkles className="w-5 h-5" />}
        >
          {isGenerating ? 'Synthesizing...' : 'Generate New Ideas'}
        </Button>
      </div>
    </div>
  );
}

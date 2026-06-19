import { useState } from 'react';
import { MessageSquareText } from 'lucide-react';
import { useIdeaList } from '../../features/ideas/hooks/useIdeas';
import { useCritiqueByIdeaId } from '../../features/critique/hooks/useCritique';
import { IdeaSelector } from '../../features/critique/components/IdeaSelector';
import { CritiquePanel } from '../../features/critique/components/CritiquePanel';
import { RecommendationPanel } from '../../features/critique/components/RecommendationPanel';
import { Skeleton } from '../../components/ui/Skeleton';
import { EmptyState } from '../../components/ui/EmptyState';

export default function CritiqueMode() {
  const [selectedIdeaId, setSelectedIdeaId] = useState<string | null>(null);
  const { data: ideas, isLoading: isLoadingIdeas } = useIdeaList();
  const { data: critiques, isLoading: isLoadingCritiques } = useCritiqueByIdeaId(selectedIdeaId);

  // For demo, extract all recommendations
  const allRecommendations = critiques 
    ? Array.from(new Set(critiques.flatMap(c => c.recommendations))).slice(0, 4)
    : [];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold text-surface-900 dark:text-white mb-2">
          Critique <span className="gradient-text">Mode</span>
        </h1>
        <p className="text-surface-500 dark:text-surface-400">
          Evaluate concepts from multiple perspectives to ensure robustness and viability.
        </p>
      </header>

      {isLoadingIdeas ? (
        <div className="flex gap-4 mb-8 overflow-hidden">
          {Array(4).fill(0).map((_, i) => <Skeleton key={i} className="h-24 w-64 rounded-xl shrink-0" />)}
        </div>
      ) : (
        <IdeaSelector 
          ideas={ideas || []} 
          selectedId={selectedIdeaId} 
          onSelect={setSelectedIdeaId} 
        />
      )}

      <div className="mt-8 border-t border-surface-200 dark:border-surface-800 pt-8">
        {!selectedIdeaId ? (
          <div className="bg-surface-50 dark:bg-surface-800/30 rounded-xl border border-dashed border-surface-300 dark:border-surface-700 p-12">
            <EmptyState
              icon={MessageSquareText}
              title="No concept selected"
              description="Select an idea above to view its multi-persona critique."
            />
          </div>
        ) : isLoadingCritiques ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Skeleton className="h-[400px] w-full rounded-xl" />
            <Skeleton className="h-[400px] w-full rounded-xl" />
          </div>
        ) : critiques && critiques.length > 0 ? (
          <div className="space-y-8 animate-fade-in">
            <CritiquePanel critiques={critiques} />
            <div className="mt-8">
              <RecommendationPanel recommendations={allRecommendations} />
            </div>
          </div>
        ) : (
          <div className="bg-surface-50 dark:bg-surface-800/30 rounded-xl border border-dashed border-surface-300 dark:border-surface-700 p-12">
            <EmptyState
              icon={MessageSquareText}
              title="Critiques generating..."
              description="Our AI personas are currently reviewing this concept."
            />
          </div>
        )}
      </div>
    </div>
  );
}

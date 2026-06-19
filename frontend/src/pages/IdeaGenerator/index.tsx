import { BriefEditor } from '../../features/ideas/components/BriefEditor';
import { GenerationControls } from '../../features/ideas/components/GenerationControls';
import { IdeaGrid } from '../../features/ideas/components/IdeaGrid';
import { useIdeaList, useGenerateIdeas } from '../../features/ideas/hooks/useIdeas';
import { Skeleton } from '../../components/ui/Skeleton';

export default function IdeaGenerator() {
  const { data: ideas, isLoading } = useIdeaList();
  const { mutate: generateIdeas, isPending } = useGenerateIdeas();

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold text-surface-900 dark:text-white mb-2">
          Idea <span className="gradient-text">Generator</span>
        </h1>
        <p className="text-surface-500 dark:text-surface-400">
          Synthesize creative briefs into actionable, structured project concepts.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 space-y-6">
          <div className="sticky top-24 space-y-6">
            <BriefEditor 
              onSubmit={(data) => generateIdeas(data)} 
              isGenerating={isPending} 
            />
            
            <GenerationControls 
              onGenerate={() => generateIdeas({ theme: 'Random Inspiration', constraints: '', inspirations: '', style: '' })} 
              isGenerating={isPending} 
            />
          </div>
        </div>

        <div className="lg:col-span-8">
          {isLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {Array(4).fill(0).map((_, i) => (
                <Skeleton key={i} className="h-64 w-full rounded-xl" />
              ))}
            </div>
          ) : (
            <IdeaGrid ideas={ideas || []} />
          )}
        </div>
      </div>
    </div>
  );
}

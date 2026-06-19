import { Lightbulb } from 'lucide-react';
import { EmptyState } from '../../../components/ui/EmptyState';
import { IdeaCard } from './IdeaCard';
import type { IdeaCard as IdeaCardType } from '../../../types/idea';

interface IdeaGridProps {
  ideas: IdeaCardType[];
}

export function IdeaGrid({ ideas }: IdeaGridProps) {
  if (!ideas || ideas.length === 0) {
    return (
      <div className="p-8 bg-surface-50 dark:bg-surface-800/50 rounded-xl border border-dashed border-surface-300 dark:border-surface-700">
        <EmptyState
          icon={Lightbulb}
          title="No ideas generated yet"
          description="Create a creative brief above and generate your first batch of AI concepts."
        />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {ideas.map((idea, index) => (
        <div 
          key={idea.id} 
          className="animate-fade-in"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          <IdeaCard idea={idea} />
        </div>
      ))}
    </div>
  );
}

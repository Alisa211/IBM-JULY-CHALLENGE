import { CheckCircle2 } from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import { cn } from '../../../utils/cn';
import type { IdeaCard as IdeaCardType } from '../../../types/idea';

interface IdeaSelectorProps {
  ideas: IdeaCardType[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function IdeaSelector({ ideas, selectedId, onSelect }: IdeaSelectorProps) {
  if (!ideas || ideas.length === 0) return null;

  return (
    <div className="mb-8">
      <h3 className="text-sm font-semibold text-surface-900 dark:text-white uppercase tracking-wider mb-4">
        Select Concept for Critique
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {ideas.map((idea) => {
          const isSelected = selectedId === idea.id;
          return (
            <Card
              key={idea.id}
              hover
              onClick={() => onSelect(idea.id)}
              className={cn(
                "p-4 cursor-pointer relative overflow-hidden transition-all duration-200",
                isSelected 
                  ? "ring-2 ring-primary-500 border-primary-500 bg-primary-50/50 dark:bg-primary-900/10 shadow-md" 
                  : "border-surface-200 dark:border-surface-700 hover:border-surface-300 dark:hover:border-surface-600"
              )}
            >
              {isSelected && (
                <div className="absolute top-3 right-3 text-primary-500">
                  <CheckCircle2 className="w-5 h-5 fill-current bg-white dark:bg-surface-900 rounded-full" />
                </div>
              )}
              <h4 className="font-medium text-surface-900 dark:text-white truncate pr-8 mb-1">
                {idea.title}
              </h4>
              <p className="text-xs text-surface-500 line-clamp-2">
                {idea.concept}
              </p>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

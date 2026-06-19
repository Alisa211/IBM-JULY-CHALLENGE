import { Card } from '../../../components/ui/Card';
import { Badge } from '../../../components/ui/Badge';
import type { IdeaCard as IdeaCardType } from '../../../types/idea';

interface IdeaCardProps {
  idea: IdeaCardType;
  onClick?: () => void;
  selected?: boolean;
}

export function IdeaCard({ idea, onClick, selected }: IdeaCardProps) {
  const statusColors = {
    draft: 'default',
    reviewed: 'secondary',
    approved: 'success',
    archived: 'danger'
  } as const;

  return (
    <Card 
      hover 
      className={`p-5 flex flex-col h-full cursor-pointer transition-all ${
        selected ? 'ring-2 ring-primary-500 border-primary-500 shadow-md' : ''
      }`}
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3 gap-2">
        <h3 className="font-semibold text-lg text-surface-900 dark:text-white leading-tight">
          {idea.title}
        </h3>
        <Badge variant={statusColors[idea.status]} size="sm" className="shrink-0 capitalize">
          {idea.status}
        </Badge>
      </div>

      <div className="flex-1 space-y-3">
        <p className="text-sm text-surface-700 dark:text-surface-300 leading-relaxed line-clamp-3">
          {idea.concept}
        </p>
        <p className="text-xs text-surface-500 dark:text-surface-400 italic leading-relaxed line-clamp-2">
          {idea.rationale}
        </p>
      </div>

      <div className="mt-4 pt-4 border-t border-surface-100 dark:border-surface-800 flex flex-wrap gap-2">
        {idea.tags.map(tag => (
          <Badge key={tag} variant="default" size="sm">
            {tag}
          </Badge>
        ))}
      </div>
    </Card>
  );
}

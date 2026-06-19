import { Card } from '../../../components/ui/Card';
import { Badge } from '../../../components/ui/Badge';
import { EmptyState } from '../../../components/ui/EmptyState';
import type { StyleSimilarity } from '../../../types/styleDna';
import { Dna } from 'lucide-react';

interface SimilarityListProps {
  similarities: StyleSimilarity[];
}

export function SimilarityList({ similarities }: SimilarityListProps) {
  if (!similarities || similarities.length === 0) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-semibold text-surface-900 dark:text-white mb-4">Similar Styles</h3>
        <EmptyState
          icon={Dna}
          title="No similarities found"
          description="We couldn't find any matching styles in the database."
        />
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-surface-900 dark:text-white">Similar Styles</h3>
        <p className="text-sm text-surface-500 dark:text-surface-400">Closest matches in the design system</p>
      </div>

      <div className="space-y-4">
        {similarities.map(similarity => (
          <div 
            key={similarity.id} 
            className="p-4 rounded-lg border border-surface-200 dark:border-surface-700 hover:bg-surface-50 dark:hover:bg-surface-800/50 transition-colors"
          >
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-medium text-surface-900 dark:text-white">{similarity.title}</h4>
              <Badge 
                variant={similarity.similarity > 0.8 ? 'success' : similarity.similarity > 0.6 ? 'warning' : 'default'}
              >
                {(similarity.similarity * 100).toFixed(1)}% Match
              </Badge>
            </div>
            
            <div className="w-full h-1.5 bg-surface-100 dark:bg-surface-800 rounded-full overflow-hidden mb-4">
              <div 
                className="h-full bg-primary-500 rounded-full"
                style={{ width: `${similarity.similarity * 100}%` }}
              />
            </div>

            <div className="flex flex-wrap gap-2">
              {similarity.traits.map(trait => (
                <Badge key={trait} variant="secondary" size="sm">
                  {trait}
                </Badge>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

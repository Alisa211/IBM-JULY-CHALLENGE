import { Card } from '../../../components/ui/Card';
import { Badge } from '../../../components/ui/Badge';
import type { StyleTrait } from '../../../types/styleDna';

interface StyleTraitsCardProps {
  traits: StyleTrait[];
}

export function StyleTraitsCard({ traits }: StyleTraitsCardProps) {
  // Group traits by category
  const groupedTraits = traits.reduce((acc, trait) => {
    if (!acc[trait.category]) {
      acc[trait.category] = [];
    }
    acc[trait.category].push(trait);
    return acc;
  }, {} as Record<string, StyleTrait[]>);

  const categories = Object.keys(groupedTraits).sort();

  return (
    <Card className="p-6 h-full" hover>
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-surface-900 dark:text-white">Style Traits</h3>
        <p className="text-sm text-surface-500 dark:text-surface-400">Deconstructed aesthetic properties</p>
      </div>

      <div className="space-y-6">
        {categories.map(category => (
          <div key={category} className="space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-medium text-surface-700 dark:text-surface-300 capitalize">
                {category}
              </h4>
              <Badge variant="default" size="sm">{groupedTraits[category].length}</Badge>
            </div>
            
            <div className="space-y-3">
              {groupedTraits[category].sort((a, b) => b.confidence - a.confidence).map(trait => (
                <div key={trait.name} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-surface-900 dark:text-white font-medium">{trait.name}</span>
                    <span className="text-surface-500">{(trait.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full h-2 bg-surface-100 dark:bg-surface-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full"
                      style={{ width: `${trait.confidence * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

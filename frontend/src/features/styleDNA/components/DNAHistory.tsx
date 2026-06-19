import { Card } from '../../../components/ui/Card';
import { Badge } from '../../../components/ui/Badge';
import type { StyleDNA } from '../../../types/styleDna';

interface DNAHistoryProps {
  entries: StyleDNA[];
}

export function DNAHistory({ entries }: DNAHistoryProps) {
  if (!entries || entries.length === 0) return null;

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-surface-900 dark:text-white">Analysis History</h3>
        <p className="text-sm text-surface-500 dark:text-surface-400">Previous style extractions</p>
      </div>

      <div className="relative border-l-2 border-surface-200 dark:border-surface-700 ml-3 space-y-8 pb-4">
        {entries.map((entry, index) => (
          <div key={entry.id} className="relative pl-6 animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
            {/* Timeline dot */}
            <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-white dark:bg-surface-900 border-4 border-primary-500" />
            
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
              <div className="flex-1">
                <div className="text-xs font-medium text-surface-400 dark:text-surface-500 mb-1">
                  {new Date(entry.createdAt).toLocaleDateString(undefined, { 
                    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
                  })}
                </div>
                <h4 className="text-base font-medium text-surface-900 dark:text-white mb-2">
                  {entry.title}
                </h4>
                <div className="flex flex-wrap gap-2 mb-3">
                  <Badge variant="primary" size="sm">
                    {entry.traits.length} Traits Identified
                  </Badge>
                  {entry.traits.slice(0, 3).map(trait => (
                    <Badge key={trait.name} variant="default" size="sm">
                      {trait.name}
                    </Badge>
                  ))}
                  {entry.traits.length > 3 && (
                    <Badge variant="default" size="sm">+{entry.traits.length - 3} more</Badge>
                  )}
                </div>
              </div>
              
              {entry.thumbnailUrl && (
                <div className="shrink-0">
                  <img 
                    src={entry.thumbnailUrl} 
                    alt={entry.title} 
                    className="w-20 h-20 rounded-lg object-cover border border-surface-200 dark:border-surface-700 shadow-sm"
                  />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

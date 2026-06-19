import { Card } from '../../../components/ui/Card';
import type { SculptureMetadata } from '../../../types/sculpture';

interface MetadataPanelProps {
  metadata: SculptureMetadata;
}

export function MetadataPanel({ metadata }: MetadataPanelProps) {
  const entries = Object.entries(metadata).filter(([_, value]) => value !== undefined && value !== '');

  if (entries.length === 0) return null;

  return (
    <Card className="p-6 bg-surface-50/50 dark:bg-surface-800/30 border-surface-200 dark:border-surface-700">
      <h3 className="text-sm font-semibold text-surface-900 dark:text-white uppercase tracking-wider mb-4">
        Extracted Metadata
      </h3>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-4 gap-x-6">
        {entries.map(([key, value]) => {
          // Format key from camelCase to Title Case
          const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
          
          return (
            <div key={key} className="space-y-1">
              <dt className="text-xs font-medium text-surface-500 dark:text-surface-400">
                {label}
              </dt>
              <dd className="text-sm font-medium text-surface-900 dark:text-white">
                {value}
              </dd>
            </div>
          );
        })}
      </div>
    </Card>
  );
}

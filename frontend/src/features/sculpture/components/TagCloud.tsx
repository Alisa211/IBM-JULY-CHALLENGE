import { Card } from '../../../components/ui/Card';
import { Badge } from '../../../components/ui/Badge';

interface TagCloudProps {
  iconography: string[];
  motifs: string[];
}

export function TagCloud({ iconography, motifs }: TagCloudProps) {
  return (
    <Card className="p-6">
      <div className="space-y-8">
        <div>
          <h3 className="text-sm font-semibold text-surface-900 dark:text-white uppercase tracking-wider mb-4 border-b border-surface-200 dark:border-surface-700 pb-2">
            Iconography & Subject Matter
          </h3>
          <div className="flex flex-wrap gap-2">
            {iconography.map((tag, index) => (
              <div 
                key={tag} 
                className="animate-fade-in"
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <Badge variant="primary" size="md" className="shadow-sm">
                  {tag}
                </Badge>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-surface-900 dark:text-white uppercase tracking-wider mb-4 border-b border-surface-200 dark:border-surface-700 pb-2">
            Visual Motifs & Form
          </h3>
          <div className="flex flex-wrap gap-2">
            {motifs.map((tag, index) => (
              <div 
                key={tag} 
                className="animate-fade-in"
                style={{ animationDelay: `${(iconography.length + index) * 50}ms` }}
              >
                <Badge variant="secondary" size="md" className="shadow-sm">
                  {tag}
                </Badge>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}

import { Lightbulb } from 'lucide-react';
import { Card } from '../../../components/ui/Card';

interface RecommendationPanelProps {
  recommendations: string[];
}

export function RecommendationPanel({ recommendations }: RecommendationPanelProps) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <Card className="p-6 bg-gradient-to-br from-surface-50 to-white dark:from-surface-900 dark:to-surface-800 border-primary-200 dark:border-primary-900/50">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-gradient-primary text-white flex items-center justify-center shadow-md">
          <Lightbulb className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-surface-900 dark:text-white">Key Recommendations</h3>
          <p className="text-sm text-surface-500 dark:text-surface-400">Synthesized from all AI personas</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {recommendations.map((rec, index) => (
          <div 
            key={index}
            className="p-4 rounded-xl bg-white dark:bg-surface-900 shadow-sm border border-surface-100 dark:border-surface-800 flex items-start gap-3"
          >
            <div className="shrink-0 w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 flex items-center justify-center text-sm font-bold">
              {index + 1}
            </div>
            <p className="text-sm font-medium text-surface-700 dark:text-surface-300 leading-relaxed pt-0.5">
              {rec}
            </p>
          </div>
        ))}
      </div>
    </Card>
  );
}

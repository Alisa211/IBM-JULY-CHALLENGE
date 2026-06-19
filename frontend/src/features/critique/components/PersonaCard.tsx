import { ScrollText, Palette, Ruler, Globe, CheckCircle2, XCircle } from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import type { Critique } from '../../../types/critique';
import { cn } from '../../../utils/cn';

interface PersonaCardProps {
  critique: Critique;
  index: number;
}

const personaConfig = {
  'historian': { icon: ScrollText, color: 'text-secondary-600', bg: 'bg-secondary-100 dark:bg-secondary-900/30', border: 'border-secondary-500' },
  'creative-director': { icon: Palette, color: 'text-primary-600', bg: 'bg-primary-100 dark:bg-primary-900/30', border: 'border-primary-500' },
  'structural-analyst': { icon: Ruler, color: 'text-emerald-600', bg: 'bg-emerald-100 dark:bg-emerald-900/30', border: 'border-emerald-500' },
  'cultural-reviewer': { icon: Globe, color: 'text-accent-600', bg: 'bg-accent-100 dark:bg-accent-900/30', border: 'border-accent-500' },
};

export function PersonaCard({ critique, index }: PersonaCardProps) {
  const config = personaConfig[critique.persona];
  const Icon = config.icon;
  const name = critique.persona.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

  return (
    <Card 
      className={cn("flex flex-col h-full animate-slide-up overflow-hidden", `border-t-4 ${config.border}`)}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <div className="p-5 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={cn("w-10 h-10 rounded-full flex items-center justify-center shrink-0", config.bg, config.color)}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-surface-900 dark:text-white">{name}</h4>
            <p className="text-xs text-surface-500">AI Persona Critique</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-black tracking-tighter" style={{ color: `var(--color-${critique.persona === 'historian' ? 'secondary' : critique.persona === 'creative-director' ? 'primary' : critique.persona === 'structural-analyst' ? 'emerald' : 'accent'}-500)` }}>
            {critique.score}
          </div>
          <div className="text-[10px] uppercase font-bold text-surface-400">Score</div>
        </div>
      </div>

      <div className="p-5 flex-1 flex flex-col gap-6">
        <p className="text-sm text-surface-700 dark:text-surface-300 italic leading-relaxed">
          "{critique.feedback}"
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <h5 className="text-xs font-bold uppercase tracking-wider text-surface-900 dark:text-white mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-green-500" />
              Strengths
            </h5>
            <ul className="space-y-1.5">
              {critique.strengths.map((item, i) => (
                <li key={i} className="text-sm text-surface-600 dark:text-surface-400 pl-5 relative">
                  <span className="absolute left-1.5 top-2 w-1.5 h-1.5 rounded-full bg-green-500" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h5 className="text-xs font-bold uppercase tracking-wider text-surface-900 dark:text-white mb-2 flex items-center gap-1.5">
              <XCircle className="w-4 h-4 text-red-500" />
              Weaknesses
            </h5>
            <ul className="space-y-1.5">
              {critique.weaknesses.map((item, i) => (
                <li key={i} className="text-sm text-surface-600 dark:text-surface-400 pl-5 relative">
                  <span className="absolute left-1.5 top-2 w-1.5 h-1.5 rounded-full bg-red-500" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-auto pt-4 border-t border-surface-100 dark:border-surface-800">
          <h5 className="text-xs font-bold uppercase tracking-wider text-surface-900 dark:text-white mb-2">
            Actionable Recommendations
          </h5>
          <ul className="space-y-2">
            {critique.recommendations.map((rec, i) => (
              <li key={i} className="text-sm text-surface-700 dark:text-surface-300 flex items-start gap-2">
                <span className="shrink-0 w-5 h-5 rounded bg-surface-100 dark:bg-surface-800 flex items-center justify-center text-xs font-medium text-surface-500">
                  {i + 1}
                </span>
                <span className="mt-0.5">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Card>
  );
}

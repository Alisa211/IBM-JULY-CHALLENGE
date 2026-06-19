import type { Critique } from '../../../types/critique';
import { PersonaCard } from './PersonaCard';

interface CritiquePanelProps {
  critiques: Critique[];
}

export function CritiquePanel({ critiques }: CritiquePanelProps) {
  if (!critiques || critiques.length === 0) return null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {critiques.map((critique, index) => (
        <PersonaCard key={critique.id} critique={critique} index={index} />
      ))}
    </div>
  );
}

export interface Critique {
  id: string;
  ideaId: string;
  persona: CritiquePersona;
  feedback: string;
  score: number;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  createdAt: string;
}

export type CritiquePersona = 'historian' | 'creative-director' | 'structural-analyst' | 'cultural-reviewer';

export interface PersonaInfo {
  id: CritiquePersona;
  name: string;
  description: string;
  icon: string;
  color: string;
}

import type { PersonaInfo } from '../types/critique';
import type { Project } from '../types/project';

export const APP_NAME = 'AI Creative Director';

export const PERSONAS: PersonaInfo[] = [
  {
    id: 'historian',
    name: 'Historian',
    description:
      'Evaluates work through the lens of art history, tracing influences, precedents, and stylistic lineage across movements and eras.',
    icon: 'BookOpen',
    color: '#2563EB',
  },
  {
    id: 'creative-director',
    name: 'Creative Director',
    description:
      'Assesses originality, visual impact, and conceptual coherence. Focuses on whether the work pushes creative boundaries while remaining accessible.',
    icon: 'Sparkles',
    color: '#7C3AED',
  },
  {
    id: 'structural-analyst',
    name: 'Structural Analyst',
    description:
      'Examines composition, balance, material integrity, and spatial relationships. Considers engineering feasibility and structural harmony.',
    icon: 'Compass',
    color: '#059669',
  },
  {
    id: 'cultural-reviewer',
    name: 'Cultural Reviewer',
    description:
      'Interprets cultural significance, symbolic resonance, and societal context. Evaluates how the work engages with contemporary discourse.',
    icon: 'Globe',
    color: '#F59E0B',
  },
];

export interface NavItem {
  label: string;
  path: string;
  icon: string;
}

export const NAV_ITEMS: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: 'LayoutDashboard' },
  { label: 'Style DNA', path: '/style-dna', icon: 'Dna' },
  { label: 'Sculpture Analyzer', path: '/sculpture', icon: 'ScanSearch' },
  { label: 'Idea Generator', path: '/ideas', icon: 'Lightbulb' },
  { label: 'Critique Mode', path: '/critique', icon: 'MessageSquare' },
  { label: 'Settings', path: '/settings', icon: 'Settings' },
];

export const ANALYSIS_STATUSES = {
  IDLE: 'idle',
  UPLOADING: 'uploading',
  ANALYZING: 'analyzing',
  COMPLETE: 'complete',
  ERROR: 'error',
} as const;

export type AnalysisStatus = (typeof ANALYSIS_STATUSES)[keyof typeof ANALYSIS_STATUSES];

export const DEFAULT_PROJECT: Project = {
  id: 'proj-default-001',
  name: 'Renaissance Revival Collection',
  description:
    'A curated exploration of Renaissance sculptural techniques reinterpreted through contemporary digital fabrication methods.',
  createdAt: '2026-01-15T10:30:00Z',
  updatedAt: '2026-06-10T14:22:00Z',
  imageCount: 24,
  analysisCount: 12,
};

export const COLORS = {
  primary: { light: '#7C3AED', dark: '#A78BFA' },
  secondary: { light: '#2563EB', dark: '#60A5FA' },
  accent: '#F59E0B',
  surface: {
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    900: '#0f172a',
    950: '#020617',
  },
} as const;

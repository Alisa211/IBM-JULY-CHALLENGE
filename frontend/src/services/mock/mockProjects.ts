import type { Project } from '../../types/project';

export const mockProjects: Project[] = [
  {
    id: 'proj-001',
    name: 'Renaissance Revival Collection',
    description:
      'A curated exploration of Renaissance sculptural techniques reinterpreted through contemporary digital fabrication methods. Emphasis on classical contrapposto, drapery studies, and chiaroscuro surface treatments.',
    createdAt: '2026-01-15T10:30:00Z',
    updatedAt: '2026-06-10T14:22:00Z',
    imageCount: 24,
    analysisCount: 12,
  },
  {
    id: 'proj-002',
    name: 'Urban Metamorphosis Series',
    description:
      'An investigation into the dialogue between organic sculptural forms and brutalist urban architecture. The series explores themes of entropy, reclamation, and biomorphic growth emerging from concrete geometries.',
    createdAt: '2026-03-02T09:15:00Z',
    updatedAt: '2026-06-12T18:45:00Z',
    imageCount: 18,
    analysisCount: 9,
  },
  {
    id: 'proj-003',
    name: 'Ephemeral Monuments',
    description:
      'Temporary large-scale installations that challenge the permanence traditionally associated with monumental sculpture. Utilizes ice, sand, biodegradable composites, and projected light as primary media.',
    createdAt: '2026-05-20T11:00:00Z',
    updatedAt: '2026-06-14T08:30:00Z',
    imageCount: 31,
    analysisCount: 15,
  },
];

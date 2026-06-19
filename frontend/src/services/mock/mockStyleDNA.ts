import type { StyleDNA } from '../../types/styleDna';

export const mockStyleDNA: StyleDNA[] = [
  {
    id: 'style-001',
    projectId: 'proj-001',
    title: 'Neo-Classical Organic Fusion',
    traits: [
      { name: 'Baroque Influence', confidence: 0.92, category: 'period' },
      { name: 'Organic Forms', confidence: 0.87, category: 'form' },
      { name: 'Marble Texture Rendering', confidence: 0.85, category: 'material' },
      { name: 'Chiaroscuro Modeling', confidence: 0.79, category: 'technique' },
      { name: 'Sublime Grandeur', confidence: 0.74, category: 'emotion' },
    ],
    embeddingId: 'emb-vec-001',
    createdAt: '2026-02-10T12:00:00Z',
    thumbnailUrl: '/thumbnails/style-001.jpg',
  },
  {
    id: 'style-002',
    projectId: 'proj-001',
    title: 'Mannerist Tension Study',
    traits: [
      { name: 'Elongated Proportions', confidence: 0.94, category: 'form' },
      { name: 'Mannerist Period', confidence: 0.91, category: 'period' },
      { name: 'Polished Bronze', confidence: 0.83, category: 'material' },
      { name: 'Serpentine Composition', confidence: 0.88, category: 'technique' },
      { name: 'Dynamic Unease', confidence: 0.76, category: 'emotion' },
    ],
    embeddingId: 'emb-vec-002',
    createdAt: '2026-03-05T15:30:00Z',
    thumbnailUrl: '/thumbnails/style-002.jpg',
  },
  {
    id: 'style-003',
    projectId: 'proj-002',
    title: 'Brutalist Biomorphism',
    traits: [
      { name: 'Geometric Fragmentation', confidence: 0.89, category: 'form' },
      { name: 'Post-War Modernism', confidence: 0.82, category: 'period' },
      { name: 'Raw Concrete & Steel', confidence: 0.91, category: 'material' },
      { name: 'Subtractive Carving', confidence: 0.78, category: 'technique' },
      { name: 'Industrial Melancholy', confidence: 0.71, category: 'emotion' },
    ],
    embeddingId: 'emb-vec-003',
    createdAt: '2026-04-18T09:00:00Z',
    thumbnailUrl: '/thumbnails/style-003.jpg',
  },
  {
    id: 'style-004',
    projectId: 'proj-003',
    title: 'Transient Materiality',
    traits: [
      { name: 'Amorphous Silhouettes', confidence: 0.86, category: 'form' },
      { name: 'Contemporary Installation', confidence: 0.93, category: 'period' },
      { name: 'Ice & Light Projection', confidence: 0.90, category: 'material' },
      { name: 'Environmental Casting', confidence: 0.84, category: 'technique' },
      { name: 'Wistful Impermanence', confidence: 0.88, category: 'emotion' },
    ],
    embeddingId: 'emb-vec-004',
    createdAt: '2026-05-25T17:45:00Z',
    thumbnailUrl: '/thumbnails/style-004.jpg',
  },
];

export const mockSimilarities: import('../../types/styleDna').StyleSimilarity[] = [
  { id: 'sim-1', styleDnaId: 'sdna-default', title: 'Baroque Evolution', similarity: 0.92, traits: ['Organic Forms', 'Chiaroscuro'] },
  { id: 'sim-2', styleDnaId: 'sdna-default', title: 'Neo-Classical Harmony', similarity: 0.85, traits: ['Proportions', 'Marble Texture'] },
];

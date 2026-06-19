import type { IdeaCard } from '../../types/idea';

export const mockIdeas: IdeaCard[] = [
  {
    id: 'idea-001',
    projectId: 'proj-001',
    title: 'Deconstructed Pietà',
    concept:
      'A large-scale marble installation that fragments Michelangelo\'s Pietà into floating shards suspended by tensioned steel cables. Each fragment is precisely cut along historically documented fracture lines, creating negative space that becomes the primary compositional element.',
    rationale:
      'By deconstructing one of sculpture\'s most revered works, the piece interrogates our relationship with canonical art. The negative space between fragments invites viewers to mentally reconstruct the original, making them active participants in meaning-making rather than passive observers.',
    tags: ['marble', 'installation', 'deconstruction', 'Renaissance', 'interactive'],
    imageUrl: '/concepts/deconstructed-pieta.jpg',
    createdAt: '2026-02-20T11:00:00Z',
    status: 'approved',
  },
  {
    id: 'idea-002',
    projectId: 'proj-001',
    title: 'Digital Ephemera Installation',
    concept:
      'A room-sized projection-mapped sculpture where physical plaster forms serve as screens for animated Renaissance frescoes. The projections age, crack, and deteriorate in real-time, compressing centuries of decay into a single viewing session.',
    rationale:
      'Bridges the temporal gap between fresco painting and digital media. The accelerated decay confronts viewers with the impermanence of all creative work while the technology paradoxically offers infinite restoration through replay.',
    tags: ['projection-mapping', 'digital', 'fresco', 'time-based', 'plaster'],
    imageUrl: '/concepts/digital-ephemera.jpg',
    createdAt: '2026-03-08T14:30:00Z',
    status: 'reviewed',
  },
  {
    id: 'idea-003',
    projectId: 'proj-002',
    title: 'Mycelium Colonnade',
    concept:
      'A series of load-bearing columns grown from mycelium composites within 3D-printed formwork shaped as classical Corinthian capitals. The living material continues to grow post-installation, gradually softening the geometric precision of the printed molds.',
    rationale:
      'Merges biotechnology with classical architectural vocabulary. The tension between biological growth and digital precision mirrors broader cultural negotiations between technological control and natural systems. The work is both structurally functional and philosophically provocative.',
    tags: ['bio-art', 'mycelium', '3D-printing', 'architecture', 'living-material'],
    createdAt: '2026-04-12T09:00:00Z',
    status: 'draft',
  },
  {
    id: 'idea-004',
    projectId: 'proj-002',
    title: 'Acoustic Shadow Garden',
    concept:
      'An outdoor sculpture garden where each piece is designed primarily for its acoustic properties. Hollow bronze forms, perforated steel planes, and resonant stone chambers create a spatial soundscape that changes with wind speed, temperature, and visitor proximity.',
    rationale:
      'Challenges the visual primacy of sculptural practice by foregrounding sonic experience. The environment-responsive nature ensures no two visits produce the same experience, transforming the garden into a living instrument played by weather and human presence.',
    tags: ['sound-art', 'bronze', 'outdoor', 'interactive', 'environmental'],
    imageUrl: '/concepts/acoustic-garden.jpg',
    createdAt: '2026-04-28T16:15:00Z',
    status: 'approved',
  },
  {
    id: 'idea-005',
    projectId: 'proj-003',
    title: 'Glacial Memory Archive',
    concept:
      'Ice cores extracted from retreating glaciers are encased in transparent resin columns, each containing thousands of years of atmospheric data as visible strata. The columns are arranged chronologically, creating a physical timeline of planetary climate that visitors walk through.',
    rationale:
      'Transforms abstract climate data into visceral, embodied experience. The beauty of the ice strata creates an emotional connection to geological time that charts and graphs cannot achieve, while the resin encasement creates a paradox of preservation—saving what is being lost.',
    tags: ['climate', 'ice', 'resin', 'data-visualization', 'environmental'],
    createdAt: '2026-05-30T08:00:00Z',
    status: 'draft',
  },
  {
    id: 'idea-006',
    projectId: 'proj-003',
    title: 'Kinetic Erosion Machine',
    concept:
      'A self-destructing kinetic sculpture that uses programmed robotic arms to slowly carve away its own material over the course of an exhibition. Sensors track visitor attention (gaze, proximity) and accelerate erosion in the most-viewed areas, making observation itself a destructive act.',
    rationale:
      'Explores the observer effect in art appreciation. The more popular a feature becomes, the faster it disappears, creating a feedback loop between audience desire and artistic loss. The sculpture documents its own destruction, producing a secondary digital artwork.',
    tags: ['kinetic', 'robotic', 'self-destructing', 'interactive', 'surveillance'],
    imageUrl: '/concepts/erosion-machine.jpg',
    createdAt: '2026-06-05T13:45:00Z',
    status: 'reviewed',
  },
];

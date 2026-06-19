import type { SculptureAnalysis } from '../../types/sculpture';

export const mockAnalyses: SculptureAnalysis[] = [
  {
    id: 'analysis-001',
    projectId: 'proj-001',
    imageUrl: '/uploads/madonna-child-relief.png',
    fileName: 'madonna-child-relief.png',
    iconography: ['Madonna and Child', 'Serpentine Column', 'Aureole'],
    motifs: ['Drapery folds', 'Contrapposto', 'Sfumato transition zones'],
    materials: ['Carrara marble', 'Gold leaf accents'],
    period: 'High Renaissance (c. 1490–1530)',
    summary:
      'This relief panel demonstrates mastery of High Renaissance sculptural conventions. The Madonna figure employs a subtle contrapposto stance, creating an S-curve that lends naturalism and grace. The drapery folds exhibit deep undercutting characteristic of Florentine workshop techniques. The serpentine column in the background references classical architecture, anchoring the sacred scene in a humanist spatial context.',
    confidence: 0.91,
    createdAt: '2026-02-12T14:30:00Z',
    metadata: {
      dimensions: '82 × 56 × 12 cm',
      estimatedPeriod: 'Late 15th century',
      style: 'Florentine High Renaissance',
      region: 'Tuscany, Italy',
      condition: 'Minor surface erosion; gold leaf partially intact',
    },
  },
  {
    id: 'analysis-002',
    projectId: 'proj-002',
    imageUrl: '/uploads/urban-growth-form.png',
    fileName: 'urban-growth-form.png',
    iconography: ['Emerging Figure', 'Fractured Facade'],
    motifs: ['Biomorphic protrusion', 'Grid disruption', 'Erosion channels'],
    materials: ['Reinforced concrete', 'Bronze patina', 'Reclaimed rebar'],
    period: 'Contemporary (2024–present)',
    summary:
      'A striking contemporary work that stages a confrontation between rigid architectural geometry and emergent organic form. The figure appears to grow from—or dissolve into—a fractured concrete slab, with bronze-patinated tendrils bridging the boundary. The deliberate exposure of rebar suggests vulnerability beneath the brutalist surface, while erosion channels evoke natural weathering accelerated to human timescales.',
    confidence: 0.87,
    createdAt: '2026-04-20T10:15:00Z',
    metadata: {
      dimensions: '210 × 140 × 95 cm',
      estimatedPeriod: 'Contemporary',
      style: 'Neo-Brutalist / Biomorphic',
      region: 'Berlin, Germany',
      condition: 'Excellent; intentional patina developing',
    },
  },
  {
    id: 'analysis-003',
    projectId: 'proj-003',
    imageUrl: '/uploads/ice-monument-dawn.png',
    fileName: 'ice-monument-dawn.png',
    iconography: ['Obelisk Form', 'Refracted Light Halo'],
    motifs: ['Crystalline fracture planes', 'Melt erosion', 'Prismatic refraction'],
    materials: ['Glacial ice blocks', 'Embedded fiber optics', 'UV-reactive pigment'],
    period: 'Contemporary Installation (2026)',
    summary:
      'This ephemeral monument exploits the temporal nature of ice as sculptural medium. The obelisk form references classical memorial traditions while its inherent impermanence subverts their intended eternity. Embedded fiber optics create an internal luminescence that shifts with ambient temperature, and UV-reactive pigments reveal hidden patterns as the surface melts, producing a continuously evolving artwork that documents its own dissolution.',
    confidence: 0.84,
    createdAt: '2026-05-28T06:45:00Z',
    metadata: {
      dimensions: '350 × 80 × 80 cm (at installation)',
      estimatedPeriod: 'Contemporary',
      style: 'Ephemeral / Environmental Installation',
      region: 'Tromsø, Norway',
      condition: 'Transient; documented via time-lapse',
    },
  },
];

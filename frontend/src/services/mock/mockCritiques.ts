import type { Critique } from '../../types/critique';

export const mockCritiques: Critique[] = [
  // ── Critiques for "Deconstructed Pietà" (idea-001) ──────────────────
  {
    id: 'crit-001',
    ideaId: 'idea-001',
    persona: 'historian',
    feedback:
      'The fragmentation of the Pietà along historically documented fracture lines demonstrates sophisticated art-historical awareness. This approach echoes the kintsugi tradition of honoring breakage, though transposed into a Western canonical context. The tension between reverence and deconstruction is compelling, but the piece risks being read as mere iconoclasm without careful curatorial framing.',
    score: 82,
    strengths: [
      'Deep engagement with art-historical precedent',
      'Innovative use of negative space as compositional driver',
      'The fracture-line research adds scholarly rigor',
    ],
    weaknesses: [
      'Could be perceived as disrespectful without contextual framing',
      'The Pietà reference may limit accessibility for non-Western-art-literate audiences',
      'Historical fracture data may not be comprehensive enough for all fragments',
    ],
    recommendations: [
      'Include a companion exhibition of the fracture-line research process',
      'Consider pairing with non-Western sculptural deconstructions for broader dialogue',
      'Document the fabrication process as part of the artwork',
    ],
    createdAt: '2026-02-22T10:00:00Z',
  },
  {
    id: 'crit-002',
    ideaId: 'idea-001',
    persona: 'creative-director',
    feedback:
      'Visually arresting concept with strong gallery appeal. The floating shards create dramatic shadow play and the negative space between fragments offers rich photographic opportunities. The concept has viral potential while maintaining intellectual depth—a rare combination. The steel cable suspension system could become a visual signature if refined.',
    score: 91,
    strengths: [
      'Exceptional visual impact and spatial drama',
      'Strong concept-to-form coherence',
      'High exhibition and media value',
      'Balances accessibility with conceptual depth',
    ],
    weaknesses: [
      'Cable tension system may create visual noise if not carefully designed',
      'Lighting design will be critical and complex',
      'Scale may limit venue options',
    ],
    recommendations: [
      'Develop a custom lighting design that emphasizes shadow patterns cast by fragments',
      'Create a scale maquette for spatial testing before full fabrication',
      'Explore AR companion experience allowing viewers to see the intact original overlaid',
    ],
    createdAt: '2026-02-22T10:30:00Z',
  },
  {
    id: 'crit-003',
    ideaId: 'idea-001',
    persona: 'structural-analyst',
    feedback:
      'The tensioned cable suspension presents significant engineering challenges. Each marble fragment will require precise center-of-gravity calculations, and the cable tension must account for thermal expansion in varying gallery climates. The connection points to the marble must be designed to distribute load without creating stress fractures in already-fragmented forms.',
    score: 68,
    strengths: [
      'Technically achievable with proper engineering',
      'Cable tensegrity offers interesting structural aesthetic',
      'Load distribution can be computed precisely with modern tools',
    ],
    weaknesses: [
      'Marble is brittle and connection points are critical failure risks',
      'Seismic considerations for gallery safety are non-trivial',
      'Installation and de-installation complexity increases cost significantly',
      'Thermal cycling could cause cable creep over extended exhibitions',
    ],
    recommendations: [
      'Commission a structural engineering feasibility study before committing to marble',
      'Consider high-strength polymer alternatives to steel cables for reduced visual weight',
      'Implement a monitoring system for cable tension over the exhibition period',
      'Design modular mounting system for easier transport between venues',
    ],
    createdAt: '2026-02-22T11:00:00Z',
  },
  {
    id: 'crit-004',
    ideaId: 'idea-001',
    persona: 'cultural-reviewer',
    feedback:
      'The deconstruction of a deeply significant Catholic artwork demands careful cultural navigation. While the concept powerfully speaks to post-modern attitudes toward canonical art, it must avoid the perception of sacrilege or cultural insensitivity. The piece succeeds when framed as an act of intimate study rather than destruction—closer to an X-ray than a hammer.',
    score: 75,
    strengths: [
      'Provokes meaningful dialogue about canonical art and cultural ownership',
      'The reconstruction-through-absence invites diverse interpretive frameworks',
      'Relevant to contemporary debates about decolonizing art collections',
    ],
    weaknesses: [
      'Religious communities may find the deconstruction disrespectful',
      'Western-canon-centric framing limits global cultural resonance',
      'Risk of being read as provocative for provocation\'s sake',
    ],
    recommendations: [
      'Engage religious and cultural advisory groups during development',
      'Frame the work explicitly as study and reverence, not destruction',
      'Include community response mechanisms within the exhibition design',
      'Consider a parallel work deconstructing a secular canonical sculpture for balance',
    ],
    createdAt: '2026-02-22T11:30:00Z',
  },

  // ── Critiques for "Kinetic Erosion Machine" (idea-006) ──────────────
  {
    id: 'crit-005',
    ideaId: 'idea-006',
    persona: 'historian',
    feedback:
      'The self-destructing sculpture has rich precedent in auto-destructive art, most notably Jean Tinguely\'s "Homage to New York" (1960) and Gustav Metzger\'s manifestos. This work advances the tradition by introducing audience complicity through gaze-tracking—the observer effect becomes literal rather than metaphorical. The feedback loop between attention and destruction is a genuinely novel contribution.',
    score: 88,
    strengths: [
      'Strong lineage in auto-destructive art tradition',
      'The gaze-tracking mechanism is a genuine conceptual innovation',
      'Creates a compelling archive of its own destruction',
    ],
    weaknesses: [
      'Must clearly acknowledge Tinguely and Metzger precedents to avoid appearing derivative',
      'The surveillance aspect may evoke negative associations that distract from artistic intent',
    ],
    recommendations: [
      'Include a dedicated historical context section in exhibition materials',
      'Consider making the surveillance mechanism visible rather than hidden',
      'Archive each exhibition iteration to build a longitudinal body of work',
    ],
    createdAt: '2026-06-07T09:00:00Z',
  },
  {
    id: 'crit-006',
    ideaId: 'idea-006',
    persona: 'creative-director',
    feedback:
      'This is a concept with extraordinary narrative potential. The idea that looking at art destroys it creates an irresistible hook for press coverage and social media discussion. The secondary digital artwork generated from destruction data adds a layer of creative output that justifies the loss. However, the pacing of destruction must be carefully calibrated—too fast and the experience feels gimmicky, too slow and the feedback loop becomes imperceptible.',
    score: 85,
    strengths: [
      'Compelling narrative that drives media engagement',
      'Dual output (physical destruction + digital creation) maximizes value',
      'Interactive element creates personal investment for visitors',
      'Strong conceptual clarity',
    ],
    weaknesses: [
      'Pacing calibration is critical and may require multiple prototyping cycles',
      'The "most-viewed areas erode fastest" mechanic could lead to homogeneous destruction patterns',
      'Technical complexity may introduce reliability issues during exhibitions',
    ],
    recommendations: [
      'Prototype with expendable materials to calibrate erosion rates',
      'Introduce randomness into the erosion algorithm to prevent predictable patterns',
      'Design the robotic arms to be visually dramatic—they are performers, not just tools',
      'Create a real-time digital visualization showing accumulated gaze data',
    ],
    createdAt: '2026-06-07T09:30:00Z',
  },
  {
    id: 'crit-007',
    ideaId: 'idea-006',
    persona: 'structural-analyst',
    feedback:
      'The robotic erosion system must be engineered for precision and safety. Material removal rates need to be controlled to prevent unexpected structural failure during public exhibition. The sculpture\'s internal structure must be designed with progressive collapse scenarios in mind, ensuring that no erosion path creates a hazardous instability.',
    score: 62,
    strengths: [
      'Robotic carving technology is well-established in industrial applications',
      'Digital control allows precise material removal programming',
      'Sensor integration for gaze tracking is technically feasible',
    ],
    weaknesses: [
      'Progressive structural integrity analysis is computationally expensive',
      'Dust and debris management in a gallery setting requires specialized systems',
      'Robotic arm failure during operation poses safety concerns',
      'Material choice must balance carvability with structural resilience',
    ],
    recommendations: [
      'Implement real-time finite element analysis to prevent unsafe erosion states',
      'Design fail-safe mechanisms that halt erosion if structural thresholds are breached',
      'Use a material with predictable fracture mechanics, such as high-density foam or plaster',
      'Install dust extraction systems integrated into the sculpture\'s base',
    ],
    createdAt: '2026-06-07T10:00:00Z',
  },
  {
    id: 'crit-008',
    ideaId: 'idea-006',
    persona: 'cultural-reviewer',
    feedback:
      'The surveillance-as-destruction metaphor resonates powerfully in our current cultural moment. The work speaks to attention economies, the commodification of observation, and the ethics of data collection—all urgent contemporary themes. The piece transforms the gallery into a microcosm of platform capitalism, where engagement metrics consume the very content they measure.',
    score: 93,
    strengths: [
      'Deeply relevant to contemporary discourse on surveillance capitalism',
      'The attention-as-consumption metaphor is immediately legible yet layered',
      'Creates a shared ethical experience among gallery visitors',
      'The self-documenting nature produces valuable cultural archive',
    ],
    weaknesses: [
      'Visitors may feel manipulated or surveilled, potentially triggering discomfort',
      'The concept might overshadow the sculptural qualities of the physical form',
    ],
    recommendations: [
      'Provide clear informed consent signage about gaze tracking',
      'Offer opt-out zones where visitors can observe without being tracked',
      'Partner with digital ethics scholars for exhibition programming',
      'Ensure the physical sculpture has aesthetic merit independent of the interactive mechanism',
    ],
    createdAt: '2026-06-07T10:30:00Z',
  },
];

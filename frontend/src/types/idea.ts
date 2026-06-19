export interface IdeaCard {
  id: string;
  projectId: string;
  title: string;
  concept: string;
  rationale: string;
  tags: string[];
  imageUrl?: string;
  createdAt: string;
  status: 'draft' | 'reviewed' | 'approved' | 'archived';
}

export interface IdeaBrief {
  theme: string;
  constraints: string;
  inspirations: string;
  style: string;
}

export interface StyleDNA {
  id: string;
  projectId: string;
  title: string;
  traits: StyleTrait[];
  embeddingId: string;
  createdAt: string;
  thumbnailUrl?: string;
}

export interface StyleTrait {
  name: string;
  confidence: number;
  category: 'form' | 'material' | 'period' | 'technique' | 'emotion';
}

export interface StyleSimilarity {
  id: string;
  styleDnaId: string;
  title: string;
  similarity: number;
  traits: string[];
}

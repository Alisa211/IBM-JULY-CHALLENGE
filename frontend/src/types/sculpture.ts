export interface SculptureAnalysis {
  id: string;
  projectId?: string;
  asset_id?: string;
  imageUrl?: string;
  fileName?: string;
  iconography: string[];
  motifs: string[];
  materials?: string[];
  style_traits?: string[];
  composition_notes?: string;
  period?: string;
  summary?: string;
  confidence: number;
  createdAt?: string;
  created_at?: string;
  metadata?: SculptureMetadata;
}

export interface SculptureMetadata {
  dimensions?: string;
  estimatedPeriod?: string;
  style?: string;
  region?: string;
  condition?: string;
}

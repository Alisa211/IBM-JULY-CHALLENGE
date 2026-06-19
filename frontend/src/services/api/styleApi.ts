import type { StyleDNA } from '../../types/styleDna';
import { mockStyleDNA, mockSimilarities } from '../mock/mockStyleDNA';

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class StyleApi {
  static async getAll(): Promise<StyleDNA[]> {
    await delay(800);
    return mockStyleDNA;
  }

  static async getById(id: string): Promise<StyleDNA | undefined> {
    await delay(500);
    return mockStyleDNA.find((s: StyleDNA) => s.id === id);
  }

  static async analyze(_file: File): Promise<StyleDNA> {
    await delay(2000);
    return {
      id: `sdna-${Date.now()}`,
      projectId: 'proj-default-001',
      title: `Analysis — ${_file.name}`,
      traits: mockStyleDNA[0].traits,
      embeddingId: `emb-${Date.now()}`,
      createdAt: new Date().toISOString(),
    };
  }

  static async getSimilarities(styleDnaId: string) {
    await delay(600);
    return mockSimilarities.filter((s: import('../../types/styleDna').StyleSimilarity) => s.styleDnaId === styleDnaId);
  }
}

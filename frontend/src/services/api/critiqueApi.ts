import type { Critique } from '../../types/critique';
import { mockCritiques } from '../mock';

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class CritiqueApi {
  static async getAll(): Promise<Critique[]> {
    await delay(800);
    return mockCritiques;
  }

  static async getByIdeaId(ideaId: string): Promise<Critique[]> {
    await delay(700);
    return mockCritiques.filter((c) => c.ideaId === ideaId);
  }

  static async critiqueIdea(ideaId: string): Promise<Critique[]> {
    await delay(4000);
    return mockCritiques
      .filter((c) => c.ideaId === 'idea-001')
      .map((c, idx) => ({
        ...c,
        id: `crit-gen-${Date.now()}-${idx}`,
        ideaId,
        createdAt: new Date().toISOString(),
      }));
  }
}

import type { IdeaCard, IdeaBrief } from '../../types/idea';
import { mockIdeas } from '../mock';
import { apiClient } from './client';

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class IdeaApi {
  static async getAll(): Promise<IdeaCard[]> {
    await delay(800);
    return mockIdeas;
  }

  static async getById(id: string): Promise<IdeaCard | undefined> {
    await delay(500);
    return mockIdeas.find((i) => i.id === id);
  }

  static async generate(brief: IdeaBrief, count = 3, styleDna: string = ""): Promise<IdeaCard[]> {
    const briefStr = `Theme: ${brief.theme}\nStyle: ${brief.style}\nConstraints: ${brief.constraints}\nInspirations: ${brief.inspirations}`;
    try {
      const response = await apiClient<any[]>('/ideas/generate', {
        method: 'POST',
        body: {
          brief: briefStr,
          style_dna: styleDna || `${brief.style} ${brief.theme}`
        }
      });
      return response.map((idea, idx) => ({
        id: `idea-gen-${Date.now()}-${idx}`,
        projectId: 'project-default',
        title: idea.title || `${brief.theme} — Concept ${idx + 1}`,
        concept: idea.description || '',
        rationale: idea.rationale || '',
        tags: idea.tags || [],
        createdAt: new Date().toISOString(),
        status: 'draft',
      }));
    } catch (e) {
      console.error("Failed to generate ideas, falling back to mock", e);
      await delay(1000);
      return mockIdeas.slice(0, count).map((idea, idx) => ({
        ...idea,
        id: `idea-gen-${Date.now()}-${idx}`,
        title: `${brief.theme} — Concept ${idx + 1}`,
        createdAt: new Date().toISOString(),
        status: 'draft' as const,
      }));
    }
  }
}

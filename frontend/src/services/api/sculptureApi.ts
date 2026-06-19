import type { SculptureAnalysis } from '../../types/sculpture';
import { apiClient } from './client';

import { mockAnalyses } from '../mock/mockAnalysis';

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export class SculptureApi {
  static async getAll(): Promise<SculptureAnalysis[]> {
    await delay(800);
    return mockAnalyses;
  }

  static async getById(id: string): Promise<SculptureAnalysis | undefined> {
    await delay(500);
    if (id === mockAnalyses[0].id) return mockAnalyses[0];
    return undefined;
  }

  static async analyze(file: File): Promise<SculptureAnalysis> {
    const formData = new FormData();
    formData.append('file', file);
    
    // Ensure we hit the correct endpoint with raw fetch to handle FormData boundaries
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/sculpture/analyze`, {
      method: 'POST',
      body: formData,
      // Do not set Content-Type, fetch will automatically set it with the boundary
    });
    
    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }
    
    return await response.json();
  }
}

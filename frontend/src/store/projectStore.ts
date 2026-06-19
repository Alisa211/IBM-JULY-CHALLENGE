import { create } from 'zustand';

import type { Project } from '../types/project';

interface ProjectState {
  currentProject: Project | null;
  projects: Project[];
  setCurrentProject: (project: Project | null) => void;
  setProjects: (projects: Project[]) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: {
    id: '1',
    name: 'AI Creative Director',
    description: 'Main project workspace',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    imageCount: 0,
    analysisCount: 0,
  },
  projects: [],
  setCurrentProject: (project) => set({ currentProject: project }),
  setProjects: (projects) => set({ projects }),
}));

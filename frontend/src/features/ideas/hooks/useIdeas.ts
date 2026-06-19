import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { IdeaApi } from '../../../services/api/ideaApi';
import type { IdeaBrief } from '../../../types/idea';

export function useIdeaList() {
  return useQuery({ 
    queryKey: ['ideas', 'list'], 
    queryFn: () => IdeaApi.getAll() 
  });
}

export function useIdeaById(id: string) {
  return useQuery({ 
    queryKey: ['ideas', id], 
    queryFn: () => IdeaApi.getById(id), 
    enabled: !!id 
  });
}

export function useGenerateIdeas() {
  const qc = useQueryClient();
  return useMutation({ 
    mutationFn: (brief: IdeaBrief) => IdeaApi.generate(brief), 
    onSuccess: () => qc.invalidateQueries({ queryKey: ['ideas'] }) 
  });
}

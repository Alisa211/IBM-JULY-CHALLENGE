import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { CritiqueApi } from '../../../services/api/critiqueApi';

export function useCritiqueList() {
  return useQuery({ 
    queryKey: ['critiques', 'list'], 
    queryFn: () => CritiqueApi.getAll() 
  });
}

export function useCritiqueByIdeaId(ideaId: string | null) {
  return useQuery({ 
    queryKey: ['critiques', ideaId], 
    queryFn: () => ideaId ? CritiqueApi.getByIdeaId(ideaId) : Promise.resolve([]), 
    enabled: !!ideaId 
  });
}

export function useCritiqueIdea() {
  const qc = useQueryClient();
  return useMutation({ 
    mutationFn: (ideaId: string) => CritiqueApi.critiqueIdea(ideaId), 
    onSuccess: () => qc.invalidateQueries({ queryKey: ['critiques'] }) 
  });
}

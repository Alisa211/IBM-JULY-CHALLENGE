import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { StyleApi } from '../../../services/api/styleApi';

export function useStyleDNAList() {
  return useQuery({ 
    queryKey: ['styleDNA', 'list'], 
    queryFn: () => StyleApi.getAll() 
  });
}

export function useStyleDNAById(id: string) {
  return useQuery({ 
    queryKey: ['styleDNA', id], 
    queryFn: () => StyleApi.getById(id), 
    enabled: !!id 
  });
}

export function useAnalyzeStyle() {
  const qc = useQueryClient();
  return useMutation({ 
    mutationFn: (file: File) => StyleApi.analyze(file), 
    onSuccess: () => qc.invalidateQueries({ queryKey: ['styleDNA'] }) 
  });
}

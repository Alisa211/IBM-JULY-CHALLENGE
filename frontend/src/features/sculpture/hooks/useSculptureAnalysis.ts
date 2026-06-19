import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { SculptureApi } from '../../../services/api/sculptureApi';

export function useAnalysisList() {
  return useQuery({ 
    queryKey: ['sculpture', 'list'], 
    queryFn: () => SculptureApi.getAll() 
  });
}

export function useAnalysisById(id: string) {
  return useQuery({ 
    queryKey: ['sculpture', id], 
    queryFn: () => SculptureApi.getById(id), 
    enabled: !!id 
  });
}

export function useAnalyzeSculpture() {
  const qc = useQueryClient();
  return useMutation({ 
    mutationFn: (file: File) => SculptureApi.analyze(file), 
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sculpture'] }) 
  });
}

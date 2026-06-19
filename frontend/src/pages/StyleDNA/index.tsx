import { Dna } from 'lucide-react';
import { useStyleDNAList } from '../../features/styleDNA/hooks/useStyleDNA';
import { StyleUploadPanel } from '../../features/styleDNA/components/StyleUploadPanel';
import { StyleTraitsCard } from '../../features/styleDNA/components/StyleTraitsCard';
import { StyleVectorCard } from '../../features/styleDNA/components/StyleVectorCard';
import { SimilarityList } from '../../features/styleDNA/components/SimilarityList';
import { DNAHistory } from '../../features/styleDNA/components/DNAHistory';
import { Skeleton } from '../../components/ui/Skeleton';
import { ErrorState } from '../../components/ui/ErrorState';
import { EmptyState } from '../../components/ui/EmptyState';

// mock similarities for demonstration
import { mockSimilarities } from '../../services/mock/mockStyleDNA';

export default function StyleDNA() {
  const { data: entries, isLoading, isError, refetch } = useStyleDNAList();

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-surface-900 dark:text-white mb-2">
          <span className="gradient-text">Style DNA</span> Analysis
        </h1>
        <p className="text-surface-500 dark:text-surface-400">
          Extract, quantify, and visualize aesthetic traits from reference imagery.
        </p>
      </header>

      <StyleUploadPanel />

      {isLoading && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          <Skeleton className="h-[400px] w-full rounded-xl" />
          <Skeleton className="h-[400px] w-full rounded-xl" />
          <Skeleton className="h-[300px] w-full rounded-xl lg:col-span-2" />
        </div>
      )}

      {isError && (
        <div className="mt-8">
          <ErrorState 
            title="Failed to load Style DNA" 
            message="There was an error communicating with the analysis service."
            onRetry={refetch} 
          />
        </div>
      )}

      {!isLoading && !isError && (!entries || entries.length === 0) && (
        <div className="mt-12 bg-white dark:bg-surface-800 rounded-xl border border-dashed border-surface-300 dark:border-surface-700 p-8">
          <EmptyState
            icon={Dna}
            title="No style analyses yet"
            description="Upload a style reference image above to extract your first Style DNA profile."
          />
        </div>
      )}

      {!isLoading && !isError && entries && entries.length > 0 && (
        <div className="mt-8 space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <StyleTraitsCard traits={entries[0].traits} />
            <StyleVectorCard />
          </div>
          
          <SimilarityList similarities={mockSimilarities} />
          
          <DNAHistory entries={entries} />
        </div>
      )}
    </div>
  );
}

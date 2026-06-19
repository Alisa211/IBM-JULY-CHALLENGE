import { useState } from 'react';
import { ScanSearch } from 'lucide-react';
import { ImageUploader } from '../../features/sculpture/components/ImageUploader';
import { ImagePreview } from '../../features/sculpture/components/ImagePreview';
import { AnalysisPanel } from '../../features/sculpture/components/AnalysisPanel';
import { TagCloud } from '../../features/sculpture/components/TagCloud';
import { MetadataPanel } from '../../features/sculpture/components/MetadataPanel';
import { useAssetStore } from '../../store/assetStore';
import { Skeleton } from '../../components/ui/Skeleton';
import { EmptyState } from '../../components/ui/EmptyState';

export default function SculptureAnalyzer() {
  const [currentAnalysis, setCurrentAnalysis] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { assets } = useAssetStore();
  
  // For demo, we just grab the last uploaded asset if it exists
  const assetsArray = Array.from(assets.values());
  const latestAsset = assetsArray.length > 0 ? assetsArray[assetsArray.length - 1] : null;

  return (
    <div className="max-w-7xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-surface-900 dark:text-white mb-2">
          Sculpture <span className="gradient-text">Analyzer</span>
        </h1>
        <p className="text-surface-500 dark:text-surface-400">
          Upload images of sculptures to identify materials, periods, and semantic iconography.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Upload & Preview */}
        <div className="lg:col-span-5 space-y-6">
          <ImageUploader 
            onUploadStart={() => setIsAnalyzing(true)}
            onAnalysisComplete={(data) => {
              setCurrentAnalysis(data);
              setIsAnalyzing(false);
            }} 
          />
          {latestAsset && (
            <ImagePreview 
              imageUrl={latestAsset.previewUrl} 
              fileName={latestAsset.file.name} 
            />
          )}
        </div>

        {/* Right Column: Analysis Results */}
        <div className="lg:col-span-7">
          {isAnalyzing ? (
            <div className="space-y-6">
              <Skeleton className="h-[300px] w-full rounded-xl" />
              <Skeleton className="h-[200px] w-full rounded-xl" />
              <Skeleton className="h-[150px] w-full rounded-xl" />
            </div>
          ) : currentAnalysis ? (
            <div className="space-y-6 animate-fade-in">
              <AnalysisPanel analysis={currentAnalysis} />
              <TagCloud 
                iconography={currentAnalysis.iconography || []} 
                motifs={currentAnalysis.motifs || []} 
              />
              <MetadataPanel metadata={currentAnalysis.metadata || {}} />
            </div>
          ) : (
            <div className="h-full min-h-[400px] flex items-center justify-center bg-white dark:bg-surface-800 rounded-xl border border-dashed border-surface-300 dark:border-surface-700 p-8">
              <EmptyState
                icon={ScanSearch}
                title="Waiting for analysis"
                description="Upload an image to the left to see the AI breakdown."
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

import { UploadCloud } from 'lucide-react';
import { useCallback, useState } from 'react';
import { Card } from '../../../components/ui/Card';
import { cn } from '../../../utils/cn';
import { useAssetStore } from '../../../store/assetStore';
import { useAnalyzeSculpture } from '../hooks/useSculptureAnalysis';

export function ImageUploader({ 
  onAnalysisComplete,
  onUploadStart 
}: { 
  onAnalysisComplete?: (data: any) => void;
  onUploadStart?: () => void;
}) {
  const [isDragging, setIsDragging] = useState(false);
  const { addAsset } = useAssetStore();
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const { mutateAsync: analyzeSculpture } = useAnalyzeSculpture();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const simulateUpload = async (file: File) => {
    if (onUploadStart) onUploadStart();
    setIsUploading(true);
    setProgress(30);
    try {
      const previewUrl = URL.createObjectURL(file);
      addAsset({ id: file.name, file, fileName: file.name, fileSize: file.size, previewUrl, uploadedAt: new Date().toISOString() });
      
      const analysis = await analyzeSculpture(file);
      setProgress(100);
      if (onAnalysisComplete) {
        onAnalysisComplete(analysis);
      }
    } catch (error) {
      console.error('Failed to analyze sculpture:', error);
    } finally {
      setIsUploading(false);
      setProgress(0);
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) simulateUpload(file);
    }
  }, [addAsset, analyzeSculpture, onAnalysisComplete]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (file.type.startsWith('image/')) simulateUpload(file);
    }
  };

  return (
    <Card className="p-6">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative flex flex-col items-center justify-center min-h-[240px] border-2 border-dashed rounded-xl transition-all duration-200",
          isDragging 
            ? "border-primary-500 bg-primary-50/50 dark:bg-primary-900/10" 
            : "border-surface-300 dark:border-surface-700 bg-surface-50 dark:bg-surface-800/50",
          isUploading && "opacity-50 pointer-events-none"
        )}
      >
        <input
          type="file"
          accept="image/*"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={handleFileSelect}
          disabled={isUploading}
        />
        
        <div className="flex flex-col items-center text-center gap-4 pointer-events-none">
          <div className="w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
            <UploadCloud className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-surface-900 dark:text-white">
              Upload Sculpture Image
            </h3>
            <p className="text-sm text-surface-500 dark:text-surface-400 mt-2 max-w-xs mx-auto">
              Drag and drop an image of a sculpture, or click to browse. High resolution images work best.
            </p>
          </div>
        </div>

        {isUploading && (
          <div className="absolute inset-x-8 bottom-8">
            <div className="flex justify-between text-xs text-surface-500 mb-2">
              <span>Uploading...</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full h-2 bg-surface-200 dark:bg-surface-700 rounded-full overflow-hidden">
              <div 
                className="h-full bg-primary-500 transition-all duration-200"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
      </div>
    </Card>
  );
}

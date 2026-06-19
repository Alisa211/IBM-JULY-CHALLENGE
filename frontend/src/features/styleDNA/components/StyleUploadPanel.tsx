import { UploadCloud, Image as ImageIcon } from 'lucide-react';
import { useCallback, useState } from 'react';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { cn } from '../../../utils/cn';
import { useAnalyzeStyle } from '../hooks/useStyleDNA';

export function StyleUploadPanel() {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { mutate: analyze, isPending } = useAnalyzeStyle();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) setSelectedFile(file);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (file.type.startsWith('image/')) setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      analyze(selectedFile, {
        onSuccess: () => setSelectedFile(null)
      });
    }
  };

  return (
    <Card className="p-6">
      <div className="flex flex-col gap-4">
        <div>
          <h3 className="text-lg font-semibold text-surface-900 dark:text-white">Style Reference</h3>
          <p className="text-sm text-surface-500 dark:text-surface-400">Upload a sculpture image to extract its style DNA.</p>
        </div>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            "relative flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-xl transition-all duration-200",
            isDragging 
              ? "border-primary-500 bg-primary-50/50 dark:bg-primary-900/10" 
              : "border-surface-300 dark:border-surface-700 bg-surface-50 dark:bg-surface-800/50",
            isPending && "opacity-50 pointer-events-none"
          )}
        >
          <input
            type="file"
            accept="image/*"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleFileSelect}
            disabled={isPending}
          />
          
          <div className="flex flex-col items-center text-center gap-3 pointer-events-none">
            <div className="w-12 h-12 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
              <UploadCloud className="w-6 h-6" />
            </div>
            <div>
              <p className="font-medium text-surface-900 dark:text-white">
                Drop your image here or click to browse
              </p>
              <p className="text-sm text-surface-500 dark:text-surface-400 mt-1">
                Supports JPG, PNG up to 10MB
              </p>
            </div>
          </div>
        </div>

        {selectedFile && (
          <div className="flex items-center justify-between p-3 rounded-lg border border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800/50">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="w-10 h-10 rounded bg-surface-200 dark:bg-surface-700 flex items-center justify-center shrink-0">
                <ImageIcon className="w-5 h-5 text-surface-500" />
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-surface-900 dark:text-white truncate">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-surface-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button 
              variant="primary" 
              size="sm" 
              onClick={handleUpload}
              isLoading={isPending}
            >
              Extract DNA
            </Button>
          </div>
        )}
      </div>
    </Card>
  );
}

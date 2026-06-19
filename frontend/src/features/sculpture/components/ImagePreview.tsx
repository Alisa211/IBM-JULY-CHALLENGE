import { ZoomIn } from 'lucide-react';

interface ImagePreviewProps {
  imageUrl: string;
  fileName: string;
}

export function ImagePreview({ imageUrl, fileName }: ImagePreviewProps) {
  return (
    <div className="group relative w-full mt-6 animate-fade-in">
      <div className="relative rounded-xl overflow-hidden shadow-lg border border-surface-200 dark:border-surface-700 bg-surface-100 dark:bg-surface-800">
        <img 
          src={imageUrl} 
          alt={fileName}
          className="w-full h-auto max-h-[500px] object-contain"
        />
        <div className="absolute inset-0 bg-surface-900/0 group-hover:bg-surface-900/20 transition-colors duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
          <button className="bg-white/90 dark:bg-surface-900/90 text-surface-900 dark:text-white p-3 rounded-full shadow-xl hover:scale-110 transition-transform">
            <ZoomIn className="w-6 h-6" />
          </button>
        </div>
      </div>
      <p className="text-center text-sm font-medium text-surface-500 mt-3 truncate px-4">
        {fileName}
      </p>
    </div>
  );
}

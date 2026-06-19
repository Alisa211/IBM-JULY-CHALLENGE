import { create } from 'zustand';

export interface UploadedAsset {
  id: string;
  file: File;
  fileName: string;
  fileSize: number;
  previewUrl: string;
  uploadedAt: string;
}

interface AssetState {
  assets: UploadedAsset[];
  currentAsset: UploadedAsset | null;
  addAsset: (asset: UploadedAsset) => void;
  setCurrentAsset: (asset: UploadedAsset | null) => void;
  removeAsset: (id: string) => void;
  clearAssets: () => void;
}

export const useAssetStore = create<AssetState>((set) => ({
  assets: [],
  currentAsset: null,
  addAsset: (asset) =>
    set((state) => ({
      assets: [...state.assets, asset],
      currentAsset: asset,
    })),
  setCurrentAsset: (asset) => set({ currentAsset: asset }),
  removeAsset: (id) =>
    set((state) => ({
      assets: state.assets.filter((a) => a.id !== id),
      currentAsset: state.currentAsset?.id === id ? null : state.currentAsset,
    })),
  clearAssets: () => set({ assets: [], currentAsset: null }),
}));

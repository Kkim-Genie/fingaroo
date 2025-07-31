import { UserAsset } from "@/app/types";
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface UserAssetState {
  data: UserAsset[];
  set: (data: UserAsset[]) => void;
  add: (userAsset: UserAsset) => void;
  update: (id: string, userAsset: UserAsset) => void;
  remove: (id: string) => void;
  reset: () => void;
}

export const initialUserAssets: UserAsset[] = [];

const useUserAssetStore = create(
  persist<UserAssetState>(
    (set) => ({
      data: initialUserAssets,
      set: (data: UserAsset[]) => set((state) => ({ ...state, data })),
      add: (userAsset: UserAsset) =>
        set((state) => ({
          ...state,
          data: [...state.data, userAsset],
        })),
      update: (id: string, userAsset: UserAsset) =>
        set((state) => ({
          ...state,
          data: state.data.map((item) => (item.id === id ? userAsset : item)),
        })),
      remove: (id: string) =>
        set((state) => ({
          ...state,
          data: state.data.filter((item) => item.id !== id),
        })),
      reset: () =>
        set((state) => ({
          ...state,
          data: initialUserAssets,
        })),
    }),
    {
      name: "fingaroo_user_assets",
    }
  )
);

export default useUserAssetStore;

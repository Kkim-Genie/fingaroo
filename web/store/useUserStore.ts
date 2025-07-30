import { User } from "@/app/types";
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface UserState {
  data: User;
  set: (data: User) => void;
  update: <K extends keyof User>(key: K, value: User[K]) => void;
  reset: () => void;
}

export const initialUser: User = {
  id: "",
  name: "",
  email: "",
  gender: "",
  birthyear: 0,
};

const useUserStore = create(
  persist<UserState>(
    (set) => ({
      data: initialUser,
      set: (data: User) => set((state) => ({ ...state, data })),
      update: <K extends keyof User>(key: K, value: User[K]) =>
        set((state) => {
          const newData = { ...state.data };
          newData[key] = value;
          return { ...state, data: newData };
        }),
      reset: () =>
        set((state) => {
          return { ...state, data: initialUser };
        }),
    }),
    {
      name: "fingaroo_user",
    }
  )
);

export default useUserStore;

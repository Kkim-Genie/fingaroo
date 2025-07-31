import { InvestLog } from "@/app/types";
import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface InvestLogState {
  data: InvestLog[];
  set: (data: InvestLog[]) => void;
  add: (investLog: InvestLog) => void;
  update: (id: string, investLog: InvestLog) => void;
  remove: (id: string) => void;
  reset: () => void;
}

export const initialInvestLogs: InvestLog[] = [];

const useInvestLogStore = create(
  persist<InvestLogState>(
    (set) => ({
      data: initialInvestLogs,
      set: (data: InvestLog[]) => set((state) => ({ ...state, data })),
      add: (investLog: InvestLog) =>
        set((state) => ({
          ...state,
          data: [...state.data, investLog],
        })),
      update: (id: string, investLog: InvestLog) =>
        set((state) => ({
          ...state,
          data: state.data.map((item) => (item.id === id ? investLog : item)),
        })),
      remove: (id: string) =>
        set((state) => ({
          ...state,
          data: state.data.filter((item) => item.id !== id),
        })),
      reset: () =>
        set((state) => ({
          ...state,
          data: initialInvestLogs,
        })),
    }),
    {
      name: "fingaroo_invest_logs",
    }
  )
);

export default useInvestLogStore;

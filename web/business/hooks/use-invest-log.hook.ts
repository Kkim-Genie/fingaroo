"use client";

import { useState, useCallback } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { InvestLog } from "@/app/types";
import useInvestLogStore from "@/store/useInvestLogStore";

export function useInvestLog() {
  const { data: investLogs, set: setInvestLogs } = useInvestLogStore();
  const [loading, setLoading] = useState(false);
  const [showInvestLogModal, setShowInvestLogModal] = useState(false);
  const [editingInvestLog, setEditingInvestLog] = useState<InvestLog | null>(
    null
  );

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  const getTokens = () => {
    const accessToken = Cookies.get("accessToken");
    const refreshToken = Cookies.get("refreshToken");
    return { accessToken, refreshToken };
  };

  const fetchInvestLogs = useCallback(async () => {
    try {
      setLoading(true);
      const { accessToken, refreshToken } = getTokens();
      const response = await axios.get(`${API_URL}/invest_log/`, {
        params: { access_token: accessToken, refresh_token: refreshToken },
      });
      setInvestLogs(response.data);
    } catch (error) {
      console.error("Failed to fetch invest logs:", error);
    } finally {
      setLoading(false);
    }
  }, [API_URL, setInvestLogs]);

  const handleInvestLogSubmit = async (data: Record<string, unknown>) => {
    try {
      const { accessToken, refreshToken } = getTokens();
      if ("invest_log" in data) {
        // Update case
        await axios.put(`${API_URL}/invest_log/`, {
          ...data,
          access_token: accessToken,
          refresh_token: refreshToken,
        });
      } else {
        // Create case
        await axios.post(`${API_URL}/invest_log/`, {
          ...data,
          access_token: accessToken,
          refresh_token: refreshToken,
        });
      }
      fetchInvestLogs();
      setShowInvestLogModal(false);
      setEditingInvestLog(null);
    } catch (error) {
      console.error("Failed to submit invest log:", error);
    }
  };

  const deleteInvestLog = async (investLogId: string) => {
    if (confirm("정말로 삭제하시겠습니까?")) {
      try {
        const { accessToken, refreshToken } = getTokens();
        await axios.delete(`${API_URL}/invest_log/`, {
          data: {
            invest_log_id: investLogId,
            access_token: accessToken,
            refresh_token: refreshToken,
          },
        });
        fetchInvestLogs();
      } catch (error) {
        console.error("Failed to delete invest log:", error);
      }
    }
  };

  const openInvestLogModal = (investLog?: InvestLog) => {
    setEditingInvestLog(investLog || null);
    setShowInvestLogModal(true);
  };

  const closeInvestLogModal = () => {
    setShowInvestLogModal(false);
    setEditingInvestLog(null);
  };

  return {
    // States
    investLogs,
    loading,
    showInvestLogModal,
    editingInvestLog,

    // Actions
    fetchInvestLogs,
    handleInvestLogSubmit,
    deleteInvestLog,
    openInvestLogModal,
    closeInvestLogModal,
  };
}

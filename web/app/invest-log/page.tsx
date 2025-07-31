"use client";

import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import dayjs from "dayjs";
import { InvestLog, UserAsset } from "../types";
import InvestLogModal from "../../components/InvestLogModal";
import UserAssetModal from "../../components/UserAssetModal";
import { cn } from "@/utils/utlis";

const InvestLogPage = () => {
  const [activeTab, setActiveTab] = useState<"invest_log" | "user_asset">(
    "invest_log"
  );
  const [investLogs, setInvestLogs] = useState<InvestLog[]>([]);
  const [userAssets, setUserAssets] = useState<UserAsset[]>([]);
  const [loading, setLoading] = useState(false);
  const [showInvestLogModal, setShowInvestLogModal] = useState(false);
  const [showUserAssetModal, setShowUserAssetModal] = useState(false);
  const [editingInvestLog, setEditingInvestLog] = useState<InvestLog | null>(
    null
  );
  const [editingUserAsset, setEditingUserAsset] = useState<UserAsset | null>(
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
  }, [API_URL]);

  const fetchUserAssets = useCallback(async () => {
    try {
      setLoading(true);
      const { accessToken, refreshToken } = getTokens();
      const response = await axios.get(`${API_URL}/invest_log/user_asset/`, {
        params: { access_token: accessToken, refresh_token: refreshToken },
      });
      setUserAssets(response.data);
    } catch (error) {
      console.error("Failed to fetch user assets:", error);
    } finally {
      setLoading(false);
    }
  }, [API_URL]);

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

  const handleUserAssetSubmit = async (data: Record<string, unknown>) => {
    try {
      const { accessToken, refreshToken } = getTokens();
      if ("user_asset" in data) {
        // Update case
        await axios.put(`${API_URL}/invest_log/user_asset/`, {
          ...data,
          access_token: accessToken,
          refresh_token: refreshToken,
        });
      } else {
        // Create case
        await axios.post(`${API_URL}/invest_log/user_asset/`, {
          ...data,
          access_token: accessToken,
          refresh_token: refreshToken,
        });
      }
      fetchUserAssets();
      setShowUserAssetModal(false);
      setEditingUserAsset(null);
    } catch (error) {
      console.error("Failed to submit user asset:", error);
    }
  };

  const deleteUserAsset = async (assetId: string) => {
    if (confirm("정말로 삭제하시겠습니까?")) {
      try {
        const { accessToken, refreshToken } = getTokens();
        await axios.delete(`${API_URL}/invest_log/user_asset/`, {
          data: {
            asset_id: assetId,
            access_token: accessToken,
            refresh_token: refreshToken,
          },
        });
        fetchUserAssets();
      } catch (error) {
        console.error("Failed to delete user asset:", error);
      }
    }
  };

  const openInvestLogModal = (investLog?: InvestLog) => {
    setEditingInvestLog(investLog || null);
    setShowInvestLogModal(true);
  };

  const openUserAssetModal = (userAsset?: UserAsset) => {
    setEditingUserAsset(userAsset || null);
    setShowUserAssetModal(true);
  };

  useEffect(() => {
    if (activeTab === "invest_log") {
      fetchInvestLogs();
    } else {
      fetchUserAssets();
    }
  }, [activeTab, fetchInvestLogs, fetchUserAssets]);

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <h1 className="text-3xl font-bold mb-8">투자 관리</h1>

      {/* Tab Navigation */}
      <div className="flex border-b mb-6">
        <button
          className={`px-6 py-3 font-medium ${
            activeTab === "invest_log"
              ? "border-b-2 border-blue-500 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
          onClick={() => setActiveTab("invest_log")}
        >
          투자 일지
        </button>
        <button
          className={`px-6 py-3 font-medium ${
            activeTab === "user_asset"
              ? "border-b-2 border-blue-500 text-blue-600"
              : "text-gray-500 hover:text-gray-700"
          }`}
          onClick={() => setActiveTab("user_asset")}
        >
          보유 자산
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>
      )}

      {/* Content */}
      {!loading && activeTab === "invest_log" && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">투자 일지</h2>
            <button
              onClick={() => openInvestLogModal()}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              일지 추가
            </button>
          </div>
          <InvestLogTable
            investLogs={investLogs}
            onEdit={openInvestLogModal}
            onDelete={deleteInvestLog}
          />
        </div>
      )}

      {!loading && activeTab === "user_asset" && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">보유 자산</h2>
            <button
              onClick={() => openUserAssetModal()}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              자산 추가
            </button>
          </div>
          <UserAssetTable
            userAssets={userAssets}
            onEdit={openUserAssetModal}
            onDelete={deleteUserAsset}
          />
        </div>
      )}

      {/* Modals */}
      {showInvestLogModal && (
        <InvestLogModal
          investLog={editingInvestLog}
          onSubmit={handleInvestLogSubmit}
          onClose={() => {
            setShowInvestLogModal(false);
            setEditingInvestLog(null);
          }}
        />
      )}

      {showUserAssetModal && (
        <UserAssetModal
          userAsset={editingUserAsset}
          onSubmit={handleUserAssetSubmit}
          onClose={() => {
            setShowUserAssetModal(false);
            setEditingUserAsset(null);
          }}
        />
      )}
    </div>
  );
};

const InvestLogTable = ({
  investLogs,
  onEdit,
  onDelete,
}: {
  investLogs: InvestLog[];
  onEdit: (investLog: InvestLog) => void;
  onDelete: (id: string) => void;
}) => {
  // 날짜 기준으로 최신 데이터가 위로 오도록 정렬 (내림차순)
  const sortedInvestLogs = [...investLogs].sort((a, b) => {
    return dayjs(b.date).valueOf() - dayjs(a.date).valueOf();
  });

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              날짜
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              종목
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              구분
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              가격
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              수량
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              손익
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              수익률
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              액션
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {sortedInvestLogs.map((log) => (
            <tr key={log.id} className="hover:bg-gray-50">
              <td className="px-4 py-2 text-sm">{log.date}</td>
              <td className="px-4 py-2 text-sm">
                <div>
                  <div className="font-medium">{log.stock_name}</div>
                  <div className="text-gray-500">{log.stock_code}</div>
                </div>
              </td>
              <td className="px-4 py-2 text-sm">
                <span
                  className={`px-2 py-1 text-xs rounded ${
                    log.action === "매수"
                      ? "bg-red-100 text-red-800"
                      : "bg-blue-100 text-blue-800"
                  }`}
                >
                  {log.action}
                </span>
              </td>
              <td className="px-4 py-2 text-sm">
                {log.price.toLocaleString()}원
              </td>
              <td className="px-4 py-2 text-sm">
                {log.amount.toLocaleString()}주
              </td>
              <td className="px-4 py-2 text-sm">
                <span
                  className={cn({
                    "text-red-600": log.profit >= 0,
                    "text-blue-600": log.profit < 0,
                    "text-black": log.action === "매수",
                  })}
                >
                  {log.action === "매수"
                    ? "-"
                    : `${log.profit.toLocaleString()}원`}
                </span>
              </td>
              <td className="px-4 py-2 text-sm">
                <span
                  className={cn({
                    "text-red-600": log.profit_ratio >= 0,
                    "text-blue-600": log.profit_ratio < 0,
                    "text-black": log.action === "매수",
                  })}
                >
                  {log.action === "매수"
                    ? "-"
                    : `${log.profit_ratio.toFixed(2)}%`}
                </span>
              </td>
              <td className="px-4 py-2 text-sm">
                <button
                  onClick={() => onEdit(log)}
                  className="text-blue-600 hover:text-blue-800 mr-2"
                >
                  수정
                </button>
                <button
                  onClick={() => onDelete(log.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  삭제
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const UserAssetTable = ({
  userAssets,
  onEdit,
  onDelete,
}: {
  userAssets: UserAsset[];
  onEdit: (userAsset: UserAsset) => void;
  onDelete: (id: string) => void;
}) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              종목
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              보유 수량
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
              액션
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {userAssets.map((asset) => (
            <tr key={asset.id} className="hover:bg-gray-50">
              <td className="px-4 py-2 text-sm">
                <div>
                  <div className="font-medium">{asset.stock_name}</div>
                  {asset.stock_code !== "0" && (
                    <div className="text-gray-500">{asset.stock_code}</div>
                  )}
                </div>
              </td>
              <td className="px-4 py-2 text-sm">
                {asset.amount.toLocaleString()}
                {asset.stock_code === "0" ? "원" : "주"}
              </td>
              <td className="px-4 py-2 text-sm">
                <button
                  onClick={() => onEdit(asset)}
                  className="text-blue-600 hover:text-blue-800 mr-2"
                >
                  수정
                </button>
                <button
                  onClick={() => onDelete(asset.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  삭제
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InvestLogPage;

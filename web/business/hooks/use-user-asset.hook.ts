"use client";

import { useState, useCallback } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { UserAsset } from "@/app/types";
import useUserAssetStore from "@/store/useUserAssetStore";

export function useUserAsset() {
  const { data: userAssets, set: setUserAssets } = useUserAssetStore();
  const [loading, setLoading] = useState(false);
  const [showUserAssetModal, setShowUserAssetModal] = useState(false);
  const [editingUserAsset, setEditingUserAsset] = useState<UserAsset | null>(
    null
  );

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  const getTokens = () => {
    const accessToken = Cookies.get("accessToken");
    const refreshToken = Cookies.get("refreshToken");
    return { accessToken, refreshToken };
  };

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
  }, [API_URL, setUserAssets]);

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

  const openUserAssetModal = (userAsset?: UserAsset) => {
    setEditingUserAsset(userAsset || null);
    setShowUserAssetModal(true);
  };

  const closeUserAssetModal = () => {
    setShowUserAssetModal(false);
    setEditingUserAsset(null);
  };

  return {
    // States
    userAssets,
    loading,
    showUserAssetModal,
    editingUserAsset,

    // Actions
    fetchUserAssets,
    handleUserAssetSubmit,
    deleteUserAsset,
    openUserAssetModal,
    closeUserAssetModal,
  };
}

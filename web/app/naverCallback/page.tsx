"use client";

import { useRouter, useSearchParams } from "next/navigation";
import React, { useEffect, useCallback, Suspense } from "react";
import { API_URL } from "../../utils/consts";
import axios from "axios";
import Cookies from "js-cookie";
import useCustomStore from "@/store/useCustomStore";
import useUserStore from "@/store/useUserStore";
import { User } from "../types";

const NaverCallbackContent = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const userStore = useCustomStore(useUserStore, (state) => state);

  const fetchUserData = useCallback(async () => {
    if (userStore === undefined || userStore.data.id !== "") {
      return;
    }
    try {
      const code = searchParams.get("code");
      const res = await axios.post(`${API_URL}/user/login`, {
        code,
      });

      const user: User = {
        id: res.data.user.id,
        name: res.data.user.name,
        email: res.data.user.email,
        gender: res.data.user.gender,
        birthyear: res.data.user.birthyear,
      };

      userStore.set(user);

      // Store tokens in cookies
      if (res.data.access_token) {
        Cookies.set("accessToken", res.data.access_token, {
          expires: 7, // 7 days
          secure: true,
          sameSite: "strict",
        });
      }

      if (res.data.refresh_token) {
        Cookies.set("refreshToken", res.data.refresh_token, {
          expires: 30, // 30 days
          secure: true,
          sameSite: "strict",
        });
      }

      // Redirect to main page after successful login
      router.push("/");
    } catch (error) {
      console.error("Login failed:", error);
      // Optionally redirect to error page or show error message
      router.push("/");
    }
  }, [userStore, searchParams, router]);

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
        <p className="mt-4 text-gray-600">로그인 처리 중...</p>
      </div>
    </div>
  );
};

const NaverCallback = () => {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
            <p className="mt-4 text-gray-600">로딩 중...</p>
          </div>
        </div>
      }
    >
      <NaverCallbackContent />
    </Suspense>
  );
};

export default NaverCallback;

"use client";

import useCustomStore from "@/store/useCustomStore";
import useUserStore from "@/store/useUserStore";
import Cookies from "js-cookie";
import React from "react";

export default function ChatHeader() {
  const userStore = useCustomStore(useUserStore, (state) => state);

  const NaverLogin = () => {
    const currentUrl = window.location.href;
    const REDIRECT_URI = `${currentUrl}naverCallback`;
    const STATE = "RANDOMSTATE";
    const NAVER_AUTH_URL = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${process.env.NEXT_PUBLIC_NAVER_CLIENT_ID}&state=${STATE}&redirect_uri=${REDIRECT_URI}`;

    window.location.href = NAVER_AUTH_URL;
  };

  const Logout = () => {
    userStore?.reset();
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");
  };

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
          <svg
            className="w-6 h-6 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
        </div>
        <div>
          <h1 className="text-lg font-semibold text-gray-900">AI 어시스턴트</h1>
          <p className="text-sm text-gray-500">무엇이든 물어보세요!</p>
        </div>
        <div className="ml-auto flex items-center gap-2">
          {userStore?.data.id === "" ? (
            <button
              className="bg-[#03c75a] text-white px-4 py-2 rounded-md font-bold"
              onClick={NaverLogin}
            >
              네이버 로그인하기
            </button>
          ) : (
            <button onClick={Logout}>Logout</button>
          )}
        </div>
      </div>
    </div>
  );
}

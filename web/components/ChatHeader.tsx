"use client";

import useCustomStore from "@/store/useCustomStore";
import useUserStore from "@/store/useUserStore";
import Cookies from "js-cookie";
import Image from "next/image";
import React from "react";
import logo from "@/assets/fingaroo_logo.png";
import { Avatar, Menu } from "@mantine/core";
import { useRouter } from "next/navigation";

export default function ChatHeader() {
  const userStore = useCustomStore(useUserStore, (state) => state);
  const router = useRouter();

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

  const moveToInvestLog = () => {
    router.push("/invest-log");
  };

  const moveToHome = () => {
    router.push("/");
  };

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center gap-3">
        <div
          className="w-12 h-12 rounded-full flex items-center justify-center cursor-pointer"
          onClick={moveToHome}
        >
          <Image className="rounded-full" src={logo} alt="logo" />
        </div>
        <div className="flex flex-col -gap-1">
          <h1
            className="text-lg font-bold text-[#FFA162]"
            style={{ fontFamily: "Batang, serif" }}
          >
            Fingaroo
          </h1>
          <p
            className="text-sm text-[#FFA060] -mt-1"
            style={{ fontFamily: "Batang, serif" }}
          >
            your finance buddy
          </p>
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
            <Menu shadow="md" width={280} position="bottom-end" offset={5}>
              <Menu.Target>
                <Avatar
                  className="cursor-pointer hover:shadow-lg transition-shadow duration-200"
                  size="md"
                  color="orange"
                />
              </Menu.Target>
              <Menu.Dropdown className="border border-gray-200 rounded-lg shadow-xl">
                {/* User Info Section */}
                <div className="px-4 py-3 border-b border-gray-100">
                  <div className="flex items-center gap-3">
                    <Avatar size="lg" color="orange" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-gray-900 truncate">
                        {userStore?.data.name || "사용자"}
                      </p>
                      <p className="text-xs text-gray-500 truncate">
                        {userStore?.data.email}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Menu Items */}
                <div className="py-1">
                  <Menu.Item
                    className="hover:bg-gray-50 transition-colors duration-150"
                    onClick={moveToInvestLog}
                  >
                    <div className="flex items-center gap-3 px-2 py-1">
                      <span className="text-gray-500">📊</span>
                      <span className="text-sm text-gray-700">매매일지</span>
                    </div>
                  </Menu.Item>

                  <Menu.Item
                    className="hover:bg-gray-50 transition-colors duration-150"
                    onClick={() => {
                      // Add profile edit functionality here if needed
                    }}
                  >
                    <div className="flex items-center gap-3 px-2 py-1">
                      <span className="text-gray-500">👤</span>
                      <span className="text-sm text-gray-700">프로필 설정</span>
                    </div>
                  </Menu.Item>

                  <Menu.Item
                    className="hover:bg-gray-50 transition-colors duration-150"
                    onClick={() => {
                      // Add preferences functionality here if needed
                    }}
                  >
                    <div className="flex items-center gap-3 px-2 py-1">
                      <span className="text-gray-500">⚙️</span>
                      <span className="text-sm text-gray-700">환경설정</span>
                    </div>
                  </Menu.Item>

                  <Menu.Divider />

                  <Menu.Item
                    className="hover:bg-red-50 transition-colors duration-150"
                    onClick={Logout}
                  >
                    <div className="flex items-center gap-3 px-2 py-1">
                      <span className="text-red-500">🚪</span>
                      <span className="text-sm text-red-600 font-medium">
                        로그아웃
                      </span>
                    </div>
                  </Menu.Item>
                </div>
              </Menu.Dropdown>
            </Menu>
          )}
        </div>
      </div>
    </div>
  );
}

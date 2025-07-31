import React, { useState } from "react";
import { UserAsset } from "../app/types";

interface UserAssetModalProps {
  userAsset: UserAsset | null;
  onSubmit: (data: Record<string, unknown>) => void;
  onClose: () => void;
}

const UserAssetModal: React.FC<UserAssetModalProps> = ({
  userAsset,
  onSubmit,
  onClose,
}) => {
  const [formData, setFormData] = useState({
    stock_code: userAsset?.stock_code || "",
    stock_name: userAsset?.stock_name || "",
    amount: userAsset?.amount || 0,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (userAsset) {
      onSubmit({ user_asset: { ...userAsset, ...formData } });
    } else {
      onSubmit(formData);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 className="text-lg font-semibold mb-4">
          {userAsset ? "자산 수정" : "자산 추가"}
        </h3>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">종목 코드</label>
            <input
              type="text"
              value={formData.stock_code}
              onChange={(e) =>
                setFormData({ ...formData, stock_code: e.target.value })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">종목명</label>
            <input
              type="text"
              value={formData.stock_name}
              onChange={(e) =>
                setFormData({ ...formData, stock_name: e.target.value })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">보유 수량</label>
            <input
              type="number"
              value={formData.amount}
              onChange={(e) =>
                setFormData({ ...formData, amount: Number(e.target.value) })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="submit"
              className="flex-1 bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              {userAsset ? "수정" : "추가"}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-300 text-gray-700 py-2 rounded hover:bg-gray-400"
            >
              취소
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserAssetModal;

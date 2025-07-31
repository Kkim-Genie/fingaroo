import React, { useState } from "react";
import { InvestLog } from "../app/types";

interface InvestLogModalProps {
  investLog: InvestLog | null;
  onSubmit: (data: Record<string, unknown>) => void;
  onClose: () => void;
}

const InvestLogModal: React.FC<InvestLogModalProps> = ({
  investLog,
  onSubmit,
  onClose,
}) => {
  const [formData, setFormData] = useState({
    date: investLog?.date || "",
    stock_code: investLog?.stock_code || "",
    stock_name: investLog?.stock_name || "",
    action: investLog?.action || "매수",
    price: investLog?.price || 0,
    amount: investLog?.amount || 0,
    reason: investLog?.reason || "",
    amount_ratio: investLog?.amount_ratio || 0,
    profit: investLog?.profit || 0,
    profit_ratio: investLog?.profit_ratio || 0,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (investLog) {
      onSubmit({ invest_log: { ...investLog, ...formData } });
    } else {
      onSubmit(formData);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <h3 className="text-lg font-semibold mb-4">
          {investLog ? "투자 일지 수정" : "투자 일지 추가"}
        </h3>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">날짜</label>
            <input
              type="date"
              value={formData.date}
              onChange={(e) =>
                setFormData({ ...formData, date: e.target.value })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>

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
            <label className="block text-sm font-medium mb-1">구분</label>
            <select
              value={formData.action}
              onChange={(e) =>
                setFormData({ ...formData, action: e.target.value })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
            >
              <option value="매수">매수</option>
              <option value="매도">매도</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">가격</label>
            <input
              type="number"
              value={formData.price}
              onChange={(e) =>
                setFormData({ ...formData, price: Number(e.target.value) })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">수량</label>
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

          <div>
            <label className="block text-sm font-medium mb-1">사유</label>
            <textarea
              value={formData.reason}
              onChange={(e) =>
                setFormData({ ...formData, reason: e.target.value })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">비중 (%)</label>
            <input
              type="number"
              step="0.01"
              value={formData.amount_ratio}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  amount_ratio: Number(e.target.value),
                })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">손익</label>
            <input
              type="number"
              value={formData.profit}
              onChange={(e) =>
                setFormData({ ...formData, profit: Number(e.target.value) })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">수익률 (%)</label>
            <input
              type="number"
              step="0.01"
              value={formData.profit_ratio}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  profit_ratio: Number(e.target.value),
                })
              }
              className="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="submit"
              className="flex-1 bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              {investLog ? "수정" : "추가"}
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

export default InvestLogModal;

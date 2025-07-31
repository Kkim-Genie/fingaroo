/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import dynamic from "next/dynamic";
import React from "react";
import dayjs from "dayjs";
import { ApexOptions } from "apexcharts";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
  ssr: false,
}) as any;

export interface StockItem {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  change: number;
  change_rate: number;
}

export interface StockData {
  stock_name: string;
  stock_code: string;
  current_price: number;
  change_price: number;
  change_rate: number;
  unit: string;
  items: StockItem[];
}

interface StockChartProps {
  stockData: StockData;
}

const StockChart = ({ stockData }: StockChartProps) => {
  const options: ApexOptions = {
    chart: {
      type: "candlestick",
      height: 350,
      defaultLocale: "ko",
      locales: [
        {
          name: "ko",
          options: {
            months: [
              "1월",
              "2월",
              "3월",
              "4월",
              "5월",
              "6월",
              "7월",
              "8월",
              "9월",
              "10월",
              "11월",
              "12월",
            ],
            shortMonths: [
              "1월",
              "2월",
              "3월",
              "4월",
              "5월",
              "6월",
              "7월",
              "8월",
              "9월",
              "10월",
              "11월",
              "12월",
            ],
            days: [
              "일요일",
              "월요일",
              "화요일",
              "수요일",
              "목요일",
              "금요일",
              "토요일",
            ],
            shortDays: ["일", "월", "화", "수", "목", "금", "토"],
          },
        },
      ],
    },
    title: {
      text: `${stockData.current_price}원 ${
        stockData.change_price > 0 ? "+" : ""
      }${stockData.change_price}원 (${stockData.change_rate.toFixed(2)}%)`,
      align: "left",
      style: {
        fontSize: "18px",
        fontWeight: "bold",
        color: stockData.change_price > 0 ? "#A50E5E" : "#185ABC",
      },
    },
    xaxis: {
      type: "datetime",
      labels: {
        datetimeFormatter: {
          year: "yyyy",
          month: "M월",
          day: "MM-dd",
        },
        formatter: function (value: any) {
          const date = new Date(value);
          const year = String(date.getFullYear()).slice(2);
          const month = String(date.getMonth() + 1).padStart(2, "0");
          const day = String(date.getDate()).padStart(2, "0");
          return `${year}-${month}-${day}`;
        },
      },
      tickPlacement: "on",
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
  };

  const stockSeries = [
    {
      data: [
        ...stockData.items.map((item) => ({
          x: dayjs(item.date).toDate(),
          y: [item.open, item.high, item.low, item.close],
        })),
        {
          x: dayjs().toDate(),
          y: [
            stockData.items[0].close,
            Math.max(stockData.items[0].high, stockData.current_price),
            Math.min(stockData.items[0].low, stockData.current_price),
            stockData.current_price,
          ],
        },
      ],
    },
  ];

  return (
    <div>
      <div className="flex items-center gap-1 text-lg font-bold ml-2">
        {stockData.stock_name}{" "}
        <p className="text-sm font-normal">({stockData.stock_code})</p>
      </div>
      <ReactApexChart
        options={options}
        series={stockSeries}
        type="candlestick"
        height={350}
      />
    </div>
  );
};

export default StockChart;

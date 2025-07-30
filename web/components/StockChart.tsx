/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import dynamic from "next/dynamic";
import React from "react";
import dayjs from "dayjs";

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
  unit: string;
  items: StockItem[];
}

interface StockChartProps {
  stockData: StockData;
}

const StockChart = ({ stockData }: StockChartProps) => {
  const options = {
    chart: {
      type: "candlestick",
      height: 350,
    },
    title: {
      text: `${stockData.stock_name} (${stockData.stock_code})`,
      align: "left",
    },
    xaxis: {
      type: "datetime",
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
  };

  const stockSeries = [
    {
      data: stockData.items.map((item) => ({
        x: dayjs(item.date).toDate(),
        y: [item.open, item.high, item.low, item.close],
      })),
    },
  ];

  return (
    <div>
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

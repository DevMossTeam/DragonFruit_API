'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { fetchFromAPI } from '@/lib/api';

// Dynamic import to avoid SSR issues with ApexCharts
const ReactApexChart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface StatisticData {
  label: string;
  value: number;
  unit: string;
  status: 'good' | 'warning' | 'danger';
}

interface SectionData {
  iotHealth: {
    uptime: StatisticData;
    temperature: StatisticData;
    humidity: StatisticData;
    signalStrength: StatisticData;
    dailyData: any[];
  };
  computerVision: {
    accuracy: StatisticData;
    processingTime: StatisticData;
    detectionRate: StatisticData;
    falsePositives: StatisticData;
    dailyData: any[];
  };
  machineLearning: {
    fuzzyAccuracy: StatisticData;
    precision: StatisticData;
    recall: StatisticData;
    f1Score: StatisticData;
    dailyData: any[];
  };
}

export default function GraphPage() {
  const [sectionData, setSectionData] = useState<SectionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        // Mock data - replace with actual API calls
        const mockData: SectionData = {
          iotHealth: {
            uptime: { label: 'Uptime', value: 99.8, unit: '%', status: 'good' },
            temperature: { label: 'Temperature', value: 28.5, unit: '°C', status: 'good' },
            humidity: { label: 'Humidity', value: 65, unit: '%', status: 'good' },
            signalStrength: { label: 'Signal Strength', value: 92, unit: 'dBm', status: 'good' },
            dailyData: [
              { date: 'Mon', uptime: 99.8, temp: 28.2, humidity: 64 },
              { date: 'Tue', uptime: 99.9, temp: 28.5, humidity: 65 },
              { date: 'Wed', uptime: 99.7, temp: 27.8, humidity: 63 },
              { date: 'Thu', uptime: 100, temp: 29.1, humidity: 66 },
              { date: 'Fri', uptime: 99.6, temp: 28.9, humidity: 67 },
              { date: 'Sat', uptime: 99.9, temp: 28.3, humidity: 64 },
              { date: 'Sun', uptime: 99.8, temp: 28.7, humidity: 65 },
            ],
          },
          computerVision: {
            accuracy: { label: 'Detection Accuracy', value: 96.5, unit: '%', status: 'good' },
            processingTime: { label: 'Avg Processing Time', value: 245, unit: 'ms', status: 'good' },
            detectionRate: { label: 'Detection Rate', value: 98.2, unit: '%', status: 'good' },
            falsePositives: { label: 'False Positives', value: 2.1, unit: '%', status: 'warning' },
            dailyData: [
              { date: 'Mon', accuracy: 96.2, processingTime: 250, detectionRate: 98.1 },
              { date: 'Tue', accuracy: 96.5, processingTime: 245, detectionRate: 98.2 },
              { date: 'Wed', accuracy: 96.8, processingTime: 240, detectionRate: 98.4 },
              { date: 'Thu', accuracy: 96.1, processingTime: 255, detectionRate: 97.9 },
              { date: 'Fri', accuracy: 96.9, processingTime: 235, detectionRate: 98.5 },
              { date: 'Sat', accuracy: 97.1, processingTime: 238, detectionRate: 98.6 },
              { date: 'Sun', accuracy: 96.5, processingTime: 248, detectionRate: 98.2 },
            ],
          },
          machineLearning: {
            fuzzyAccuracy: { label: 'Fuzzy Logic Accuracy', value: 94.7, unit: '%', status: 'good' },
            precision: { label: 'Precision', value: 95.2, unit: '%', status: 'good' },
            recall: { label: 'Recall', value: 94.1, unit: '%', status: 'good' },
            f1Score: { label: 'F1 Score', value: 94.6, unit: '%', status: 'good' },
            dailyData: [
              { date: 'Mon', fuzzyAccuracy: 94.5, precision: 95.0, recall: 93.9 },
              { date: 'Tue', fuzzyAccuracy: 94.7, precision: 95.2, recall: 94.1 },
              { date: 'Wed', fuzzyAccuracy: 94.9, precision: 95.4, recall: 94.3 },
              { date: 'Thu', fuzzyAccuracy: 94.3, precision: 94.8, recall: 93.7 },
              { date: 'Fri', fuzzyAccuracy: 95.1, precision: 95.6, recall: 94.5 },
              { date: 'Sat', fuzzyAccuracy: 95.3, precision: 95.8, recall: 94.8 },
              { date: 'Sun', fuzzyAccuracy: 94.7, precision: 95.2, recall: 94.1 },
            ],
          },
        };

        setSectionData(mockData);
        setLoading(false);
      } catch (err) {
        setError('Failed to load chart data');
        setLoading(false);
        console.error(err);
      }
    };

    fetchChartData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-gray-600">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  if (!sectionData) return null;

  // Helper function to get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good':
        return 'border-green-500 bg-green-50';
      case 'warning':
        return 'border-yellow-500 bg-yellow-50';
      case 'danger':
        return 'border-red-500 bg-red-50';
      default:
        return 'border-gray-500 bg-gray-50';
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'good':
        return 'bg-green-100 text-green-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'danger':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // IoT Health Charts
  const iotLineChartOptions = {
    chart: {
      type: 'line' as const,
      toolbar: { show: true },
    },
    colors: ['#3b82f6', '#ef4444', '#10b981'],
    xaxis: {
      categories: sectionData.iotHealth.dailyData.map((d) => d.date),
    },
    yaxis: {
      title: { text: 'Values' },
    },
    stroke: { curve: 'smooth' as const, width: 3 },
    markers: { size: 5 },
    legend: { position: 'top' as const },
  };

  const iotLineChartSeries = [
    {
      name: 'Uptime (%)',
      data: sectionData.iotHealth.dailyData.map((d) => d.uptime),
    },
    {
      name: 'Temperature (°C)',
      data: sectionData.iotHealth.dailyData.map((d) => d.temp),
    },
    {
      name: 'Humidity (%)',
      data: sectionData.iotHealth.dailyData.map((d) => d.humidity),
    },
  ];

  // Computer Vision Charts
  const cvLineChartOptions = {
    chart: {
      type: 'line' as const,
      toolbar: { show: true },
    },
    colors: ['#8b5cf6', '#ec4899', '#06b6d4'],
    xaxis: {
      categories: sectionData.computerVision.dailyData.map((d) => d.date),
    },
    yaxis: {
      title: { text: 'Accuracy/Detection Rate (%)' },
    },
    stroke: { curve: 'smooth' as const, width: 3 },
    markers: { size: 5 },
    legend: { position: 'top' as const },
  };

  const cvLineChartSeries = [
    {
      name: 'Accuracy (%)',
      data: sectionData.computerVision.dailyData.map((d) => d.accuracy),
    },
    {
      name: 'Detection Rate (%)',
      data: sectionData.computerVision.dailyData.map((d) => d.detectionRate),
    },
  ];

  // ML Fuzzy Charts
  // ML Radial/Gauge Charts Options
  const createRadialChartOptions = (title: string, color: string) => ({
    chart: {
      type: 'radialBar' as const,
      sparkline: {
        enabled: false,
      },
      toolbar: {
        show: false,
      },
    },
    colors: [color],
    plotOptions: {
      radialBar: {
        startAngle: -135,
        endAngle: 135,
        hollow: {
          margin: 0,
          size: '70%',
          background: '#fff',
          image: undefined,
          imageHeight: 151,
          imageWidth: 151,
        },
        track: {
          background: '#f2f2f2',
          strokeWidth: '97%',
          margin: 5,
          dropShadow: {
            enabled: true,
            top: 2,
            left: 0,
            color: '#999',
            opacity: 1,
            blur: 2,
          },
        },
        dataLabels: {
          show: true,
          name: {
            offsetY: -10,
            show: true,
            color: '#888',
            fontSize: '13px',
          },
          value: {
            formatter: function (val: number) {
              return parseInt(val.toString()) + '%';
            },
            color: '#111',
            fontSize: '30px',
            show: true,
          },
        },
      },
    },
    stroke: {
      lineCap: 'round' as const,
    },
    labels: [title],
  });

  const mlFuzzyChartOptions = createRadialChartOptions('Fuzzy Accuracy', '#f59e0b');
  const mlFuzzyChartSeries = [sectionData.machineLearning.fuzzyAccuracy.value];

  const mlPrecisionChartOptions = createRadialChartOptions('Precision', '#14b8a6');
  const mlPrecisionChartSeries = [sectionData.machineLearning.precision.value];

  const mlRecallChartOptions = createRadialChartOptions('Recall', '#6366f1');
  const mlRecallChartSeries = [sectionData.machineLearning.recall.value];

  const mlF1ScoreChartOptions = createRadialChartOptions('F1 Score', '#ec4899');
  const mlF1ScoreChartSeries = [sectionData.machineLearning.f1Score.value];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-800">System Analytics & Monitoring</h1>
        <p className="mt-1 text-gray-600">
          Real-time monitoring of IoT Health, Computer Vision, and Machine Learning Fuzzy Logic systems
        </p>
      </div>

      {/* ==================== PART 1: IoT HEALTH STATISTICS ==================== */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold text-gray-800">🌐 IoT Health Statistics</h2>
          <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full">
            Device Monitoring
          </span>
        </div>

        {/* IoT Health Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            sectionData.iotHealth.uptime,
            sectionData.iotHealth.temperature,
            sectionData.iotHealth.humidity,
            sectionData.iotHealth.signalStrength,
          ].map((stat) => (
            <div
              key={stat.label}
              className={`rounded-xl shadow-md p-6 border-l-4 ${getStatusColor(stat.status)}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {stat.value}{stat.unit}
                  </p>
                </div>
                <span className={`text-xs font-semibold px-2 py-1 rounded ${getStatusBadgeColor(stat.status)}`}>
                  {stat.status.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* IoT Health Chart */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">7-Day Performance Trend</h3>
          <div className="h-80">
            <ReactApexChart
              options={iotLineChartOptions}
              series={iotLineChartSeries}
              type="line"
              height={320}
            />
          </div>
        </div>
      </section>

      {/* ==================== PART 2: COMPUTER VISION STATISTICS ==================== */}
      <section className="space-y-4 pt-8 border-t-2 border-gray-200">
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold text-gray-800">👁️ Computer Vision Statistics</h2>
          <span className="bg-purple-100 text-purple-800 text-xs font-semibold px-3 py-1 rounded-full">
            Image Analysis
          </span>
        </div>

        {/* Computer Vision Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            sectionData.computerVision.accuracy,
            sectionData.computerVision.processingTime,
            sectionData.computerVision.detectionRate,
            sectionData.computerVision.falsePositives,
          ].map((stat) => (
            <div
              key={stat.label}
              className={`rounded-xl shadow-md p-6 border-l-4 ${getStatusColor(stat.status)}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">
                    {stat.value}{stat.unit}
                  </p>
                </div>
                <span className={`text-xs font-semibold px-2 py-1 rounded ${getStatusBadgeColor(stat.status)}`}>
                  {stat.status.toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Computer Vision Chart */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">7-Day Accuracy & Detection Performance</h3>
          <div className="h-80">
            <ReactApexChart
              options={cvLineChartOptions}
              series={cvLineChartSeries}
              type="line"
              height={320}
            />
          </div>
        </div>
      </section>

      {/* ==================== PART 3: MACHINE LEARNING FUZZY STATISTICS ==================== */}
      <section className="space-y-4 pt-8 border-t-2 border-gray-200">
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold text-gray-800">🤖 Machine Learning Fuzzy Logic Statistics</h2>
          <span className="bg-orange-100 text-orange-800 text-xs font-semibold px-3 py-1 rounded-full">
            AI Classification
          </span>
        </div>

        {/* ML Fuzzy Gauge Charts */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Fuzzy Accuracy Gauge */}
          <div className="bg-white rounded-xl shadow-md p-4">
            <div className="h-80">
              <ReactApexChart
                options={mlFuzzyChartOptions}
                series={mlFuzzyChartSeries}
                type="radialBar"
                height={320}
              />
            </div>
            <div className="text-center mt-2">
              <p className="text-xs text-gray-500">Fuzzy Logic Accuracy</p>
              <p className="text-sm font-semibold text-gray-800">{sectionData.machineLearning.fuzzyAccuracy.value}%</p>
            </div>
          </div>

          {/* Precision Gauge */}
          <div className="bg-white rounded-xl shadow-md p-4">
            <div className="h-80">
              <ReactApexChart
                options={mlPrecisionChartOptions}
                series={mlPrecisionChartSeries}
                type="radialBar"
                height={320}
              />
            </div>
            <div className="text-center mt-2">
              <p className="text-xs text-gray-500">Precision</p>
              <p className="text-sm font-semibold text-gray-800">{sectionData.machineLearning.precision.value}%</p>
            </div>
          </div>

          {/* Recall Gauge */}
          <div className="bg-white rounded-xl shadow-md p-4">
            <div className="h-80">
              <ReactApexChart
                options={mlRecallChartOptions}
                series={mlRecallChartSeries}
                type="radialBar"
                height={320}
              />
            </div>
            <div className="text-center mt-2">
              <p className="text-xs text-gray-500">Recall</p>
              <p className="text-sm font-semibold text-gray-800">{sectionData.machineLearning.recall.value}%</p>
            </div>
          </div>

          {/* F1 Score Gauge */}
          <div className="bg-white rounded-xl shadow-md p-4">
            <div className="h-80">
              <ReactApexChart
                options={mlF1ScoreChartOptions}
                series={mlF1ScoreChartSeries}
                type="radialBar"
                height={320}
              />
            </div>
            <div className="text-center mt-2">
              <p className="text-xs text-gray-500">F1 Score</p>
              <p className="text-sm font-semibold text-gray-800">{sectionData.machineLearning.f1Score.value}%</p>
            </div>
          </div>
        </div>

        {/* Performance Summary */}
        <div className="bg-white rounded-xl shadow-md p-6 mt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Performance Overview</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="border-l-4 border-orange-500 pl-4">
              <p className="text-sm text-gray-600">Fuzzy Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">{sectionData.machineLearning.fuzzyAccuracy.value}%</p>
              <p className="text-xs text-green-600 mt-1">✓ Good</p>
            </div>
            <div className="border-l-4 border-emerald-500 pl-4">
              <p className="text-sm text-gray-600">Precision</p>
              <p className="text-2xl font-bold text-gray-900">{sectionData.machineLearning.precision.value}%</p>
              <p className="text-xs text-green-600 mt-1">✓ Good</p>
            </div>
            <div className="border-l-4 border-indigo-500 pl-4">
              <p className="text-sm text-gray-600">Recall</p>
              <p className="text-2xl font-bold text-gray-900">{sectionData.machineLearning.recall.value}%</p>
              <p className="text-xs text-green-600 mt-1">✓ Good</p>
            </div>
            <div className="border-l-4 border-pink-500 pl-4">
              <p className="text-sm text-gray-600">F1 Score</p>
              <p className="text-2xl font-bold text-gray-900">{sectionData.machineLearning.f1Score.value}%</p>
              <p className="text-xs text-green-600 mt-1">✓ Good</p>
            </div>
          </div>
        </div>
      </section>

      {/* Summary Section */}
      <section className="pt-8 border-t-2 border-gray-200">
        <div className="bg-linear-to-r from-blue-50 to-purple-50 rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">System Health Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">IoT Health Status</p>
              <p className="text-xl font-bold text-green-600">✓ Excellent</p>
              <p className="text-xs text-gray-500 mt-1">All devices operating normally</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">Vision Analysis Status</p>
              <p className="text-xl font-bold text-green-600">✓ Operational</p>
              <p className="text-xs text-gray-500 mt-1">High detection accuracy maintained</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">ML Fuzzy Logic Status</p>
              <p className="text-xl font-bold text-green-600">✓ Performing Well</p>
              <p className="text-xs text-gray-500 mt-1">Classification accuracy above 94%</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

import React from 'react';
import { Layout } from '../components/Layout';
import { Card } from '../components/Card';
import { Badge } from '../components/Badge';

const recentDetections = [
  { id: 1, name: 'John Smith', time: '2 min ago', mask: true },
  { id: 2, name: 'Unknown', time: '5 min ago', mask: false },
  { id: 3, name: 'Mary Johnson', time: '8 min ago', mask: true },
  { id: 4, name: 'Unknown', time: '12 min ago', mask: true },
  { id: 5, name: 'Robert Chen', time: '15 min ago', mask: true },
];

export const CameraMonitor: React.FC = () => {
  return (
    <Layout title="Camera Monitor">
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_350px] gap-8">
        {/* Video Preview */}
        <div className="flex flex-col gap-4">
          <Card title="Live Camera Feed">
            <div className="relative bg-bg-secondary rounded-lg overflow-hidden border border-border-primary aspect-video">
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-bg-tertiary to-slate-900 text-5xl text-text-tertiary">
                📹
              </div>
              <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/40" />
              
              {/* Mock bounding boxes */}
              <div className="absolute top-[30%] left-[20%] w-[150px] h-[200px] border-4 border-blue-500 rounded shadow-glow p-1">
                <div className="absolute -top-8 left-0 bg-blue-500 text-white px-2 py-1 rounded text-xs font-semibold whitespace-nowrap flex items-center gap-2">
                  John Smith • <Badge variant="success">Mask</Badge>
                </div>
              </div>
              
              <div className="absolute top-[40%] left-[60%] w-[140px] h-[190px] border-4 border-amber-500 rounded p-1" style={{ boxShadow: '0 0 20px rgba(245, 158, 11, 0.5)' }}>
                <div className="absolute -top-8 left-0 bg-amber-500 text-white px-2 py-1 rounded text-xs font-semibold whitespace-nowrap flex items-center gap-2">
                  Unknown • <Badge variant="warning">No Mask</Badge>
                </div>
              </div>
            </div>
          </Card>

          <div className="grid grid-cols-3 gap-4">
            <Card>
              <div className="text-center">
                <div className="text-text-tertiary text-sm">Resolution</div>
                <div className="text-text-primary text-xl font-semibold mt-2">1920x1080</div>
              </div>
            </Card>
            <Card>
              <div className="text-center">
                <div className="text-text-tertiary text-sm">FPS</div>
                <div className="text-text-primary text-xl font-semibold mt-2">30</div>
              </div>
            </Card>
            <Card>
              <div className="text-center">
                <div className="text-text-tertiary text-sm">Latency</div>
                <div className="text-text-primary text-xl font-semibold mt-2">45ms</div>
              </div>
            </Card>
          </div>
        </div>

        {/* Side Panel */}
        <div className="flex flex-col gap-4">
          <Card title="Current Statistics">
            <div className="flex flex-col gap-2">
              <div className="flex justify-between items-center p-4 bg-bg-tertiary rounded-md border border-border-primary">
                <span className="text-sm text-text-secondary">People Count</span>
                <span className="text-xl font-bold text-text-primary">2</span>
              </div>
              <div className="flex justify-between items-center p-4 bg-bg-tertiary rounded-md border border-border-primary">
                <span className="text-sm text-text-secondary">Unknown</span>
                <span className="text-xl font-bold text-amber-500">1</span>
              </div>
            </div>
          </Card>

          <Card title="Recent Detections">
            <div className="flex flex-col gap-2 max-h-[400px] overflow-y-auto">
              {recentDetections.map((detection) => (
                <div key={detection.id} className="flex gap-3 p-3 bg-bg-tertiary border border-border-primary rounded-md hover:bg-bg-hover hover:border-border-secondary transition-all">
                  <div className="w-15 h-15 rounded-md bg-bg-secondary flex-shrink-0 flex items-center justify-center text-2xl">
                    {detection.name === 'Unknown' ? '❓' : '👤'}
                  </div>
                  <div className="flex-1 flex flex-col gap-1">
                    <div className="font-semibold text-text-primary text-sm">{detection.name}</div>
                    <div className="text-xs text-text-tertiary">{detection.time}</div>
                    <Badge variant={detection.mask ? 'success' : 'warning'}>
                      {detection.mask ? 'Mask' : 'No Mask'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </Layout>
  );
};

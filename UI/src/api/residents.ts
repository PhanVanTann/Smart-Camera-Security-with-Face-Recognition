const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ResidentCreate {
  first_name: string;
  last_name: string;
  age?: number;
  address?: string;
}

export interface Resident {
  _id: string;
  first_name: string;
  last_name: string;
  age?: number;
  address?: string;
  embeddings?: Array<{
    vector: number[];
    angle?: string;
    mask?: boolean;
    distance?: string;
  }>;
}

export interface FaceUploadParams {
  resident_id: string;
  image: File;
  angle: 'frontal' | 'left' | 'right';
  mask: boolean;
  distance: 'near' | 'medium' | 'far';
}

export const residentsAPI = {
  // Tạo resident mới
  async createResident(data: ResidentCreate): Promise<{ id: string; msg: string }> {
    const response = await fetch(`${API_BASE_URL}/residents/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create resident');
    }

    return response.json();
  },

  // Upload ảnh khuôn mặt
  async uploadFace(params: FaceUploadParams): Promise<{ message: string }> {
    const formData = new FormData();
    formData.append('image', params.image);
    formData.append('angle', params.angle);
    formData.append('mask', params.mask.toString());
    formData.append('distance', params.distance);

    const response = await fetch(
      `${API_BASE_URL}/residents/${params.resident_id}/face`,
      {
        method: 'POST',
        body: formData,
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to upload face image');
    }

    return response.json();
  },

  // Lấy danh sách residents (nếu có API)
  async getResidents(): Promise<Resident[]> {
    const response = await fetch(`${API_BASE_URL}/residents/get_all`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch residents');
    }

    return response.json();
  },
};

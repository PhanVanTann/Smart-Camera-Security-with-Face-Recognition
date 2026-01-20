import React, { useState, useRef, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { Button } from '../components/Button';
import { residentsAPI, type ResidentCreate, type Resident as APIResident } from '../api/residents';

interface Resident {
  _id: string;
  first_name: string;
  last_name: string;
  age?: number;
  address?: string;
}

interface FormData {
  first_name: string;
  last_name: string;
  age: string;
  address: string;
}

interface FaceUploadData {
  angle: 'frontal' | 'left' | 'right';
  mask: boolean;
  distance: 'near' | 'medium' | 'far';
}

export const Residents: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const [residents, setResidents] = useState<Resident[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState<FormData>({
    first_name: '',
    last_name: '',
    age: '',
    address: '',
  });
  
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [faceUploadData, setFaceUploadData] = useState<FaceUploadData>({
    angle: 'frontal',
    mask: false,
    distance: 'medium',
  });
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load residents on mount
  useEffect(() => {
    loadResidents();
  }, []);

  const loadResidents = async () => {
    try {
      setLoading(true);
      const data = await residentsAPI.getResidents();
      setResidents(data);
    } catch (err) {
      console.error('Failed to load residents:', err);
      // Không hiển thị error nếu API chưa có endpoint GET
    } finally {
      setLoading(false);
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file');
        return;
      }

      setSelectedImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    setError(null);
    setSuccess(null);

    // Validation
    if (!formData.first_name.trim() || !formData.last_name.trim()) {
      setError('First name and last name are required');
      return;
    }

    if (!selectedImage) {
      setError('Please upload a face image');
      return;
    }

    try {
      setLoading(true);

      // Step 1: Create resident
      const residentData: ResidentCreate = {
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        age: formData.age ? parseInt(formData.age) : undefined,
        address: formData.address.trim() || undefined,
      };

      const createResponse = await residentsAPI.createResident(residentData);
      const residentId = createResponse.id;

      // Step 2: Upload face image
      await residentsAPI.uploadFace({
        resident_id: residentId,
        image: selectedImage,
        angle: faceUploadData.angle,
        mask: faceUploadData.mask,
        distance: faceUploadData.distance,
      });

      setSuccess('Resident created successfully!');
      
      // Reset form
      setFormData({ first_name: '', last_name: '', age: '', address: '' });
      setSelectedImage(null);
      setImagePreview(null);
      setFaceUploadData({ angle: 'frontal', mask: false, distance: 'medium' });
      
      // Reload residents list
      await loadResidents();
      
      // Close modal after 1.5s
      setTimeout(() => {
        setShowModal(false);
        setSuccess(null);
      }, 1500);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create resident');
    } finally {
      setLoading(false);
    }
  };

  const resetModal = () => {
    setFormData({ first_name: '', last_name: '', age: '', address: '' });
    setSelectedImage(null);
    setImagePreview(null);
    setFaceUploadData({ angle: 'frontal', mask: false, distance: 'medium' });
    setError(null);
    setSuccess(null);
    setShowModal(false);
  };

  return (
    <Layout title="Residents">
      <div className="flex flex-col gap-6">
        <div className="bg-bg-card rounded-lg border border-border-primary overflow-hidden">
          <div className="p-6 border-b border-border-primary flex items-center justify-between">
            <div>
              <h3 className="text-xl font-semibold text-text-primary">Registered Residents</h3>
              <p className="text-sm text-text-tertiary mt-1">Manage and view all registered residents</p>
            </div>
            <Button onClick={() => setShowModal(true)}>+ Add Resident</Button>
          </div>

          <table className="w-full">
            <thead className="bg-bg-tertiary sticky top-0 z-10">
              <tr>
                <th className="text-left p-4 text-sm font-semibold text-text-secondary uppercase tracking-wide border-b border-border-primary">Resident</th>
                <th className="text-left p-4 text-sm font-semibold text-text-secondary uppercase tracking-wide border-b border-border-primary">Age</th>
                <th className="text-left p-4 text-sm font-semibold text-text-secondary uppercase tracking-wide border-b border-border-primary">Address</th>
                <th className="text-left p-4 text-sm font-semibold text-text-secondary uppercase tracking-wide border-b border-border-primary">Faces</th>
                <th className="text-left p-4 text-sm font-semibold text-text-secondary uppercase tracking-wide border-b border-border-primary">Actions</th>
              </tr>
            </thead>
            <tbody>
              {residents.length === 0 ? (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-text-tertiary">
                    No residents found. Add your first resident to get started.
                  </td>
                </tr>
              ) : (
                residents.map((resident) => (
                  <tr key={resident._id} className="border-b border-border-primary hover:bg-bg-hover transition-all">
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
                          {resident.first_name[0]}{resident.last_name[0]}
                        </div>
                        <div className="font-semibold text-text-primary">
                          {resident.first_name} {resident.last_name}
                        </div>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="text-text-secondary text-sm">{resident.age || 'N/A'}</span>
                    </td>
                    <td className="p-4">
                      <span className="text-text-secondary text-sm">{resident.address || 'N/A'}</span>
                    </td>
                    <td className="p-4">
                      <span className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded border bg-emerald-500/15 text-accent-success border-emerald-500/30">
                        Registered
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        <Button size="sm" variant="secondary">View</Button>
                        <Button size="sm" variant="danger">Delete</Button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Resident Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-[1000] animate-fade-in" onClick={resetModal}>
          <div className="bg-bg-secondary rounded-xl border border-border-primary w-[90%] max-w-[600px] shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="p-8 border-b border-border-primary flex items-center justify-between sticky top-0 bg-bg-secondary z-10">
              <h2 className="text-2xl font-bold text-text-primary">Add New Resident</h2>
              <button 
                className="w-8 h-8 flex items-center justify-center bg-bg-tertiary rounded-md text-text-secondary text-lg hover:bg-bg-hover hover:text-text-primary transition-all" 
                onClick={resetModal}
                disabled={loading}
              >
                ×
              </button>
            </div>

            <div className="p-8">
              {/* Error/Success Messages */}
              {error && (
                <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                  {error}
                </div>
              )}
              
              {success && (
                <div className="mb-6 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400 text-sm">
                  {success}
                </div>
              )}

              {/* Personal Information */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-text-primary mb-4">Personal Information</h3>
                
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-semibold text-text-primary mb-2">
                      First Name <span className="text-red-500">*</span>
                    </label>
                    <input 
                      type="text" 
                      className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all" 
                      placeholder="Văn Tấn"
                      value={formData.first_name}
                      onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-semibold text-text-primary mb-2">
                      Last Name <span className="text-red-500">*</span>
                    </label>
                    <input 
                      type="text" 
                      className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all" 
                      placeholder="Phan"
                      value={formData.last_name}
                      onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-text-primary mb-2">Age</label>
                    <input 
                      type="number" 
                      className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all" 
                      placeholder="25"
                      value={formData.age}
                      onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-semibold text-text-primary mb-2">Address</label>
                    <input 
                      type="text" 
                      className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all" 
                      placeholder="123 ABC Street"
                      value={formData.address}
                      onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              {/* Face Image Upload */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-text-primary mb-4">
                  Face Image <span className="text-red-500">*</span>
                </h3>
                
                <input 
                  ref={fileInputRef}
                  type="file" 
                  accept="image/*"
                  className="hidden"
                  onChange={handleImageSelect}
                  disabled={loading}
                />
                
                <div 
                  className="w-full h-[200px] border-2 border-dashed border-border-secondary rounded-lg flex flex-col items-center justify-center gap-3 cursor-pointer hover:border-accent-primary hover:bg-bg-hover transition-all bg-bg-tertiary overflow-hidden"
                  onClick={() => !loading && fileInputRef.current?.click()}
                >
                  {imagePreview ? (
                    <img src={imagePreview} alt="Preview" className="w-full h-full object-cover" />
                  ) : (
                    <>
                      <div className="text-5xl text-text-tertiary">📷</div>
                      <div className="text-sm text-text-secondary">Click to upload face image</div>
                      <div className="text-xs text-text-tertiary">PNG, JPG up to 10MB</div>
                    </>
                  )}
                </div>
                
                {selectedImage && (
                  <div className="mt-3 text-sm text-text-secondary">
                    Selected: {selectedImage.name}
                  </div>
                )}
              </div>

              {/* Face Upload Metadata */}
              {selectedImage && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-text-primary mb-4">Image Details</h3>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-text-primary mb-2">Angle</label>
                      <select 
                        className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all"
                        value={faceUploadData.angle}
                        onChange={(e) => setFaceUploadData({ ...faceUploadData, angle: e.target.value as any })}
                        disabled={loading}
                      >
                        <option value="frontal">Frontal</option>
                        <option value="left">Left</option>
                        <option value="right">Right</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-semibold text-text-primary mb-2">Distance</label>
                      <select 
                        className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all"
                        value={faceUploadData.distance}
                        onChange={(e) => setFaceUploadData({ ...faceUploadData, distance: e.target.value as any })}
                        disabled={loading}
                      >
                        <option value="near">Near</option>
                        <option value="medium">Medium</option>
                        <option value="far">Far</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-semibold text-text-primary mb-2">Mask</label>
                      <div className="flex items-center h-[48px]">
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input 
                            type="checkbox" 
                            className="sr-only peer"
                            checked={faceUploadData.mask}
                            onChange={(e) => setFaceUploadData({ ...faceUploadData, mask: e.target.checked })}
                            disabled={loading}
                          />
                          <div className="w-11 h-6 bg-bg-tertiary border border-border-primary rounded-full peer peer-checked:bg-accent-primary peer-checked:border-accent-primary transition-all"></div>
                          <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-all peer-checked:translate-x-5"></div>
                        </label>
                        <span className="ml-3 text-sm text-text-secondary">
                          {faceUploadData.mask ? 'Yes' : 'No'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="p-8 border-t border-border-primary flex gap-3 justify-end sticky bottom-0 bg-bg-secondary">
              <Button variant="secondary" onClick={resetModal} disabled={loading}>
                Cancel
              </Button>
              <Button 
                variant="success" 
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? 'Creating...' : 'Add Resident'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
};

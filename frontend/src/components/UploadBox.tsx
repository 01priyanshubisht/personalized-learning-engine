import { useState, useRef } from 'react';
import { Upload, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { documentsApi } from '../api/documents';
import { LEARNER_ID } from '../App';
import { UploadResponse } from '../types/api';

const UploadBox = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<UploadResponse | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // reset states
    setError(null);
    setSuccess(null);
    setIsUploading(true);

    try {
      const response = await documentsApi.upload(LEARNER_ID, file);
      setSuccess(response);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to upload document.');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
      {!isUploading && !success && !error && (
        <div 
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:bg-gray-50 hover:border-indigo-400 transition-colors cursor-pointer flex flex-col items-center justify-center"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-1">Upload PDF</h3>
          <p className="text-gray-500 text-sm">Click to browse your files</p>
        </div>
      )}

      {isUploading && (
        <div className="py-12 flex flex-col items-center justify-center space-y-4">
          <Loader2 className="h-10 w-10 text-indigo-600 animate-spin" />
          <div className="text-center">
            <p className="text-lg font-medium text-gray-900">Uploading...</p>
            <p className="text-gray-500">Processing document...</p>
            <p className="text-gray-500">Extracting knowledge...</p>
          </div>
        </div>
      )}

      {success && (
        <div className="py-8 bg-green-50 rounded-xl border border-green-100 flex flex-col items-center justify-center text-center px-4">
          <CheckCircle2 className="h-12 w-12 text-green-500 mb-4" />
          <h3 className="text-xl font-bold text-green-900 mb-2">✓ Knowledge added</h3>
          <p className="text-green-700">{success.page_count} pages processed</p>
          <p className="text-green-700">Concepts extracted</p>
          <p className="text-green-700 mb-6">Learner knowledge updated</p>
          <button 
            onClick={() => setSuccess(null)}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Upload Another
          </button>
        </div>
      )}

      {error && (
        <div className="py-8 bg-red-50 rounded-xl border border-red-100 flex flex-col items-center justify-center text-center px-4">
          <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
          <h3 className="text-xl font-bold text-red-900 mb-2">Upload Failed</h3>
          <p className="text-red-700 mb-6">{error}</p>
          <button 
            onClick={() => setError(null)}
            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      )}

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="application/pdf"
        className="hidden"
      />
    </div>
  );
};

export default UploadBox;

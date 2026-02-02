"use client";

import { useState } from 'react';
import { Upload, FileText, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { toast } from 'sonner';
import apiClient from '@/lib/api';

interface CVUploadProps {
  onDataParsed: (data: any) => void;
  onError?: (error: string) => void;
}

export function CVUpload({ onDataParsed, onError }: CVUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFile = async (file: File) => {
    // Validation
    if (!file.type.includes('pdf')) {
      toast.error('Seuls les fichiers PDF sont acceptés');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      toast.error('Le fichier ne doit pas dépasser 10MB');
      return;
    }

    setSelectedFile(file);
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post('/profile/parse-cv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        toast.success(response.data.message || 'CV analysé avec succès !');
        onDataParsed(response.data.profile_data);
      } else {
        throw new Error(response.data.message || 'Erreur lors de l\'analyse');
      }
    } catch (error: any) {
      console.error('Erreur upload CV:', error);
      const errorMsg = error.response?.data?.detail || 'Erreur lors de l\'analyse du CV';
      toast.error(errorMsg);
      onError?.(errorMsg);
    } finally {
      setUploading(false);
      setSelectedFile(null);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
  };

  return (
    <Card className="w-full">
      <CardContent className="pt-6">
        <div
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center transition-colors
            ${dragActive ? 'border-primary bg-primary/5' : 'border-gray-300'}
            ${uploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-primary hover:bg-gray-50'}
          `}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => !uploading && document.getElementById('cv-upload-input')?.click()}
        >
          <input
            id="cv-upload-input"
            type="file"
            accept=".pdf"
            onChange={handleChange}
            disabled={uploading}
            className="hidden"
          />

          {uploading ? (
            <div className="flex flex-col items-center gap-4">
              <Loader2 className="w-12 h-12 text-primary animate-spin" />
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Analyse en cours...</h3>
                <p className="text-sm text-gray-600 mt-1">
                  L'IA analyse votre CV. Cela peut prendre quelques secondes.
                </p>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-4">
              <div className="rounded-full bg-primary/10 p-4">
                <Upload className="w-8 h-8 text-primary" />
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Importez votre CV
                </h3>
                <p className="text-sm text-gray-600 mt-2">
                  Glissez-déposez votre CV PDF ici, ou <span className="text-primary font-medium">cliquez pour parcourir</span>
                </p>
                <p className="text-xs text-gray-500 mt-2">
                  PDF uniquement • Maximum 10MB
                </p>
              </div>

              <div className="flex items-center gap-2 mt-2 text-sm text-gray-600">
                <CheckCircle2 className="w-4 h-4 text-green-600" />
                <span>Extraction automatique par IA</span>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 space-y-3">
          <div className="flex items-start gap-2 text-sm text-gray-600">
            <FileText className="w-4 h-4 mt-0.5 text-blue-600" />
            <p>
              <span className="font-medium">L'IA extrait automatiquement</span> vos expériences, formations et compétences
            </p>
          </div>
          <div className="flex items-start gap-2 text-sm text-gray-600">
            <AlertCircle className="w-4 h-4 mt-0.5 text-amber-600" />
            <p>
              Vous pourrez <span className="font-medium">vérifier et modifier</span> toutes les informations avant de sauvegarder
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

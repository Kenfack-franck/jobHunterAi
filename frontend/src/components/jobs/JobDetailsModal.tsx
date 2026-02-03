"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { JobOffer } from '@/types';
import { 
  MapPin, 
  Briefcase, 
  Building2, 
  ExternalLink,
  Calendar,
  FileText,
  Globe,
  Sparkles,
  Save,
  CheckCircle
} from 'lucide-react';

interface JobDetailsModalProps {
  job: JobOffer | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave?: () => void;
  onAnalyze?: () => void;
  isSaved?: boolean;
}

export function JobDetailsModal({ 
  job, 
  open, 
  onOpenChange, 
  onSave, 
  onAnalyze,
  isSaved = false 
}: JobDetailsModalProps) {
  if (!job) return null;

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getJobTypeVariant = (type: string) => {
    switch (type.toLowerCase()) {
      case 'cdi': return 'default';
      case 'cdd': return 'secondary';
      case 'stage': return 'outline';
      case 'freelance': return 'outline';
      default: return 'outline';
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto backdrop-blur-xl bg-white/95 border-2 border-gray-200/50 shadow-2xl">
        <DialogHeader>
          <div className="flex items-center gap-4 mb-3">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
              <Briefcase className="w-7 h-7 text-white" />
            </div>
            <div className="flex-1">
              <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                {job.job_title}
              </DialogTitle>
              <DialogDescription className="text-lg flex items-center gap-2 mt-1 text-gray-600">
                <Building2 className="w-5 h-5 text-purple-500" />
                {job.company_name}
              </DialogDescription>
            </div>
            {isSaved && (
              <Badge className="bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg border-0">
                <CheckCircle className="w-4 h-4 mr-1" />
                Sauvegardée
              </Badge>
            )}
          </div>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          {/* Informations principales */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {job.location && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-gradient-to-br from-blue-50 to-purple-50 border border-blue-100 hover:shadow-md transition-all">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <MapPin className="w-4 h-4 text-white" />
                </div>
                <span className="font-medium text-gray-700">{job.location}</span>
              </div>
            )}
            
            {job.job_type && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-gradient-to-br from-green-50 to-emerald-50 border border-green-100 hover:shadow-md transition-all">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                  <Briefcase className="w-4 h-4 text-white" />
                </div>
                <Badge className="bg-gradient-to-r from-green-500 to-emerald-500 text-white border-0">
                  {job.job_type}
                </Badge>
              </div>
            )}
            
            {job.work_mode && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-gradient-to-br from-pink-50 to-rose-50 border border-pink-100 hover:shadow-md transition-all">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                  <Globe className="w-4 h-4 text-white" />
                </div>
                <Badge className="bg-gradient-to-r from-pink-500 to-rose-500 text-white border-0">
                  {job.work_mode === 'remote' && '🏠 Télétravail'}
                  {job.work_mode === 'hybrid' && '🔀 Hybride'}
                  {job.work_mode === 'onsite' && '🏢 Présentiel'}
                  {!['remote', 'hybrid', 'onsite'].includes(job.work_mode) && job.work_mode}
                </Badge>
              </div>
            )}
          </div>

          {/* Dates et source */}
          <div className="flex flex-wrap gap-4 text-sm text-gray-600 py-3 px-4 rounded-lg bg-gradient-to-r from-gray-50 to-gray-100/50 border border-gray-200/50">
            {job.posted_date && (
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-blue-500" />
                <span>Publié le <span className="font-semibold text-gray-800">{formatDate(job.posted_date)}</span></span>
              </div>
            )}
            {job.source_platform && (
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4 text-purple-500" />
                <span>Source: <span className="font-semibold text-gray-800">{job.source_platform}</span></span>
              </div>
            )}
          </div>

          {/* Description */}
          {job.description && (
            <Card className="border-2 border-blue-100 hover:border-blue-200 hover:shadow-lg transition-all duration-300">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-md">
                    <FileText className="w-5 h-5 text-white" />
                  </div>
                  <h3 className="font-bold text-lg bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    Description du poste
                  </h3>
                </div>
                <div className="h-px bg-gradient-to-r from-blue-200 via-purple-200 to-transparent mb-4" />
                <div 
                  className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: job.description.replace(/\n/g, '<br/>') }}
                />
              </CardContent>
            </Card>
          )}

          {/* Requirements */}
          {job.requirements && (
            <Card className="border-2 border-green-100 hover:border-green-200 hover:shadow-lg transition-all duration-300">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-md">
                    <CheckCircle className="w-5 h-5 text-white" />
                  </div>
                  <h3 className="font-bold text-lg bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                    Exigences
                  </h3>
                </div>
                <div className="h-px bg-gradient-to-r from-green-200 via-emerald-200 to-transparent mb-4" />
                <div 
                  className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: job.requirements.replace(/\n/g, '<br/>') }}
                />
              </CardContent>
            </Card>
          )}

          {/* Technologies / Compétences requises */}
          {job.extracted_keywords && job.extracted_keywords.length > 0 && (
            <div className="p-4 rounded-xl bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 border-2 border-purple-100">
              <h3 className="font-bold text-lg mb-3 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                💎 Mots-clés extraits
              </h3>
              <div className="flex flex-wrap gap-2">
                {job.extracted_keywords.map((keyword, idx) => (
                  <Badge 
                    key={idx} 
                    className="bg-gradient-to-r from-purple-500 to-pink-500 text-white border-0 hover:shadow-lg hover:scale-105 transition-all cursor-default"
                  >
                    {keyword}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-wrap gap-3 pt-6">
            <div className="h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent w-full mb-2" />
            {job.source_url && (
              <Button 
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-300"
                onClick={() => window.open(job.source_url, '_blank')}
              >
                <ExternalLink className="w-4 h-4 mr-2" />
                Postuler sur {job.source_platform || 'le site'}
              </Button>
            )}

            {onAnalyze && (
              <Button 
                variant="outline" 
                className="flex-1 border-2 border-purple-300 hover:bg-purple-50 hover:border-purple-500 transition-all duration-300"
                onClick={() => {
                  onAnalyze();
                  onOpenChange(false);
                }}
              >
                <Sparkles className="w-4 h-4 mr-2 text-purple-500" />
                Analyser compatibilité
              </Button>
            )}

            {onSave && !isSaved && (
              <Button 
                variant="outline"
                className="border-2 border-green-300 hover:bg-green-50 hover:border-green-500 transition-all duration-300"
                onClick={() => {
                  onSave();
                  onOpenChange(false);
                }}
              >
                <Save className="w-4 h-4 mr-2 text-green-500" />
                Sauvegarder
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

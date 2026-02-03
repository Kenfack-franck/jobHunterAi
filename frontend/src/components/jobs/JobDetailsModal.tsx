"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { JobOffer } from '@/types';
import { 
  MapPin, 
  Briefcase, 
  Clock, 
  DollarSign, 
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
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <DialogTitle className="text-2xl mb-2">{job.job_title}</DialogTitle>
              <DialogDescription className="text-lg flex items-center gap-2">
                <Building2 className="w-5 h-5" />
                {job.company_name}
              </DialogDescription>
            </div>
            {isSaved && (
              <Badge variant="default" className="bg-green-600">
                <CheckCircle className="w-4 h-4 mr-1" />
                Sauvegardée
              </Badge>
            )}
          </div>
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {/* Informations principales */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {job.location && (
              <div className="flex items-center gap-2 text-sm">
                <MapPin className="w-4 h-4 text-gray-500" />
                <span className="font-medium">{job.location}</span>
              </div>
            )}
            
            {job.job_type && (
              <div className="flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-gray-500" />
                <Badge variant={getJobTypeVariant(job.job_type)}>{job.job_type}</Badge>
              </div>
            )}
            
            {job.work_mode && (
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4 text-gray-500" />
                <Badge variant="outline">
                  {job.work_mode === 'remote' && '🏠 Télétravail'}
                  {job.work_mode === 'hybrid' && '🔀 Hybride'}
                  {job.work_mode === 'onsite' && '🏢 Présentiel'}
                  {!['remote', 'hybrid', 'onsite'].includes(job.work_mode) && job.work_mode}
                </Badge>
              </div>
            )}
            
            {job.salary && (
              <div className="flex items-center gap-2 text-sm">
                <DollarSign className="w-4 h-4 text-gray-500" />
                <span className="font-medium">{job.salary}</span>
              </div>
            )}

            {job.experience_level && (
              <div className="flex items-center gap-2 text-sm">
                <Clock className="w-4 h-4 text-gray-500" />
                <span className="font-medium">{job.experience_level}</span>
              </div>
            )}
          </div>

          {/* Dates et source */}
          <div className="flex flex-wrap gap-4 text-sm text-gray-600 border-t border-b py-3">
            {job.posted_date && (
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Publié le {formatDate(job.posted_date)}
              </div>
            )}
            {job.source_platform && (
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4" />
                Source: <span className="font-medium">{job.source_platform}</span>
              </div>
            )}
          </div>

          {/* Description */}
          {job.description && (
            <Card>
              <CardContent className="pt-6">
                <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Description du poste
                </h3>
                <div 
                  className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap"
                  dangerouslySetInnerHTML={{ __html: job.description.replace(/\n/g, '<br/>') }}
                />
              </CardContent>
            </Card>
          )}

          {/* Requirements */}
          {job.requirements && (
            <Card>
              <CardContent className="pt-6">
                <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  Exigences
                </h3>
                <div 
                  className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap"
                  dangerouslySetInnerHTML={{ __html: job.requirements.replace(/\n/g, '<br/>') }}
                />
              </CardContent>
            </Card>
          )}

          {/* Technologies / Compétences requises */}
          {job.required_skills && job.required_skills.length > 0 && (
            <div>
              <h3 className="font-semibold text-lg mb-3">Compétences requises</h3>
              <div className="flex flex-wrap gap-2">
                {job.required_skills.map((skill, idx) => (
                  <Badge key={idx} variant="secondary">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-wrap gap-3 pt-4 border-t">
            {(job.apply_url || job.source_url) && (
              <Button 
                variant="default" 
                className="flex-1"
                onClick={() => window.open(job.apply_url || job.source_url, '_blank')}
              >
                <ExternalLink className="w-4 h-4 mr-2" />
                Postuler sur {job.source_platform || 'le site'}
              </Button>
            )}

            {onAnalyze && (
              <Button 
                variant="outline" 
                className="flex-1"
                onClick={() => {
                  onAnalyze();
                  onOpenChange(false);
                }}
              >
                <Sparkles className="w-4 h-4 mr-2" />
                Analyser compatibilité
              </Button>
            )}

            {onSave && !isSaved && (
              <Button 
                variant="outline"
                onClick={() => {
                  onSave();
                  onOpenChange(false);
                }}
              >
                <Save className="w-4 h-4 mr-2" />
                Sauvegarder
              </Button>
            )}
          </div>

          {/* Company website */}
          {job.company_website && (
            <div className="text-sm text-gray-600">
              <a 
                href={job.company_website} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2 hover:text-primary"
              >
                <Globe className="w-4 h-4" />
                Site web de l'entreprise
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

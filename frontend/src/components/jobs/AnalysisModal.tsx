"use client"
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Loader2, FileText, Mail, CheckCircle2, ExternalLink } from "lucide-react";
import { documentsService, Document } from "@/lib/documentsService";
import profileService from "@/lib/profile";
import { Profile } from "@/types";

interface AnalysisModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  jobId: string;
  jobTitle: string;
  companyName: string;
}

export function AnalysisModal({ open, onOpenChange, jobId, jobTitle, companyName }: AnalysisModalProps) {
  const router = useRouter();
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [generatedDocs, setGeneratedDocs] = useState<{ cv?: Document; coverLetter?: Document } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [compatibilityScore, setCompatibilityScore] = useState<number | null>(null);
  const [loadingScore, setLoadingScore] = useState(false);

  useEffect(() => {
    if (open) {
      loadProfiles();
      setCompatibilityScore(null);
      setGeneratedDocs(null);
      setError(null);
    }
  }, [open]);

  // Calcul du score de compatibilité avec l'IA
  useEffect(() => {
    if (selectedProfileId && jobId && open) {
      calculateCompatibility();
    }
  }, [selectedProfileId, jobId, open]);

  const calculateCompatibility = async () => {
    setLoadingScore(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`http://localhost:8000/api/v1/jobs/${jobId}/compatibility/${selectedProfileId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Erreur lors du calcul de compatibilité');
      }
      
      const data = await response.json();
      if (data.success && data.analysis) {
        setCompatibilityScore(data.analysis.score);
      }
    } catch (err) {
      console.error('Erreur calcul compatibilité:', err);
      setCompatibilityScore(null);
    } finally {
      setLoadingScore(false);
    }
  };

  const loadProfiles = async () => {
    setLoading(true);
    try {
      const profile = await profileService.getProfile();
      // Convertir le profil unique en tableau pour compatibilité
      setProfiles([profile]);
      setSelectedProfileId(profile.id);
    } catch (err) {
      console.error("Erreur de chargement du profil:", err);
      setError("Vous devez créer un profil avant d'analyser une offre");
      setProfiles([]);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!selectedProfileId) {
      setError("Veuillez sélectionner un profil");
      return;
    }

    setGenerating(true);
    setError(null);

    try {
      const result = await documentsService.generateDocuments(jobId, selectedProfileId, {
        include_cv: true,
        include_cover_letter: true,
        tone: 'professional',
        length: 'medium'
      });

      setGeneratedDocs({
        cv: result.documents?.find((d: Document) => d.document_type === 'resume'),
        coverLetter: result.documents?.find((d: Document) => d.document_type === 'cover_letter')
      });
    } catch (err: any) {
      console.error("Erreur de génération:", err);
      // Extraire le message d'erreur proprement
      let errorMessage = "Erreur lors de la génération des documents";
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        // Si c'est un tableau d'erreurs Pydantic
        if (Array.isArray(detail)) {
          errorMessage = detail.map((e: any) => e.msg || "Erreur").join(", ");
        } 
        // Si c'est une string
        else if (typeof detail === 'string') {
          errorMessage = detail;
        }
        // Si c'est un objet
        else if (typeof detail === 'object') {
          errorMessage = JSON.stringify(detail);
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (docId: string, filename: string) => {
    try {
      const blob = await documentsService.downloadDocument(docId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error("Erreur de téléchargement:", err);
      setError("Impossible de télécharger le document");
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "bg-green-500";
    if (score >= 60) return "bg-blue-500";
    if (score >= 40) return "bg-yellow-500";
    return "bg-red-500";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent match";
    if (score >= 60) return "Bon match";
    if (score >= 40) return "Match moyen";
    return "Faible match";
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">Analyse de compatibilité</DialogTitle>
          <DialogDescription>
            {jobTitle} • {companyName}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Score de compatibilité */}
          <div className="bg-gray-50 p-6 rounded-lg text-center">
            <div className="flex justify-center mb-4">
              <div className="relative w-32 h-32">
                <svg className="transform -rotate-90 w-32 h-32">
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="#e5e7eb"
                    strokeWidth="8"
                    fill="none"
                  />
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${2 * Math.PI * 56}`}
                    strokeDashoffset={`${2 * Math.PI * 56 * (1 - (compatibilityScore || 0) / 100)}`}
                    className={getScoreColor(compatibilityScore || 0).replace('bg-', 'text-')}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  {loadingScore ? (
                    <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                  ) : compatibilityScore !== null ? (
                    <span className="text-3xl font-bold">{compatibilityScore}%</span>
                  ) : (
                    <span className="text-xl text-gray-400">--</span>
                  )}
                </div>
              </div>
            </div>
            {compatibilityScore !== null && (
              <Badge className={getScoreColor(compatibilityScore)}>
                {getScoreLabel(compatibilityScore)}
              </Badge>
            )}
            {loadingScore && (
              <p className="text-sm text-gray-500 mt-2">Calcul du score avec l'IA...</p>
            )}
          </div>

          {/* Sélection du profil */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Profil à utiliser pour postuler
            </label>
            {loading ? (
              <div className="text-sm text-gray-500">Chargement des profils...</div>
            ) : profiles.length === 0 ? (
              <div className="text-sm text-red-500">
                Vous devez créer un profil avant de générer des documents
              </div>
            ) : (
              <Select value={selectedProfileId} onValueChange={setSelectedProfileId}>
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner un profil" />
                </SelectTrigger>
                <SelectContent>
                  {profiles.map((profile) => (
                    <SelectItem key={profile.id} value={profile.id}>
                      {profile.title || "Profil sans titre"}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
          </div>

          {/* Analyse IA (placeholder) */}
          <div className="space-y-2">
            <h3 className="font-semibold text-sm">Analyse IA</h3>
            <div className="space-y-1 text-sm">
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5" />
                <span>Compétences techniques correspondent bien</span>
              </div>
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5" />
                <span>Expérience alignée avec les exigences</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="w-4 h-4 text-yellow-500 mt-0.5">⚠️</span>
                <span>Points à améliorer : certifications manquantes</span>
              </div>
            </div>
          </div>

          {/* Erreur */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Documents générés */}
          {generatedDocs && (
            <div className="bg-green-50 border border-green-200 p-4 rounded-lg space-y-3">
              <div className="flex items-center gap-2 text-green-700 font-medium">
                <CheckCircle2 className="w-5 h-5" />
                <span>Documents générés avec succès !</span>
              </div>
              
              <div className="space-y-2">
                {generatedDocs.cv && (
                  <div className="flex items-center justify-between bg-white p-3 rounded border">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4" />
                      <span className="text-sm font-medium">{generatedDocs.cv.filename}</span>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDownload(generatedDocs.cv!.id, generatedDocs.cv!.filename)}
                    >
                      Télécharger
                    </Button>
                  </div>
                )}

                {generatedDocs.coverLetter && (
                  <div className="flex items-center justify-between bg-white p-3 rounded border">
                    <div className="flex items-center gap-2">
                      <Mail className="w-4 h-4" />
                      <span className="text-sm font-medium">{generatedDocs.coverLetter.filename}</span>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDownload(generatedDocs.coverLetter!.id, generatedDocs.coverLetter!.filename)}
                    >
                      Télécharger
                    </Button>
                  </div>
                )}
              </div>
              
              {/* Bouton pour aller voir tous les documents */}
              <Button
                variant="outline"
                className="w-full mt-3"
                onClick={() => {
                  onOpenChange(false);
                  router.push('/documents');
                }}
              >
                <ExternalLink className="w-4 h-4 mr-2" />
                Voir tous mes documents
              </Button>
            </div>
          )}

          {/* Message de progression pendant la génération */}
          {generating && (
            <div className="bg-blue-50 border border-blue-200 text-blue-800 p-4 rounded-lg flex items-start gap-3">
              <Loader2 className="w-5 h-5 animate-spin mt-0.5" />
              <div className="flex-1 text-sm">
                <p className="font-medium mb-1">⏳ Génération en cours...</p>
                <p className="text-xs opacity-75">
                  L'IA personnalise vos documents. Cela peut prendre 1-2 minutes. Veuillez patienter.
                </p>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-3">
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              Fermer
            </Button>
            
            {!generatedDocs && (
              <Button 
                onClick={handleGenerate}
                disabled={generating || profiles.length === 0 || !selectedProfileId}
              >
                {generating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <FileText className="w-4 h-4 mr-2" />
                    Générer les documents
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

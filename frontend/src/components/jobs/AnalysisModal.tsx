"use client"
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Loader2, FileText, Mail, CheckCircle2, ExternalLink, Sparkles } from "lucide-react";
import { documentsService, Document } from "@/lib/documentsService";
import profileService from "@/lib/profile";
import { Profile } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface AnalysisModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  jobId: string;
  jobTitle: string;
  companyName?: string;
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
      const response = await fetch(`${API_URL}/jobs/${jobId}/compatibility/${selectedProfileId}`, {
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
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto backdrop-blur-xl bg-white/95 border-2 border-purple-200/50 shadow-2xl">
        <DialogHeader>
          <div className="flex items-center gap-4 mb-3">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 flex items-center justify-center shadow-lg animate-pulse">
              <Sparkles className="w-7 h-7 text-white" />
            </div>
            <div className="flex-1">
              <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                ✨ Analyse de compatibilité
              </DialogTitle>
              <DialogDescription className="text-base mt-1 font-medium text-gray-600">
                {jobTitle} {companyName && `• ${companyName}`}
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          {/* Score de compatibilité */}
          <div className="p-8 rounded-2xl bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 border-2 border-purple-200 shadow-lg text-center">
            <div className="flex justify-center mb-6">
              <div className="relative w-40 h-40">
                <svg className="transform -rotate-90 w-40 h-40">
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    stroke="#e5e7eb"
                    strokeWidth="12"
                    fill="none"
                  />
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    stroke="url(#gradient)"
                    strokeWidth="12"
                    fill="none"
                    strokeDasharray={`${2 * Math.PI * 70}`}
                    strokeDashoffset={`${2 * Math.PI * 70 * (1 - (compatibilityScore || 0) / 100)}`}
                    strokeLinecap="round"
                    className="transition-all duration-1000"
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#8b5cf6" />
                      <stop offset="50%" stopColor="#ec4899" />
                      <stop offset="100%" stopColor="#3b82f6" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  {loadingScore ? (
                    <Loader2 className="w-10 h-10 animate-spin text-purple-600" />
                  ) : compatibilityScore !== null ? (
                    <>
                      <span className="text-4xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                        {compatibilityScore}%
                      </span>
                    </>
                  ) : (
                    <span className="text-2xl text-gray-400">--</span>
                  )}
                </div>
              </div>
            </div>
            {compatibilityScore !== null && (
              <Badge className={`${getScoreColor(compatibilityScore)} text-white border-0 shadow-lg text-base px-4 py-2`}>
                {getScoreLabel(compatibilityScore)}
              </Badge>
            )}
            {loadingScore && (
              <p className="text-sm text-purple-600 mt-3 font-medium animate-pulse">
                🤖 Calcul du score avec l'IA...
              </p>
            )}
          </div>

          {/* Sélection du profil */}
          <div className="p-5 rounded-xl bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
            <label className="block text-sm font-bold mb-3 flex items-center gap-2 text-gray-700">
              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                <FileText className="w-3 h-3 text-white" />
              </div>
              Profil à utiliser pour postuler
            </label>
            {loading ? (
              <div className="flex items-center gap-2 text-sm text-blue-600">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Chargement des profils...</span>
              </div>
            ) : profiles.length === 0 ? (
              <div className="bg-red-50 border-2 border-red-200 text-red-700 p-3 rounded-lg text-sm flex items-center gap-2">
                <span className="text-lg">⚠️</span>
                <span>Vous devez créer un profil avant de générer des documents</span>
              </div>
            ) : (
              <Select value={selectedProfileId} onValueChange={setSelectedProfileId}>
                <SelectTrigger className="border-2 border-blue-300 hover:border-blue-400 bg-white">
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
          <div className="p-5 rounded-xl bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 border-2 border-green-200">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-md">
                <CheckCircle2 className="w-4 h-4 text-white" />
              </div>
              <h3 className="font-bold text-base bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                Analyse détaillée
              </h3>
            </div>
            <div className="h-px bg-gradient-to-r from-green-200 to-transparent mb-4" />
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-3 p-3 rounded-lg bg-white/60 border border-green-200">
                <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700">Compétences techniques correspondent bien</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-white/60 border border-green-200">
                <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700">Expérience alignée avec les exigences</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-yellow-50 border border-yellow-200">
                <span className="text-xl mt-0.5 flex-shrink-0">⚠️</span>
                <span className="text-gray-700">Points à améliorer : certifications manquantes</span>
              </div>
            </div>
          </div>

          {/* Erreur */}
          {error && (
            <div className="bg-gradient-to-r from-red-50 to-pink-50 border-2 border-red-300 text-red-700 px-5 py-4 rounded-xl shadow-lg flex items-start gap-3">
              <span className="text-2xl flex-shrink-0">❌</span>
              <span className="font-medium">{error}</span>
            </div>
          )}

          {/* Documents générés */}
          {generatedDocs && (
            <div className="bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 border-2 border-green-300 p-6 rounded-2xl shadow-xl space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-lg">
                  <CheckCircle2 className="w-6 h-6 text-white" />
                </div>
                <span className="text-lg font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                  ✅ Documents générés avec succès !
                </span>
              </div>
              
              <div className="space-y-3">
                {generatedDocs.cv && (
                  <div className="flex items-center justify-between bg-white p-4 rounded-xl border-2 border-green-200 hover:border-green-400 hover:shadow-lg transition-all duration-300">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                        <FileText className="w-5 h-5 text-white" />
                      </div>
                      <span className="text-sm font-semibold text-gray-700">{generatedDocs.cv.filename}</span>
                    </div>
                    <Button
                      size="sm"
                      className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white shadow-md"
                      onClick={() => handleDownload(generatedDocs.cv!.id, generatedDocs.cv!.filename)}
                    >
                      Télécharger
                    </Button>
                  </div>
                )}

                {generatedDocs.coverLetter && (
                  <div className="flex items-center justify-between bg-white p-4 rounded-xl border-2 border-green-200 hover:border-green-400 hover:shadow-lg transition-all duration-300">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                        <Mail className="w-5 h-5 text-white" />
                      </div>
                      <span className="text-sm font-semibold text-gray-700">{generatedDocs.coverLetter.filename}</span>
                    </div>
                    <Button
                      size="sm"
                      className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white shadow-md"
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
                className="w-full mt-4 border-2 border-green-400 hover:bg-green-50 hover:border-green-500"
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
            <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 border-2 border-blue-300 text-blue-800 p-5 rounded-2xl shadow-lg flex items-start gap-4">
              <Loader2 className="w-7 h-7 animate-spin mt-0.5 text-purple-600 flex-shrink-0" />
              <div className="flex-1">
                <p className="font-bold text-base mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  ⏳ Génération en cours...
                </p>
                <p className="text-sm text-gray-600">
                  L'IA personnalise vos documents. Cela peut prendre 1-2 minutes. Veuillez patienter.
                </p>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4">
            <div className="h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent w-full mb-3" />
            <Button 
              variant="outline" 
              onClick={() => onOpenChange(false)}
              className="border-2 border-gray-300 hover:border-gray-400"
            >
              Fermer
            </Button>
            
            {!generatedDocs && (
              <Button 
                onClick={handleGenerate}
                disabled={generating || profiles.length === 0 || !selectedProfileId}
                className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 hover:from-purple-700 hover:via-pink-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
              >
                {generating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
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

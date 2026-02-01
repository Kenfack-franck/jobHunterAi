"use client";

import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2, FileText, Mail, Download, Edit, Sparkles } from "lucide-react";
import { generateDocument, getDocumentStats } from "@/lib/documents";
import { GeneratedDocument, DocumentStatsResponse } from "@/types";
import { toast } from "sonner";

interface DocumentGeneratorProps {
  jobOfferId: string;
  jobTitle?: string;
  companyName?: string;
}

type DocumentType = "resume" | "cover_letter";
type Tone = "professional" | "creative" | "dynamic" | "enthusiastic" | "confident";
type Language = "fr" | "en";
type Length = "short" | "medium" | "long";

export default function DocumentGenerator({
  jobOfferId,
  jobTitle = "ce poste",
  companyName = "cette entreprise",
}: DocumentGeneratorProps) {
  // State pour les paramètres
  const [documentType, setDocumentType] = useState<DocumentType>("resume");
  const [tone, setTone] = useState<Tone>("professional");
  const [language, setLanguage] = useState<Language>("fr");
  const [length, setLength] = useState<Length>("medium");

  // State pour la génération
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedDoc, setGeneratedDoc] = useState<GeneratedDocument | null>(null);

  // State pour les statistiques
  const [stats, setStats] = useState<DocumentStatsResponse | null>(null);
  const [loadingStats, setLoadingStats] = useState(true);

  // Charger les statistiques au montage
  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('Non authentifié');
      }
      const data = await getDocumentStats(token);
      setStats(data);
    } catch (error) {
      console.error("Erreur chargement stats:", error);
    } finally {
      setLoadingStats(false);
    }
  };

  const handleGenerate = async () => {
    if (!stats?.can_generate) {
      toast.error("Limite quotidienne atteinte (10/10)");
      return;
    }

    setIsGenerating(true);
    setGeneratedDoc(null);

    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('Non authentifié');
      }
      
      const doc = await generateDocument({
        job_offer_id: jobOfferId,
        document_type: documentType,
        tone,
        language,
        length: documentType === "cover_letter" ? length : undefined,
      }, token);

      setGeneratedDoc(doc);
      toast.success(`${documentType === "resume" ? "CV" : "Lettre"} généré avec succès !`);

      // Recharger les stats
      await loadStats();
    } catch (error: any) {
      console.error("Erreur génération:", error);
      const message = error.response?.data?.detail || "Erreur lors de la génération";
      toast.error(message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    if (!generatedDoc) return;

    const filename = documentType === "resume"
      ? `CV_${companyName.replace(/\s+/g, "_")}_${new Date().toISOString().split("T")[0]}.txt`
      : `LM_${companyName.replace(/\s+/g, "_")}_${new Date().toISOString().split("T")[0]}.txt`;

    const blob = new Blob([generatedDoc.content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);

    toast.success("Document téléchargé");
  };

  const toneLabels: Record<Tone, string> = {
    professional: "Professionnel",
    creative: "Créatif",
    dynamic: "Dynamique",
    enthusiastic: "Enthousiaste",
    confident: "Confiant",
  };

  const lengthLabels: Record<Length, string> = {
    short: "Court (2 paragraphes)",
    medium: "Moyen (3-4 paragraphes)",
    long: "Long (5+ paragraphes)",
  };

  return (
    <Card className="p-6 space-y-6">
      {/* Header avec toggle et badge limite */}
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          <Button
            variant={documentType === "resume" ? "default" : "outline"}
            onClick={() => setDocumentType("resume")}
            className="gap-2"
          >
            <FileText className="w-4 h-4" />
            CV
          </Button>
          <Button
            variant={documentType === "cover_letter" ? "default" : "outline"}
            onClick={() => setDocumentType("cover_letter")}
            className="gap-2"
          >
            <Mail className="w-4 h-4" />
            Lettre de Motivation
          </Button>
        </div>

        {loadingStats ? (
          <Badge variant="secondary">Chargement...</Badge>
        ) : stats ? (
          <Badge
            variant={stats.can_generate ? "default" : "destructive"}
            className="text-sm"
          >
            {stats.remaining_today}/{stats.daily_limit} restant
            {stats.remaining_today === 0 && " 🚫"}
          </Badge>
        ) : null}
      </div>

      {/* Formulaire de paramètres */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Ton */}
        <div className="space-y-2">
          <Label>Ton</Label>
          <Select value={tone} onValueChange={(v) => setTone(v as Tone)}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(toneLabels).map(([value, label]) => (
                <SelectItem key={value} value={value}>
                  {label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Langue */}
        <div className="space-y-2">
          <Label>Langue</Label>
          <div className="flex gap-2">
            <Button
              type="button"
              variant={language === "fr" ? "default" : "outline"}
              onClick={() => setLanguage("fr")}
              className="flex-1"
            >
              🇫🇷 Français
            </Button>
            <Button
              type="button"
              variant={language === "en" ? "default" : "outline"}
              onClick={() => setLanguage("en")}
              className="flex-1"
            >
              🇬🇧 English
            </Button>
          </div>
        </div>

        {/* Longueur (lettres uniquement) */}
        {documentType === "cover_letter" && (
          <div className="space-y-2">
            <Label>Longueur</Label>
            <Select value={length} onValueChange={(v) => setLength(v as Length)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(lengthLabels).map(([value, label]) => (
                  <SelectItem key={value} value={value}>
                    {label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}
      </div>

      {/* Bouton de génération */}
      <Button
        onClick={handleGenerate}
        disabled={isGenerating || !stats?.can_generate}
        className="w-full gap-2"
        size="lg"
      >
        {isGenerating ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Génération en cours...
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            Générer {documentType === "resume" ? "le CV" : "la lettre de motivation"}
          </>
        )}
      </Button>

      {/* Message si limite atteinte */}
      {stats && !stats.can_generate && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
          <p className="text-red-800 font-medium">
            Limite quotidienne atteinte ({stats.daily_limit}/{stats.daily_limit})
          </p>
          <p className="text-red-600 text-sm mt-1">
            Revenez demain pour générer de nouveaux documents
          </p>
        </div>
      )}

      {/* Zone de prévisualisation */}
      {generatedDoc && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">
              {documentType === "resume" ? "📄 CV Généré" : "✉️ Lettre de Motivation"}
            </h3>
            <div className="flex gap-2">
              <Button onClick={handleDownload} variant="outline" size="sm" className="gap-2">
                <Download className="w-4 h-4" />
                Télécharger
              </Button>
              <Button
                onClick={() => setGeneratedDoc(null)}
                variant="outline"
                size="sm"
                className="gap-2"
              >
                <Edit className="w-4 h-4" />
                Nouveau
              </Button>
            </div>
          </div>

          {/* Contenu */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 max-h-[500px] overflow-y-auto">
            <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed">
              {generatedDoc.content}
            </pre>
          </div>

          {/* Métadonnées */}
          <div className="flex gap-4 text-sm text-gray-600">
            <span>📏 {generatedDoc.content.length} caractères</span>
            <span>
              🕐{" "}
              {new Date(generatedDoc.generated_at).toLocaleString("fr-FR", {
                day: "2-digit",
                month: "short",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
          </div>
        </div>
      )}
    </Card>
  );
}

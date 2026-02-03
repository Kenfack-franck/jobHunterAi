import { JobOffer } from "@/types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Sparkles, ExternalLink, MapPin, Building2, Globe, Save } from "lucide-react";

interface JobOfferCardProps {
  job: JobOffer;
  onClick?: () => void;
  onEdit?: () => void;
  onDelete?: () => void;
  onAnalyze?: () => void;
  onSave?: () => void;
}

export function JobOfferCard({ job, onClick, onEdit, onDelete, onAnalyze, onSave }: JobOfferCardProps) {
  const formatDate = (dateString?: string) => {
    if (!dateString) return "Date inconnue";
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return "Date inconnue";
      return date.toLocaleDateString("fr-FR", { day: "numeric", month: "short", year: "numeric" });
    } catch {
      return "Date inconnue";
    }
  };

  // Fonction pour nettoyer le HTML et extraire le texte
  const stripHtml = (html: string): string => {
    if (!html) return "";
    // Créer un élément temporaire pour parser le HTML
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    // Extraire le texte sans les balises
    return tmp.textContent || tmp.innerText || "";
  };

  const getSourceBadge = (source?: string) => {
    if (!source || source === "manual") {
      return <Badge variant="outline" className="text-xs">📝 Manuel</Badge>;
    }
    
    const sourceMap: { [key: string]: { label: string; emoji: string; color: string } } = {
      remoteok: { label: "RemoteOK", emoji: "🌐", color: "bg-blue-100 text-blue-800 border-blue-300" },
      indeed: { label: "Indeed", emoji: "💼", color: "bg-green-100 text-green-800 border-green-300" },
      wttj: { label: "WTTJ", emoji: "🚀", color: "bg-purple-100 text-purple-800 border-purple-300" },
    };
    
    const sourceInfo = sourceMap[source.toLowerCase()] || { label: source, emoji: "🔗", color: "bg-gray-100 text-gray-800 border-gray-300" };
    
    return (
      <Badge variant="outline" className={`text-xs ${sourceInfo.color}`}>
        {sourceInfo.emoji} {sourceInfo.label}
      </Badge>
    );
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start gap-2 mb-2">
          <div className="flex-1">
            <CardTitle className="text-lg leading-tight">{job.job_title}</CardTitle>
          </div>
          <div className="flex flex-col gap-1 items-end">
            {job.job_type && <Badge variant="secondary" className="text-xs">{job.job_type}</Badge>}
            {job.company_name && (
              <Badge variant="outline" className="text-xs">
                🏢 {job.company_name}
              </Badge>
            )}
          </div>
        </div>
        
        <div className="space-y-1 text-sm text-muted-foreground">
          {job.location && (
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <MapPin className="w-3 h-3" />
              <span>{job.location}</span>
            </div>
          )}
          {job.work_mode && (
            <div className="flex items-center gap-1 text-xs">
              <Badge variant="outline" className="text-xs">
                {job.work_mode === 'remote' && '🏠 Télétravail'}
                {job.work_mode === 'hybrid' && '🔀 Hybride'}
                {job.work_mode === 'onsite' && '🏢 Présentiel'}
              </Badge>
            </div>
          )}
        </div>
      </CardHeader>

      <CardContent>
        {job.description && (
          <p className="text-sm text-gray-600 mb-3 line-clamp-3">
            {stripHtml(job.description)}
          </p>
        )}

        {job.extracted_keywords && job.extracted_keywords.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-3">
            {job.extracted_keywords.slice(0, 8).map((keyword, idx) => (
              <Badge key={idx} variant="outline" className="text-xs px-2 py-0">
                {keyword}
              </Badge>
            ))}
            {job.extracted_keywords.length > 8 && (
              <Badge variant="outline" className="text-xs px-2 py-0">
                +{job.extracted_keywords.length - 8}
              </Badge>
            )}
          </div>
        )}

        <div className="flex justify-between items-center text-xs text-gray-500 mb-3">
          <span>Ajoutée le {formatDate(job.posted_date || job.scraped_at || job.created_at)}</span>
          {job.source_url && (
            <a 
              href={job.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="flex items-center gap-1 text-blue-600 hover:underline"
            >
              <Globe className="w-3 h-3" />
              Voir l&apos;offre
            </a>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
          {/* Bouton Voir détails - toujours visible */}
          {onClick && (
            <Button 
              variant="outline" 
              size="sm" 
              className="flex-1"
              onClick={onClick}
            >
              <ExternalLink className="w-4 h-4 mr-1" />
              Voir détails
            </Button>
          )}
          
          {/* Bouton Sauvegarder - uniquement pour offres non sauvegardées (offres scrapées sans user_id) */}
          {onSave && !job.user_id && job.source_platform && job.source_platform !== "manual" && (
            <Button 
              variant="outline" 
              size="sm" 
              className="flex-1"
              onClick={onSave}
            >
              <Save className="w-4 h-4 mr-1" />
              Sauvegarder
            </Button>
          )}
          
          {onAnalyze && (
            <Button 
              variant="default" 
              size="sm" 
              className="flex-1 bg-blue-600 hover:bg-blue-700"
              onClick={onAnalyze}
            >
              <Sparkles className="w-4 h-4 mr-1" />
              Analyser
            </Button>
          )}
          {onEdit && (
            <Button variant="ghost" size="sm" onClick={onEdit}>
              ✏️
            </Button>
          )}
          {onDelete && (
            <Button variant="ghost" size="sm" onClick={onDelete}>
              🗑️
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

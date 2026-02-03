"use client"
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { JobOffer, JobOfferSearchParams } from "@/types";
import jobOfferService from "@/lib/jobOffer";
import { SearchBar } from "@/components/jobs/SearchBar";
import { JobOfferCard } from "@/components/jobs/JobOfferCard";
import { AnalysisModal } from "@/components/jobs/AnalysisModal";
import { JobDetailsModal } from "@/components/jobs/JobDetailsModal";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { Loader2, CheckCircle2, XCircle, AlertCircle, RefreshCw, Briefcase, Plus } from "lucide-react";

export default function JobsPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [jobs, setJobs] = useState<JobOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useState<JobOfferSearchParams>({});
  const [searchStatus, setSearchStatus] = useState<"idle" | "searching" | "success" | "error">("idle");
  const [searchMessage, setSearchMessage] = useState("");
  const [scrapingProgress, setScrapingProgress] = useState<string>("");
  
  // Filtre d'affichage
  const [filter, setFilter] = useState<"all" | "saved" | "unsaved">("all");
  
  // Modal d'analyse
  const [selectedJob, setSelectedJob] = useState<JobOffer | null>(null);
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);
  
  // Modal de détails
  const [selectedJobForDetails, setSelectedJobForDetails] = useState<JobOffer | null>(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);

  useEffect(() => {
    // Attendre que l'auth soit chargé
    if (authLoading) return;
    
    if (!isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    
    // Charger les offres sauvegardées
    loadSavedJobs();
  }, [authLoading, isAuthenticated, router]);

  // Charger les offres sauvegardées depuis la DB
  const loadSavedJobs = async () => {
    setLoading(true);
    try {
      const savedJobs = await jobOfferService.getJobOffers(100, 0);
      setJobs(savedJobs);
      console.log(`✅ ${savedJobs.length} offre(s) sauvegardée(s) chargée(s)`);
    } catch (error: any) {
      console.error("Erreur chargement offres sauvegardées:", error);
      // Si erreur 401, l'utilisateur sera redirigé vers login
      if (error.response?.status === 401) {
        router.push("/auth/login");
      }
    } finally {
      setLoading(false);
    }
  };

  const loadJobs = async (params: JobOfferSearchParams = {}) => {
    setLoading(true);
    setSearchStatus("searching");
    setScrapingProgress("🔍 Recherche dans la base de données locale...");
    setSearchMessage("⏳ Recherche en cours... Veuillez patienter (peut prendre jusqu'à 30 secondes).");
    
    try {
      // Simulation d'étapes de progression pour le scraping
      const progressInterval = setInterval(() => {
        const messages = [
          "🌐 Connexion aux plateformes de recrutement...",
          "🤖 Scraping des sources prioritaires...",
          "📊 Extraction et analyse des offres...",
          "🔄 Traitement et déduplication...",
          "💾 Sauvegarde des nouvelles offres...",
        ];
        setScrapingProgress(messages[Math.floor(Math.random() * messages.length)]);
      }, 3000);
      
      const data = await jobOfferService.searchJobOffersWithScraping(params);
      
      clearInterval(progressInterval);
      
      // Feedback avec cache et sources
      if (data.cached) {
        setSearchMessage(`⚡ ${data.count} offre(s) depuis le cache (instantané !)`);
        setScrapingProgress(`📦 Sources: ${data.sources_used?.join(', ') || 'Toutes'}`);
      } else {
        setSearchMessage(`✅ ${data.count} offre(s) trouvée(s) !`);
        setScrapingProgress(`📦 Sources scrapées: ${data.sources_used?.join(', ') || 'Aucune'}`);
      }
      
      // Petite pause pour que l'utilisateur voie le message
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setJobs(data.offers);
      setSearchParams(params);
      
      if (data.count === 0) {
        setSearchStatus("idle");
        // Afficher le message du backend s'il existe, sinon message par défaut
        if (data.message) {
          setSearchMessage(`⚠️ ${data.message}`);
        } else {
          setSearchMessage("😞 Aucune offre trouvée. Essayez d'autres mots-clés ou une localisation différente.");
        }
        setScrapingProgress("");
      } else {
        setSearchStatus("success");
        // Clear success message after 5s
        setTimeout(() => {
          setSearchStatus("idle");
          setSearchMessage("");
        }, 5000);
      }
    } catch (error: any) {
      console.error("Erreur de chargement:", error);
      setSearchStatus("error");
      setScrapingProgress("");
      
      // Messages d'erreur plus descriptifs
      if (error.response?.status === 401) {
        setSearchMessage("❌ Session expirée. Veuillez vous reconnecter.");
      } else if (error.response?.status === 404) {
        setSearchMessage("❌ Endpoint introuvable. Vérifiez que le backend est démarré.");
      } else if (error.response?.status === 422) {
        // Erreur de validation - extraire le message
        const detail = error.response?.data?.detail;
        if (Array.isArray(detail)) {
          const firstError = detail[0];
          setSearchMessage(`❌ Erreur de validation : ${firstError.msg || 'Données invalides'}`);
        } else if (typeof detail === 'string') {
          setSearchMessage(`❌ ${detail}`);
        } else {
          setSearchMessage("❌ Erreur de validation. Vérifiez les paramètres de recherche.");
        }
      } else if (error.code === "ECONNABORTED" || error.message.includes("timeout")) {
        setSearchMessage("⏱️ Le scraping a pris trop de temps. Veuillez réessayer ou affiner votre recherche.");
      } else {
        const detail = error.response?.data?.detail;
        const errorMsg = typeof detail === 'string' ? detail : "❌ Erreur lors de la recherche. Veuillez réessayer.";
        setSearchMessage(errorMsg);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (params: JobOfferSearchParams) => {
    loadJobs(params);
  };

  const handleSave = async (job: JobOffer) => {
    try {
      // Sauvegarder l'offre en base de données
      const savedJob = await jobOfferService.createJobOffer({
        job_title: job.job_title,
        company_name: job.company_name,
        location: job.location,
        job_type: job.job_type,
        description: job.description,
        source_url: job.source_url,
        source_platform: job.source_platform
      });
      
      // Mettre à jour l'offre dans le state local en utilisant source_url comme clé unique
      // (car l'ID temporaire change après sauvegarde)
      setJobs(prevJobs => prevJobs.map(j => 
        j.source_url === job.source_url && j.job_title === job.job_title
          ? { ...savedJob } // Remplacer par l'offre complète sauvegardée
          : j
      ));
      
      alert("✅ Offre sauvegardée avec succès !");
    } catch (error) {
      console.error("Erreur de sauvegarde:", error);
      alert("❌ Erreur lors de la sauvegarde");
    }
  };

  const handleDelete = async (jobId: string) => {
    if (confirm("Supprimer cette offre ?")) {
      try {
        await jobOfferService.deleteJobOffer(jobId);
        // Retirer l'offre du state local au lieu de recharger
        setJobs(prevJobs => prevJobs.filter(j => j.id !== jobId));
        alert("✅ Offre supprimée");
      } catch (error) {
        console.error("Erreur de suppression:", error);
        alert("❌ Erreur lors de la suppression");
      }
    }
  };

  const handleAnalyze = async (job: JobOffer) => {
    // Si l'offre n'est pas sauvegardée (pas de user_id), la sauvegarder d'abord
    if (!job.user_id) {
      try {
        const savedJob = await jobOfferService.createJobOffer({
          job_title: job.job_title,
          company_name: job.company_name,
          location: job.location,
          job_type: job.job_type,
          description: job.description,
          source_url: job.source_url,
          source_platform: job.source_platform
        });
        
        // Mettre à jour dans le state en utilisant source_url comme clé
        setJobs(prevJobs => prevJobs.map(j => 
          j.source_url === job.source_url && j.job_title === job.job_title
            ? { ...savedJob }
            : j
        ));
        
        // Utiliser l'offre sauvegardée pour l'analyse
        setSelectedJob(savedJob);
      } catch (error) {
        console.error("Erreur de sauvegarde avant analyse:", error);
        alert("❌ Impossible de sauvegarder l'offre pour l'analyse");
        return;
      }
    } else {
      setSelectedJob(job);
    }
    
    setShowAnalysisModal(true);
  };

  const handleViewDetails = (job: JobOffer) => {
    setSelectedJobForDetails(job);
    setShowDetailsModal(true);
  };

  // Filtrer les offres selon le filtre actif
  const filteredJobs = jobs.filter(job => {
    if (filter === "saved") return job.user_id;
    if (filter === "unsaved") return !job.user_id;
    return true;
  });

  if (loading && jobs.length === 0 && searchStatus === "idle") {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-purple-50/30 relative">
      {/* Animated background blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-400/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <nav className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
              <Briefcase className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Recherche d&apos;Offres
            </h1>
          </div>
          <Button variant="outline" onClick={() => router.push("/dashboard")} className="hover:border-purple-400 transition-all">
            ← Retour
          </Button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-6 relative z-10">
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Status Messages */}
        {searchStatus !== "idle" && (
          <div className={`p-5 rounded-2xl border-2 flex items-center gap-3 shadow-lg backdrop-blur-sm transition-all ${
            searchStatus === "searching" ? "bg-gradient-to-r from-blue-50 to-blue-100 border-blue-300 text-blue-900" :
            searchStatus === "success" ? "bg-gradient-to-r from-green-50 to-green-100 border-green-300 text-green-900" :
            "bg-gradient-to-r from-red-50 to-red-100 border-red-300 text-red-900"
          }`}>
            {searchStatus === "searching" && <Loader2 className="w-6 h-6 animate-spin flex-shrink-0" />}
            {searchStatus === "success" && <CheckCircle2 className="w-6 h-6 flex-shrink-0" />}
            {searchStatus === "error" && <XCircle className="w-6 h-6 flex-shrink-0" />}
            <div className="flex-1">
              <p className="font-semibold text-base">{searchMessage}</p>
              {scrapingProgress && searchStatus === "searching" && (
                <p className="text-sm mt-1 opacity-80">{scrapingProgress}</p>
              )}
            </div>
          </div>
        )}

        {/* Filtres */}
        <div className="flex gap-3 justify-between items-center flex-wrap">
          <div className="flex gap-3 flex-wrap">
            <Button
              variant={filter === "all" ? "default" : "outline"}
              onClick={() => setFilter("all")}
              className={`flex items-center gap-2 transition-all ${filter === "all" ? "shadow-md" : "hover:border-purple-400"}`}
            >
              Tout
              <span className={`${filter === "all" ? "bg-white/20" : "bg-purple-100 text-purple-700"} px-2 py-0.5 rounded-full text-sm font-semibold`}>
                {jobs.length}
              </span>
            </Button>
            <Button
              variant={filter === "saved" ? "default" : "outline"}
              onClick={() => setFilter("saved")}
              className={`flex items-center gap-2 transition-all ${filter === "saved" ? "shadow-md" : "hover:border-green-400"}`}
            >
              Sauvegardées
              <span className={`${filter === "saved" ? "bg-white/20" : "bg-green-100 text-green-700"} px-2 py-0.5 rounded-full text-sm font-semibold`}>
                {jobs.filter(j => j.user_id).length}
              </span>
            </Button>
            <Button
              variant={filter === "unsaved" ? "default" : "outline"}
              onClick={() => setFilter("unsaved")}
              className={`flex items-center gap-2 transition-all ${filter === "unsaved" ? "shadow-md" : "hover:border-blue-400"}`}
            >
              Non sauvegardées
              <span className={`${filter === "unsaved" ? "bg-white/20" : "bg-blue-100 text-blue-700"} px-2 py-0.5 rounded-full text-sm font-semibold`}>
                {jobs.filter(j => !j.user_id).length}
              </span>
            </Button>
          </div>
          
          <Button
            variant="outline"
            size="sm"
            onClick={loadSavedJobs}
            disabled={loading}
            className="flex items-center gap-2 hover:border-purple-400 hover:shadow-md transition-all"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Recharger mes offres
          </Button>
        </div>

        <div className="flex justify-between items-center bg-white/70 backdrop-blur-sm rounded-2xl p-5 border-2 border-purple-100 shadow-sm">
          <h2 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            {filteredJobs.length} offre{filteredJobs.length > 1 ? "s" : ""} {
              filter === "saved" ? "sauvegardée" : 
              filter === "unsaved" ? "non sauvegardée" : 
              "trouvée"
            }{filteredJobs.length > 1 ? "s" : ""}
          </h2>
          <Button onClick={() => router.push("/jobs/add")} className="gap-2 shadow-md hover:shadow-lg transition-all">
            <Plus className="w-4 h-4" />
            Ajouter manuellement
          </Button>
        </div>

        {filteredJobs.length === 0 && !loading ? (
          <div className="text-center py-16 bg-white/70 backdrop-blur-sm rounded-3xl border-2 border-dashed border-purple-200 shadow-lg">
            <div className="p-4 rounded-full bg-gradient-to-br from-purple-100 to-pink-100 w-24 h-24 mx-auto mb-6 flex items-center justify-center">
              <AlertCircle className="w-12 h-12 text-purple-500" />
            </div>
            <p className="text-gray-700 mb-2 text-lg font-semibold">
              {filter === "all" && "Aucune offre trouvée"}
              {filter === "saved" && "Aucune offre sauvegardée"}
              {filter === "unsaved" && "Aucune offre non sauvegardée"}
            </p>
            <p className="text-sm text-gray-500 max-w-md mx-auto">
              {filter === "all" && "Essayez d'autres mots-clés ou ajoutez une offre manuellement"}
              {filter === "saved" && "Sauvegardez des offres pour les retrouver ici"}
              {filter === "unsaved" && "Toutes les offres ont été sauvegardées"}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredJobs.map((job, index) => (
              <JobOfferCard
                key={job.id || `${job.source_url}-${job.job_title}-${index}`}
                job={job}
                onClick={() => handleViewDetails(job)}
                onSave={() => handleSave(job)}
                onDelete={() => handleDelete(job.id)}
                onAnalyze={() => handleAnalyze(job)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Modal d'analyse */}
      {selectedJob && (
        <AnalysisModal
          open={showAnalysisModal}
          onOpenChange={setShowAnalysisModal}
          jobId={selectedJob.id}
          jobTitle={selectedJob.job_title}
          companyName={selectedJob.company_name}
        />
      )}

      {/* Modal de détails */}
      <JobDetailsModal
        job={selectedJobForDetails}
        open={showDetailsModal}
        onOpenChange={setShowDetailsModal}
        onSave={selectedJobForDetails && !selectedJobForDetails.user_id ? () => handleSave(selectedJobForDetails) : undefined}
        onAnalyze={selectedJobForDetails ? () => handleAnalyze(selectedJobForDetails) : undefined}
        isSaved={selectedJobForDetails?.user_id !== undefined}
      />
    </div>
  );
}

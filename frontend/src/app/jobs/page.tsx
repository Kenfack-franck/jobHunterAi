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
import { authService } from "@/lib/auth";
import { Loader2, CheckCircle2, XCircle, AlertCircle } from "lucide-react";

export default function JobsPage() {
  const router = useRouter();
  const [jobs, setJobs] = useState<JobOffer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useState<JobOfferSearchParams>({});
  const [searchStatus, setSearchStatus] = useState<"idle" | "searching" | "success" | "error">("idle");
  const [searchMessage, setSearchMessage] = useState("");
  const [scrapingProgress, setScrapingProgress] = useState<string>("");
  
  // Modal d'analyse
  const [selectedJob, setSelectedJob] = useState<JobOffer | null>(null);
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);
  
  // Modal de détails
  const [selectedJobForDetails, setSelectedJobForDetails] = useState<JobOffer | null>(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push("/auth/login");
      return;
    }
    loadJobs();
  }, [router]);

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
          "🤖 Scraping RemoteOK en cours...",
          "📊 Extraction et analyse des offres...",
          "🔄 Traitement et déduplication...",
          "💾 Sauvegarde des nouvelles offres...",
        ];
        setScrapingProgress(messages[Math.floor(Math.random() * messages.length)]);
      }, 3000);
      
      const data = await jobOfferService.searchJobOffers(params);
      
      clearInterval(progressInterval);
      
      // Feedback avec statistiques
      const dbOffers = data.filter(j => !j.source_platform || j.source_platform === "manual");
      const scrapedOffers = data.filter(j => j.source_platform && j.source_platform !== "manual");
      
      if (scrapedOffers.length > 0) {
        setSearchMessage(`✅ ${data.length} offre(s) trouvée(s) : ${dbOffers.length} en base + ${scrapedOffers.length} scrapées !`);
      } else {
        setSearchMessage(`✅ ${data.length} offre(s) trouvée(s) dans votre base de données.`);
      }
      
      setScrapingProgress("");
      
      // Petite pause pour que l'utilisateur voie le message
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setJobs(data);
      setSearchParams(params);
      
      if (data.length === 0) {
        setSearchStatus("idle");
        setSearchMessage("😞 Aucune offre trouvée. Essayez d'autres mots-clés ou une localisation différente.");
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
      } else if (error.code === "ECONNABORTED" || error.message.includes("timeout")) {
        setSearchMessage("⏱️ Le scraping a pris trop de temps. Veuillez réessayer ou affiner votre recherche.");
      } else {
        setSearchMessage(error.response?.data?.detail || "❌ Erreur lors de la recherche. Veuillez réessayer.");
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
      await jobOfferService.createJobOffer({
        job_title: job.job_title,
        company_name: job.company_name,
        location: job.location,
        job_type: job.job_type,
        description: job.description,
        source_url: job.source_url,
        source_platform: job.source_platform
      });
      
      // Recharger les offres pour inclure la nouvelle
      await loadJobs(searchParams);
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
        await loadJobs(searchParams);
      } catch (error) {
        console.error("Erreur de suppression:", error);
      }
    }
  };

  const handleAnalyze = (job: JobOffer) => {
    setSelectedJob(job);
    setShowAnalysisModal(true);
  };

  const handleViewDetails = (job: JobOffer) => {
    setSelectedJobForDetails(job);
    setShowDetailsModal(true);
  };

  if (loading && jobs.length === 0 && searchStatus === "idle") {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">🔍 Recherche d&apos;Offres</h1>
          <Button variant="outline" onClick={() => router.push("/dashboard")}>
            ← Retour
          </Button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-6">
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Status Messages */}
        {searchStatus !== "idle" && (
          <div className={`p-4 rounded-lg border flex items-center gap-3 ${
            searchStatus === "searching" ? "bg-blue-50 border-blue-200 text-blue-800" :
            searchStatus === "success" ? "bg-green-50 border-green-200 text-green-800" :
            "bg-red-50 border-red-200 text-red-800"
          }`}>
            {searchStatus === "searching" && <Loader2 className="w-5 h-5 animate-spin" />}
            {searchStatus === "success" && <CheckCircle2 className="w-5 h-5" />}
            {searchStatus === "error" && <XCircle className="w-5 h-5" />}
            <div className="flex-1">
              <p className="font-medium">{searchMessage}</p>
              {scrapingProgress && searchStatus === "searching" && (
                <p className="text-sm mt-1 opacity-75">{scrapingProgress}</p>
              )}
            </div>
          </div>
        )}

        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">
            {jobs.length} offre{jobs.length > 1 ? "s" : ""} trouvée{jobs.length > 1 ? "s" : ""}
          </h2>
          <Button onClick={() => router.push("/jobs/add")}>
            + Ajouter une offre manuellement
          </Button>
        </div>

        {jobs.length === 0 && !loading ? (
          <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed">
            <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 mb-2">Aucune offre trouvée</p>
            <p className="text-sm text-gray-400">
              Essayez d&apos;autres mots-clés ou ajoutez une offre manuellement
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobs.map((job) => (
              <JobOfferCard
                key={job.id}
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

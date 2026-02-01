"use client"
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { JobOffer } from "@/types";
import jobOfferService from "@/lib/jobOffer";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AnalysisModal } from "@/components/jobs/AnalysisModal";

export default function JobDetailPage() {
  const router = useRouter();
  const params = useParams();
  const jobId = params.id as string;
  
  const [job, setJob] = useState<JobOffer | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);

  useEffect(() => {
    loadJob();
  }, [jobId]);

  const loadJob = async () => {
    try {
      const data = await jobOfferService.getJobOfferById(jobId);
      setJob(data);
    } catch (error) {
      console.error("Erreur:", error);
      router.push("/jobs");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (confirm("Supprimer cette offre ?")) {
      try {
        await jobOfferService.deleteJobOffer(jobId);
        router.push("/jobs");
      } catch (error) {
        console.error("Erreur:", error);
      }
    }
  };

  const handleAnalyze = () => {
    setShowAnalysisModal(true);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Chargement...</p>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Offre non trouvée</p>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("fr-FR");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">{job.job_title}</h1>
          <Button variant="outline" onClick={() => router.push("/jobs")}>
            ← Retour aux offres
          </Button>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-3xl">{job.job_title}</CardTitle>
            <CardDescription className="text-xl">{job.company_name}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex gap-4 flex-wrap">
              {job.location && (
                <Badge variant="secondary">📍 {job.location}</Badge>
              )}
              {job.work_mode && (
                <Badge variant="secondary">💼 {job.work_mode}</Badge>
              )}
              {job.job_type && (
                <Badge variant="secondary">📋 {job.job_type}</Badge>
              )}
            </div>

            {job.description && (
              <div>
                <h3 className="font-semibold mb-2">Description</h3>
                <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
              </div>
            )}

            {job.requirements && (
              <div>
                <h3 className="font-semibold mb-2">Compétences requises</h3>
                <p className="text-gray-700 whitespace-pre-wrap">{job.requirements}</p>
              </div>
            )}

            {job.extracted_keywords && job.extracted_keywords.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Mots-clés</h3>
                <div className="flex gap-2 flex-wrap">
                  {job.extracted_keywords.map((keyword, idx) => (
                    <Badge key={idx} variant="default">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            <div className="border-t pt-4 text-sm text-gray-500">
              <p>Ajoutée le {formatDate(job.created_at)}</p>
              {job.analyzed_at && (
                <p>Analysée le {formatDate(job.analyzed_at)}</p>
              )}
            </div>

            <div className="flex gap-2 pt-4">
              <Button 
                className="flex-1 bg-blue-600 hover:bg-blue-700"
                onClick={handleAnalyze}
              >
                🤖 Analyser avec mon profil
              </Button>
              <Button variant="destructive" onClick={handleDelete}>
                🗑️ Supprimer
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>

      {/* Modal d'analyse */}
      {job && (
        <AnalysisModal
          open={showAnalysisModal}
          onOpenChange={setShowAnalysisModal}
          jobId={job.id}
          jobTitle={job.job_title}
          companyName={job.company_name}
        />
      )}
    </div>
  );
}

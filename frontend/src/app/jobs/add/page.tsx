"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import { JobOfferCreate } from "@/types";
import jobOfferService from "@/lib/jobOffer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function AddJobPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<JobOfferCreate>({
    job_title: "",
    company_name: "",
    location: "",
    job_type: "",
    description: "",
    requirements: "",
    source_url: "",
    source_platform: "Manual",
    extracted_keywords: [],
  });
  const [keywordInput, setKeywordInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (field: keyof JobOfferCreate, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleAddKeyword = () => {
    if (keywordInput.trim()) {
      setFormData((prev) => ({
        ...prev,
        extracted_keywords: [...(prev.extracted_keywords || []), keywordInput.trim()],
      }));
      setKeywordInput("");
    }
  };

  const handleRemoveKeyword = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      extracted_keywords: prev.extracted_keywords?.filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.job_title.trim()) {
      alert("Le titre du poste est requis");
      return;
    }

    setLoading(true);
    try {
      await jobOfferService.createJobOffer(formData);
      router.push("/jobs");
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur lors de la création de l offre");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Ajouter une Offre</h1>
          <Button variant="outline" onClick={() => router.push("/jobs")}>
            ← Retour
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Informations de l&apos;offre</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Titre du poste <span className="text-red-500">*</span>
                </label>
                <Input
                  value={formData.job_title}
                  onChange={(e) => handleChange("job_title", e.target.value)}
                  placeholder="Ex: Développeur Full Stack"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Entreprise</label>
                  <Input
                    value={formData.company_name}
                    onChange={(e) => handleChange("company_name", e.target.value)}
                    placeholder="Ex: TechCorp"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Localisation</label>
                  <Input
                    value={formData.location}
                    onChange={(e) => handleChange("location", e.target.value)}
                    placeholder="Ex: Paris, France"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Type de contrat</label>
                  <Input
                    value={formData.job_type}
                    onChange={(e) => handleChange("job_type", e.target.value)}
                    placeholder="Ex: CDI, CDD, Stage..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Source</label>
                  <Input
                    value={formData.source_platform}
                    onChange={(e) => handleChange("source_platform", e.target.value)}
                    placeholder="Ex: LinkedIn, Indeed..."
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">URL de l&apos;offre</label>
                <Input
                  value={formData.source_url}
                  onChange={(e) => handleChange("source_url", e.target.value)}
                  placeholder="https://..."
                  type="url"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <Textarea
                  value={formData.description}
                  onChange={(e) => handleChange("description", e.target.value)}
                  placeholder="Description du poste..."
                  rows={4}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Compétences requises</label>
                <Textarea
                  value={formData.requirements}
                  onChange={(e) => handleChange("requirements", e.target.value)}
                  placeholder="Compétences et qualifications..."
                  rows={3}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Mots-clés</label>
                <div className="flex gap-2 mb-2">
                  <Input
                    value={keywordInput}
                    onChange={(e) => setKeywordInput(e.target.value)}
                    placeholder="Ajouter un mot-clé"
                    onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), handleAddKeyword())}
                  />
                  <Button type="button" onClick={handleAddKeyword} variant="outline">
                    + Ajouter
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.extracted_keywords?.map((keyword, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm flex items-center gap-1"
                    >
                      {keyword}
                      <button
                        type="button"
                        onClick={() => handleRemoveKeyword(idx)}
                        className="text-red-500 hover:text-red-700"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex gap-2">
                <Button type="submit" className="flex-1" disabled={loading}>
                  {loading ? "Création..." : "Créer l offre"}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => router.push("/jobs")}
                >
                  Annuler
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

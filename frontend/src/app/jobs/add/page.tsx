"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import { JobOfferCreate } from "@/types";
import jobOfferService from "@/lib/jobOffer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Link2, FileText, Sparkles, Loader2, CheckCircle, AlertCircle } from "lucide-react";
import { toast } from "sonner";

export default function AddJobPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"text" | "manual">("text");
  
  // Text Parsing State
  const [jobText, setJobText] = useState("");
  const [parsingText, setParsingText] = useState(false);
  const [textParsed, setTextParsed] = useState(false);
  
  // Manual Form State
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

  const handleParseText = async () => {
    if (!jobText.trim()) {
      toast.error("Veuillez coller le texte de l'offre");
      return;
    }

    if (jobText.trim().length < 100) {
      toast.error("Le texte semble trop court. Collez l'offre complète.");
      return;
    }

    try {
      setParsingText(true);
      
      // Appeler l'API de parsing de texte
      const result = await jobOfferService.parseJobText(jobText);
      
      if (result.success) {
        // Remplir le formulaire avec les données extraites
        setFormData(result.job_offer);
        setTextParsed(true);
        toast.success("✅ " + result.message);
      } else {
        toast.error("⚠️ " + result.message);
      }
    } catch (error: any) {
      console.error("Erreur:", error);
      toast.error(error.message || "Erreur lors de l'analyse du texte");
    } finally {
      setParsingText(false);
    }
  };

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
      toast.error("Le titre du poste est requis");
      return;
    }

    setLoading(true);
    try {
      await jobOfferService.createJobOffer(formData);
      toast.success("✅ Offre enregistrée avec succès !");
      router.push("/jobs");
    } catch (error) {
      console.error("Erreur:", error);
      toast.error("Erreur lors de la création de l'offre");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold mb-2">Ajouter une Offre d'Emploi</h1>
            <p className="text-gray-600">
              Collez une URL pour analyse automatique ou remplissez manuellement
            </p>
          </div>
          <Button variant="outline" onClick={() => router.push("/jobs")}>
            ← Retour
          </Button>
        </div>

        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as "text" | "manual")} className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="text" className="gap-2">
              <FileText className="h-4 w-4" />
              Coller le texte
            </TabsTrigger>
            <TabsTrigger value="manual" className="gap-2">
              <FileText className="h-4 w-4" />
              Saisie manuelle
            </TabsTrigger>
          </TabsList>

          {/* Text Parsing Tab */}
          <TabsContent value="text" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary" />
                  Analyse Intelligente de Texte
                </CardTitle>
                <CardDescription>
                  Copiez-collez le texte complet de l'offre d'emploi. Notre IA va extraire automatiquement toutes les informations.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Textarea
                    placeholder="Collez ici le texte complet de l'offre (titre, entreprise, description, compétences requises...)"
                    value={jobText}
                    onChange={(e) => setJobText(e.target.value)}
                    disabled={parsingText}
                    rows={12}
                    className="font-mono text-sm"
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    💡 Exemple : Copiez tout le contenu d'une offre depuis LinkedIn, Indeed, ou un site carrières
                  </p>
                </div>

                <Button
                  onClick={handleParseText}
                  disabled={parsingText || !jobText.trim()}
                  className="w-full gap-2"
                  size="lg"
                >
                  {parsingText ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      Analyse en cours...
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-5 w-5" />
                      Analyser le texte avec l'IA
                    </>
                  )}
                </Button>

                {parsingText && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-center gap-3">
                      <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                      <div>
                        <p className="font-medium text-blue-900">Analyse en cours...</p>
                        <p className="text-sm text-blue-700">
                          Extraction automatique : titre, entreprise, localisation, type de contrat, description, compétences requises, mots-clés
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {textParsed && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center gap-3 mb-3">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <p className="font-medium text-green-900">Offre analysée avec succès !</p>
                    </div>
                    <p className="text-sm text-green-700 mb-3">
                      Les informations ont été extraites automatiquement. 
                      Vérifiez-les ci-dessous et modifiez si nécessaire.
                    </p>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => {
                        setTextParsed(false);
                        setJobText("");
                        setFormData({
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
                      }}
                    >
                      Analyser un autre texte
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>

            {textParsed && (
              <Card>
                <CardHeader>
                  <CardTitle>Informations Extraites</CardTitle>
                  <CardDescription>
                    Vérifiez et modifiez les informations avant de sauvegarder
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <FormFields
                      formData={formData}
                      handleChange={handleChange}
                      keywordInput={keywordInput}
                      setKeywordInput={setKeywordInput}
                      handleAddKeyword={handleAddKeyword}
                      handleRemoveKeyword={handleRemoveKeyword}
                    />

                    <div className="flex gap-3 pt-4">
                      <Button type="submit" disabled={loading} className="flex-1">
                        {loading ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Enregistrement...
                          </>
                        ) : (
                          "💾 Enregistrer l'offre"
                        )}
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Manual Entry Tab */}
          <TabsContent value="manual">
            <Card>
              <CardHeader>
                <CardTitle>Saisie Manuelle</CardTitle>
                <CardDescription>
                  Remplissez les informations de l'offre manuellement
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <FormFields
                    formData={formData}
                    handleChange={handleChange}
                    keywordInput={keywordInput}
                    setKeywordInput={setKeywordInput}
                    handleAddKeyword={handleAddKeyword}
                    handleRemoveKeyword={handleRemoveKeyword}
                  />

                  <div className="flex gap-3 pt-4">
                    <Button type="submit" disabled={loading} className="flex-1">
                      {loading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Enregistrement...
                        </>
                      ) : (
                        "💾 Enregistrer l'offre"
                      )}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

// Composant réutilisable pour les champs du formulaire
function FormFields({
  formData,
  handleChange,
  keywordInput,
  setKeywordInput,
  handleAddKeyword,
  handleRemoveKeyword
}: {
  formData: JobOfferCreate;
  handleChange: (field: keyof JobOfferCreate, value: any) => void;
  keywordInput: string;
  setKeywordInput: (value: string) => void;
  handleAddKeyword: () => void;
  handleRemoveKeyword: (index: number) => void;
}) {
  return (
    <>
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
              className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm flex items-center gap-1 cursor-pointer hover:bg-blue-200"
              onClick={() => handleRemoveKeyword(idx)}
            >
              {keyword}
              <span className="text-blue-500 ml-1">×</span>
            </span>
          ))}
        </div>
      </div>
    </>
  );
}

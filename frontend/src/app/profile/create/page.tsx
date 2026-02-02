"use client"
import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import profileService from "@/lib/profile";
import { ProfileForm } from "@/components/profile/ProfileForm";
import { CVUpload } from "@/components/profile/CVUpload";
import { CVReview } from "@/components/profile/CVReview";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { FileUp, PenSquare, ArrowLeft } from "lucide-react";

export default function CreateProfilePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [mode, setMode] = useState<'choice' | 'upload' | 'review' | 'manual'>('choice');
  const [parsedData, setParsedData] = useState<any>(null);

  // Support URL parameter from onboarding
  useEffect(() => {
    const urlMode = searchParams.get('mode');
    if (urlMode === 'upload' || urlMode === 'form') {
      setMode(urlMode === 'upload' ? 'upload' : 'manual');
    }
  }, [searchParams]);

  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    try {
      await profileService.createProfile(data);
      router.push("/profile");
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCVParsed = (data: any) => {
    setParsedData(data);
    setMode('review'); // Passer à la page de revue
  };

  const handleReviewConfirm = async (editedData: any) => {
    await handleSubmit(editedData);
  };

  // Écran de choix
  if (mode === 'choice') {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-3">
              Créez votre profil
            </h1>
            <p className="text-lg text-gray-600">
              Choisissez la méthode qui vous convient
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Option 1: Import CV */}
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-primary" onClick={() => setMode('upload')}>
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                  <FileUp className="w-8 h-8 text-primary" />
                </div>
                <CardTitle className="text-2xl">Import automatique</CardTitle>
                <CardDescription className="text-base mt-2">
                  Rapide et intelligent
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✓</span>
                  <span>Téléchargez votre CV PDF</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✓</span>
                  <span>L'IA extrait automatiquement vos informations</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">✓</span>
                  <span>Vérifiez et ajustez si nécessaire</span>
                </div>
                <div className="mt-4 pt-4 border-t text-center">
                  <span className="text-primary font-semibold">⏱️ ~30 secondes</span>
                </div>
              </CardContent>
            </Card>

            {/* Option 2: Formulaire manuel */}
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-primary" onClick={() => setMode('manual')}>
              <CardHeader className="text-center pb-4">
                <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                  <PenSquare className="w-8 h-8 text-blue-600" />
                </div>
                <CardTitle className="text-2xl">Saisie manuelle</CardTitle>
                <CardDescription className="text-base mt-2">
                  Contrôle total
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">✓</span>
                  <span>Remplissez le formulaire à votre rythme</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">✓</span>
                  <span>Contrôle précis sur chaque information</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-blue-600 font-bold">✓</span>
                  <span>Ajoutez vos expériences, formations, compétences</span>
                </div>
                <div className="mt-4 pt-4 border-t text-center">
                  <span className="text-blue-600 font-semibold">⏱️ ~5-10 minutes</span>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-8">
            <p className="text-sm text-gray-500">
              💡 Astuce : Utilisez l'import automatique pour gagner du temps, vous pourrez toujours modifier après !
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Écran d'upload CV
  if (mode === 'upload') {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-2xl mx-auto px-4">
          <Button
            variant="ghost"
            onClick={() => setMode('choice')}
            className="mb-6"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour au choix
          </Button>

          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Importez votre CV
            </h1>
            <p className="text-gray-600">
              L'IA va extraire automatiquement vos informations
            </p>
          </div>

          <CVUpload 
            onDataParsed={handleCVParsed}
            onError={(error) => console.error(error)}
          />

          <div className="mt-6 text-center">
            <Button
              variant="outline"
              onClick={() => setMode('manual')}
            >
              Ou remplir manuellement
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Écran formulaire (mode='manual')
  if (mode === 'manual') {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-2xl mx-auto px-4">
          <Button
            variant="ghost"
            onClick={() => {
              setParsedData(null);
              setMode('choice');
            }}
            className="mb-6"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour au choix
          </Button>

          <div className="mb-6">
            <h1 className="text-3xl font-bold mb-2">Créer votre profil</h1>
            <p className="text-gray-600">Remplissez vos informations professionnelles</p>
          </div>

          <ProfileForm 
            onSubmit={handleSubmit} 
            isLoading={isLoading}
          />
        </div>
      </div>
    );
  }

  // Écran de revue (mode='review')
  if (mode === 'review' && parsedData) {
    return (
      <CVReview 
        parsedData={parsedData}
        onConfirm={handleReviewConfirm}
        onCancel={() => {
          setParsedData(null);
          setMode('choice');
        }}
      />
    );
  }

  // Par défaut, retour au choix
  return null;
}

"use client";
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { X, ArrowRight, ArrowLeft, Check, Upload, Rocket, Target, Zap } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';

interface OnboardingWizardProps {
  onComplete: () => void;
  onSkip?: () => void;
}

export default function OnboardingWizard({ onComplete, onSkip }: OnboardingWizardProps) {
  const [step, setStep] = useState(1);
  const router = useRouter();
  const totalSteps = 3;

  const handleNext = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      handleComplete();
    }
  };

  const handlePrevious = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleComplete = () => {
    toast.success('Bienvenue sur Job Hunter AI ! 🎉');
    localStorage.setItem('onboarding_completed', 'true');
    onComplete();
  };

  const handleSkipAll = () => {
    if (onSkip) {
      onSkip();
    } else {
      handleComplete();
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-3xl relative">
        {/* Close Button */}
        <button
          onClick={handleSkipAll}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Progress Bar */}
        <div className="h-2 bg-gray-200 rounded-t-lg">
          <div
            className="h-full bg-primary transition-all duration-300"
            style={{ width: `${(step / totalSteps) * 100}%` }}
          />
        </div>

        <CardContent className="p-8">
          {/* Step 1: Welcome */}
          {step === 1 && (
            <div className="space-y-6 text-center">
              <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
                <Rocket className="h-10 w-10 text-primary" />
              </div>
              <div>
                <h2 className="text-3xl font-bold mb-3">Bienvenue sur Job Hunter AI ! 🎉</h2>
                <p className="text-gray-600 text-lg">
                  Votre assistant personnel pour automatiser la recherche d'emploi
                </p>
              </div>
              <div className="grid md:grid-cols-3 gap-4 pt-6">
                <Card className="border-2">
                  <CardContent className="pt-6 text-center">
                    <Target className="h-8 w-8 text-primary mx-auto mb-2" />
                    <h3 className="font-semibold mb-1">Recherche Ciblée</h3>
                    <p className="text-sm text-gray-600">Trouvez les offres qui matchent</p>
                  </CardContent>
                </Card>
                <Card className="border-2">
                  <CardContent className="pt-6 text-center">
                    <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
                    <h3 className="font-semibold mb-1">Documents IA</h3>
                    <p className="text-sm text-gray-600">CV et LM personnalisés</p>
                  </CardContent>
                </Card>
                <Card className="border-2">
                  <CardContent className="pt-6 text-center">
                    <Check className="h-8 w-8 text-primary mx-auto mb-2" />
                    <h3 className="font-semibold mb-1">Candidature Rapide</h3>
                    <p className="text-sm text-gray-600">Postulez en 1 clic</p>
                  </CardContent>
                </Card>
              </div>
              <p className="text-sm text-gray-500 pt-4">
                Ce guide vous aidera à configurer votre profil en 2 minutes ⏱️
              </p>
            </div>
          )}

          {/* Step 2: Profile Setup */}
          {step === 2 && (
            <div className="space-y-6">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Upload className="h-8 w-8 text-primary" />
                </div>
                <h2 className="text-3xl font-bold mb-2">Créez votre profil</h2>
                <p className="text-gray-600">
                  Deux options pour commencer rapidement
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <Card className="border-2 hover:border-primary/50 transition-all cursor-pointer group">
                  <CardHeader>
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                      <Upload className="h-6 w-6 text-blue-600" />
                    </div>
                    <CardTitle>Import CV (Rapide)</CardTitle>
                    <CardDescription>
                      Uploadez votre CV PDF et l'IA extrait automatiquement vos infos
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button
                      onClick={() => {
                        router.push('/profile?mode=upload');
                        handleComplete();
                      }}
                      className="w-full"
                      variant="outline"
                    >
                      Uploader mon CV
                    </Button>
                  </CardContent>
                </Card>

                <Card className="border-2 hover:border-primary/50 transition-all cursor-pointer group">
                  <CardHeader>
                    <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                      <Target className="h-6 w-6 text-green-600" />
                    </div>
                    <CardTitle>Formulaire Guidé</CardTitle>
                    <CardDescription>
                      Remplissez un formulaire étape par étape pour créer votre profil
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button
                      onClick={() => {
                        router.push('/profile?mode=form');
                        handleComplete();
                      }}
                      className="w-full"
                      variant="outline"
                    >
                      Créer manuellement
                    </Button>
                  </CardContent>
                </Card>
              </div>

              <div className="text-center">
                <Button variant="ghost" onClick={handleSkipAll}>
                  Je le ferai plus tard
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Tour */}
          {step === 3 && (
            <div className="space-y-6">
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="h-8 w-8 text-primary" />
                </div>
                <h2 className="text-3xl font-bold mb-2">Tour rapide des fonctionnalités</h2>
                <p className="text-gray-600">
                  Voici ce que vous pouvez faire avec Job Hunter AI
                </p>
              </div>

              <div className="space-y-4">
                <Card className="border-l-4 border-l-primary">
                  <CardContent className="pt-6">
                    <div className="flex gap-4">
                      <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-primary font-bold">1</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1">🔍 Recherchez des offres</h3>
                        <p className="text-sm text-gray-600">
                          Menu "Offres" → Recherche par mots-clés, localisation, type de contrat
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-l-4 border-l-blue-500">
                  <CardContent className="pt-6">
                    <div className="flex gap-4">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-blue-600 font-bold">2</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1">🤖 Analysez la compatibilité</h3>
                        <p className="text-sm text-gray-600">
                          Cliquez sur une offre → Obtenez un score IA + suggestions
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-l-4 border-l-green-500">
                  <CardContent className="pt-6">
                    <div className="flex gap-4">
                      <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-green-600 font-bold">3</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1">📄 Générez vos documents</h3>
                        <p className="text-sm text-gray-600">
                          CV et lettre de motivation personnalisés automatiquement par l'IA
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-l-4 border-l-purple-500">
                  <CardContent className="pt-6">
                    <div className="flex gap-4">
                      <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-purple-600 font-bold">4</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1">🏢 Surveillez des entreprises</h3>
                        <p className="text-sm text-gray-600">
                          Menu "Veille Entreprise" → Ajoutez vos entreprises cibles pour scraping auto
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between pt-8 border-t mt-8">
            <Button
              variant="ghost"
              onClick={handlePrevious}
              disabled={step === 1}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Précédent
            </Button>
            <div className="flex gap-2 items-center">
              {Array.from({ length: totalSteps }).map((_, idx) => (
                <div
                  key={idx}
                  className={`h-2 w-2 rounded-full transition-all ${
                    idx + 1 === step ? 'bg-primary w-8' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
            <Button onClick={handleNext}>
              {step === totalSteps ? (
                <>
                  Terminer
                  <Check className="ml-2 h-4 w-4" />
                </>
              ) : (
                <>
                  Suivant
                  <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

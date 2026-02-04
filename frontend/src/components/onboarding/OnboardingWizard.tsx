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
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
      <Card className="w-full max-w-3xl relative my-4 sm:my-0">
        {/* Close Button */}
        <button
          onClick={handleSkipAll}
          className="absolute top-2 right-2 sm:top-4 sm:right-4 text-gray-400 hover:text-gray-600 z-10"
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

        <CardContent className="p-4 sm:p-6 md:p-8">
          {/* Step 1: Welcome */}
          {step === 1 && (
            <div className="space-y-4 sm:space-y-6 text-center">
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
                <Rocket className="h-8 w-8 sm:h-10 sm:w-10 text-primary" />
              </div>
              <div>
                <h2 className="text-2xl sm:text-3xl font-bold mb-2 sm:mb-3 px-2">Bienvenue sur Job Hunter AI ! 🎉</h2>
                <p className="text-gray-600 text-base sm:text-lg px-2">
                  Votre assistant personnel pour la recherche d'emploi et de stage
                </p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 pt-4 sm:pt-6">
                <Card className="border-2">
                  <CardContent className="pt-4 sm:pt-6 text-center">
                    <Target className="h-6 w-6 sm:h-8 sm:w-8 text-primary mx-auto mb-2" />
                    <h3 className="font-semibold mb-1 text-sm sm:text-base">Recherche Multi-Sources</h3>
                    <p className="text-xs sm:text-sm text-gray-600">6+ plateformes simultanées</p>
                  </CardContent>
                </Card>
                <Card className="border-2">
                  <CardContent className="pt-4 sm:pt-6 text-center">
                    <Zap className="h-6 w-6 sm:h-8 sm:w-8 text-primary mx-auto mb-2" />
                    <h3 className="font-semibold mb-1 text-sm sm:text-base">Documents IA</h3>
                    <p className="text-xs sm:text-sm text-gray-600">CV et lettres personnalisés</p>
                  </CardContent>
                </Card>
                <Card className="border-2">
                  <CardContent className="pt-4 sm:pt-6 text-center">
                    <Check className="h-6 w-6 sm:h-8 sm:w-8 text-primary mx-auto mb-2" />
                    <h3 className="font-semibold mb-1 text-sm sm:text-base">Analyse IA</h3>
                    <p className="text-xs sm:text-sm text-gray-600">Score de compatibilité</p>
                  </CardContent>
                </Card>
              </div>
              <p className="text-xs sm:text-sm text-gray-500 pt-2 sm:pt-4">
                Ce guide vous aidera à configurer votre profil en 2 minutes ⏱️
              </p>
            </div>
          )}

          {/* Step 2: Profile Setup */}
          {step === 2 && (
            <div className="space-y-4 sm:space-y-6">
              <div className="text-center mb-4 sm:mb-6">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <Upload className="h-7 w-7 sm:h-8 sm:w-8 text-primary" />
                </div>
                <h2 className="text-2xl sm:text-3xl font-bold mb-2 px-2">Créez votre profil</h2>
                <p className="text-gray-600 text-sm sm:text-base px-2">
                  Deux options pour commencer rapidement
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <Card className="border-2 hover:border-primary/50 transition-all cursor-pointer group">
                  <CardHeader className="pb-3">
                    <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-2 sm:mb-3 group-hover:scale-110 transition-transform">
                      <Upload className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
                    </div>
                    <CardTitle className="text-base sm:text-lg">Import CV (Rapide) ⚡</CardTitle>
                    <CardDescription className="text-xs sm:text-sm">
                      Uploadez votre CV PDF et l'IA extrait automatiquement vos infos
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button
                      onClick={() => {
                        router.push('/profile?mode=upload');
                        handleComplete();
                      }}
                      className="w-full text-sm"
                      variant="outline"
                      size="sm"
                    >
                      Uploader mon CV
                    </Button>
                  </CardContent>
                </Card>

                <Card className="border-2 hover:border-primary/50 transition-all cursor-pointer group">
                  <CardHeader className="pb-3">
                    <div className="w-10 h-10 sm:w-12 sm:h-12 bg-green-100 rounded-lg flex items-center justify-center mb-2 sm:mb-3 group-hover:scale-110 transition-transform">
                      <Target className="h-5 w-5 sm:h-6 sm:w-6 text-green-600" />
                    </div>
                    <CardTitle className="text-base sm:text-lg">Formulaire Guidé</CardTitle>
                    <CardDescription className="text-xs sm:text-sm">
                      Remplissez un formulaire étape par étape pour créer votre profil
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button
                      onClick={() => {
                        router.push('/profile?mode=form');
                        handleComplete();
                      }}
                      className="w-full text-sm"
                      variant="outline"
                      size="sm"
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
            <div className="space-y-4 sm:space-y-6">
              <div className="text-center mb-4 sm:mb-6">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <Zap className="h-7 w-7 sm:h-8 sm:w-8 text-primary" />
                </div>
                <h2 className="text-2xl sm:text-3xl font-bold mb-2 px-2">Tour rapide des fonctionnalités</h2>
                <p className="text-gray-600 text-sm sm:text-base px-2">
                  Voici ce que vous pouvez faire avec Job Hunter AI
                </p>
              </div>

              <div className="space-y-3 sm:space-y-4">
                <Card className="border-l-4 border-l-primary">
                  <CardContent className="pt-4 sm:pt-6">
                    <div className="flex gap-3 sm:gap-4">
                      <div className="w-8 h-8 sm:w-10 sm:h-10 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-primary font-bold text-sm sm:text-base">1</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1 text-sm sm:text-base">🔍 Recherchez emplois & stages</h3>
                        <p className="text-xs sm:text-sm text-gray-600">
                          Menu "Offres" → 6+ plateformes simultanées (Indeed, LinkedIn, RemoteOK...)
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-l-4 border-l-blue-500">
                  <CardContent className="pt-4 sm:pt-6">
                    <div className="flex gap-3 sm:gap-4">
                      <div className="w-8 h-8 sm:w-10 sm:h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-blue-600 font-bold text-sm sm:text-base">2</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1 text-sm sm:text-base">🤖 Analysez la compatibilité</h3>
                        <p className="text-xs sm:text-sm text-gray-600">
                          Score IA (0-100%) pour chaque offre + suggestions personnalisées
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-l-4 border-l-green-500">
                  <CardContent className="pt-4 sm:pt-6">
                    <div className="flex gap-3 sm:gap-4">
                      <div className="w-8 h-8 sm:w-10 sm:h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-green-600 font-bold text-sm sm:text-base">3</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1 text-sm sm:text-base">📄 Générez vos documents</h3>
                        <p className="text-xs sm:text-sm text-gray-600">
                          CV et lettre personnalisés par l'IA en 30 secondes
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-l-4 border-l-purple-500">
                  <CardContent className="pt-4 sm:pt-6">
                    <div className="flex gap-3 sm:gap-4">
                      <div className="w-8 h-8 sm:w-10 sm:h-10 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-purple-600 font-bold text-sm sm:text-base">4</span>
                      </div>
                      <div>
                        <h3 className="font-bold mb-1 text-sm sm:text-base">📊 Suivez vos candidatures</h3>
                        <p className="text-xs sm:text-sm text-gray-600">
                          Menu "Candidatures" → Organisez et suivez l'état de chaque candidature
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between pt-6 sm:pt-8 border-t mt-6 sm:mt-8">
            <Button
              variant="ghost"
              onClick={handlePrevious}
              disabled={step === 1}
              size="sm"
              className="text-xs sm:text-sm"
            >
              <ArrowLeft className="mr-1 sm:mr-2 h-3 w-3 sm:h-4 sm:w-4" />
              <span className="hidden sm:inline">Précédent</span>
              <span className="sm:hidden">Préc.</span>
            </Button>
            <div className="flex gap-1.5 sm:gap-2 items-center">
              {Array.from({ length: totalSteps }).map((_, idx) => (
                <div
                  key={idx}
                  className={`h-1.5 sm:h-2 w-1.5 sm:w-2 rounded-full transition-all ${
                    idx + 1 === step ? 'bg-primary w-6 sm:w-8' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
            <Button onClick={handleNext} size="sm" className="text-xs sm:text-sm">
              {step === totalSteps ? (
                <>
                  Terminer
                  <Check className="ml-1 sm:ml-2 h-3 w-3 sm:h-4 sm:w-4" />
                </>
              ) : (
                <>
                  Suivant
                  <ArrowRight className="ml-1 sm:ml-2 h-3 w-3 sm:h-4 sm:w-4" />
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

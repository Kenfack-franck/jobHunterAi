"use client"
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";
import { useProfile } from "@/contexts/ProfileContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import OnboardingWizard from "@/components/onboarding/OnboardingWizard";
import { Briefcase, FileText, Settings, TrendingUp, Target, Sparkles, CheckCircle2, Clock } from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const { user } = useAuth();
  const { profile, hasProfile, completion } = useProfile();
  const [showOnboarding, setShowOnboarding] = useState(false);

  useEffect(() => {
    // Check if user has completed onboarding AND has a profile
    const onboardingCompleted = localStorage.getItem('onboarding_completed');
    
    // Show onboarding if: not completed OR no profile yet
    if (!onboardingCompleted && !hasProfile) {
      setShowOnboarding(true);
    }
  }, [hasProfile]);

  return (
    <ProtectedRoute>
      {showOnboarding && (
        <OnboardingWizard
          onComplete={() => setShowOnboarding(false)}
          onSkip={() => setShowOnboarding(false)}
        />
      )}
      <div className="space-y-8">
        {/* Hero Section */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 p-8 md:p-12">
          <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:20px_20px]" />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-6 h-6 text-yellow-300 animate-pulse" />
              <span className="text-white/80 text-sm font-medium">Votre espace de travail</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Bienvenue{user?.full_name ? `, ${user.full_name}` : ""} !
            </h1>
            <p className="text-white/90 text-lg max-w-2xl">
              Automatisez votre recherche d&apos;emploi, générez des candidatures personnalisées et trouvez l&apos;opportunité parfaite.
            </p>
          </div>
        </div>

        {/* Quick Stats */}
        {hasProfile && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200">
              <div className="flex items-center justify-between mb-2">
                <Target className="w-8 h-8 text-blue-600" />
                <TrendingUp className="w-4 h-4 text-blue-500" />
              </div>
              <div className="text-2xl font-bold text-blue-900">{completion}%</div>
              <div className="text-sm text-blue-700">Profil complété</div>
            </div>
            
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border border-purple-200">
              <Briefcase className="w-8 h-8 text-purple-600 mb-2" />
              <div className="text-2xl font-bold text-purple-900">{profile?.experiences?.length || 0}</div>
              <div className="text-sm text-purple-700">Expériences</div>
            </div>
            
            <div className="bg-gradient-to-br from-pink-50 to-pink-100 rounded-2xl p-6 border border-pink-200">
              <FileText className="w-8 h-8 text-pink-600 mb-2" />
              <div className="text-2xl font-bold text-pink-900">{profile?.skills?.length || 0}</div>
              <div className="text-sm text-pink-700">Compétences</div>
            </div>
            
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border border-green-200">
              <CheckCircle2 className="w-8 h-8 text-green-600 mb-2" />
              <div className="text-2xl font-bold text-green-900">18</div>
              <div className="text-sm text-green-700">Sources actives</div>
            </div>
          </div>
        )}

        {/* Main Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-blue-400 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-blue-100 group-hover:bg-blue-200 transition-colors">
                  <Target className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <CardTitle>Mon Profil</CardTitle>
                  <CardDescription>{hasProfile ? "Profil actif" : "Créez votre profil"}</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              {hasProfile ? (
                <>
                  <p className="text-sm mb-2"><strong>{profile?.title}</strong></p>
                  <div className="mb-4">
                    <div className="flex justify-between text-xs mb-1">
                      <span>Complétion</span>
                      <span>{completion}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${completion}%` }} />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Button className="w-full" onClick={() => router.push("/profile")}>Voir mon profil</Button>
                    <p className="text-xs text-gray-500 text-center">
                      {profile?.experiences?.length || 0} exp. | {profile?.educations?.length || 0} form. | {profile?.skills?.length || 0} comp.
                    </p>
                  </div>
                </>
              ) : (
                <>
                  <p className="text-sm text-gray-600 mb-4">Créez votre profil professionnel pour commencer</p>
                  <Button className="w-full" onClick={() => router.push("/profile/create")}>Créer mon profil</Button>
                </>
              )}
            </CardContent>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-purple-400 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-purple-100 group-hover:bg-purple-200 transition-colors">
                  <Briefcase className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <CardTitle>Recherche d&apos;Offres</CardTitle>
                  <CardDescription>Trouvez des opportunités</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <p className="text-sm text-gray-600 mb-4">Recherchez parmi des milliers d&apos;offres provenant de sources multiples</p>
              <Button className="w-full group-hover:bg-purple-600 transition-colors" onClick={() => router.push("/jobs")}>
                Voir les offres
              </Button>
            </CardContent>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-pink-400 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-pink-500/5 to-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-pink-100 group-hover:bg-pink-200 transition-colors">
                  <Settings className="w-6 h-6 text-pink-600" />
                </div>
                <div>
                  <CardTitle>Mes Sources</CardTitle>
                  <CardDescription>Personnalisez votre recherche</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-sm text-gray-600 mb-4 space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500" />
                  <span>18 sources disponibles</span>
                </div>
                <p className="text-xs pl-4">• 3 agrégateurs (RemoteOK, WTTJ, LinkedIn)</p>
                <p className="text-xs pl-4">• 15 grandes entreprises françaises</p>
              </div>
              <Button 
                className="w-full" 
                variant="outline"
                onClick={() => router.push("/settings/sources")}
              >
                Configurer
              </Button>
            </CardContent>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-indigo-400 relative overflow-hidden opacity-75">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-indigo-100 group-hover:bg-indigo-200 transition-colors">
                  <FileText className="w-6 h-6 text-indigo-600" />
                </div>
                <div>
                  <CardTitle>Documents IA</CardTitle>
                  <CardDescription>CV et lettres personnalisés</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <p className="text-sm text-gray-600 mb-4">Générez des candidatures adaptées avec l&apos;IA</p>
              <div className="flex items-center gap-2 mb-3">
                <Clock className="w-4 h-4 text-indigo-500" />
                <span className="text-xs text-indigo-600 font-medium">Disponible</span>
              </div>
              <Button variant="outline" className="w-full" disabled>
                Enregistrez des offres pour generer
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Success Banner */}
        {hasProfile && (
          <Card className="border-2 border-green-300 bg-gradient-to-r from-green-50 to-emerald-50 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-green-400/10 rounded-full -mr-16 -mt-16" />
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-full bg-green-100">
                  <CheckCircle2 className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <CardTitle className="text-green-900">Phase 2 Complète !</CardTitle>
                  <CardDescription className="text-green-700">Système de gestion de profil opérationnel</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-green-500" />
                <p className="text-sm text-green-800 font-medium">
                  Vous pouvez maintenant gérer votre profil professionnel complet et rechercher des offres !
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </ProtectedRoute>
  );
}

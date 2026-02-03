"use client"
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/contexts/AuthContext";
import { useProfile } from "@/contexts/ProfileContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import OnboardingWizard from "@/components/onboarding/OnboardingWizard";

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
      <div>
        <h2 className="text-3xl font-bold mb-2">
          Bienvenue{user?.full_name ? `, ${user.full_name}` : ""} !
        </h2>
        <p className="text-gray-600 mb-8">Votre dashboard pour automatiser votre recherche d emploi</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>📝 Mon Profil</CardTitle>
              <CardDescription>{hasProfile ? "Profil actif" : "Créez votre profil"}</CardDescription>
            </CardHeader>
            <CardContent>
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

          <Card>
            <CardHeader>
              <CardTitle>🔍 Recherche d Offres</CardTitle>
              <CardDescription>Trouvez des opportunités</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">Recherchez et gérez vos offres d emploi</p>
              <Button className="w-full" onClick={() => router.push("/jobs")}>Voir les offres</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>⚙️ Mes sources</CardTitle>
              <CardDescription>Personnalisez votre recherche</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-gray-600 mb-4 space-y-1">
                <p>18 sources disponibles</p>
                <p className="text-xs">• 3 agrégateurs (RemoteOK, WTTJ, LinkedIn)</p>
                <p className="text-xs">• 15 grandes entreprises françaises</p>
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

          <Card>
            <CardHeader>
              <CardTitle>🤖 Documents IA</CardTitle>
              <CardDescription>CV et lettres personnalisés</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">Générez des candidatures avec l IA</p>
              <Button variant="outline" className="w-full" disabled>Générer (Phase 4)</Button>
            </CardContent>
          </Card>
        </div>

        {hasProfile && (
          <div className="mt-8">
            <Card>
              <CardHeader>
                <CardTitle>✅ Phase 2 Complète !</CardTitle>
                <CardDescription>Système de gestion de profil opérationnel</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-green-600 font-medium">
                  🎉 Vous pouvez maintenant gérer votre profil professionnel complet !
                </p>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}

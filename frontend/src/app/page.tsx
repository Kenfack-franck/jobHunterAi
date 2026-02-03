"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle, Zap, Shield, TrendingUp, FileText, Search, Building2, Mail } from 'lucide-react';
import { ContactModal } from '@/components/contact/ContactModal';

export default function Home() {
  const router = useRouter();
  const [showContactModal, setShowContactModal] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Détecter l'authentification côté client uniquement (évite l'erreur d'hydratation)
  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated());
  }, []);

  const features = [
    {
      icon: Search,
      title: '🔍 Recherche Multi-Sources',
      description: 'Agrégation automatique d\'offres depuis LinkedIn, Indeed, RemoteOK et sites carrières d\'entreprises'
    },
    {
      icon: Building2,
      title: '🏢 Veille Entreprise',
      description: 'Surveillez les offres de vos entreprises cibles et soyez alerté dès qu\'un poste correspond'
    },
    {
      icon: FileText,
      title: '🤖 Documents IA Personnalisés',
      description: 'CV et lettres de motivation générés automatiquement et optimisés pour chaque offre'
    },
    {
      icon: Mail,
      title: '✉️ Candidature Automatisée',
      description: 'Envoyez vos candidatures par email directement depuis l\'application avec les documents générés'
    }
  ];

  const steps = [
    { number: '1', title: 'Créez votre profil', desc: 'Uploadez votre CV ou remplissez le formulaire guidé' },
    { number: '2', title: 'Recherchez & Analysez', desc: 'Trouvez des offres et obtenez un score de compatibilité IA' },
    { number: '3', title: 'Générez & Postulez', desc: 'L\'IA crée vos documents personnalisés, vous cliquez sur "Envoyer"' }
  ];

  const stats = [
    { value: '500+', label: 'Offres scrapées' },
    { value: '95%', label: 'Taux de compatibilité' },
    { value: '< 2min', label: 'Par candidature' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* NAVBAR */}
      <nav className="border-b bg-white/80 backdrop-blur-sm fixed top-0 w-full z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2 sm:gap-3">
            <span className="text-2xl sm:text-3xl">🎯</span>
            <div>
              <h1 className="font-bold text-lg sm:text-xl lg:text-2xl bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
                Job Hunter AI
              </h1>
              <p className="text-xs sm:text-sm text-gray-600 hidden sm:block">Votre assistant IA de recherche d'emploi</p>
            </div>
          </div>
          
          <div className="flex gap-2 sm:gap-3">
            {isAuthenticated ? (
              <Link href="/dashboard">
                <Button size="sm" className="text-sm sm:text-base">
                  <span className="hidden sm:inline">Mon Dashboard</span>
                  <span className="sm:hidden">Dashboard</span>
                </Button>
              </Link>
            ) : (
              <>
                <Link href="/auth/login">
                  <Button variant="outline" size="sm" className="text-sm sm:text-base">
                    <span className="hidden sm:inline">Se connecter</span>
                    <span className="sm:hidden">Login</span>
                  </Button>
                </Link>
                <Link href="/auth/register">
                  <Button size="sm" className="text-sm sm:text-base">
                    <span className="hidden sm:inline">Commencer gratuitement</span>
                    <span className="sm:hidden">Signup</span>
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="pt-24 sm:pt-32 pb-12 sm:pb-20 px-4 sm:px-6 bg-gradient-to-b from-blue-50 to-white">
        <div className="max-w-6xl mx-auto text-center space-y-6 sm:space-y-8">
          <div className="inline-block px-3 sm:px-4 py-2 bg-primary/10 rounded-full text-primary font-semibold text-xs sm:text-sm mb-4">
            🚀 L'assistant IA qui révolutionne la recherche d'emploi
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-extrabold leading-tight px-2">
            Trouvez votre job de rêve<br />
            <span className="bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
              en 10x moins de temps
            </span>
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-gray-600 max-w-3xl mx-auto px-4">
            Job Hunter AI automatise votre recherche d'emploi : scraping multi-sources, génération de CV/LM personnalisés par IA, et envoi de candidatures en un clic. Concentrez-vous sur les entretiens, on gère le reste.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-3 sm:gap-4 pt-4 px-4">
            {isAuthenticated ? (
              <>
                <Link href="/jobs" className="w-full sm:w-auto">
                  <Button size="lg" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6">
                    Rechercher des offres →
                  </Button>
                </Link>
                <Link href="/dashboard" className="w-full sm:w-auto">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6">
                    Accéder au Dashboard
                  </Button>
                </Link>
              </>
            ) : (
              <>
                <Link href="/auth/register" className="w-full sm:w-auto">
                  <Button size="lg" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6">
                    Commencer gratuitement →
                  </Button>
                </Link>
                <Link href="#how-it-works" className="w-full sm:w-auto">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6">
                    <span className="hidden sm:inline">Voir comment ça marche</span>
                    <span className="sm:hidden">En savoir plus</span>
                  </Button>
                </Link>
              </>
            )}
          </div>
          <div className="flex flex-col sm:flex-row justify-center gap-4 sm:gap-8 pt-6 sm:pt-8 px-4">
            {stats.map((stat, idx) => (
              <div key={idx} className="text-center">
                <p className="text-2xl sm:text-3xl md:text-4xl font-bold text-primary">{stat.value}</p>
                <p className="text-sm sm:text-base text-gray-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="py-12 sm:py-20 px-4 sm:px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-3 sm:mb-4">Fonctionnalités qui changent la donne</h2>
            <p className="text-gray-600 text-base sm:text-lg">Tout ce qu'il vous faut pour réussir votre recherche d'emploi</p>
          </div>
          <div className="grid sm:grid-cols-2 gap-6 sm:gap-8">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <Card key={idx} className="border-2 hover:border-primary/50 transition-all hover:shadow-lg">
                  <CardHeader>
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                      <Icon className="h-6 w-6 text-primary" />
                    </div>
                    <CardTitle className="text-2xl">{feature.title}</CardTitle>
                    <CardDescription className="text-base">{feature.description}</CardDescription>
                  </CardHeader>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" className="py-12 sm:py-20 px-4 sm:px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-3 sm:mb-4">Comment ça marche ?</h2>
            <p className="text-gray-600 text-base sm:text-lg">3 étapes simples pour décrocher votre prochain job</p>
          </div>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
            {steps.map((step, idx) => (
              <div key={idx} className="text-center">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary text-white rounded-full flex items-center justify-center text-xl sm:text-2xl font-bold mx-auto mb-3 sm:mb-4">
                  {step.number}
                </div>
                <h3 className="text-lg sm:text-xl font-bold mb-2">{step.title}</h3>
                <p className="text-sm sm:text-base text-gray-600">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA SECTION */}
      <section className="py-12 sm:py-20 px-4 sm:px-6 bg-gradient-to-r from-primary to-blue-600 text-white">
        <div className="max-w-4xl mx-auto text-center space-y-4 sm:space-y-6">
          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold px-2">Prêt à transformer votre recherche d'emploi ?</h2>
          <p className="text-base sm:text-lg md:text-xl text-blue-100 px-4">Rejoignez les professionnels qui utilisent l'IA pour trouver leur job idéal</p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center px-4">
            <Link href="/auth/register" className="w-full sm:w-auto">
              <Button size="lg" variant="outline" className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6 bg-white text-primary hover:bg-gray-100">
                Créer mon compte gratuitement →
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              onClick={() => setShowContactModal(true)}
              className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-4 sm:py-6 border-white text-white hover:bg-white/10"
            >
              Nous contacter
            </Button>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-gray-900 text-gray-400 py-12 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-white font-bold mb-4">Job Hunter AI</h3>
              <p className="text-sm">Votre assistant IA pour automatiser la recherche d'emploi</p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Produit</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#features" className="hover:text-white">Fonctionnalités</Link></li>
                <li><Link href="#how-it-works" className="hover:text-white">Comment ça marche</Link></li>
                <li><Link href="/auth/register" className="hover:text-white">Tarifs</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white">Documentation</Link></li>
                <li><Link href="#" className="hover:text-white">FAQ</Link></li>
                <li>
                  <button 
                    onClick={() => setShowContactModal(true)}
                    className="hover:text-white transition-colors"
                  >
                    Contact
                  </button>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Légal</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white">Confidentialité</Link></li>
                <li><Link href="#" className="hover:text-white">Conditions</Link></li>
                <li><Link href="#" className="hover:text-white">RGPD</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-sm">
            <p>© 2026 Job Hunter AI. Tous droits réservés.</p>
          </div>
        </div>
      </footer>

      {/* Modal de contact */}
      <ContactModal open={showContactModal} onOpenChange={setShowContactModal} />
    </div>
  );
}

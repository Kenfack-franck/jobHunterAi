"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";
import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle, Zap, Shield, TrendingUp, FileText, Search, Building2, Mail, ArrowRight, Sparkles, Target, Clock } from 'lucide-react';
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
      title: 'Recherche Multi-Sources',
      description: 'Agrégation automatique depuis LinkedIn, Indeed, RemoteOK et 50+ sites carrières',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Sparkles,
      title: 'IA Générative',
      description: 'CV et lettres de motivation personnalisés par GPT-4 pour chaque offre',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: Target,
      title: 'Score de Compatibilité',
      description: 'Analyse sémantique IA qui calcule votre match avec chaque poste',
      gradient: 'from-orange-500 to-red-500'
    },
    {
      icon: Clock,
      title: 'Gain de Temps 10x',
      description: 'Automatisez la recherche, génération de docs et envoi de candidatures',
      gradient: 'from-green-500 to-emerald-500'
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

      {/* HERO SECTION - Design Moderne */}
      <section className="relative pt-20 sm:pt-24 pb-12 sm:pb-20 px-4 sm:px-6 overflow-hidden">
        {/* Gradient Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 -z-10" />
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20 -z-10" />
        
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left: Content */}
            <div className="space-y-8 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-sm border border-gray-200">
                <Sparkles className="w-4 h-4 text-primary animate-pulse" />
                <span className="text-sm font-medium bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                  Propulsé par l'IA
                </span>
              </div>
              
              <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-[1.1] tracking-tight">
                Décrochez votre<br />
                <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  job/stage idéal
                </span>
                <br />en 10x moins de temps
              </h1>
              
              <p className="text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto lg:mx-0">
                L'IA qui automatise votre recherche d'emploi/stage de A à Z. Scraping intelligent, documents personnalisés, candidatures en 1 clic.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                {isAuthenticated ? (
                  <>
                    <Link href="/jobs">
                      <Button size="lg" className="group px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all">
                        Lancer une recherche
                        <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
                      </Button>
                    </Link>
                    <Link href="/dashboard">
                      <Button size="lg" variant="outline" className="px-8 py-6 text-lg">
                        Mon Dashboard
                      </Button>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link href="/auth/register">
                      <Button size="lg" className="group px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all">
                        Démarrer gratuitement
                        <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
                      </Button>
                    </Link>
                    <Link href="#features">
                      <Button size="lg" variant="outline" className="px-8 py-6 text-lg">
                        Découvrir
                      </Button>
                    </Link>
                  </>
                )}
              </div>
              
              {/* Stats */}
              <div className="flex flex-wrap justify-center lg:justify-start gap-8 pt-8">
                {stats.map((stat, idx) => (
                  <div key={idx}>
                    <p className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                      {stat.value}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">{stat.label}</p>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Right: Hero Image */}
            <div className="relative hidden lg:block">
              <div className="relative w-full aspect-square">
                {/* Placeholder avec gradient et texte pour l'image */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 via-purple-500/20 to-pink-500/20 rounded-3xl backdrop-blur-sm border border-white/20 shadow-2xl flex items-center justify-center">
                  <div className="text-center p-8">
                    <div className="w-32 h-32 mx-auto mb-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center">
                      <Sparkles className="w-16 h-16 text-white" />
                    </div>
                    <p className="text-gray-600 text-lg font-medium">
                      📸 Placez votre image hero ici
                    </p>
                    <p className="text-gray-500 text-sm mt-2">
                      /public/hero.jpg (1200x1200px)
                    </p>
                    <p className="text-gray-400 text-xs mt-4 max-w-sm mx-auto">
                      Suggestion: Photo d'une personne satisfaite devant un dashboard moderne avec des graphiques de succès
                    </p>
                  </div>
                </div>
                
                <Image 
                  src="/hero.jpg" 
                  alt="Job Hunter AI Dashboard" 
                  fill
                  className="object-cover rounded-3xl shadow-2xl"
                  priority
                />
                
              </div>
              
              {/* Floating Elements */}
              <div className="absolute -top-4 -left-4 w-24 h-24 bg-blue-500 rounded-2xl opacity-20 blur-xl animate-pulse" />
              <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-purple-500 rounded-2xl opacity-20 blur-xl animate-pulse delay-700" />
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION - Modern Cards */}
      <section id="features" className="py-20 px-4 sm:px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-block px-4 py-2 bg-primary/10 rounded-full text-primary font-semibold text-sm mb-6">
              ✨ Fonctionnalités
            </div>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4">
              Tout ce dont vous avez besoin
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Une suite complète d'outils IA pour transformer votre recherche d'emploi
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <div 
                  key={idx} 
                  className="group relative bg-white rounded-2xl p-8 border border-gray-200 hover:border-transparent hover:shadow-2xl transition-all duration-300"
                >
                  {/* Gradient Border on Hover */}
                  <div className={`absolute inset-0 rounded-2xl bg-gradient-to-r ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity -z-10 blur-xl`} />
                  
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                  <p className="text-gray-600 text-lg leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS - Visual Timeline */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-block px-4 py-2 bg-primary/10 rounded-full text-primary font-semibold text-sm mb-6">
              ⚡ Simple & Rapide
            </div>
            <h2 className="text-4xl sm:text-5xl font-bold mb-4">
              3 étapes vers le succès
            </h2>
            <p className="text-xl text-gray-600">
              De l'inscription à l'entretien en moins d'une heure
            </p>
          </div>
          
          <div className="relative">
            {/* Timeline Line */}
            <div className="hidden md:block absolute top-24 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full" 
                 style={{width: 'calc(100% - 12rem)', margin: '0 6rem'}} 
            />
            
            <div className="grid md:grid-cols-3 gap-8 md:gap-4">
              {steps.map((step, idx) => (
                <div key={idx} className="relative">
                  <div className="flex flex-col items-center text-center">
                    {/* Number Circle */}
                    <div className="relative z-10 w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-2xl flex items-center justify-center text-2xl font-bold mb-6 shadow-xl">
                      {step.number}
                      <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl blur-xl opacity-50 -z-10" />
                    </div>
                    
                    <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA SECTION - Modern Gradient */}
      <section className="relative py-24 px-4 sm:px-6 overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600" />
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />
        
        {/* Floating Orbs */}
        <div className="absolute top-10 left-10 w-72 h-72 bg-blue-400 rounded-full blur-3xl opacity-20 animate-pulse" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-400 rounded-full blur-3xl opacity-20 animate-pulse delay-1000" />
        
        <div className="relative max-w-4xl mx-auto text-center space-y-8 text-white">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
            <Sparkles className="w-4 h-4 animate-pulse" />
            <span className="text-sm font-medium">Gratuit • Sans carte bancaire • Accès immédiat</span>
          </div>
          
          <h2 className="text-4xl sm:text-5xl md:text-6xl font-black leading-tight">
            Prêt à décrocher<br />votre prochain job ?
          </h2>
          
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Rejoignez les centaines de professionnels qui utilisent l'IA pour automatiser leur recherche d'emploi
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link href="/auth/register">
              <Button 
                size="lg" 
                className="group bg-white text-primary hover:bg-gray-100 px-10 py-7 text-lg font-semibold shadow-2xl"
              >
                Commencer gratuitement
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Button
              size="lg"
              variant="outline"
              onClick={() => setShowContactModal(true)}
              className="px-10 py-7 text-lg border-2 border-white text-white hover:bg-white/10 backdrop-blur-sm"
            >
              Nous contacter
            </Button>
          </div>
          
          <p className="text-sm text-blue-200 pt-4">
            ✨ Aucune installation requise • 🚀 Prêt en 2 minutes • 💪 Support francophone
          </p>
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

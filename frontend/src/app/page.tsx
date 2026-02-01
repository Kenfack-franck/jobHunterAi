"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle, Zap, Shield, TrendingUp, FileText, Search, Building2, Mail } from 'lucide-react';

export default function Home() {
  const router = useRouter();

  // Rediriger vers dashboard si déjà connecté
  useEffect(() => {
    if (authService.isAuthenticated()) {
      router.push("/dashboard");
    }
  }, [router]);

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
    <div className="min-h-screen">
      {/* NAVBAR */}
      <nav className="border-b bg-white/80 backdrop-blur-sm fixed top-0 w-full z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
            Job Hunter AI
          </h1>
          <div className="flex items-center gap-4">
            <Link href="#features"><Button variant="ghost">Fonctionnalités</Button></Link>
            <Link href="#how-it-works"><Button variant="ghost">Comment ça marche</Button></Link>
            <Link href="/auth/login"><Button variant="outline">Se connecter</Button></Link>
            <Link href="/auth/register"><Button>Commencer →</Button></Link>
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="pt-32 pb-20 px-6 bg-gradient-to-b from-blue-50 to-white">
        <div className="max-w-6xl mx-auto text-center space-y-8">
          <div className="inline-block px-4 py-2 bg-primary/10 rounded-full text-primary font-semibold text-sm mb-4">
            🚀 L'assistant IA qui révolutionne la recherche d'emploi
          </div>
          <h1 className="text-6xl md:text-7xl font-extrabold leading-tight">
            Trouvez votre job de rêve<br />
            <span className="bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
              en 10x moins de temps
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Job Hunter AI automatise votre recherche d'emploi : scraping multi-sources, génération de CV/LM personnalisés par IA, et envoi de candidatures en un clic. Concentrez-vous sur les entretiens, on gère le reste.
          </p>
          <div className="flex justify-center gap-4 pt-4">
            <Link href="/auth/register">
              <Button size="lg" className="text-lg px-8 py-6">
                Commencer gratuitement →
              </Button>
            </Link>
            <Link href="#how-it-works">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                Voir comment ça marche
              </Button>
            </Link>
          </div>
          <div className="flex justify-center gap-8 pt-8">
            {stats.map((stat, idx) => (
              <div key={idx} className="text-center">
                <p className="text-4xl font-bold text-primary">{stat.value}</p>
                <p className="text-gray-600">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="py-20 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Fonctionnalités qui changent la donne</h2>
            <p className="text-gray-600 text-lg">Tout ce qu'il vous faut pour réussir votre recherche d'emploi</p>
          </div>
          <div className="grid md:grid-cols-2 gap-8">
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
      <section id="how-it-works" className="py-20 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Comment ça marche ?</h2>
            <p className="text-gray-600 text-lg">3 étapes simples pour décrocher votre prochain job</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, idx) => (
              <div key={idx} className="text-center">
                <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  {step.number}
                </div>
                <h3 className="text-xl font-bold mb-2">{step.title}</h3>
                <p className="text-gray-600">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA SECTION */}
      <section className="py-20 px-6 bg-gradient-to-r from-primary to-blue-600 text-white">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h2 className="text-4xl md:text-5xl font-bold">Prêt à transformer votre recherche d'emploi ?</h2>
          <p className="text-xl text-blue-100">Rejoignez les professionnels qui utilisent l'IA pour trouver leur job idéal</p>
          <Link href="/auth/register">
            <Button size="lg" variant="outline" className="text-lg px-8 py-6 bg-white text-primary hover:bg-gray-100">
              Créer mon compte gratuitement →
            </Button>
          </Link>
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
                <li><Link href="#" className="hover:text-white">Contact</Link></li>
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
    </div>
  );
}

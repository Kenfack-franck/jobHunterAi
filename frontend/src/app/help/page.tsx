"use client";
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  ChevronDown, ChevronUp, Search, Book, HelpCircle, Video, MessageCircle, 
  Briefcase, FileText, Target, Sparkles, CheckCircle, ArrowRight, Settings,
  Users, Database, Mail, PlayCircle, ExternalLink
} from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

interface FAQItem {
  question: string;
  answer: string;
  category: string;
  tags?: string[];
}

interface GuideStep {
  title: string;
  description: string;
  icon: any;
  link?: string;
}

export default function HelpPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const quickStartGuide: GuideStep[] = [
    {
      title: '1. Créez votre profil',
      description: 'Uploadez votre CV ou remplissez le formulaire guidé pour créer votre profil professionnel',
      icon: FileText,
      link: '/profile/create'
    },
    {
      title: '2. Configurez vos sources',
      description: 'Sélectionnez les 17 sources d\'offres (Adzuna, RemoteOK, entreprises cibles)',
      icon: Settings,
      link: '/settings/sources'
    },
    {
      title: '3. Recherchez des offres',
      description: 'Utilisez la recherche multi-sources avec mots-clés, localisation et filtres',
      icon: Search,
      link: '/jobs'
    },
    {
      title: '4. Analysez et sauvegardez',
      description: 'Analysez chaque offre avec l\'IA et sauvegardez celles qui vous intéressent',
      icon: Sparkles,
      link: '/jobs'
    },
    {
      title: '5. Suivez vos candidatures',
      description: 'Gérez vos candidatures et mettez à jour leur statut au fil du processus',
      icon: Target,
      link: '/applications'
    }
  ];

  const faqs: FAQItem[] = [
    // DÉMARRAGE
    {
      category: '🚀 Démarrage',
      question: 'Comment créer mon premier profil ?',
      answer: 'Allez dans "Mon Profil" → "Créer un profil". Vous avez 2 options : (1) Uploader votre CV en PDF pour extraction automatique par l\'IA, ou (2) Remplir le formulaire guidé étape par étape. Conseil : l\'upload CV est plus rapide !',
      tags: ['profil', 'cv', 'démarrage']
    },
    {
      category: '🚀 Démarrage',
      question: 'Puis-je avoir plusieurs profils ?',
      answer: 'Oui ! Vous pouvez créer plusieurs variantes de profil (ex: "Backend Developer", "Data Engineer", "Fullstack"). Cela permet d\'adapter vos candidatures selon les types de postes. Astuce : dupliquez un profil existant pour gagner du temps.',
      tags: ['profil', 'multiple']
    },
    {
      category: '🚀 Démarrage',
      question: 'Comment configurer mes sources d\'offres ?',
      answer: 'Allez dans "Sources" (menu latéral). Vous verrez 17 sources disponibles : Adzuna (15 entreprises françaises) + RemoteOK + Custom. Sélectionnez celles qui vous intéressent et cliquez sur "Sauvegarder les préférences". Vos recherches utiliseront uniquement ces sources.',
      tags: ['sources', 'configuration', 'adzuna']
    },

    // RECHERCHE D\'OFFRES
    {
      category: '🔍 Recherche d\'Offres',
      question: 'Comment rechercher des offres d\'emploi ?',
      answer: 'Allez dans "Offres d\'emploi" → Remplissez le formulaire : (1) Intitulé du poste (ex: "Ingénieur", "Développeur"), (2) Mode de travail (Télétravail/Présentiel), (3) Localisation (ex: "Paris", "France"), (4) Type de contrat. Cliquez sur "🔍 Rechercher". Le système agrège les offres de vos sources activées.',
      tags: ['recherche', 'offres', 'jobs']
    },
    {
      category: '🔍 Recherche d\'Offres',
      question: 'Pourquoi je n\'obtiens aucun résultat ?',
      answer: 'Vérifiez : (1) Avez-vous activé au moins une source dans "Sources" ? (2) Utilisez des mots-clés simples ("Développeur", "Ingénieur") plutôt que trop spécifiques. (3) Essayez "Télétravail" au lieu de "Présentiel" pour plus de résultats. (4) Élargissez la localisation ("France" au lieu d\'une ville).',
      tags: ['recherche', 'problème', 'résultats']
    },
    {
      category: '🔍 Recherche d\'Offres',
      question: 'Quelles sont les 17 sources disponibles ?',
      answer: '15 entreprises via Adzuna API (Capgemini, Sopra Steria, Thales, Airbus, Safran, Dassault, Orange, EDF, Engie, Atos, L\'Oréal, Schneider Electric, Renault, PSA, Veolia) + RemoteOK (remote jobs) + Custom sources (personnalisées). Total : 1000+ offres quotidiennes.',
      tags: ['sources', 'liste', 'entreprises']
    },
    {
      category: '🔍 Recherche d\'Offres',
      question: 'Comment sauvegarder une offre ?',
      answer: 'Cliquez sur le bouton "💾 Sauvegarder" sur une carte d\'offre. L\'offre sera enregistrée dans votre base de données et accessible via le bouton "🔄 Recharger mes offres" en haut de la page. Vous pouvez aussi l\'analyser avant de sauvegarder.',
      tags: ['sauvegarder', 'offres']
    },
    {
      category: '🔍 Recherche d\'Offres',
      question: 'Comment fonctionne l\'analyse d\'offre ?',
      answer: 'Cliquez sur "✨ Analyser" sur une offre. L\'IA compare l\'offre avec votre profil et génère : (1) Score de compatibilité, (2) Points forts de votre candidature, (3) Compétences manquantes, (4) Conseils personnalisés. L\'offre est automatiquement sauvegardée après analyse.',
      tags: ['analyse', 'ia', 'offres']
    },

    // VEILLE ENTREPRISE
    {
      category: '🏢 Veille Entreprise',
      question: 'Comment fonctionne la veille entreprise ?',
      answer: 'Dans "Veille Entreprise", ajoutez le nom et l\'URL de la page carrières de vos entreprises cibles (ex: "Safran", "https://careers.safran-group.com/jobs"). Notre système scrapera automatiquement leurs nouvelles offres toutes les 4 heures et vous notifiera par email.',
      tags: ['veille', 'entreprise', 'scraping']
    },
    {
      category: '🏢 Veille Entreprise',
      question: 'Quelles entreprises puis-je surveiller ?',
      answer: 'Toutes les entreprises ayant une page carrières publique (non protégée par login). Fonctionne mieux avec : pages carrières Workday, Greenhouse, Lever, BambooHR, et sites custom. Testez avec le bouton "Tester" avant d\'activer la veille.',
      tags: ['veille', 'entreprise']
    },
    {
      category: '🏢 Veille Entreprise',
      question: 'Comment recevoir les alertes de veille ?',
      answer: 'Les alertes sont envoyées par email à l\'adresse de votre compte. Fréquence : toutes les 4 heures. Vous recevez un email uniquement s\'il y a de nouvelles offres. Vous pouvez désactiver une veille à tout moment en cliquant sur "Désactiver".',
      tags: ['veille', 'alertes', 'email']
    },

    // CANDIDATURES
    {
      category: '📤 Candidatures',
      question: 'Comment suivre mes candidatures ?',
      answer: 'Allez dans "Candidatures" pour voir toutes vos candidatures sauvegardées. Pour chaque offre, vous pouvez : (1) Voir les détails, (2) Mettre à jour le statut (En attente, En cours, Acceptée, Refusée), (3) Ajouter des notes, (4) Supprimer. Le tableau de bord affiche des statistiques en temps réel.',
      tags: ['candidatures', 'suivi', 'statut']
    },
    {
      category: '📤 Candidatures',
      question: 'Comment mettre à jour le statut d\'une candidature ?',
      answer: 'Sur la page "Candidatures", cliquez sur le menu déroulant du statut de n\'importe quelle candidature. Sélectionnez le nouveau statut : "En attente" (par défaut), "En cours" (entretien planifié), "Acceptée" (offre reçue), ou "Refusée". Les statistiques se mettent à jour automatiquement.',
      tags: ['candidatures', 'statut', 'mise à jour']
    },
    {
      category: '📤 Candidatures',
      question: 'Puis-je supprimer une candidature ?',
      answer: 'Oui. Cliquez sur l\'icône poubelle (🗑️) sur la carte de la candidature. Confirmation vous sera demandée. Attention : cette action est irréversible. Les statistiques sont recalculées après suppression.',
      tags: ['candidatures', 'supprimer']
    },

    // DOCUMENTS
    {
      category: '📄 Documents',
      question: 'Puis-je télécharger mes documents générés ?',
      answer: 'Oui ! Tous les documents (CV, lettres de motivation) générés par l\'IA sont disponibles dans "Mes Documents". Vous pouvez les télécharger en PDF, les prévisualiser, ou les régénérer avec un autre template. Tous vos documents sont conservés.',
      tags: ['documents', 'télécharger', 'pdf']
    },

    // PARAMÈTRES
    {
      category: '⚙️ Paramètres',
      question: 'Comment modifier mes informations personnelles ?',
      answer: 'Allez dans "Paramètres" (icône engrenage) → Onglet "Compte". Vous pouvez y modifier : email, nom complet, mot de passe. N\'oubliez pas de cliquer sur "Sauvegarder" après modifications.',
      tags: ['paramètres', 'compte', 'profil']
    },
    {
      category: '⚙️ Paramètres',
      question: 'Mes données sont-elles sécurisées ?',
      answer: 'Oui. Vos données sont : (1) Chiffrées en base de données PostgreSQL, (2) Hébergées en Europe (RGPD), (3) Non partagées avec des tiers, (4) Accessibles uniquement par vous. Vous pouvez exporter ou supprimer vos données à tout moment.',
      tags: ['sécurité', 'rgpd', 'données']
    },
    {
      category: '⚙️ Paramètres',
      question: 'Comment supprimer mon compte ?',
      answer: 'Dans "Paramètres" → Zone rouge en bas de page "Supprimer mon compte". Cliquez, confirmez votre mot de passe. ⚠️ Cette action est IRRÉVERSIBLE et supprime : profils, candidatures, documents, veilles, préférences. Pensez à exporter vos données avant !',
      tags: ['compte', 'supprimer', 'données']
    },

    // TECHNIQUE
    {
      category: '🔧 Technique',
      question: 'Quelles IA sont utilisées ?',
      answer: 'Nous utilisons : (1) Google Gemini (génération documents, analyse offres), (2) OpenAI GPT-4 (fallback si Gemini indisponible). L\'analyse de CV utilise pdfplumber + NLP. Tout est optimisé pour rapidité et pertinence.',
      tags: ['ia', 'technique', 'api']
    },
    {
      category: '🔧 Technique',
      question: 'Comment fonctionne le scraping multi-sources ?',
      answer: 'Architecture : (1) Vous sélectionnez des sources, (2) Recherche déclenchée, (3) Scraping parallèle de chaque source activée, (4) Déduplication des doublons (même titre + entreprise), (5) Normalisation des champs, (6) Mise en cache Redis (24h). Résultat : agrégation de 100-300 offres en 2-3 secondes.',
      tags: ['scraping', 'technique', 'sources']
    },
    {
      category: '🔧 Technique',
      question: 'Y a-t-il des limites d\'utilisation ?',
      answer: 'Limites actuelles : (1) Adzuna API : 1000 requêtes/mois (largement suffisant), (2) Génération documents : illimité, (3) Stockage : illimité, (4) Profils : illimité. Pas de quota sur le nombre de recherches ou candidatures.',
      tags: ['limites', 'quotas', 'utilisation']
    }
  ];

  const filteredFaqs = faqs.filter(faq =>
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.tags?.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const categories = Array.from(new Set(faqs.map(f => f.category)));

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12 px-4">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
          Centre d'aide Job Hunter AI
        </h1>
        <p className="text-gray-600 text-lg">
          Tout ce que vous devez savoir pour maximiser votre recherche d'emploi
        </p>
      </div>

      {/* Search Bar */}
      <Card className="border-2 border-primary/20">
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <Input
              placeholder="Rechercher : profil, sources, candidatures, IA..."
              className="pl-10 h-12 text-base"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            💡 Essayez : "créer profil", "adzuna", "sauvegarder offre", "veille entreprise"
          </p>
        </CardContent>
      </Card>

      {/* Quick Start Guide */}
      {!searchQuery && (
        <Card className="bg-gradient-to-br from-blue-50 to-primary/5 border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-2xl">
              <PlayCircle className="h-7 w-7 text-primary" />
              Guide de démarrage rapide
            </CardTitle>
            <CardDescription className="text-base">
              Suivez ces 5 étapes pour commencer à utiliser Job Hunter AI efficacement
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {quickStartGuide.map((step, index) => (
                <div key={index} className="flex items-start gap-4 p-4 bg-white rounded-lg border hover:border-primary/50 transition-all group">
                  <div className="p-2 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-colors">
                    <step.icon className="h-6 w-6 text-primary" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-1">{step.title}</h3>
                    <p className="text-sm text-gray-600">{step.description}</p>
                  </div>
                  {step.link && (
                    <Link href={step.link}>
                      <Button variant="ghost" size="sm" className="gap-1">
                        Accéder
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Links */}
      <div className="grid md:grid-cols-2 gap-4">
        <Link href="/contact">
          <Card className="h-full hover:shadow-lg hover:border-primary/50 transition-all cursor-pointer group">
            <CardHeader>
              <Mail className="h-8 w-8 text-primary mb-2 group-hover:scale-110 transition-transform" />
              <CardTitle className="text-lg">Contacter le support</CardTitle>
              <CardDescription>
                Une question ? Contactez directement le développeur
              </CardDescription>
            </CardHeader>
          </Card>
        </Link>

        <Card className="h-full hover:shadow-lg hover:border-blue-500/50 transition-all cursor-pointer group bg-gradient-to-br from-blue-50 to-transparent">
          <CardHeader>
            <Book className="h-8 w-8 text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
            <CardTitle className="text-lg">Documentation complète</CardTitle>
            <CardDescription>
              Guides détaillés sur toutes les fonctionnalités
            </CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* FAQ Section */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold">Questions Fréquentes</h2>
          {searchQuery && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => setSearchQuery('')}
            >
              Tout afficher
            </Button>
          )}
        </div>
        
        {categories.map((category) => {
          const categoryFaqs = filteredFaqs.filter(f => f.category === category);
          if (categoryFaqs.length === 0) return null;

          return (
            <div key={category}>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                {category}
              </h3>
              <div className="space-y-3">
                {categoryFaqs.map((faq, index) => {
                  const globalIndex = faqs.indexOf(faq);
                  const isOpen = openIndex === globalIndex;

                  return (
                    <Card key={globalIndex} className="overflow-hidden hover:border-primary/30 transition-colors">
                      <button
                        className="w-full text-left"
                        onClick={() => setOpenIndex(isOpen ? null : globalIndex)}
                      >
                        <CardHeader className="flex flex-row items-center justify-between hover:bg-gray-50 transition-colors">
                          <div className="flex items-start gap-3 flex-1">
                            <HelpCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                            <CardTitle className="text-base font-medium pr-4">
                              {faq.question}
                            </CardTitle>
                          </div>
                          {isOpen ? (
                            <ChevronUp className="h-5 w-5 text-gray-500 flex-shrink-0" />
                          ) : (
                            <ChevronDown className="h-5 w-5 text-gray-500 flex-shrink-0" />
                          )}
                        </CardHeader>
                      </button>
                      {isOpen && (
                        <CardContent className="pt-0 pb-4">
                          <div className="pl-8">
                            <p className="text-gray-700 leading-relaxed">{faq.answer}</p>
                            {faq.tags && (
                              <div className="flex flex-wrap gap-2 mt-3">
                                {faq.tags.map((tag, i) => (
                                  <span 
                                    key={i}
                                    className="text-xs px-2 py-1 bg-primary/10 text-primary rounded-full"
                                  >
                                    {tag}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </CardContent>
                      )}
                    </Card>
                  );
                })}
              </div>
            </div>
          );
        })}

        {filteredFaqs.length === 0 && (
          <Card className="border-2 border-dashed">
            <CardContent className="pt-6 text-center py-12">
              <Search className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600 mb-2 text-lg">
                Aucune question trouvée pour <strong>"{searchQuery}"</strong>
              </p>
              <p className="text-gray-500 text-sm mb-4">
                Essayez des termes plus généraux ou contactez le support
              </p>
              <div className="flex gap-3 justify-center">
                <Button variant="outline" onClick={() => setSearchQuery('')}>
                  Réinitialiser la recherche
                </Button>
                <Link href="/contact">
                  <Button className="gap-2">
                    <MessageCircle className="h-4 w-4" />
                    Poser une question
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Contact Support CTA */}
      <Card className="bg-gradient-to-r from-primary to-blue-600 text-white border-none">
        <CardHeader>
          <CardTitle className="text-white text-2xl flex items-center gap-2">
            <MessageCircle className="h-6 w-6" />
            Vous n'avez pas trouvé votre réponse ?
          </CardTitle>
          <CardDescription className="text-blue-100">
            Notre développeur est disponible pour vous aider directement
          </CardDescription>
        </CardHeader>
        <CardContent className="flex gap-3">
          <Button 
            variant="outline" 
            className="gap-2 bg-white hover:bg-gray-100 text-gray-900 border-white"
            onClick={() => {
              const feedbackBtn = document.querySelector('[data-feedback-button]') as HTMLElement;
              if (feedbackBtn) feedbackBtn.click();
            }}
          >
            <Mail className="h-4 w-4" />
            Contacter le support
          </Button>
          <Button 
            variant="outline" 
            className="gap-2 border-white text-white hover:bg-white/10"
            onClick={() => window.open('https://franckkenfack.works', '_blank')}
          >
            <ExternalLink className="h-4 w-4" />
            Portfolio développeur
          </Button>
        </CardContent>
      </Card>

      {/* Stats Footer */}
      <Card className="bg-gray-50 border-dashed">
        <CardContent className="pt-6">
          <div className="grid md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-primary mb-1">17</div>
              <div className="text-sm text-gray-600">Sources d'offres</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-1">1000+</div>
              <div className="text-sm text-gray-600">Offres quotidiennes</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-1">2</div>
              <div className="text-sm text-gray-600">IA (Gemini + GPT-4)</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-1">24/7</div>
              <div className="text-sm text-gray-600">Veille automatique</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

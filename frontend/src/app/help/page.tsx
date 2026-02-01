"use client";
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ChevronDown, ChevronUp, Search, Book, HelpCircle, Video, MessageCircle } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface FAQItem {
  question: string;
  answer: string;
  category: string;
}

export default function HelpPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs: FAQItem[] = [
    {
      category: 'Démarrage',
      question: 'Comment créer mon premier profil ?',
      answer: 'Allez dans "Mon Profil" → "Créer un profil". Vous avez 2 options : (1) Uploader votre CV en PDF pour extraction automatique, ou (2) Remplir le formulaire guidé étape par étape.'
    },
    {
      category: 'Démarrage',
      question: 'Puis-je avoir plusieurs profils ?',
      answer: 'Oui ! Vous pouvez créer plusieurs variantes de profil (ex: "Backend Developer", "Data Engineer"). Cela permet d\'adapter vos candidatures selon les types de postes.'
    },
    {
      category: 'Recherche',
      question: 'Comment rechercher des offres d\'emploi ?',
      answer: 'Allez dans "Offres d\'emploi" → Utilisez les filtres (mots-clés, localisation, type de contrat). Vous pouvez aussi coller une URL d\'offre directement pour l\'analyser.'
    },
    {
      category: 'Recherche',
      question: 'Comment fonctionne la veille entreprise ?',
      answer: 'Dans "Veille Entreprise", ajoutez le nom et l\'URL carrières de vos entreprises cibles. Notre système scrapera automatiquement leurs nouvelles offres toutes les 4 heures.'
    },
    {
      category: 'Recherche',
      question: 'Quelles plateformes sont supportées pour le scraping ?',
      answer: 'Actuellement : LinkedIn, Indeed, RemoteOK, et sites carrières d\'entreprises (si accessibles). La liste s\'agrandit régulièrement.'
    },
    {
      category: 'Documents IA',
      question: 'Comment l\'IA génère-t-elle mes documents ?',
      answer: 'L\'IA (Google Gemini) analyse l\'offre d\'emploi, compare avec votre profil, puis génère un CV réorganisé et une lettre de motivation personnalisée en mettant en avant vos points forts pertinents.'
    },
    {
      category: 'Documents IA',
      question: 'Puis-je modifier les documents générés ?',
      answer: 'Oui ! Après génération, vous pouvez prévisualiser et éditer la lettre de motivation avant l\'envoi. Le CV peut aussi être régénéré avec un autre template.'
    },
    {
      category: 'Documents IA',
      question: 'Combien de documents puis-je générer ?',
      answer: 'Illimité pour le moment. Tous vos documents sont sauvegardés dans "Mes Documents" pour consultation et réutilisation.'
    },
    {
      category: 'Candidatures',
      question: 'Comment envoyer une candidature ?',
      answer: 'Après avoir généré vos documents pour une offre, cliquez sur "Envoyer par email". Vous pourrez éditer l\'email et confirmer avant envoi. Tout est enregistré dans "Mes Candidatures".'
    },
    {
      category: 'Candidatures',
      question: 'Puis-je suivre mes candidatures envoyées ?',
      answer: 'Oui ! Dans "Mes Candidatures", vous verrez l\'historique complet : date d\'envoi, entreprise, poste, statut (en attente, réponse, entretien, refusé).'
    },
    {
      category: 'Compte',
      question: 'Comment modifier mes informations personnelles ?',
      answer: 'Allez dans "Paramètres" → Onglet "Compte". Vous pouvez y modifier votre email, nom, et mot de passe.'
    },
    {
      category: 'Compte',
      question: 'Mes données sont-elles sécurisées ?',
      answer: 'Oui. Vos données sont chiffrées en base de données, non partagées avec des tiers, et vous pouvez les exporter (RGPD) ou supprimer votre compte à tout moment.'
    },
    {
      category: 'Compte',
      question: 'Comment supprimer mon compte ?',
      answer: 'Dans "Paramètres" → Onglet "Confidentialité" → Zone rouge "Supprimer mon compte". Cette action est irréversible et supprime toutes vos données.'
    }
  ];

  const filteredFaqs = faqs.filter(faq =>
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const categories = Array.from(new Set(faqs.map(f => f.category)));

  return (
    <div className="space-y-6 max-w-4xl mx-auto pb-12">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">❓ Centre d'aide</h1>
        <p className="text-gray-600 text-lg">Trouvez rapidement des réponses à vos questions</p>
      </div>

      {/* Search Bar */}
      <Card>
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <Input
              placeholder="Rechercher dans la FAQ..."
              className="pl-10"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Quick Links */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <Book className="h-8 w-8 text-primary mb-2" />
            <CardTitle className="text-lg">Documentation</CardTitle>
            <CardDescription>Guides complets et tutoriels</CardDescription>
          </CardHeader>
        </Card>
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <Video className="h-8 w-8 text-primary mb-2" />
            <CardTitle className="text-lg">Tutoriels Vidéo</CardTitle>
            <CardDescription>Apprenez en vidéo</CardDescription>
          </CardHeader>
        </Card>
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <MessageCircle className="h-8 w-8 text-primary mb-2" />
            <CardTitle className="text-lg">Support Direct</CardTitle>
            <CardDescription>Contactez notre équipe</CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* FAQ Section */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold">Questions Fréquentes</h2>
        
        {categories.map((category) => {
          const categoryFaqs = filteredFaqs.filter(f => f.category === category);
          if (categoryFaqs.length === 0) return null;

          return (
            <div key={category}>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <HelpCircle className="h-5 w-5 text-primary" />
                {category}
              </h3>
              <div className="space-y-3">
                {categoryFaqs.map((faq, index) => {
                  const globalIndex = faqs.indexOf(faq);
                  const isOpen = openIndex === globalIndex;

                  return (
                    <Card key={globalIndex} className="overflow-hidden">
                      <button
                        className="w-full text-left"
                        onClick={() => setOpenIndex(isOpen ? null : globalIndex)}
                      >
                        <CardHeader className="flex flex-row items-center justify-between hover:bg-gray-50 transition-colors">
                          <CardTitle className="text-base font-medium pr-4">
                            {faq.question}
                          </CardTitle>
                          {isOpen ? (
                            <ChevronUp className="h-5 w-5 text-gray-500 flex-shrink-0" />
                          ) : (
                            <ChevronDown className="h-5 w-5 text-gray-500 flex-shrink-0" />
                          )}
                        </CardHeader>
                      </button>
                      {isOpen && (
                        <CardContent className="pt-0">
                          <p className="text-gray-600">{faq.answer}</p>
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
          <Card>
            <CardContent className="pt-6 text-center">
              <p className="text-gray-600 mb-4">Aucune question trouvée pour "{searchQuery}"</p>
              <Button variant="outline" onClick={() => setSearchQuery('')}>
                Réinitialiser la recherche
              </Button>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Contact Support */}
      <Card className="bg-gradient-to-r from-primary to-blue-600 text-white">
        <CardHeader>
          <CardTitle className="text-white">Besoin d'aide supplémentaire ?</CardTitle>
          <CardDescription className="text-blue-100">
            Notre équipe est là pour vous aider
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" className="bg-white hover:bg-gray-100">
            <MessageCircle className="mr-2 h-4 w-4" />
            Contacter le support
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

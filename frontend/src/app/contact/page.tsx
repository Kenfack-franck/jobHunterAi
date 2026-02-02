"use client";
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Mail, Phone, Linkedin, ExternalLink, Send, Github } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/lib/api';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [sending, setSending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.message) {
      toast.error('Veuillez remplir tous les champs obligatoires');
      return;
    }

    try {
      setSending(true);
      await apiClient.post('/contact/send', formData);
      toast.success('Message envoyé avec succès !');
      setFormData({ name: '', email: '', subject: '', message: '' });
    } catch (error) {
      console.error('Erreur:', error);
      toast.error('Erreur lors de l\'envoi. Veuillez réessayer ou m\'écrire directement à kenfackfranck08@gmail.com');
    } finally {
      setSending(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Contactez-moi
          </h1>
          <p className="text-xl text-gray-600">
            Des questions ? Des suggestions ? Je suis à votre écoute !
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Informations personnelles */}
          <Card>
            <CardHeader>
              <CardTitle>À propos du créateur</CardTitle>
              <CardDescription>
                Développeur Full-Stack passionné par l'IA et l'automatisation
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Nom */}
              <div>
                <h3 className="font-semibold text-lg mb-2">
                  KENFACK NOUMEDEM FRANCK ULRICH
                </h3>
                <p className="text-gray-600 text-sm">
                  Ingénieur Informatique - Double diplôme ENSTA Paris & ENSPY Yaoundé
                </p>
              </div>

              {/* Contact */}
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-gray-700">
                  <Mail className="w-5 h-5 text-blue-600" />
                  <a href="mailto:kenfackfranck08@gmail.com" className="hover:text-blue-600 transition-colors">
                    kenfackfranck08@gmail.com
                  </a>
                </div>
                <div className="flex items-center gap-3 text-gray-700">
                  <Phone className="w-5 h-5 text-green-600" />
                  <a href="tel:+33780863790" className="hover:text-green-600 transition-colors">
                    +33 7 80 86 37 90
                  </a>
                </div>
              </div>

              {/* Liens */}
              <div className="space-y-3 pt-4 border-t">
                <a 
                  href="https://franckkenfack.works" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 text-blue-600 hover:underline"
                >
                  <ExternalLink className="w-5 h-5" />
                  Portfolio : franckkenfack.works
                </a>
                <a 
                  href="https://www.linkedin.com/in/franck-ulrich-kenfack-947231252" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 text-blue-700 hover:underline"
                >
                  <Linkedin className="w-5 h-5" />
                  LinkedIn : Franck Ulrich KENFACK
                </a>
                <a 
                  href="https://github.com/kenfackfranck08" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 text-gray-800 hover:underline"
                >
                  <Github className="w-5 h-5" />
                  GitHub : @kenfackfranck08
                </a>
              </div>

              {/* Formation */}
              <div className="pt-4 border-t">
                <h4 className="font-semibold mb-3 text-gray-900">Formation</h4>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>
                    <span className="font-medium">2025 - présent :</span> Majeure Informatique (double diplôme), ENSTA Paris
                  </li>
                  <li>
                    <span className="font-medium">2023 - 2025 :</span> Génie Informatique, ENSPY Yaoundé, Cameroun
                  </li>
                  <li>
                    <span className="font-medium">2021 - 2023 :</span> Mathématiques et Sciences Physiques, ENSPY
                  </li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Formulaire de contact */}
          <Card>
            <CardHeader>
              <CardTitle>Envoyez-moi un message</CardTitle>
              <CardDescription>
                Feedback, bug report, suggestion... tout est bienvenu !
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="name">Nom *</Label>
                  <Input
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Votre nom"
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="votre.email@exemple.com"
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="subject">Sujet</Label>
                  <Input
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    placeholder="Ex: Suggestion d'amélioration"
                  />
                </div>

                <div>
                  <Label htmlFor="message">Message *</Label>
                  <Textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Votre message..."
                    rows={6}
                    required
                  />
                </div>

                <Button 
                  type="submit" 
                  className="w-full"
                  disabled={sending}
                >
                  {sending ? (
                    <>Envoi en cours...</>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Envoyer le message
                    </>
                  )}
                </Button>

                <p className="text-xs text-gray-500 text-center">
                  Votre message sera envoyé directement à kenfackfranck08@gmail.com
                </p>
              </form>
            </CardContent>
          </Card>
        </div>

        {/* CTA */}
        <div className="mt-12 text-center bg-blue-50 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Job Hunter AI - Projet Open Source
          </h2>
          <p className="text-gray-600 mb-4">
            Automatisez votre recherche d'emploi avec l'intelligence artificielle
          </p>
          <div className="flex justify-center gap-4">
            <Button variant="outline" asChild>
              <a href="https://franckkenfack.works" target="_blank" rel="noopener noreferrer">
                Voir mon portfolio
              </a>
            </Button>
            <Button asChild>
              <a href="https://www.linkedin.com/in/franck-ulrich-kenfack-947231252" target="_blank" rel="noopener noreferrer">
                Me suivre sur LinkedIn
              </a>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

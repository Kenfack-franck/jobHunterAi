"use client";

import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Mail, Phone, Linkedin, ExternalLink, Send, Github } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/lib/api';

interface ContactModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function ContactModal({ open, onOpenChange }: ContactModalProps) {
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
      onOpenChange(false);
    } catch (error) {
      console.error('Erreur:', error);
      toast.error('Erreur lors de l\'envoi. Écrivez-moi directement à kenfackfranck08@gmail.com');
    } finally {
      setSending(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl">Contactez-moi</DialogTitle>
          <DialogDescription>
            Des questions ? Des suggestions ? Je suis à votre écoute !
          </DialogDescription>
        </DialogHeader>

        <div className="grid md:grid-cols-2 gap-6 mt-4">
          {/* Informations personnelles */}
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold text-lg mb-2">
                KENFACK NOUMEDEM FRANCK ULRICH
              </h3>
              <p className="text-sm text-gray-600">
                Ingénieur Informatique - Double diplôme ENSTA Paris & ENSPY Yaoundé
              </p>
            </div>

            {/* Contact */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm">
                <Mail className="w-4 h-4 text-blue-600" />
                <a href="mailto:kenfackfranck08@gmail.com" className="hover:text-blue-600 transition-colors">
                  kenfackfranck08@gmail.com
                </a>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Phone className="w-4 h-4 text-green-600" />
                <a href="tel:+33780863790" className="hover:text-green-600 transition-colors">
                  +33 7 80 86 37 90
                </a>
              </div>
            </div>

            {/* Liens */}
            <div className="space-y-2">
              <a 
                href="https://franckkenfack.works" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-blue-600 hover:underline"
              >
                <ExternalLink className="w-4 h-4" />
                Portfolio : franckkenfack.works
              </a>
              <a 
                href="https://www.linkedin.com/in/franck-ulrich-kenfack-947231252" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-blue-700 hover:underline"
              >
                <Linkedin className="w-4 h-4" />
                LinkedIn : Franck Ulrich KENFACK
              </a>
              <a 
                href="https://github.com/kenfackfranck08" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-sm text-gray-800 hover:underline"
              >
                <Github className="w-4 h-4" />
                GitHub : @kenfackfranck08
              </a>
            </div>

            {/* Formation */}
            <div className="pt-2 border-t">
              <h4 className="font-semibold mb-2 text-sm">Formation</h4>
              <ul className="space-y-1 text-xs text-gray-600">
                <li>
                  <span className="font-medium">2025 - présent :</span> Majeure Informatique, ENSTA Paris
                </li>
                <li>
                  <span className="font-medium">2023 - 2025 :</span> Génie Informatique, ENSPY Yaoundé
                </li>
                <li>
                  <span className="font-medium">2021 - 2023 :</span> Mathématiques et Sciences Physiques, ENSPY
                </li>
              </ul>
            </div>
          </div>

          {/* Formulaire de contact */}
          <Card>
            <CardContent className="pt-6">
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
                    rows={4}
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
      </DialogContent>
    </Dialog>
  );
}

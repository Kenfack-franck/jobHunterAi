"use client";

import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Mail, Phone, Linkedin, ExternalLink, Send, Github, MessageCircle, Loader2 } from 'lucide-react';
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
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto backdrop-blur-xl bg-white/95 border-2 border-blue-200/50 shadow-2xl">
        <DialogHeader>
          <div className="flex items-center gap-4 mb-3">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
              <Mail className="w-7 h-7 text-white" />
            </div>
            <div className="flex-1">
              <DialogTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                📧 Contactez-moi
              </DialogTitle>
              <DialogDescription className="text-base mt-1 text-gray-600 font-medium">
                Des questions ? Des suggestions ? Je suis à votre écoute !
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="grid md:grid-cols-2 gap-8 mt-6">
          {/* Informations personnelles */}
          <div className="space-y-6 p-6 rounded-2xl bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 border-2 border-blue-200">
            <div className="pb-4 border-b-2 border-blue-200">
              <h3 className="font-bold text-xl mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                KENFACK NOUMEDEM FRANCK ULRICH
              </h3>
              <p className="text-sm text-gray-600 font-medium">
                🎓 Ingénieur Informatique - Double diplôme ENSTA Paris & ENSPY Yaoundé
              </p>
            </div>

            {/* Contact */}
            <div className="space-y-3">
              <h4 className="font-bold text-sm text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-lg">📞</span>
                <span>Contactez-moi</span>
              </h4>
              <div className="flex items-center gap-3 p-3 bg-white/60 rounded-xl border border-blue-200 hover:bg-white hover:shadow-md transition-all">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <Mail className="w-5 h-5 text-white" />
                </div>
                <a href="mailto:kenfackfranck08@gmail.com" className="text-sm font-semibold text-blue-600 hover:text-purple-600 transition-colors">
                  kenfackfranck08@gmail.com
                </a>
              </div>
              <div className="flex items-center gap-3 p-3 bg-white/60 rounded-xl border border-green-200 hover:bg-white hover:shadow-md transition-all">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                  <Phone className="w-5 h-5 text-white" />
                </div>
                <a href="tel:+33780863790" className="text-sm font-semibold text-green-600 hover:text-emerald-600 transition-colors">
                  +33 7 80 86 37 90
                </a>
              </div>
            </div>

            {/* Liens */}
            <div className="space-y-3">
              <h4 className="font-bold text-sm text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-lg">🔗</span>
                <span>Mes liens</span>
              </h4>
              <a 
                href="https://franckkenfack.works" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-white/60 rounded-xl border border-purple-200 hover:bg-white hover:shadow-md transition-all group"
              >
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                  <ExternalLink className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1">
                  <div className="text-xs text-gray-500 font-medium">Portfolio</div>
                  <div className="text-sm font-bold text-purple-600 group-hover:text-pink-600 transition-colors">
                    franckkenfack.works
                  </div>
                </div>
              </a>
              <a 
                href="https://www.linkedin.com/in/franck-ulrich-kenfack-947231252" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-white/60 rounded-xl border border-blue-200 hover:bg-white hover:shadow-md transition-all group"
              >
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-blue-500 flex items-center justify-center">
                  <Linkedin className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1">
                  <div className="text-xs text-gray-500 font-medium">LinkedIn</div>
                  <div className="text-sm font-bold text-blue-700 group-hover:text-blue-800 transition-colors">
                    Franck Ulrich KENFACK
                  </div>
                </div>
              </a>
              <a 
                href="https://github.com/kenfackfranck08" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-white/60 rounded-xl border border-gray-300 hover:bg-white hover:shadow-md transition-all group"
              >
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-800 to-gray-700 flex items-center justify-center">
                  <Github className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1">
                  <div className="text-xs text-gray-500 font-medium">GitHub</div>
                  <div className="text-sm font-bold text-gray-800 group-hover:text-gray-900 transition-colors">
                    @kenfackfranck08
                  </div>
                </div>
              </a>
            </div>

            {/* Formation */}
            <div className="pt-4 border-t-2 border-blue-200">
              <h4 className="font-bold text-sm text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-lg">🎓</span>
                <span>Formation</span>
              </h4>
              <div className="space-y-2">
                <div className="p-3 bg-white/60 rounded-lg border border-blue-100">
                  <div className="text-xs text-blue-600 font-bold">2025 - présent</div>
                  <div className="text-sm text-gray-700 font-medium">Majeure Informatique, ENSTA Paris</div>
                </div>
                <div className="p-3 bg-white/60 rounded-lg border border-purple-100">
                  <div className="text-xs text-purple-600 font-bold">2023 - 2025</div>
                  <div className="text-sm text-gray-700 font-medium">Génie Informatique, ENSPY Yaoundé</div>
                </div>
                <div className="p-3 bg-white/60 rounded-lg border border-pink-100">
                  <div className="text-xs text-pink-600 font-bold">2021 - 2023</div>
                  <div className="text-sm text-gray-700 font-medium">Maths & Sciences Physiques, ENSPY</div>
                </div>
              </div>
            </div>
          </div>

          {/* Formulaire de contact */}
          <Card className="border-2 border-purple-200 hover:border-purple-300 shadow-xl transition-all">
            <CardContent className="pt-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center shadow-md">
                  <Send className="w-5 h-5 text-white" />
                </div>
                <h3 className="font-bold text-lg bg-gradient-to-r from-pink-600 to-rose-600 bg-clip-text text-transparent">
                  Envoyez-moi un message
                </h3>
              </div>
              <div className="h-px bg-gradient-to-r from-pink-200 via-rose-200 to-transparent mb-6" />
              
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <Label htmlFor="name" className="text-sm font-bold flex items-center gap-2 mb-2 text-gray-700">
                    <div className="w-5 h-5 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                      <span className="text-white text-xs">👤</span>
                    </div>
                    Nom *
                  </Label>
                  <Input
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Votre nom"
                    required
                    className="border-2 border-blue-200 focus:border-purple-400"
                  />
                </div>

                <div>
                  <Label htmlFor="email" className="text-sm font-bold flex items-center gap-2 mb-2 text-gray-700">
                    <div className="w-5 h-5 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                      <Mail className="w-3 h-3 text-white" />
                    </div>
                    Email *
                  </Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="votre.email@exemple.com"
                    required
                    className="border-2 border-green-200 focus:border-emerald-400"
                  />
                </div>

                <div>
                  <Label htmlFor="subject" className="text-sm font-bold flex items-center gap-2 mb-2 text-gray-700">
                    <div className="w-5 h-5 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                      <span className="text-white text-xs">📌</span>
                    </div>
                    Sujet
                  </Label>
                  <Input
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    placeholder="Ex: Suggestion d'amélioration"
                    className="border-2 border-purple-200 focus:border-pink-400"
                  />
                </div>

                <div>
                  <Label htmlFor="message" className="text-sm font-bold flex items-center gap-2 mb-2 text-gray-700">
                    <div className="w-5 h-5 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                      <MessageCircle className="w-3 h-3 text-white" />
                    </div>
                    Message *
                  </Label>
                  <Textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Votre message..."
                    rows={5}
                    required
                    className="border-2 border-pink-200 focus:border-rose-400 resize-none"
                  />
                </div>

                <Button 
                  type="submit" 
                  className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 text-base py-6"
                  disabled={sending}
                >
                  {sending ? (
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Envoi en cours...</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <Send className="w-5 h-5" />
                      <span>Envoyer le message</span>
                    </div>
                  )}
                </Button>

                <p className="text-xs text-gray-500 text-center flex items-center justify-center gap-1">
                  <span>💌</span>
                  <span>Votre message sera envoyé directement à kenfackfranck08@gmail.com</span>
                </p>
              </form>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
}

"use client";
import { useState, useEffect } from 'react';
import { MessageCircle, X, Send, Mail } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { toast } from 'sonner';
import { contactService } from '@/lib/contact';
import { useAuth } from '@/contexts/AuthContext';

interface FeedbackButtonProps {
  onOpenContactModal?: () => void;
}

export function FeedbackButton({ onOpenContactModal }: FeedbackButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  // Pré-remplir l'email de l'utilisateur connecté
  useEffect(() => {
    if (user?.email && !email) {
      setEmail(user.email);
    }
  }, [user, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim()) {
      toast.error('Veuillez entrer un message');
      return;
    }

    setLoading(true);
    try {
      await contactService.sendMessage({
        name: user?.full_name || 'Utilisateur',
        email: email || 'anonymous@feedback.com',
        subject: '💬 Feedback utilisateur',
        message: message,
      });

      toast.success('Merci pour votre retour ! 🙏');
      setMessage('');
      setIsOpen(false);
    } catch (error) {
      toast.error('Erreur lors de l\'envoi. Réessayez plus tard.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenContactInfo = () => {
    toast.info(
      '📧 kenfackfranck08@gmail.com\n📞 +33 7 80 86 37 90\n🌐 franckkenfack.works',
      { duration: 8000 }
    );
  };

  return (
    <>
      {/* Bouton flottant */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        data-feedback-button
        className={`
          fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50
          w-12 h-12 sm:w-14 sm:h-14 rounded-full
          bg-gradient-to-br from-primary to-blue-600
          text-white shadow-lg
          hover:shadow-xl hover:scale-110
          transition-all duration-300
          flex items-center justify-center
          ${isOpen ? 'rotate-90' : ''}
        `}
        aria-label="Feedback"
      >
        {isOpen ? (
          <X className="h-5 w-5 sm:h-6 sm:w-6" />
        ) : (
          <MessageCircle className="h-5 w-5 sm:h-6 sm:w-6" />
        )}
      </button>

      {/* Modal de feedback */}
      {isOpen && (
        <Card className="fixed bottom-20 sm:bottom-24 right-4 sm:right-6 z-40 w-[calc(100vw-2rem)] sm:w-[450px] max-w-md shadow-2xl border-2 border-purple-200 backdrop-blur-xl bg-white/95">
          <CardHeader className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-t-lg">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                <MessageCircle className="h-5 w-5" />
              </div>
              <CardTitle className="text-xl font-bold">Votre avis compte !</CardTitle>
            </div>
            <CardDescription className="text-white/90 font-medium">
              💡 Partagez vos idées pour améliorer l'application
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-5">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-sm font-bold mb-2 block flex items-center gap-2 text-gray-700">
                  <div className="w-5 h-5 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                    <Mail className="w-3 h-3 text-white" />
                  </div>
                  Votre email
                </label>
                <Input
                  type="email"
                  placeholder="votre@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full border-2 border-blue-200 focus:border-purple-400"
                />
                {user?.email && (
                  <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
                    <span>💡</span>
                    <span>Votre email est pré-rempli. Vous pouvez le modifier si besoin.</span>
                  </p>
                )}
              </div>

              <div>
                <label className="text-sm font-bold mb-2 block flex items-center gap-2 text-gray-700">
                  <div className="w-5 h-5 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                    <MessageCircle className="w-3 h-3 text-white" />
                  </div>
                  Votre retour
                </label>
                <Textarea
                  placeholder="Suggestions, bugs, améliorations... Nous sommes à l'écoute ! 👂"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={5}
                  className="w-full resize-none border-2 border-pink-200 focus:border-rose-400"
                />
              </div>

              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsOpen(false)}
                  className="flex-1 border-2 border-gray-300 hover:border-gray-400"
                  disabled={loading}
                >
                  Annuler
                </Button>
                <Button
                  type="submit"
                  className="flex-1 gap-2 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 text-white shadow-lg"
                  disabled={loading || !message.trim()}
                >
                  {loading ? (
                    <>Envoi...</>
                  ) : (
                    <>
                      <Send className="h-4 w-4" />
                      Envoyer
                    </>
                  )}
                </Button>
              </div>
            </form>

            {/* Mes coordonnées */}
            <div className="pt-4 border-t-2 border-gray-200">
              <p className="text-sm font-bold text-gray-700 mb-3 text-center flex items-center justify-center gap-2">
                <span className="text-lg">📞</span>
                <span>Mes coordonnées</span>
              </p>
              <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 border-2 border-blue-200 rounded-xl p-4 space-y-3 text-sm">
                <div className="flex items-center gap-3 p-2 bg-white/60 rounded-lg hover:bg-white transition-colors">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                    <Mail className="w-4 h-4 text-white" />
                  </div>
                  <a 
                    href="mailto:kenfackfranck08@gmail.com" 
                    className="text-blue-600 hover:underline font-medium"
                  >
                    kenfackfranck08@gmail.com
                  </a>
                </div>
                <div className="flex items-center gap-3 p-2 bg-white/60 rounded-lg hover:bg-white transition-colors">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                    <span className="text-white">📞</span>
                  </div>
                  <a 
                    href="tel:+33780863790" 
                    className="text-blue-600 hover:underline font-medium"
                  >
                    +33 7 80 86 37 90
                  </a>
                </div>
                <div className="flex items-center gap-3 p-2 bg-white/60 rounded-lg hover:bg-white transition-colors">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                    <span className="text-white">🌐</span>
                  </div>
                  <a 
                    href="https://franckkenfack.works" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline font-medium"
                  >
                    franckkenfack.works
                  </a>
                </div>
              </div>
            </div>

            <p className="text-xs text-gray-500 text-center pt-2 flex items-center justify-center gap-1">
              <span>💡</span>
              <span>Votre feedback nous aide à améliorer l'expérience pour tous</span>
            </p>
          </CardContent>
        </Card>
      )}
    </>
  );
}

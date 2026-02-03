"use client";
import { useState, useEffect } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
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
        <Card className="fixed bottom-20 sm:bottom-24 right-4 sm:right-6 z-40 w-[calc(100vw-2rem)] sm:w-[420px] max-w-md shadow-2xl border-2">
          <CardHeader className="bg-gradient-to-r from-primary to-blue-600 text-white">
            <CardTitle className="flex items-center gap-2">
              <MessageCircle className="h-5 w-5" />
              Votre avis compte !
            </CardTitle>
            <CardDescription className="text-white/90">
              Partagez vos idées pour améliorer l'application
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Votre email
                </label>
                <Input
                  type="email"
                  placeholder="votre@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full"
                />
                {user?.email && (
                  <p className="text-xs text-gray-500 mt-1">
                    💡 Votre email est pré-rempli. Vous pouvez le modifier si besoin.
                  </p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Votre retour
                </label>
                <Textarea
                  placeholder="Suggestions, bugs, améliorations... Nous sommes à l'écoute ! 👂"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={5}
                  className="w-full resize-none"
                />
              </div>

              <div className="flex gap-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsOpen(false)}
                  className="flex-1"
                  disabled={loading}
                >
                  Annuler
                </Button>
                <Button
                  type="submit"
                  className="flex-1 gap-2"
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
            <div className="pt-4 border-t">
              <p className="text-xs font-semibold text-gray-700 mb-3 text-center">
                📞 Mes coordonnées
              </p>
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <span>📧</span>
                  <a 
                    href="mailto:kenfackfranck08@gmail.com" 
                    className="text-blue-600 hover:underline"
                  >
                    kenfackfranck08@gmail.com
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <span>📞</span>
                  <a 
                    href="tel:+33780863790" 
                    className="text-blue-600 hover:underline"
                  >
                    +33 7 80 86 37 90
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <span>🌐</span>
                  <a 
                    href="https://franckkenfack.works" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    franckkenfack.works
                  </a>
                </div>
              </div>
            </div>

            <p className="text-xs text-gray-500 text-center pt-2">
              💡 Votre feedback nous aide à améliorer l'expérience pour tous
            </p>
          </CardContent>
        </Card>
      )}
    </>
  );
}

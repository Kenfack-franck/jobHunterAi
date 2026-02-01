"use client";
import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { Save, AlertTriangle, Download, Trash2, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { userService } from '@/lib/userService';
import { useRouter } from 'next/navigation';

export default function SettingsPage() {
  const { user, refreshUser, logout } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'account' | 'notifications' | 'privacy'>('account');
  
  const [accountData, setAccountData] = useState({
    fullName: '',
    email: '',
    language: 'fr'
  });

  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const [notifSettings, setNotifSettings] = useState({
    emailNewOffers: true,
    emailApplicationUpdates: true,
    emailWeeklySummary: false,
    pushNotifications: true
  });

  const [isUpdating, setIsUpdating] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  useEffect(() => {
    if (user) {
      setAccountData({
        fullName: user.full_name || '',
        email: user.email || '',
        language: user.language || 'fr'
      });
    }
  }, [user]);

  const handleSaveAccount = async () => {
    try {
      setIsUpdating(true);
      await userService.updateProfile({
        full_name: accountData.fullName,
        language: accountData.language
      });
      await refreshUser();
      toast.success('Profil mis à jour avec succès');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erreur lors de la mise à jour');
      console.error(error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleChangePassword = async () => {
    if (!passwordData.currentPassword || !passwordData.newPassword) {
      toast.error('Veuillez remplir tous les champs');
      return;
    }

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('Les mots de passe ne correspondent pas');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      toast.error('Le mot de passe doit contenir au moins 8 caractères');
      return;
    }

    try {
      setIsUpdating(true);
      await userService.updatePassword({
        current_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      });
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
      toast.success('Mot de passe modifié avec succès');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Erreur lors du changement de mot de passe');
      console.error(error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleSaveNotifications = () => {
    // TODO: Backend API pour sauvegarder préférences notifications
    toast.success('Préférences de notification enregistrées');
  };

  const handleExportData = async () => {
    try {
      setIsExporting(true);
      const blob = await userService.exportData();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `jobhunter_data_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success('Données exportées avec succès');
    } catch (error) {
      toast.error('Cette fonctionnalité sera disponible prochainement');
      console.error(error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleDeleteAccount = async () => {
    const confirmation = prompt(
      '⚠️ ATTENTION : Cette action est IRRÉVERSIBLE.\n\n' +
      'Toutes vos données seront supprimées définitivement :\n' +
      '- Profil et expériences\n' +
      '- Documents générés\n' +
      '- Candidatures\n' +
      '- Entreprises surveillées\n\n' +
      'Pour confirmer, tapez "SUPPRIMER" en majuscules :'
    );

    if (confirmation !== 'SUPPRIMER') {
      toast.info('Suppression annulée');
      return;
    }

    try {
      await userService.deleteAccount();
      toast.success('Compte supprimé. Vous allez être déconnecté...');
      setTimeout(() => {
        logout();
        router.push('/');
      }, 2000);
    } catch (error) {
      toast.error('Cette fonctionnalité sera disponible prochainement');
      console.error(error);
    }
  };

  const tabs = [
    { id: 'account', label: '👤 Compte', active: activeTab === 'account' },
    { id: 'notifications', label: '🔔 Notifications', active: activeTab === 'notifications' },
    { id: 'privacy', label: '🔒 Confidentialité', active: activeTab === 'privacy' }
  ];

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">⚙️ Paramètres</h1>
          <p className="text-gray-600 mt-1">Gérez votre compte et vos préférences</p>
        </div>

        <div className="flex gap-2 border-b">
          {tabs.map((tab) => (
            <Button
              key={tab.id}
              variant={tab.active ? 'default' : 'ghost'}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className="rounded-b-none"
            >
              {tab.label}
            </Button>
          ))}
        </div>

        {activeTab === 'account' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Informations du compte</CardTitle>
                <CardDescription>Modifiez vos informations personnelles</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Nom complet</Label>
                  <Input 
                    value={accountData.fullName}
                    onChange={(e) => setAccountData({ ...accountData, fullName: e.target.value })}
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <Label>Email</Label>
                  <Input 
                    type="email" 
                    value={accountData.email}
                    disabled
                    className="bg-gray-50"
                  />
                  <p className="text-xs text-gray-500 mt-1">L'email ne peut pas être modifié</p>
                </div>
                <div>
                  <Label>Langue</Label>
                  <select
                    value={accountData.language}
                    onChange={(e) => setAccountData({ ...accountData, language: e.target.value })}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  >
                    <option value="fr">Français</option>
                    <option value="en">English</option>
                  </select>
                </div>
                <Button onClick={handleSaveAccount} disabled={isUpdating}>
                  {isUpdating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Enregistrement...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Enregistrer les modifications
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Changer le mot de passe</CardTitle>
                <CardDescription>Mettez à jour votre mot de passe</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Mot de passe actuel</Label>
                  <Input 
                    type="password" 
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                  />
                </div>
                <div>
                  <Label>Nouveau mot de passe</Label>
                  <Input 
                    type="password" 
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                  />
                </div>
                <div>
                  <Label>Confirmer le nouveau mot de passe</Label>
                  <Input 
                    type="password" 
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                  />
                </div>
                <Button onClick={handleChangePassword} disabled={isUpdating} variant="outline">
                  {isUpdating ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Modification...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Changer le mot de passe
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'notifications' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Préférences de notification</CardTitle>
                <CardDescription>Choisissez comment vous souhaitez être informé</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries({
                  emailNewOffers: 'Nouvelles offres correspondant à mon profil',
                  emailApplicationUpdates: 'Mises à jour de mes candidatures',
                  emailWeeklySummary: 'Résumé hebdomadaire',
                  pushNotifications: 'Notifications push (navigateur)'
                }).map(([key, label]) => (
                  <div key={key} className="flex items-center justify-between">
                    <Label className="cursor-pointer">{label}</Label>
                    <input
                      type="checkbox"
                      checked={notifSettings[key as keyof typeof notifSettings]}
                      onChange={(e) => setNotifSettings({ ...notifSettings, [key]: e.target.checked })}
                      className="h-4 w-4"
                    />
                  </div>
                ))}
              </CardContent>
            </Card>
            <Button onClick={handleSaveNotifications} className="w-full md:w-auto">
              <Save className="mr-2 h-4 w-4" />
              Enregistrer les préférences
            </Button>
          </div>
        )}

        {activeTab === 'privacy' && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Données RGPD</CardTitle>
                <CardDescription>Exportez ou supprimez vos données</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button 
                  variant="outline" 
                  onClick={handleExportData} 
                  disabled={isExporting}
                  className="w-full"
                >
                  {isExporting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Export en cours...
                    </>
                  ) : (
                    <>
                      <Download className="mr-2 h-4 w-4" />
                      Exporter mes données (RGPD)
                    </>
                  )}
                </Button>
                <p className="text-sm text-gray-600">
                  Téléchargez toutes vos données personnelles au format JSON
                </p>
              </CardContent>
            </Card>

            <Card className="border-red-200">
              <CardHeader>
                <CardTitle className="text-red-600 flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  Zone dangereuse
                </CardTitle>
                <CardDescription>Actions irréversibles</CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="destructive" onClick={handleDeleteAccount} className="w-full">
                  <Trash2 className="mr-2 h-4 w-4" />
                  Supprimer définitivement mon compte
                </Button>
                <p className="text-sm text-red-600 mt-2">
                  ⚠️ Tous vos profils, candidatures et documents seront supprimés définitivement.
                </p>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}

"use client"

import { useState } from 'react';
import { Profile, ProfileCreate, ProfileUpdate } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface ProfileFormProps {
  profile?: Profile | null;
  onSubmit: (data: ProfileCreate | ProfileUpdate) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
  initialData?: any; // Données du CV parsé
}

export function ProfileForm({ profile, onSubmit, onCancel, isLoading = false, initialData }: ProfileFormProps) {
  const [formData, setFormData] = useState<ProfileCreate | ProfileUpdate>({
    title: initialData?.title || profile?.title || '',
    summary: initialData?.summary || profile?.summary || '',
    location: initialData?.location || profile?.location || '',
    phone: initialData?.phone || profile?.phone || '',
    linkedin_url: initialData?.linkedin_url || profile?.linkedin_url || '',
    github_url: initialData?.github_url || profile?.github_url || '',
    portfolio_url: initialData?.portfolio_url || profile?.portfolio_url || '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title || formData.title.trim().length === 0) {
      newErrors.title = 'Le titre professionnel est requis';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    try {
      // Inclure les données du CV parsé (experiences, educations, skills)
      const completeData = {
        ...formData,
        ...(initialData?.experiences && { experiences: initialData.experiences }),
        ...(initialData?.educations && { educations: initialData.educations }),
        ...(initialData?.skills && { skills: initialData.skills }),
      };
      
      await onSubmit(completeData);
    } catch (error) {
      console.error('Error submitting profile:', error);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{profile ? 'Modifier le profil' : 'Créer votre profil'}</CardTitle>
        <CardDescription>
          {initialData ? (
            <span className="text-green-600 font-medium">
              ✅ Données extraites de votre CV ! Vérifiez et complétez si nécessaire.
              {initialData.experiences?.length > 0 && ` ${initialData.experiences.length} expérience(s)`}
              {initialData.educations?.length > 0 && `, ${initialData.educations.length} formation(s)`}
              {initialData.skills?.length > 0 && `, ${initialData.skills.length} compétence(s)`}
            </span>
          ) : (
            'Renseignez vos informations professionnelles de base'
          )}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Titre professionnel */}
          <div className="space-y-2">
            <Label htmlFor="title">
              Titre professionnel <span className="text-red-500">*</span>
            </Label>
            <Input
              id="title"
              name="title"
              placeholder="ex: Senior Backend Developer"
              value={formData.title}
              onChange={handleChange}
              disabled={isLoading}
              className={errors.title ? 'border-red-500' : ''}
            />
            {errors.title && (
              <p className="text-sm text-red-500">{errors.title}</p>
            )}
          </div>

          {/* Résumé professionnel */}
          <div className="space-y-2">
            <Label htmlFor="summary">Résumé professionnel</Label>
            <Textarea
              id="summary"
              name="summary"
              placeholder="Décrivez brièvement votre parcours et vos compétences principales..."
              value={formData.summary || ''}
              onChange={handleChange}
              disabled={isLoading}
              rows={4}
            />
          </div>

          {/* Localisation */}
          <div className="space-y-2">
            <Label htmlFor="location">Localisation</Label>
            <Input
              id="location"
              name="location"
              placeholder="ex: Paris, France"
              value={formData.location || ''}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          {/* Téléphone */}
          <div className="space-y-2">
            <Label htmlFor="phone">Téléphone</Label>
            <Input
              id="phone"
              name="phone"
              type="tel"
              placeholder="ex: +33 6 12 34 56 78"
              value={formData.phone || ''}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          {/* LinkedIn */}
          <div className="space-y-2">
            <Label htmlFor="linkedin_url">LinkedIn</Label>
            <Input
              id="linkedin_url"
              name="linkedin_url"
              type="url"
              placeholder="https://linkedin.com/in/votre-profil"
              value={formData.linkedin_url || ''}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          {/* GitHub */}
          <div className="space-y-2">
            <Label htmlFor="github_url">GitHub</Label>
            <Input
              id="github_url"
              name="github_url"
              type="url"
              placeholder="https://github.com/votre-username"
              value={formData.github_url || ''}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          {/* Portfolio */}
          <div className="space-y-2">
            <Label htmlFor="portfolio_url">Portfolio / Site web</Label>
            <Input
              id="portfolio_url"
              name="portfolio_url"
              type="url"
              placeholder="https://votre-portfolio.com"
              value={formData.portfolio_url || ''}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          {/* Boutons d'action */}
          <div className="flex justify-end gap-2 pt-4">
            {onCancel && (
              <Button type="button" variant="outline" onClick={onCancel} disabled={isLoading}>
                Annuler
              </Button>
            )}
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Enregistrement...' : profile ? 'Mettre à jour' : 'Créer le profil'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

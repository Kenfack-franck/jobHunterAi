"use client"
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Profile, Experience, Education, Skill } from "@/types";
import profileService from "@/lib/profile";
import { ProfileForm } from "@/components/profile/ProfileForm";
import { ExperienceCard } from "@/components/profile/ExperienceCard";
import { ExperienceForm } from "@/components/profile/ExperienceForm";
import { EducationCard } from "@/components/profile/EducationCard";
import { EducationForm } from "@/components/profile/EducationForm";
import { SkillsList } from "@/components/profile/SkillsList";
import { SkillForm } from "@/components/profile/SkillForm";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [editingProfile, setEditingProfile] = useState(false);
  const [expFormOpen, setExpFormOpen] = useState(false);
  const [eduFormOpen, setEduFormOpen] = useState(false);
  const [skillFormOpen, setSkillFormOpen] = useState(false);
  const [editingExp, setEditingExp] = useState<Experience | null>(null);
  const [editingEdu, setEditingEdu] = useState<Education | null>(null);
  const [editingSkill, setEditingSkill] = useState<Skill | null>(null);

  useEffect(() => { 
    loadProfile(); 
  }, []);

  const loadProfile = async () => {
    try {
      const data = await profileService.getProfile();
      setProfile(data);
    } catch (err: any) {
      if (err.response?.status === 404) {
        router.push("/profile/create");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async (data: any) => {
    await profileService.updateProfile(data);
    setEditingProfile(false);
    await loadProfile();
  };

  const handleAddExperience = async (data: any) => {
    await profileService.addExperience(data);
    await loadProfile();
  };

  const handleUpdateExperience = async (data: any) => {
    if (editingExp) {
      await profileService.updateExperience(editingExp.id, data);
      setEditingExp(null);
      await loadProfile();
    }
  };

  const handleDeleteExperience = async (id: string) => {
    if (confirm("Supprimer cette expérience ?")) {
      await profileService.deleteExperience(id);
      await loadProfile();
    }
  };

  const handleAddEducation = async (data: any) => {
    await profileService.addEducation(data);
    await loadProfile();
  };

  const handleUpdateEducation = async (data: any) => {
    if (editingEdu) {
      await profileService.updateEducation(editingEdu.id, data);
      setEditingEdu(null);
      await loadProfile();
    }
  };

  const handleDeleteEducation = async (id: string) => {
    if (confirm("Supprimer cette formation ?")) {
      await profileService.deleteEducation(id);
      await loadProfile();
    }
  };

  const handleAddSkill = async (data: any) => {
    await profileService.addSkill(data);
    await loadProfile();
  };

  const handleUpdateSkill = async (data: any) => {
    if (editingSkill) {
      await profileService.updateSkill(editingSkill.id, data);
      setEditingSkill(null);
      await loadProfile();
    }
  };

  const handleDeleteSkill = async (id: string) => {
    await profileService.deleteSkill(id);
    await loadProfile();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Chargement...</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Redirection...</p>
      </div>
    );
  }

  const completion = profileService.calculateCompletion(profile);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4 space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Mon Profil</h1>
          <Button variant="outline" onClick={() => router.push("/dashboard")}>
            ← Dashboard
          </Button>
        </div>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">
                Profil complété à {completion}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-600 h-2 rounded-full transition-all" 
                style={{ width: completion + '%' }} 
              />
            </div>
          </CardContent>
        </Card>

        {editingProfile ? (
          <ProfileForm 
            profile={profile} 
            onSubmit={handleUpdateProfile} 
            onCancel={() => setEditingProfile(false)} 
          />
        ) : (
          <Card>
            <CardHeader>
              <div className="flex justify-between">
                <div>
                  <CardTitle>{profile.title}</CardTitle>
                  {profile.location && (
                    <CardDescription>{profile.location}</CardDescription>
                  )}
                </div>
                <Button onClick={() => setEditingProfile(true)}>
                  Modifier
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {profile.summary && <p>{profile.summary}</p>}
              <div className="grid grid-cols-2 gap-4 text-sm">
                {profile.phone && (
                  <div>
                    <span className="font-medium">Téléphone:</span> {profile.phone}
                  </div>
                )}
                {profile.linkedin_url && (
                  <a href={profile.linkedin_url} target="_blank" className="text-blue-600">
                    LinkedIn →
                  </a>
                )}
                {profile.github_url && (
                  <a href={profile.github_url} target="_blank" className="text-blue-600">
                    GitHub →
                  </a>
                )}
                {profile.portfolio_url && (
                  <a href={profile.portfolio_url} target="_blank" className="text-blue-600">
                    Portfolio →
                  </a>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        <div>
          <div className="flex justify-between mb-4">
            <h2 className="text-2xl font-bold">Expériences</h2>
            <Button onClick={() => setExpFormOpen(true)}>+ Ajouter</Button>
          </div>
          <div className="space-y-4">
            {profile.experiences.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center text-gray-500">
                  Aucune expérience
                </CardContent>
              </Card>
            ) : (
              profile.experiences.map(exp => (
                <ExperienceCard 
                  key={exp.id} 
                  experience={exp} 
                  onEdit={() => { 
                    setEditingExp(exp); 
                    setExpFormOpen(true); 
                  }} 
                  onDelete={handleDeleteExperience} 
                />
              ))
            )}
          </div>
        </div>

        <div>
          <div className="flex justify-between mb-4">
            <h2 className="text-2xl font-bold">Formations</h2>
            <Button onClick={() => setEduFormOpen(true)}>+ Ajouter</Button>
          </div>
          <div className="space-y-4">
            {profile.educations.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center text-gray-500">
                  Aucune formation
                </CardContent>
              </Card>
            ) : (
              profile.educations.map(edu => (
                <EducationCard 
                  key={edu.id} 
                  education={edu} 
                  onEdit={() => { 
                    setEditingEdu(edu); 
                    setEduFormOpen(true); 
                  }} 
                  onDelete={handleDeleteEducation} 
                />
              ))
            )}
          </div>
        </div>

        <SkillsList 
          skills={profile.skills} 
          onAdd={() => setSkillFormOpen(true)} 
          onEdit={(skill) => { 
            setEditingSkill(skill); 
            setSkillFormOpen(true); 
          }} 
          onDelete={handleDeleteSkill} 
        />
      </div>

      <ExperienceForm 
        open={expFormOpen} 
        onOpenChange={(open) => { 
          setExpFormOpen(open); 
          if (!open) setEditingExp(null); 
        }} 
        experience={editingExp} 
        onSubmit={editingExp ? handleUpdateExperience : handleAddExperience} 
      />
      
      <EducationForm 
        open={eduFormOpen} 
        onOpenChange={(open) => { 
          setEduFormOpen(open); 
          if (!open) setEditingEdu(null); 
        }} 
        education={editingEdu} 
        onSubmit={editingEdu ? handleUpdateEducation : handleAddEducation} 
      />
      
      <SkillForm 
        open={skillFormOpen} 
        onOpenChange={(open) => { 
          setSkillFormOpen(open); 
          if (!open) setEditingSkill(null); 
        }} 
        skill={editingSkill} 
        onSubmit={editingSkill ? handleUpdateSkill : handleAddSkill} 
      />
    </div>
  );
}

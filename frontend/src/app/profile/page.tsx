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
import { User, Briefcase, GraduationCap, Wrench, Plus, Edit, ArrowLeft, Sparkles } from "lucide-react";

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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-purple-50/30 to-blue-50/30 py-8 relative">
      {/* Animated background blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-1/4 w-96 h-96 bg-purple-400/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 left-1/4 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="max-w-5xl mx-auto px-4 space-y-8 relative z-10">
        <div className="flex justify-between items-center bg-white/70 backdrop-blur-lg rounded-2xl p-6 border-2 border-purple-100 shadow-lg">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-md">
              <User className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Mon Profil
            </h1>
          </div>
          <Button variant="outline" onClick={() => router.push("/dashboard")} className="hover:border-purple-400 transition-all gap-2">
            <ArrowLeft className="w-4 h-4" />
            Dashboard
          </Button>
        </div>

        <Card className="border-2 border-purple-200 shadow-lg bg-white/80 backdrop-blur-sm hover:shadow-xl transition-all">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-500" />
                Profil complété à {completion}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden shadow-inner">
              <div 
                className="h-3 rounded-full transition-all duration-500 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" 
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
          <Card className="border-2 border-blue-200 shadow-lg bg-white/80 backdrop-blur-sm hover:shadow-xl transition-all group">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="p-2 rounded-lg bg-blue-100 group-hover:bg-blue-200 transition-colors">
                      <User className="w-5 h-5 text-blue-600" />
                    </div>
                    <CardTitle className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                      {profile.title}
                    </CardTitle>
                  </div>
                  {profile.location && (
                    <CardDescription className="text-base">{profile.location}</CardDescription>
                  )}
                </div>
                <Button onClick={() => setEditingProfile(true)} className="gap-2 shadow-md hover:shadow-lg transition-all">
                  <Edit className="w-4 h-4" />
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
          <div className="flex justify-between items-center mb-4 bg-white/70 backdrop-blur-sm rounded-2xl p-5 border-2 border-purple-100 shadow-sm">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Briefcase className="w-6 h-6 text-purple-600" />
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Expériences
              </span>
            </h2>
            <Button onClick={() => setExpFormOpen(true)} className="gap-2 shadow-md hover:shadow-lg transition-all">
              <Plus className="w-4 h-4" />
              Ajouter
            </Button>
          </div>
          <div className="space-y-4">
            {profile.experiences.length === 0 ? (
              <Card className="border-2 border-dashed border-purple-200 bg-white/70 backdrop-blur-sm">
                <CardContent className="py-12 text-center text-gray-500">
                  <Briefcase className="w-12 h-12 text-purple-300 mx-auto mb-3" />
                  <p>Aucune expérience</p>
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
          <div className="flex justify-between items-center mb-4 bg-white/70 backdrop-blur-sm rounded-2xl p-5 border-2 border-blue-100 shadow-sm">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <GraduationCap className="w-6 h-6 text-blue-600" />
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Formations
              </span>
            </h2>
            <Button onClick={() => setEduFormOpen(true)} className="gap-2 shadow-md hover:shadow-lg transition-all">
              <Plus className="w-4 h-4" />
              Ajouter
            </Button>
          </div>
          <div className="space-y-4">
            {profile.educations.length === 0 ? (
              <Card className="border-2 border-dashed border-blue-200 bg-white/70 backdrop-blur-sm">
                <CardContent className="py-12 text-center text-gray-500">
                  <GraduationCap className="w-12 h-12 text-blue-300 mx-auto mb-3" />
                  <p>Aucune formation</p>
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

"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Trash2, Edit2, Plus, Check, X } from 'lucide-react';

interface CVReviewProps {
  parsedData: any;
  onConfirm: (editedData: any) => void;
  onCancel: () => void;
}

export function CVReview({ parsedData, onConfirm, onCancel }: CVReviewProps) {
  const [data, setData] = useState(parsedData);
  const [editingExp, setEditingExp] = useState<number | null>(null);
  const [editingEdu, setEditingEdu] = useState<number | null>(null);
  const [editingSkill, setEditingSkill] = useState<number | null>(null);

  // Expériences
  const removeExperience = (index: number) => {
    setData((prev: any) => ({
      ...prev,
      experiences: prev.experiences.filter((_: any, i: number) => i !== index)
    }));
  };

  const updateExperience = (index: number, field: string, value: any) => {
    setData((prev: any) => ({
      ...prev,
      experiences: prev.experiences.map((exp: any, i: number) => 
        i === index ? { ...exp, [field]: value } : exp
      )
    }));
  };

  // Formations
  const removeEducation = (index: number) => {
    setData((prev: any) => ({
      ...prev,
      educations: prev.educations.filter((_: any, i: number) => i !== index)
    }));
  };

  const updateEducation = (index: number, field: string, value: any) => {
    setData((prev: any) => ({
      ...prev,
      educations: prev.educations.map((edu: any, i: number) => 
        i === index ? { ...edu, [field]: value } : edu
      )
    }));
  };

  // Compétences
  const removeSkill = (index: number) => {
    setData((prev: any) => ({
      ...prev,
      skills: prev.skills.filter((_: any, i: number) => i !== index)
    }));
  };

  const updateSkill = (index: number, field: string, value: any) => {
    setData((prev: any) => ({
      ...prev,
      skills: prev.skills.map((skill: any, i: number) => 
        i === index ? { ...skill, [field]: value } : skill
      )
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Vérifiez vos informations</h1>
          <p className="text-gray-600">
            Revue des données extraites de votre CV. Modifiez, supprimez ou ajoutez ce que vous voulez.
          </p>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-3xl font-bold text-blue-600">{data.experiences?.length || 0}</div>
              <div className="text-sm text-gray-600">Expériences</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-3xl font-bold text-green-600">{data.educations?.length || 0}</div>
              <div className="text-sm text-gray-600">Formations</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6 text-center">
              <div className="text-3xl font-bold text-purple-600">{data.skills?.length || 0}</div>
              <div className="text-sm text-gray-600">Compétences</div>
            </CardContent>
          </Card>
        </div>

        {/* Informations de base */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Informations de base</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Nom complet</Label>
                <Input 
                  value={data.full_name || ''} 
                  onChange={(e) => setData({ ...data, full_name: e.target.value })}
                />
              </div>
              <div>
                <Label>Téléphone</Label>
                <Input 
                  value={data.phone || ''} 
                  onChange={(e) => setData({ ...data, phone: e.target.value })}
                />
              </div>
            </div>
            <div>
              <Label>Titre professionnel</Label>
              <Input 
                value={data.title || ''} 
                onChange={(e) => setData({ ...data, title: e.target.value })}
              />
            </div>
            <div>
              <Label>Résumé</Label>
              <Textarea 
                value={data.summary || ''} 
                onChange={(e) => setData({ ...data, summary: e.target.value })}
                rows={4}
              />
            </div>
          </CardContent>
        </Card>

        {/* Expériences */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>💼 Expériences professionnelles ({data.experiences?.length || 0})</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data.experiences && data.experiences.length > 0 ? (
              <div className="space-y-4">
                {data.experiences.map((exp: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4 relative">
                    <div className="absolute top-2 right-2 flex gap-2">
                      <Button 
                        size="sm" 
                        variant="ghost"
                        onClick={() => setEditingExp(editingExp === index ? null : index)}
                      >
                        <Edit2 className="w-4 h-4" />
                      </Button>
                      <Button 
                        size="sm" 
                        variant="ghost"
                        onClick={() => removeExperience(index)}
                      >
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </Button>
                    </div>
                    
                    {editingExp === index ? (
                      <div className="space-y-3 pr-20">
                        <Input 
                          placeholder="Titre du poste"
                          value={exp.title || ''} 
                          onChange={(e) => updateExperience(index, 'title', e.target.value)}
                        />
                        <Input 
                          placeholder="Entreprise"
                          value={exp.company || ''} 
                          onChange={(e) => updateExperience(index, 'company', e.target.value)}
                        />
                        <Textarea 
                          placeholder="Description"
                          value={exp.description || ''} 
                          onChange={(e) => updateExperience(index, 'description', e.target.value)}
                          rows={3}
                        />
                      </div>
                    ) : (
                      <div className="pr-20">
                        <h4 className="font-semibold">{exp.title}</h4>
                        <p className="text-sm text-gray-600">{exp.company}</p>
                        {exp.description && (
                          <p className="text-sm mt-2 text-gray-700">{exp.description}</p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Aucune expérience extraite</p>
            )}
          </CardContent>
        </Card>

        {/* Formations */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>🎓 Formations ({data.educations?.length || 0})</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data.educations && data.educations.length > 0 ? (
              <div className="space-y-4">
                {data.educations.map((edu: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4 relative">
                    <div className="absolute top-2 right-2 flex gap-2">
                      <Button 
                        size="sm" 
                        variant="ghost"
                        onClick={() => setEditingEdu(editingEdu === index ? null : index)}
                      >
                        <Edit2 className="w-4 h-4" />
                      </Button>
                      <Button 
                        size="sm" 
                        variant="ghost"
                        onClick={() => removeEducation(index)}
                      >
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </Button>
                    </div>
                    
                    {editingEdu === index ? (
                      <div className="space-y-3 pr-20">
                        <Input 
                          placeholder="Diplôme"
                          value={edu.degree || ''} 
                          onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                        />
                        <Input 
                          placeholder="Établissement"
                          value={edu.institution || ''} 
                          onChange={(e) => updateEducation(index, 'institution', e.target.value)}
                        />
                        <Input 
                          placeholder="Domaine d'études"
                          value={edu.field_of_study || ''} 
                          onChange={(e) => updateEducation(index, 'field_of_study', e.target.value)}
                        />
                      </div>
                    ) : (
                      <div className="pr-20">
                        <h4 className="font-semibold">{edu.degree}</h4>
                        <p className="text-sm text-gray-600">{edu.institution}</p>
                        {edu.field_of_study && (
                          <p className="text-sm text-gray-500">{edu.field_of_study}</p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Aucune formation extraite</p>
            )}
          </CardContent>
        </Card>

        {/* Compétences */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>⚡ Compétences ({data.skills?.length || 0})</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data.skills && data.skills.length > 0 ? (
              <div className="space-y-4">
                {/* Grouper par catégorie - en anglais maintenant */}
                {[
                  { key: 'language', label: 'Langages' },
                  { key: 'framework', label: 'Frameworks' },
                  { key: 'tool', label: 'Outils' },
                  { key: 'soft_skill', label: 'Soft Skills' },
                  { key: 'other', label: 'Autres' }
                ].map(({ key, label }) => {
                  const categorySkills = data.skills.filter((s: any) => s.category === key);
                  if (categorySkills.length === 0) return null;
                  
                  return (
                    <div key={key}>
                      <h4 className="font-semibold mb-2">{label}</h4>
                      <div className="flex flex-wrap gap-2">
                        {categorySkills.map((skill: any, index: number) => {
                          const globalIndex = data.skills.indexOf(skill);
                          return (
                            <Badge 
                              key={globalIndex} 
                              variant="secondary"
                              className="px-3 py-1 flex items-center gap-2"
                            >
                              {skill.name}
                              {skill.level && (
                                <span className="text-xs opacity-70">
                                  ({skill.level === 'beginner' ? 'Débutant' : 
                                    skill.level === 'intermediate' ? 'Intermédiaire' :
                                    skill.level === 'advanced' ? 'Avancé' : 
                                    skill.level === 'expert' ? 'Expert' : skill.level})
                                </span>
                              )}
                              <button
                                onClick={() => removeSkill(globalIndex)}
                                className="ml-1 hover:text-red-500"
                              >
                                <X className="w-3 h-3" />
                              </button>
                            </Badge>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Aucune compétence extraite</p>
            )}
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="flex gap-4 justify-end sticky bottom-4 bg-white p-4 rounded-lg shadow-lg border">
          <Button variant="outline" onClick={onCancel}>
            Annuler
          </Button>
          <Button onClick={() => onConfirm(data)} className="bg-green-600 hover:bg-green-700">
            <Check className="w-4 h-4 mr-2" />
            Confirmer et créer mon profil
          </Button>
        </div>
      </div>
    </div>
  );
}

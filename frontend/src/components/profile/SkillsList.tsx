"use client"

import { Skill, SkillLevel, SkillCategory } from '@/types';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface SkillsListProps {
  skills: Skill[];
  onEdit: (skill: Skill) => void;
  onDelete: (id: string) => void;
  onAdd: () => void;
}

const skillLevelLabels: Record<SkillLevel, string> = {
  [SkillLevel.BEGINNER]: 'Débutant',
  [SkillLevel.INTERMEDIATE]: 'Intermédiaire',
  [SkillLevel.ADVANCED]: 'Avancé',
  [SkillLevel.EXPERT]: 'Expert',
};

const skillCategoryLabels: Record<SkillCategory, string> = {
  [SkillCategory.LANGUAGE]: 'Langage',
  [SkillCategory.FRAMEWORK]: 'Framework',
  [SkillCategory.TOOL]: 'Outil',
  [SkillCategory.SOFT_SKILL]: 'Soft Skill',
  [SkillCategory.OTHER]: 'Autre',
};

export function SkillsList({ skills, onEdit, onDelete, onAdd }: SkillsListProps) {
  // Group skills by category
  const groupedSkills = skills.reduce((acc, skill) => {
    const category = skill.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(skill);
    return acc;
  }, {} as Record<SkillCategory, Skill[]>);

  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Compétences</CardTitle>
          <Button onClick={onAdd} size="sm">
            + Ajouter
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {skills.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            Aucune compétence ajoutée. Cliquez sur "Ajouter" pour commencer.
          </p>
        ) : (
          <div className="space-y-6">
            {Object.entries(groupedSkills).map(([category, categorySkills]) => (
              <div key={category}>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  {skillCategoryLabels[category as SkillCategory]}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {categorySkills.map((skill) => (
                    <div key={skill.id} className="group relative">
                      <Badge variant="outline" className="pr-16">
                        {skill.name} - {skillLevelLabels[skill.level]}
                      </Badge>
                      <div className="absolute right-1 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-5 w-5 p-0"
                          onClick={() => onEdit(skill)}
                        >
                          ✏️
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-5 w-5 p-0"
                          onClick={() => onDelete(skill.id)}
                        >
                          🗑️
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

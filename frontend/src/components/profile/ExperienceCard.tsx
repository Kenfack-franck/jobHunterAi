"use client"

import { Experience } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface ExperienceCardProps {
  experience: Experience;
  onEdit: (experience: Experience) => void;
  onDelete: (id: string) => void;
}

export function ExperienceCard({ experience, onEdit, onDelete }: ExperienceCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' });
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h3 className="text-lg font-semibold">{experience.title}</h3>
            <p className="text-md text-gray-600">{experience.company}</p>
            {experience.location && (
              <p className="text-sm text-gray-500">{experience.location}</p>
            )}
            
            <p className="text-sm text-gray-500 mt-1">
              {formatDate(experience.start_date)} - {experience.current ? 'Présent' : formatDate(experience.end_date!)}
            </p>

            {experience.description && (
              <p className="text-sm mt-3 text-gray-700">{experience.description}</p>
            )}

            {experience.technologies && experience.technologies.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3">
                {experience.technologies.map((tech, index) => (
                  <Badge key={index} variant="secondary">
                    {tech}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          <div className="flex gap-2 ml-4">
            <Button variant="outline" size="sm" onClick={() => onEdit(experience)}>
              Modifier
            </Button>
            <Button variant="destructive" size="sm" onClick={() => onDelete(experience.id)}>
              Supprimer
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

"use client"

import { Education } from '@/types';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface EducationCardProps {
  education: Education;
  onEdit: (education: Education) => void;
  onDelete: (id: string) => void;
}

export function EducationCard({ education, onEdit, onDelete }: EducationCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' });
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h3 className="text-lg font-semibold">{education.degree}</h3>
            <p className="text-md text-gray-600">{education.institution}</p>
            {education.location && (
              <p className="text-sm text-gray-500">{education.location}</p>
            )}
            
            <p className="text-sm text-gray-500 mt-1">
              {formatDate(education.start_date)} - {education.end_date ? formatDate(education.end_date) : 'En cours'}
            </p>

            {education.description && (
              <p className="text-sm mt-3 text-gray-700">{education.description}</p>
            )}
          </div>

          <div className="flex gap-2 ml-4">
            <Button variant="outline" size="sm" onClick={() => onEdit(education)}>
              Modifier
            </Button>
            <Button variant="destructive" size="sm" onClick={() => onDelete(education.id)}>
              Supprimer
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

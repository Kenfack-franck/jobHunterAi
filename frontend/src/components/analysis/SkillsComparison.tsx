/**
 * Composant d'affichage de la comparaison des compétences
 */
import { Badge } from '@/components/ui/badge';

interface SkillsComparisonProps {
  matchingSkills: string[];
  missingSkills: string[];
}

export default function SkillsComparison({
  matchingSkills,
  missingSkills,
}: SkillsComparisonProps) {
  return (
    <div className="bg-white rounded-lg border p-6 shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Analyse des Compétences</h3>

      {/* Compétences correspondantes */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-green-600 text-xl">✓</span>
          <h4 className="font-medium text-gray-900">
            Compétences qui correspondent ({matchingSkills.length})
          </h4>
        </div>
        {matchingSkills.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {matchingSkills.map((skill) => (
              <Badge
                key={skill}
                className="bg-green-100 text-green-800 hover:bg-green-200"
              >
                {skill}
              </Badge>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500 italic">
            Aucune compétence ne correspond directement
          </p>
        )}
      </div>

      {/* Compétences manquantes */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-orange-600 text-xl">!</span>
          <h4 className="font-medium text-gray-900">
            Compétences à acquérir ({missingSkills.length})
          </h4>
        </div>
        {missingSkills.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill) => (
              <Badge
                key={skill}
                className="bg-orange-100 text-orange-800 hover:bg-orange-200"
              >
                {skill}
              </Badge>
            ))}
          </div>
        ) : (
          <p className="text-sm text-green-600 font-medium">
            ✓ Vous possédez toutes les compétences demandées !
          </p>
        )}
      </div>
    </div>
  );
}

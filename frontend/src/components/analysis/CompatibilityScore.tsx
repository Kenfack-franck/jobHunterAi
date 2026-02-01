/**
 * Composant d'affichage du score de compatibilité avec jauge circulaire
 */
interface CompatibilityScoreProps {
  score: number;
  semanticScore: number;
  skillMatchScore: number;
  experienceScore: number;
}

export default function CompatibilityScore({
  score,
  semanticScore,
  skillMatchScore,
  experienceScore,
}: CompatibilityScoreProps) {
  // Déterminer la couleur selon le score
  const getScoreColor = (s: number) => {
    if (s >= 70) return 'text-green-600';
    if (s >= 50) return 'text-yellow-600';
    if (s >= 30) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreLabel = (s: number) => {
    if (s >= 70) return '🟢 Excellent match';
    if (s >= 50) return '🟡 Bon match';
    if (s >= 30) return '🟠 Match moyen';
    return '🔴 Match faible';
  };

  // Calcul SVG pour la jauge circulaire
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="bg-white rounded-lg border p-6 shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Score de Compatibilité</h3>

      {/* Jauge circulaire */}
      <div className="flex flex-col items-center mb-6">
        <div className="relative inline-flex items-center justify-center">
          <svg className="transform -rotate-90" width="180" height="180">
            {/* Cercle de fond */}
            <circle
              cx="90"
              cy="90"
              r={radius}
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              className="text-gray-200"
            />
            {/* Cercle de progression */}
            <circle
              cx="90"
              cy="90"
              r={radius}
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className={`${getScoreColor(score)} transition-all duration-1000 ease-out`}
            />
          </svg>
          <div className="absolute text-center">
            <div className={`text-4xl font-bold ${getScoreColor(score)}`}>
              {Math.round(score)}%
            </div>
          </div>
        </div>
        <p className="text-sm text-gray-600 mt-2">{getScoreLabel(score)}</p>
      </div>

      {/* Détails des scores */}
      <div className="space-y-3">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600">Similarité sémantique</span>
            <span className="font-medium">{Math.round(semanticScore)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-1000"
              style={{ width: `${semanticScore}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600">Correspondance compétences</span>
            <span className="font-medium">{Math.round(skillMatchScore)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-purple-600 h-2 rounded-full transition-all duration-1000"
              style={{ width: `${skillMatchScore}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-600">Expériences pertinentes</span>
            <span className="font-medium">{Math.round(experienceScore)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-green-600 h-2 rounded-full transition-all duration-1000"
              style={{ width: `${experienceScore}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

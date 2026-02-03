# Test du flux d'authentification

## Problème rapporté
1. La connexion ne fonctionne pas
2. Le bouton "Se connecter" dans register ne redirige pas

## Corrections appliquées

### ✅ Navigation entre pages
- **Login → Register** : Changé de `<Link><Button></Button></Link>` à `<Button onClick={() => router.push('/auth/register')}>`
- **Register → Login** : Changé de `<Link><Button></Button></Link>` à `<Button onClick={() => router.push('/auth/login')}>`
- Ajouté `type="button"` pour éviter la soumission du formulaire

### Structure vérifiée
- ✅ Formulaire avec `<form onSubmit={handleSubmit}>`
- ✅ Button submit avec `type="submit"`
- ✅ Logic `handleSubmit` intacte
- ✅ AuthContext `login()` appelé correctement
- ✅ Redirection vers `/dashboard` après succès

## À tester
1. **Page de connexion** (`/auth/login`)
   - Saisir email et mot de passe
   - Cliquer sur "Se connecter"
   - Vérifier la redirection vers `/dashboard`
   - Vérifier le toast de succès

2. **Page d'inscription** (`/auth/register`)
   - Saisir les informations
   - Cliquer sur "Créer mon compte"
   - Vérifier la connexion auto et redirection

3. **Navigation entre pages**
   - Dans login, cliquer "Créer un compte" → doit aller à `/auth/register`
   - Dans register, cliquer "Se connecter" → doit aller à `/auth/login`

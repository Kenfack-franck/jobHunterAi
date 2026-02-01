"use client"
import { useState } from "react";
import { Skill, SkillCreate, SkillUpdate, SkillLevel, SkillCategory } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogFooter } from "@/components/ui/dialog";

interface SkillFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  skill?: Skill | null;
  onSubmit: (data: SkillCreate | SkillUpdate) => Promise<void>;
}

export function SkillForm({ open, onOpenChange, skill, onSubmit }: SkillFormProps) {
  const [formData, setFormData] = useState<SkillCreate | SkillUpdate>({
    name: skill?.name || "",
    category: skill?.category || SkillCategory.LANGUAGE,
    level: skill?.level || SkillLevel.INTERMEDIATE,
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onSubmit(formData);
      onOpenChange(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent title={skill ? "Modifier la compétence" : "Ajouter une compétence"}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Nom *</Label>
            <Input id="name" name="name" value={formData.name} onChange={handleChange} required placeholder="ex: Python, React, Docker..." />
          </div>
          <div className="space-y-2">
            <Label htmlFor="category">Catégorie *</Label>
            <select 
              id="category" 
              name="category" 
              value={formData.category} 
              onChange={handleChange} 
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
            >
              <option value={SkillCategory.LANGUAGE}>Langage</option>
              <option value={SkillCategory.FRAMEWORK}>Framework</option>
              <option value={SkillCategory.TOOL}>Outil</option>
              <option value={SkillCategory.SOFT_SKILL}>Soft Skill</option>
              <option value={SkillCategory.OTHER}>Autre</option>
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="level">Niveau *</Label>
            <select 
              id="level" 
              name="level" 
              value={formData.level} 
              onChange={handleChange} 
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
            >
              <option value={SkillLevel.BEGINNER}>Débutant</option>
              <option value={SkillLevel.INTERMEDIATE}>Intermédiaire</option>
              <option value={SkillLevel.ADVANCED}>Avancé</option>
              <option value={SkillLevel.EXPERT}>Expert</option>
            </select>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>Annuler</Button>
            <Button type="submit" disabled={loading}>{loading ? "Enregistrement..." : "Enregistrer"}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

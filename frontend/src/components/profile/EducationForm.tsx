"use client"
import { useState } from "react";
import { Education, EducationCreate, EducationUpdate } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogFooter } from "@/components/ui/dialog";

interface EducationFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  education?: Education | null;
  onSubmit: (data: EducationCreate | EducationUpdate) => Promise<void>;
}

export function EducationForm({ open, onOpenChange, education, onSubmit }: EducationFormProps) {
  const [formData, setFormData] = useState<EducationCreate | EducationUpdate>({
    degree: education?.degree || "",
    institution: education?.institution || "",
    field_of_study: education?.field_of_study || "",
    location: education?.location || "",
    start_date: education?.start_date?.split("T")[0] || "",
    end_date: education?.end_date?.split("T")[0] || "",
    description: education?.description || "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Clean empty strings to undefined for optional fields
      const cleanedData: any = { ...formData };
      
      if (cleanedData.end_date === "") {
        cleanedData.end_date = undefined;
      }
      if (cleanedData.location === "") {
        cleanedData.location = undefined;
      }
      if (cleanedData.field_of_study === "") {
        cleanedData.field_of_study = undefined;
      }
      if (cleanedData.description === "") {
        cleanedData.description = undefined;
      }
      
      await onSubmit(cleanedData);
      onOpenChange(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent title={education ? "Modifier la formation" : "Ajouter une formation"}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="degree">Diplôme *</Label>
            <Input id="degree" name="degree" value={formData.degree} onChange={handleChange} required placeholder="ex: Master en Informatique" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="institution">Établissement *</Label>
            <Input id="institution" name="institution" value={formData.institution} onChange={handleChange} required placeholder="ex: Université Paris-Saclay" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="field_of_study">Domaine d'études</Label>
            <Input id="field_of_study" name="field_of_study" value={formData.field_of_study || ""} onChange={handleChange} placeholder="ex: Informatique, Génie Logiciel" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="location">Localisation</Label>
            <Input id="location" name="location" value={formData.location || ""} onChange={handleChange} placeholder="ex: Orsay, France" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="start_date">Date de début *</Label>
              <Input id="start_date" name="start_date" type="date" value={formData.start_date} onChange={handleChange} required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="end_date">Date de fin</Label>
              <Input id="end_date" name="end_date" type="date" value={formData.end_date || ""} onChange={handleChange} />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea 
              id="description" 
              name="description" 
              value={formData.description || ""} 
              onChange={handleChange}
              rows={3}
              placeholder="Projets, cours, mentions..."
            />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Annuler
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? "Enregistrement..." : education ? "Modifier" : "Ajouter"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

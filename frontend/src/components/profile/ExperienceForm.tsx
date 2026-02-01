"use client"
import { useState } from "react";
import { Experience, ExperienceCreate, ExperienceUpdate } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";

interface ExperienceFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  experience?: Experience | null;
  onSubmit: (data: ExperienceCreate | ExperienceUpdate) => Promise<void>;
}

export function ExperienceForm({ open, onOpenChange, experience, onSubmit }: ExperienceFormProps) {
  const [formData, setFormData] = useState<ExperienceCreate | ExperienceUpdate>({
    title: experience?.title || "",
    company: experience?.company || "",
    location: experience?.location || "",
    start_date: experience?.start_date?.split("T")[0] || "",
    end_date: experience?.end_date?.split("T")[0] || "",
    current: experience?.current || false,
    description: experience?.description || "",
    technologies: experience?.technologies || [],
  });
  const [techInput, setTechInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    setFormData(prev => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const addTechnology = () => {
    if (techInput.trim()) {
      setFormData(prev => ({ ...prev, technologies: [...(prev.technologies || []), techInput.trim()] }));
      setTechInput("");
    }
  };

  const removeTechnology = (index: number) => {
    setFormData(prev => ({ ...prev, technologies: prev.technologies?.filter((_, i) => i !== index) }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Clean empty strings to null/undefined before sending
      const cleanedData: any = { ...formData };
      
      // Convert empty strings to undefined for optional fields
      if (cleanedData.end_date === "") {
        cleanedData.end_date = undefined;
      }
      if (cleanedData.location === "") {
        cleanedData.location = undefined;
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
      <DialogContent title={experience ? "Modifier l'expérience" : "Ajouter une expérience"}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">Poste *</Label>
            <Input id="title" name="title" value={formData.title} onChange={handleChange} required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="company">Entreprise *</Label>
            <Input id="company" name="company" value={formData.company} onChange={handleChange} required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="location">Localisation</Label>
            <Input id="location" name="location" value={formData.location || ""} onChange={handleChange} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="start_date">Date de début *</Label>
              <Input id="start_date" name="start_date" type="date" value={formData.start_date} onChange={handleChange} required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="end_date">Date de fin</Label>
              <Input 
                id="end_date" 
                name="end_date" 
                type="date" 
                value={formData.end_date || ""} 
                onChange={handleChange}
                disabled={formData.current}
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Input 
              id="current" 
              name="current" 
              type="checkbox" 
              checked={formData.current} 
              onChange={handleChange}
              className="w-4 h-4"
            />
            <Label htmlFor="current" className="font-normal">Poste actuel</Label>
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea 
              id="description" 
              name="description" 
              value={formData.description || ""} 
              onChange={handleChange}
              rows={4}
            />
          </div>
          <div className="space-y-2">
            <Label>Technologies</Label>
            <div className="flex gap-2">
              <Input 
                value={techInput} 
                onChange={(e) => setTechInput(e.target.value)}
                placeholder="Ex: Python, FastAPI..."
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTechnology())}
              />
              <Button type="button" onClick={addTechnology} variant="outline">
                Ajouter
              </Button>
            </div>
            {formData.technologies && formData.technologies.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {formData.technologies.map((tech, index) => (
                  <span 
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center gap-2"
                  >
                    {tech}
                    <button
                      type="button"
                      onClick={() => removeTechnology(index)}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Annuler
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? "Enregistrement..." : experience ? "Modifier" : "Ajouter"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

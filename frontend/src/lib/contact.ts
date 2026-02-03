import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface ContactMessage {
  name: string;
  email: string;
  subject: string;
  message: string;
}

class ContactService {
  async sendMessage(data: ContactMessage): Promise<void> {
    const token = localStorage.getItem('auth_token');
    const headers: any = {
      'Content-Type': 'application/json',
    };

    // Ajouter le token si disponible (optionnel pour contact)
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    await axios.post(`${API_URL}/contact/send`, data, { headers });
  }
}

export const contactService = new ContactService();

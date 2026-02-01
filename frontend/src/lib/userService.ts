import apiClient from './api';

export interface UpdateUserRequest {
  full_name?: string;
  language?: string;
}

export interface UpdatePasswordRequest {
  current_password: string;
  new_password: string;
}

class UserService {
  async updateProfile(data: UpdateUserRequest) {
    const response = await apiClient.put('/auth/me', data);
    return response.data;
  }

  async updatePassword(data: UpdatePasswordRequest) {
    // Note: Cette route n'existe peut-être pas encore
    // TODO: Vérifier avec le backend
    const response = await apiClient.put('/auth/me/password', data);
    return response.data;
  }

  async deleteAccount() {
    // Note: Cette route n'existe peut-être pas encore
    // TODO: Vérifier avec le backend
    await apiClient.delete('/auth/me');
  }

  async exportData() {
    const response = await apiClient.get('/auth/me/export', {
      responseType: 'blob'
    });
    return response.data;
  }
}

export const userService = new UserService();

export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  phone_number?: string;
  is_verified?: boolean;
  profile_image?: string | null;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  tokens: AuthTokens;
  user: User;
}

export interface Session {
  id: string;
  ip_address: string;
  user_agent: string;
  last_active: string;
  is_current_session: boolean;
}

export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isInitialized: boolean;
  initializeAuth: () => void;
  setTokens: (tokens: AuthTokens) => void;
  setUser: (user: User) => void;
  clearAuth: () => void;
  logout: () => void;
}
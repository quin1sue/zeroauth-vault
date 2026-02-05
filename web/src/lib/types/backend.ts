export type GoogleAuthResponse = {
  credential?: string;
  clientId?: string;
}

export type AuthTokenResponse = {
  accessToken: string;
  token_type: string;
  user: {
    id: string;
    email: string;
  }
}
export interface Organization {
  id: string;
  name: string;
  created_at: string;
  created_by: string;
}

export interface UserProfile {
  id: string;
  user_id: string;
  organization_id?: string;
  role?: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Database {
  public: {
    Tables: {
      organizations: {
        Row: Organization;
        Insert: Omit<Organization, "id" | "created_at">;
        Update: Partial<Omit<Organization, "id" | "created_at">>;
      };
      user_profiles: {
        Row: UserProfile;
        Insert: Omit<UserProfile, "id" | "created_at" | "updated_at">;
        Update: Partial<Omit<UserProfile, "id" | "created_at">>;
      };
    };
  };
}

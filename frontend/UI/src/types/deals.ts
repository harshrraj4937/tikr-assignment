import { User } from './auth';

export interface Deal {
  id: number;
  name: string;
  company_url: string | null;
  owner: User;
  stage: string;
  round: string | null;
  check_size: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface DealCreate {
  name: string;
  company_url?: string;
  round?: string;
  check_size?: number;
}

export interface DealUpdate {
  name?: string;
  company_url?: string;
  round?: string;
  check_size?: number;
}

export interface DealStageUpdate {
  stage: string;
}

export interface Activity {
  id: number;
  deal_id: number;
  user: User;
  action: string;
  created_at: string;
}


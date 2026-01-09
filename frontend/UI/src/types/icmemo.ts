import { User } from './auth';

export interface ICMemoSections {
  summary: string;
  market: string;
  product: string;
  traction: string;
  risks: string;
  open_questions: string;
}

export interface ICMemo {
  id: number;
  deal_id: number;
  version: number;
  sections: ICMemoSections;
  created_by: User;
  created_at: string;
}

export interface ICMemoCreate {
  sections: ICMemoSections;
}

export const MEMO_SECTION_LABELS: { [key in keyof ICMemoSections]: string } = {
  summary: 'Summary',
  market: 'Market',
  product: 'Product',
  traction: 'Traction',
  risks: 'Risks',
  open_questions: 'Open Questions',
};

export const MEMO_SECTION_DESCRIPTIONS: { [key in keyof ICMemoSections]: string } = {
  summary: 'Executive summary of the investment opportunity',
  market: 'Market size, opportunity, and competition analysis',
  product: 'What the company builds and how it works',
  traction: 'Metrics, growth, revenue, user base',
  risks: 'What could go wrong with this investment',
  open_questions: 'Things that need more investigation',
};



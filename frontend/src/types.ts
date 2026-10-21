export type LineType =
  | "input"
  | "output"
  | "tool"
  | "success"
  | "info"
  | "warn"
  | "muted"
  | "accent"
  | "diff";

export interface TerminalLine {
  type: LineType;
  text: string;
}

export interface TerminalStep {
  id: string;
  title: string;
  narration: string;
  command?: string;
  lines: TerminalLine[];
  tip?: string;
}

export interface Agent {
  id: string;
  name: string;
  tagline: string;
  kind: string;
  license: string;
  docs: string;
  repo: string;
  install: string;
  install_alt: string;
  install_windows: string;
  best_for: string;
  highlights: string[];
  commands: [string, string][];
  walkthroughs: string[];
  accent: string;
  stars?: string;
  verified?: boolean;
}

export interface Walkthrough {
  id: string;
  title: string;
  agent: string;
  level: string;
  duration_min: number;
  summary: string;
  outcome: string[];
  steps: TerminalStep[];
}

export interface CheatsheetRow {
  agent: string;
  group: string;
  command: string;
  description: string;
}

export interface LoopStage {
  id: string;
  title: string;
  body: string;
  you_control: string;
  failure: string;
}

export interface CraftExample {
  lines: TerminalLine[];
}

export interface Craft {
  id: string;
  title: string;
  body: string;
  before: CraftExample;
  after: CraftExample;
  rule: string;
}

export interface ModelGuide {
  id: string;
  title: string;
  body: string;
  rows: string[][];
}

export interface ConfigSnippet {
  title: string;
  language: string;
  code: string;
}

export interface ProviderInfo {
  id: string;
  label: string;
  kind: string;
  tier: string;
  tags: string[];
  note: string;
  signup_url: string;
  requires_key: boolean;
  default_base_url: string;
  env_key: string;
  has_key: boolean;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  provider_label: string;
  description: string;
  context_window: string;
  free: boolean;
  requires_key: boolean;
}

export interface ComparisonRow {
  feature: string;
  values: Record<string, boolean>;
}

export interface HarnessLayer {
  id: string;
  title: string;
  body: string;
  control: string;
  fails: string;
}

export interface HarnessProject {
  id: string;
  name: string;
  repo: string;
  stars: string;
  license: string;
  tagline: string;
  why: string;
  steal: string;
}

export interface SkillFormat {
  id: string;
  title: string;
  body: string;
  why_it_matters: string;
  locations: string[];
  frontmatter: Record<string, string>;
  example: string;
  permissions: string;
  troubleshooting: string[];
}

export interface SkillPackage {
  id: string;
  name: string;
  repo: string;
  stars: string;
  license: string;
  tagline: string;
  what: string;
}

export interface Orchestrator {
  id: string;
  name: string;
  repo: string;
  stars: string;
  kind: string;
  what: string;
}

export interface Protocol {
  id: string;
  name: string;
  what: string;
  portable: string;
  cost: string;
  example: string;
}

export interface ContextEntry {
  id: string;
  title: string;
  body: string;
  bad: string;
  good: string;
}

export interface SiteContent {
  agents: Agent[];
  walkthroughs: Walkthrough[];
  cheatsheet: CheatsheetRow[];
  cheatsheet_groups: string[];
  loop_stages: LoopStage[];
  craft: Craft[];
  model_guide: ModelGuide[];
  config_snippets: ConfigSnippet[];
  comparison: ComparisonRow[];
  providers: ProviderInfo[];
  models: ModelInfo[];
  harness_layers: HarnessLayer[];
  harness_projects: HarnessProject[];
  skill_format: SkillFormat;
  skill_packages: SkillPackage[];
  orchestrators: Orchestrator[];
  protocols: Protocol[];
  context_playbook: ContextEntry[];
}

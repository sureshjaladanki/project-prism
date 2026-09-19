import { readFileSync } from "node:fs";
import path from "node:path";

export type PrismPage = "home" | "sleeve" | "slice" | "house" | "notfound";

export type SiteSleeve = {
  token: string;
  path: string;
  header_label: string;
  hub_label: string;
};

export type SiteSlice = {
  template_id: string;
  charter: string;
  sleeve: string;
  slug: string;
  path: string;
  citizen_question: string;
  fact_lede: string;
  vintage_id: string;
};

export type SiteHouse = {
  path: string;
  title: string;
  h1: string;
  description: string;
};

export type SiteCatalog = {
  cms_mode: "preview" | "citizen";
  vintage_id: string;
  sleeves: SiteSleeve[];
  slices: SiteSlice[];
  house: SiteHouse[];
};

export type SliceBound = {
  template_id: string;
  vintage_id: string;
  charts: Record<string, unknown>;
  body: string;
};

const boundDir = process.env.PRISM_BOUND_DIR ?? "";
if (!boundDir) {
  throw new Error("PRISM_BOUND_DIR is required");
}

export const HOME_TITLE = "Prism — official numbers on India";
export const HOME_DESCRIPTION =
  "Give anyone in India a clear, non-partisan picture of the country from official government statistics — and nothing else.";
export const HOME_H1 =
  "A shared, checkable picture of India that does not belong to a party, a ministry, or a news cycle.";

export function loadSite(): SiteCatalog {
  return JSON.parse(
    readFileSync(path.join(boundDir, "site.json"), "utf8"),
  ) as SiteCatalog;
}

export function loadSliceBound(templateId: string): SliceBound {
  const dir = path.join(boundDir, "slices", templateId);
  const bound = JSON.parse(
    readFileSync(path.join(dir, "bound.json"), "utf8"),
  ) as Omit<SliceBound, "body">;
  const body = readFileSync(path.join(dir, "body.html"), "utf8");
  return { ...bound, body };
}

export function hubDescription(hubLabel: string): string {
  return `Official statistics on ${hubLabel}, from the producing agencies.`;
}

export function sleeveByPath(
  site: SiteCatalog,
  sleevePath: string,
): SiteSleeve | undefined {
  return site.sleeves.find((sleeve) => sleeve.path === sleevePath);
}

export function slicesInSleeve(
  site: SiteCatalog,
  sleeveToken: string,
): SiteSlice[] {
  return site.slices.filter((slice) => slice.sleeve === sleeveToken);
}

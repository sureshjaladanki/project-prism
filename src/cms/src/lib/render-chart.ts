import * as vega from "vega";
import * as vegaLite from "vega-lite";

type Json = Record<string, unknown>;

/** Plot width that fits the 46rem portrait column after axes. */
const PORTRAIT_PLOT_WIDTH = 640;
const PORTRAIT_PLOT_HEIGHT = 280;

function stripUnsupportedInvalid(node: unknown): void {
  if (Array.isArray(node)) {
    for (const item of node) {
      stripUnsupportedInvalid(item);
    }
    return;
  }
  if (node === null || typeof node !== "object") {
    return;
  }
  const record = node as Json;
  const mark = record.mark;
  if (mark !== null && typeof mark === "object" && !Array.isArray(mark)) {
    const { invalid: _ignored, ...rest } = mark as Json;
    record.mark = rest;
  }
  for (const value of Object.values(record)) {
    stripUnsupportedInvalid(value);
  }
}

function wrapLine(text: string, maxChars: number): string[] {
  const words = text.trim().split(/\s+/);
  const lines: string[] = [];
  let current = words[0];
  for (const word of words.slice(1)) {
    const next = `${current} ${word}`;
    if (next.length > maxChars) {
      lines.push(current);
      current = word;
    } else {
      current = next;
    }
  }
  lines.push(current);
  return lines;
}

function wrapTitleField(value: unknown, maxChars: number): unknown {
  if (typeof value !== "string") {
    return value;
  }
  const lines = wrapLine(value, maxChars);
  return lines.length === 1 ? lines[0] : lines;
}

function applyPortraitFrame(spec: Json): void {
  if (spec.width === undefined) {
    spec.width = PORTRAIT_PLOT_WIDTH;
  }
  if (spec.height === undefined) {
    spec.height = PORTRAIT_PLOT_HEIGHT;
  }
  // Vega sizes the SVG to the title if it is unlimited. Long subtitles then
  // become 2–3k px wide; CSS max-width scales the plot down with them.
  const titleChars = Math.max(36, Math.floor(PORTRAIT_PLOT_WIDTH / 10));
  const subtitleChars = Math.max(42, Math.floor(PORTRAIT_PLOT_WIDTH / 9));
  const title = spec.title;
  if (typeof title === "string") {
    spec.title = { text: wrapTitleField(title, titleChars) };
  } else if (
    title !== null &&
    typeof title === "object" &&
    !Array.isArray(title)
  ) {
    const record = title as Json;
    spec.title = {
      ...record,
      text: wrapTitleField(record.text, titleChars),
      ...(record.subtitle === undefined
        ? {}
        : { subtitle: wrapTitleField(record.subtitle, subtitleChars) }),
    };
  }
  const config = (spec.config ?? {}) as Json;
  const titleConfig = (config.title ?? {}) as Json;
  const axis = (config.axis ?? {}) as Json;
  const legend = (config.legend ?? {}) as Json;
  spec.config = {
    ...config,
    axis: { labelFontSize: 12, titleFontSize: 12, ...axis },
    legend: { labelFontSize: 12, titleFontSize: 12, ...legend },
    title: {
      fontSize: 14,
      subtitleFontSize: 11,
      subtitleLineHeight: 16,
      ...titleConfig,
    },
  };
}

export async function specToSvg(spec: unknown): Promise<string> {
  const clone = structuredClone(spec) as Json;
  stripUnsupportedInvalid(clone);
  applyPortraitFrame(clone);
  const compiled = vegaLite.compile(clone as vegaLite.TopLevelSpec).spec;
  const runtime = vega.parse(compiled);
  const view = new vega.View(runtime, { renderer: "none" });
  return await view.toSVG();
}

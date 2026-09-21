/** Civic desk tokens. Pages and charts inherit; they do not restyle. */

export const color = {
  paper: "#F3EEE6",
  card: "#FFFFFF",
  well: "#EAF0F5",
  ink: "#1C1A17",
  muted: "#5B5548",
  rule: "#DDD6C9",
  mark: "#1F4E79",
  mark2: "#9C5233",
  mark3: "#4A6670",
  mark4: "#5C5C5C",
  hole: "#6E6656",
  focus: "#1F4E79",
  break: "#332E27",
  holeBand: "#E7E0D2",
  ruleStrong: "#8C8370",
} as const;

export const type = {
  sans: "IBM Plex Sans",
  serif: "IBM Plex Serif",
  mono: "IBM Plex Mono",
  sansStack:
    '"IBM Plex Sans", "Source Sans 3", "Segoe UI", system-ui, sans-serif',
  serifStack: '"IBM Plex Serif", Georgia, "Times New Roman", serif',
  monoStack: '"IBM Plex Mono", ui-monospace, monospace',
} as const;

export const space = {
  1: "4px",
  2: "8px",
  3: "12px",
  4: "16px",
  5: "24px",
  6: "32px",
  7: "48px",
  8: "72px",
} as const;

export const measure = {
  prose: "40rem",
  desk: "68rem",
  radius: "12px",
  radiusLg: "20px",
  hair: "1px",
  headerRule: "4px",
  lift: "0 1px 3px rgb(28 26 23 / 0.08)",
  liftAnswer:
    "0 10px 24px rgb(28 26 23 / 0.10), 0 2px 6px rgb(28 26 23 / 0.06)",
} as const;

export const chart = {
  plotWidth: 720,
  plotHeight: 280,
  barStep: 26,
  barPaddingInner: 0.3,
  barCornerRadius: 2,
  labelSize: 12,
  lineStrokeWidth: 2,
  valueLabelPad: 96,
  fitWidth: 974,
  minScale: 1,
  series: [color.mark, color.mark2, color.mark3, color.mark4] as const,
  gridOpacity: 0.5,
  axisSize: 12,
} as const;

export const cssVars: Record<string, string> = {
  paper: color.paper,
  card: color.card,
  well: color.well,
  ink: color.ink,
  muted: color.muted,
  rule: color.rule,
  mark: color.mark,
  "mark-2": color.mark2,
  "mark-3": color.mark3,
  "mark-4": color.mark4,
  hole: color.hole,
  "hole-band": color.holeBand,
  focus: color.focus,
  break: color.break,
  "rule-strong": color.ruleStrong,
  "space-1": space[1],
  "space-2": space[2],
  "space-3": space[3],
  "space-4": space[4],
  "space-5": space[5],
  "space-6": space[6],
  "space-7": space[7],
  "space-8": space[8],
  measure: measure.prose,
  desk: measure.desk,
  radius: measure.radius,
  "radius-lg": measure.radiusLg,
  lift: measure.lift,
  "lift-answer": measure.liftAnswer,
  hair: measure.hair,
  "header-rule": measure.headerRule,
  "font-sans": type.sansStack,
  "font-serif": type.serifStack,
  "font-mono": type.monoStack,
  "chart-fit-width": `${chart.fitWidth}px`,
  "chart-min-scale": String(chart.minScale),
};

export const rootStyle = Object.entries(cssVars)
  .map(([name, value]) => `--${name}: ${value}`)
  .join("; ");

export function vegaConfig(): Record<string, unknown> {
  const face = type.sans;
  return {
    font: face,
    padding: { left: 4, right: 8, top: 4, bottom: 4 },
    view: { stroke: null },
    axis: {
      labelFont: face,
      titleFont: face,
      labelColor: color.muted,
      titleColor: color.muted,
      labelFontSize: chart.axisSize,
      titleFontSize: chart.axisSize,
      labelAngle: 0,
      grid: false,
      gridColor: color.rule,
      gridOpacity: chart.gridOpacity,
      domainColor: color.ruleStrong,
      tickColor: color.ruleStrong,
    },
    axisQuantitative: {
      grid: true,
      gridColor: color.rule,
      gridOpacity: chart.gridOpacity,
      domainColor: color.ruleStrong,
      domainWidth: 1,
      tickColor: color.ruleStrong,
      labelExpr: "indianFormat(datum.value)",
    },
    axisBand: {
      grid: false,
      ticks: false,
      domain: false,
    },
    legend: {
      labelFont: face,
      titleFont: face,
      labelColor: color.muted,
      titleColor: color.muted,
      labelFontSize: chart.axisSize,
      titleFontSize: chart.axisSize,
    },
    bar: {
      fill: color.mark,
      cornerRadiusEnd: chart.barCornerRadius,
      cornerRadiusTopRight: chart.barCornerRadius,
      cornerRadiusBottomRight: chart.barCornerRadius,
    },
    line: {
      strokeWidth: chart.lineStrokeWidth,
    },
    point: {
      filled: true,
    },
    text: {
      font: face,
      fontSize: chart.labelSize,
      fill: color.ink,
      fontWeight: 500,
    },
    scale: {
      bandPaddingInner: chart.barPaddingInner,
      bandPaddingOuter: 0.12,
    },
  };
}

const SERIES_BY_LEGACY: Record<string, string> = {
  "#1f4e79": color.mark,
  "#7a542e": color.mark2,
  "#9c5233": color.mark2,
  "#4a6670": color.mark3,
  "#5c5c5c": color.mark4,
  "#333333": color.break,
  "#332e27": color.break,
  "#d9d9d9": color.holeBand,
  "#e3dfd8": color.holeBand,
  "#e7e0d2": color.holeBand,
};

function inheritPaint(value: string): string {
  const mapped = SERIES_BY_LEGACY[value.toLowerCase()];
  return mapped ?? value;
}

export function inheritChartPaint(node: unknown): void {
  if (Array.isArray(node)) {
    for (const item of node) {
      inheritChartPaint(item);
    }
    return;
  }
  if (node === null || typeof node !== "object") {
    return;
  }
  const record = node as Record<string, unknown>;
  const mark = record.mark;
  if (mark !== null && typeof mark === "object" && !Array.isArray(mark)) {
    const paint = mark as Record<string, unknown>;
    if (typeof paint.color === "string") {
      paint.color = inheritPaint(paint.color);
    }
  }
  const encoding = record.encoding;
  if (
    encoding !== null &&
    typeof encoding === "object" &&
    !Array.isArray(encoding)
  ) {
    const colorEnc = (encoding as Record<string, unknown>).color;
    if (
      colorEnc !== null &&
      typeof colorEnc === "object" &&
      !Array.isArray(colorEnc)
    ) {
      const scale = (colorEnc as Record<string, unknown>).scale;
      if (
        scale !== null &&
        typeof scale === "object" &&
        !Array.isArray(scale)
      ) {
        const range = (scale as Record<string, unknown>).range;
        if (
          Array.isArray(range) &&
          range.every((item) => typeof item === "string")
        ) {
          (scale as Record<string, unknown>).range = chart.series.slice(
            0,
            range.length,
          );
        }
      }
    }
  }
  for (const value of Object.values(record)) {
    inheritChartPaint(value);
  }
}

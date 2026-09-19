import * as vega from "vega";
import * as vegaLite from "vega-lite";
import { chart, color, inheritChartPaint, vegaConfig } from "./theme";

type Json = Record<string, unknown>;

type ChartCaption = {
  title: string;
  subtitle?: string;
};

function asRecord(value: unknown): Json | undefined {
  if (value !== null && typeof value === "object" && !Array.isArray(value)) {
    return value as Json;
  }
  return undefined;
}

function markType(mark: unknown): string | undefined {
  if (typeof mark === "string") {
    return mark;
  }
  const record = asRecord(mark);
  return typeof record?.type === "string" ? record.type : undefined;
}

function channelType(encoding: Json, channel: string): string | undefined {
  const rec = asRecord(encoding[channel]);
  return typeof rec?.type === "string" ? rec.type : undefined;
}

function escapeHtml(text: string): string {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function pullCaption(spec: Json): ChartCaption {
  const title = spec.title;
  spec.title = undefined;
  if (typeof title === "string" && title.trim() !== "") {
    return { title: title.trim() };
  }
  const record = asRecord(title);
  if (record === undefined) {
    throw new Error("chart spec is missing a title");
  }
  const text = record.text;
  if (typeof text !== "string" || text.trim() === "") {
    throw new Error("chart spec is missing a title");
  }
  const subtitle = record.subtitle;
  if (typeof subtitle === "string" && subtitle.trim() !== "") {
    return { title: text.trim(), subtitle: subtitle.trim() };
  }
  return { title: text.trim() };
}

function stripUnsupportedInvalid(node: unknown): void {
  if (Array.isArray(node)) {
    for (const item of node) {
      stripUnsupportedInvalid(item);
    }
    return;
  }
  const record = asRecord(node);
  if (record === undefined) {
    return;
  }
  const mark = record.mark;
  if (mark !== null && typeof mark === "object" && !Array.isArray(mark)) {
    const { invalid: _ignored, ...rest } = mark as Json;
    record.mark = rest;
  }
  for (const value of Object.values(record)) {
    stripUnsupportedInvalid(value);
  }
}

function stripLinePoints(node: unknown): void {
  if (Array.isArray(node)) {
    for (const item of node) {
      stripLinePoints(item);
    }
    return;
  }
  const record = asRecord(node);
  if (record === undefined) {
    return;
  }
  const mark = asRecord(record.mark);
  if (mark !== undefined && mark.type === "line" && mark.point === true) {
    mark.point = undefined;
  }
  for (const value of Object.values(record)) {
    stripLinePoints(value);
  }
}

function isBarMark(spec: Json): boolean {
  return markType(spec.mark) === "bar";
}

function hasBarLayer(spec: Json): boolean {
  if (isBarMark(spec)) {
    return true;
  }
  if (!Array.isArray(spec.layer)) {
    return false;
  }
  return spec.layer.some((layer) => {
    const record = asRecord(layer);
    return record !== undefined && isBarMark(record);
  });
}

function isStepHeight(height: unknown): boolean {
  const record = asRecord(height);
  return record !== undefined && typeof record.step === "number";
}

function isCategoricalBar(spec: Json): boolean {
  if (isStepHeight(spec.height) || hasBarLayer(spec)) {
    return true;
  }
  if (!isBarMark(spec)) {
    return false;
  }
  const encoding = asRecord(spec.encoding);
  if (encoding === undefined) {
    return false;
  }
  const yType = channelType(encoding, "y");
  const xType = channelType(encoding, "x");
  return (
    (yType === "nominal" || yType === "ordinal") && xType === "quantitative"
  );
}

function orientBarsHorizontal(spec: Json): void {
  if (!isBarMark(spec)) {
    return;
  }
  const encoding = asRecord(spec.encoding);
  if (encoding === undefined) {
    return;
  }
  const xType = channelType(encoding, "x");
  const yType = channelType(encoding, "y");
  if (xType !== "nominal" && xType !== "ordinal") {
    return;
  }
  if (yType !== "quantitative") {
    return;
  }
  const xEnc = encoding.x;
  encoding.x = encoding.y;
  encoding.y = xEnc;
}

function scaleIncludesZero(encoding: Json, channel: string): boolean {
  const rec = asRecord(encoding[channel]);
  if (rec === undefined || rec.type !== "quantitative") {
    return false;
  }
  const scale = asRecord(rec.scale);
  return scale?.zero === true;
}

function encodings(node: unknown): Json[] {
  if (Array.isArray(node)) {
    return node.flatMap((item) => encodings(item));
  }
  const record = asRecord(node);
  if (record === undefined) {
    return [];
  }
  const found: Json[] = [];
  const encoding = asRecord(record.encoding);
  if (encoding !== undefined) {
    found.push(encoding);
  }
  for (const value of Object.values(record)) {
    found.push(...encodings(value));
  }
  return found;
}

function zeroChannel(spec: Json): "x" | "y" | undefined {
  for (const encoding of encodings(spec)) {
    if (scaleIncludesZero(encoding, "x")) {
      return "x";
    }
    if (scaleIncludesZero(encoding, "y")) {
      return "y";
    }
  }
  return undefined;
}

function zeroRule(channel: "x" | "y"): Json {
  return {
    data: { values: [{}] },
    mark: { type: "rule", color: color.ink, strokeWidth: 1 },
    encoding: {
      [channel]: { datum: 0, type: "quantitative" },
    },
  };
}

function addBarValueLabels(spec: Json): void {
  if (!isBarMark(spec)) {
    return;
  }
  const encoding = asRecord(spec.encoding);
  if (encoding === undefined) {
    return;
  }
  const xEnc = asRecord(encoding.x);
  const field = typeof xEnc?.field === "string" ? xEnc.field : "plotValue";
  const barLayer: Json = {
    mark: spec.mark,
    encoding,
  };
  const labelLayer: Json = {
    mark: {
      type: "text",
      align: "left",
      baseline: "middle",
      dx: 4,
      color: color.ink,
      fontSize: chart.labelSize,
    },
    encoding: {
      y: encoding.y,
      x: encoding.x,
      text: {
        field,
        type: "quantitative",
        format: ".2~f",
      },
    },
  };
  spec.layer = [barLayer, labelLayer];
  spec.mark = undefined;
  spec.encoding = undefined;
}

function addZeroRule(spec: Json): void {
  const channel = zeroChannel(spec);
  if (channel === undefined || !Array.isArray(spec.layer)) {
    return;
  }
  spec.layer = [zeroRule(channel), ...spec.layer];
}

function applyHouseSize(spec: Json): void {
  spec.width = chart.plotWidth;
  if (isCategoricalBar(spec)) {
    spec.height = { step: chart.barStep };
    return;
  }
  spec.height = chart.plotHeight;
}

function mergeHouse(house: Json, specPart: unknown): Json {
  const fromSpec = asRecord(specPart) ?? {};
  return { ...fromSpec, ...house };
}

function applyHouseConfig(spec: Json): void {
  const config = asRecord(spec.config) ?? {};
  const house = vegaConfig();
  spec.config = {
    ...config,
    font: house.font,
    padding: house.padding,
    view: mergeHouse(asRecord(house.view) ?? {}, config.view),
    axis: mergeHouse(asRecord(house.axis) ?? {}, config.axis),
    axisQuantitative: mergeHouse(
      asRecord(house.axisQuantitative) ?? {},
      config.axisQuantitative,
    ),
    axisBand: mergeHouse(asRecord(house.axisBand) ?? {}, config.axisBand),
    legend: mergeHouse(asRecord(house.legend) ?? {}, config.legend),
    title: mergeHouse(asRecord(house.title) ?? {}, config.title),
    bar: mergeHouse(asRecord(house.bar) ?? {}, config.bar),
    line: mergeHouse(asRecord(house.line) ?? {}, config.line),
    point: mergeHouse(asRecord(house.point) ?? {}, config.point),
    text: mergeHouse(asRecord(house.text) ?? {}, config.text),
    scale: mergeHouse(asRecord(house.scale) ?? {}, config.scale),
  };
}

function applyBarPadding(spec: Json): void {
  if (!hasBarLayer(spec) && !isStepHeight(spec.height)) {
    return;
  }
  spec.padding = {
    left: 4,
    right: chart.valueLabelPad,
    top: 4,
    bottom: 8,
  };
}

function dropUndefined(value: Json): Json {
  return JSON.parse(JSON.stringify(value)) as Json;
}

function applyPortraitFrame(spec: Json): void {
  inheritChartPaint(spec);
  stripLinePoints(spec);
  orientBarsHorizontal(spec);
  applyHouseSize(spec);
  addBarValueLabels(spec);
  addZeroRule(spec);
  applyHouseConfig(spec);
  applyBarPadding(spec);
}

async function compileSvg(spec: Json): Promise<string> {
  const framed = dropUndefined(spec);
  const compiled = vegaLite.compile(framed as vegaLite.TopLevelSpec).spec;
  const runtime = vega.parse(compiled);
  const view = new vega.View(runtime, { renderer: "none" });
  return await view.toSVG();
}

function svgWidth(svg: string): number {
  const match = /<svg[^>]*\bwidth="([0-9.]+)"/.exec(svg);
  if (match === null) {
    throw new Error("chart SVG is missing width");
  }
  return Number(match[1]);
}

function fitPlotWidth(spec: Json, svg: string): void {
  if (typeof spec.width !== "number") {
    return;
  }
  spec.width = Math.max(240, spec.width + (chart.fitWidth - svgWidth(svg)));
}

function figureHtml(
  chartId: string,
  caption: ChartCaption,
  svg: string,
): string {
  const titleId = `chart-${chartId}-title`;
  const subtitleId = `chart-${chartId}-subtitle`;
  const labelledBy =
    caption.subtitle === undefined ? titleId : `${titleId} ${subtitleId}`;
  const subtitle =
    caption.subtitle === undefined
      ? ""
      : `<p class="chart-subtitle" id="${subtitleId}">${escapeHtml(caption.subtitle)}</p>`;
  return `<figure class="chart" id="chart-${chartId}" aria-labelledby="${labelledBy}"><figcaption><p class="chart-title" id="${titleId}">${escapeHtml(caption.title)}</p>${subtitle}</figcaption><div class="chart-plot">${svg}</div></figure>`;
}

export async function specToFigure(
  chartId: string,
  spec: unknown,
): Promise<string> {
  const clone = structuredClone(spec) as Json;
  const caption = pullCaption(clone);
  stripUnsupportedInvalid(clone);
  applyPortraitFrame(clone);
  const firstSvg = await compileSvg(clone);
  fitPlotWidth(clone, firstSvg);
  const svg = await compileSvg(clone);
  return figureHtml(chartId, caption, svg);
}

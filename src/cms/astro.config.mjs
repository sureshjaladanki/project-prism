import { defineConfig } from "astro/config";

const outDir = process.env.PRISM_RENDER_OUT;
if (!outDir) {
  throw new Error("PRISM_RENDER_OUT is required");
}

export default defineConfig({
  output: "static",
  outDir,
  trailingSlash: "never",
  build: {
    format: "directory",
    assets: "_astro",
  },
});

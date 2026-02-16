import markdownIt from "markdown-it";
import implicitFigures from "markdown-it-implicit-figures";

export default function (eleventyConfig) {
  // Markdown: enable figure/figcaption from ![alt](src) patterns
  const md = markdownIt({ html: true, linkify: true });
  md.use(implicitFigures, { figcaption: true });
  eleventyConfig.setLibrary("md", md);

  // Date filter for templates
  eleventyConfig.addFilter("date", function (date, format) {
    if (!date) return "";
    // Handle YAML date (may be a Date object or string like "2026-02-13")
    const d = date instanceof Date ? date : new Date(date + "T00:00:00Z");
    if (isNaN(d.getTime())) return String(date);
    if (format === "YYYY-MM-DD") return d.toISOString().split("T")[0];
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      timeZone: "UTC",
    });
  });

  // Passthrough copy: CSS and session screenshots
  eleventyConfig.addPassthroughCopy({ "templates/bip-web.css": "css/bip-web.css" });
  eleventyConfig.addPassthroughCopy("*-*-26/screenshots");
  eleventyConfig.addPassthroughCopy("*-*-26/agile-coffee-board.png");

  // Collection: all session summaries, newest first
  eleventyConfig.addCollection("sessions", function (collectionApi) {
    return collectionApi
      .getFilteredByGlob("*-*-26/*-session-summary.md")
      .sort((a, b) => new Date(b.data.date) - new Date(a.data.date));
  });

  return {
    dir: {
      input: ".",
      includes: "_includes",
      output: "_site",
    },
    templateFormats: ["md", "njk"],
    markdownTemplateEngine: "njk",
    pathPrefix: process.env.ELEVENTY_PATH_PREFIX || "/",
  };
}

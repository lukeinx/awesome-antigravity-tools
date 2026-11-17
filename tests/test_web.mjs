import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  filterAndSortTools,
  formatCompactNumber,
  getScoreTier,
  getStatusLabel,
  parseParamsToState,
  serializeStateToParams,
} from "../docs/catalog-logic.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const bundlePath = path.resolve(__dirname, "..", "docs", "catalog-bundle.json");
const bundle = JSON.parse(fs.readFileSync(bundlePath, "utf8"));

test("bundle contains expected categories and enriched tools", () => {
  assert.ok(bundle.categories.length >= 4);
  assert.ok(bundle.tools.length >= 19);
  for (const tool of bundle.tools) {
    assert.ok(tool.id && tool.name && tool.url && tool.telemetry);
  }
});

test("filterAndSortTools handles multi-token bilingual search and sorting", () => {
  const quotaTools = filterAndSortTools(bundle.tools, { query: "quota", sort: "stars" });
  assert.ok(quotaTools.length >= 3);
  for (let i = 1; i < quotaTools.length; i++) {
    assert.ok((quotaTools[i - 1].telemetry?.stars ?? 0) >= (quotaTools[i].telemetry?.stars ?? 0));
  }

  const zhSearch = filterAndSortTools(bundle.tools, { query: "硬链接" });
  assert.equal(zhSearch.length, 1);
  assert.equal(zhSearch[0].id, "antigravity-junction-skill-fix");

  const byScore = filterAndSortTools(bundle.tools, { sort: "score" });
  for (let i = 1; i < byScore.length; i++) {
    assert.ok(
      (byScore[i - 1].telemetry?.health_score ?? -1) >= (byScore[i].telemetry?.health_score ?? -1)
    );
  }

  const byName = filterAndSortTools(bundle.tools, { sort: "name" });
  for (let i = 1; i < byName.length; i++) {
    assert.ok(byName[i - 1].name.toLowerCase().localeCompare(byName[i].name.toLowerCase()) <= 0);
  }
});

test("category, platform, and status filters compose accurately", () => {
  const winPatches = filterAndSortTools(bundle.tools, {
    category: "platform-fixes-runtime-patches",
    platform: "Windows",
    status: "HEALTHY",
  });
  assert.ok(winPatches.length >= 3);
  for (const t of winPatches) {
    assert.equal(t.category, "platform-fixes-runtime-patches");
    assert.ok(t.platforms.includes("Windows"));
    assert.equal(t.telemetry.status, "HEALTHY");
  }
});

test("URL state serialization round-trips cleanly", () => {
  const original = {
    query: "acp rust",
    category: "dedicated-gateways-migration",
    platform: "Linux",
    status: "HEALTHY",
    sort: "score",
    lang: "zh",
    openToolId: "liftgate",
  };
  const qs = serializeStateToParams(original).toString();
  const parsed = parseParamsToState(`?${qs}`);
  assert.deepEqual(parsed, original);
});

test("formatting and tier helpers behave deterministically", () => {
  assert.equal(formatCompactNumber(999), "999");
  assert.equal(formatCompactNumber(1500), "1.5k");
  assert.equal(formatCompactNumber(1_250_000), "1.3M");
  assert.equal(getStatusLabel("HEALTHY", "en"), "Healthy");
  assert.equal(getStatusLabel("HEALTHY", "zh"), "活跃健康");
  assert.equal(getScoreTier(95), "excellent");
  assert.equal(getScoreTier(72), "good");
  assert.equal(getScoreTier(45), "warn");
  assert.equal(getScoreTier(10), "danger");
});

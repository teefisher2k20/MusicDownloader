import React from "react";
import { AbsoluteFill, Sequence, spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { z } from "zod";
import { zColor } from "@remotion/zod-types";

const featureSchema = z.object({
  title: z.string().min(1).max(80),
  description: z.string().min(1).max(300),
  screenshot_url: z.string().url().optional(),
  impact_tag: z.enum(["performance", "ux", "security", "api", "infra", "other"]).default("other"),
  priority_rank: z.number().int().min(1).max(10).default(5),
});

const metricsSchema = z
  .object({
    commits: z.number().int().min(0).optional(),
    contributors: z.number().int().min(0).optional(),
    issues_closed: z.number().int().min(0).optional(),
    adoption_percent: z.number().min(0).max(100).optional(),
  })
  .optional();

export const releaseTrailerSchema = z.object({
  version_name: z.string().min(1).max(64),
  release_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  headline: z.string().min(1).max(200),
  features: z.array(featureSchema).min(1).max(12),
  metrics: metricsSchema,
  cta_text: z.string().min(1).max(80).default("Explore the release"),
  cta_url: z.string().url().optional(),
  brand_color: zColor().default("#7C3AED"),
  channel: z.enum(["youtube", "linkedin", "twitter", "internal"]).default("youtube"),
});

type ReleaseTrailerProps = z.infer<typeof releaseTrailerSchema>;

const slideStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  padding: "84px 120px",
  textAlign: "center",
};

export const ReleaseTrailerV1: React.FC<ReleaseTrailerProps> = ({
  version_name,
  release_date,
  headline,
  features,
  metrics,
  cta_text,
  cta_url,
  brand_color,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const introFrames = Math.round(3 * fps);
  const featureFrames = Math.round(4 * fps);
  const metricsFrames = Math.round(3 * fps);
  const outroFrames = Math.round(5 * fps);

  const introOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const orderedFeatures = [...features].sort((a, b) => b.priority_rank - a.priority_rank).slice(0, 3);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f172a", color: "#f8fafc", fontFamily: "Arial, sans-serif" }}>
      <Sequence from={0} durationInFrames={introFrames}>
        <AbsoluteFill style={{ ...slideStyle, opacity: introOpacity }}>
          <div
            style={{
              fontSize: 16,
              letterSpacing: 1.2,
              textTransform: "uppercase",
              color: "#cbd5e1",
            }}
          >
            {release_date}
          </div>
          <div style={{ fontSize: 62, fontWeight: 700, marginTop: 18 }}>{version_name}</div>
          <div style={{ fontSize: 30, color: "#e2e8f0", marginTop: 20, maxWidth: 1280 }}>{headline}</div>
        </AbsoluteFill>
      </Sequence>

      {orderedFeatures.map((feature, idx) => {
        const from = introFrames + idx * featureFrames;
        return (
          <Sequence key={feature.title} from={from} durationInFrames={featureFrames}>
            <FeatureSlide
              title={feature.title}
              description={feature.description}
              impactTag={feature.impact_tag}
              color={brand_color}
              frame={frame - from}
              fps={fps}
            />
          </Sequence>
        );
      })}

      <Sequence from={introFrames + orderedFeatures.length * featureFrames} durationInFrames={metricsFrames}>
        <MetricsSlide metrics={metrics} color={brand_color} />
      </Sequence>

      <Sequence
        from={introFrames + orderedFeatures.length * featureFrames + metricsFrames}
        durationInFrames={outroFrames}
      >
        <OutroSlide ctaText={cta_text} ctaUrl={cta_url} color={brand_color} />
      </Sequence>
    </AbsoluteFill>
  );
};

const FeatureSlide: React.FC<{
  title: string;
  description: string;
  impactTag: string;
  color: string;
  frame: number;
  fps: number;
}> = ({ title, description, impactTag, color, frame, fps }) => {
  const reveal = spring({
    frame,
    fps,
    config: { damping: 100, mass: 0.7 },
  });

  return (
    <AbsoluteFill style={slideStyle}>
      <div
        style={{
          backgroundColor: `${color}30`,
          border: `1px solid ${color}`,
          borderRadius: 999,
          padding: "6px 16px",
          fontSize: 18,
          textTransform: "uppercase",
          letterSpacing: 1,
        }}
      >
        {impactTag}
      </div>
      <div
        style={{
          marginTop: 24,
          fontSize: 52,
          fontWeight: 700,
          transform: `scale(${0.92 + reveal * 0.08})`,
          color,
        }}
      >
        {title}
      </div>
      <div style={{ marginTop: 16, fontSize: 30, maxWidth: 1200, color: "#cbd5e1" }}>{description}</div>
    </AbsoluteFill>
  );
};

const MetricsSlide: React.FC<{ metrics: ReleaseTrailerProps["metrics"]; color: string }> = ({ metrics, color }) => {
  const rows = [
    ["Commits", metrics?.commits],
    ["Contributors", metrics?.contributors],
    ["Issues Closed", metrics?.issues_closed],
    ["Adoption", metrics?.adoption_percent != null ? `${metrics.adoption_percent}%` : undefined],
  ].filter(([, value]) => value != null);

  return (
    <AbsoluteFill style={slideStyle}>
      <div style={{ fontSize: 40, fontWeight: 700, color }}>Release Metrics</div>
      {rows.length === 0 ? (
        <div style={{ marginTop: 24, fontSize: 28, color: "#cbd5e1" }}>No metrics provided for this release.</div>
      ) : (
        <div style={{ marginTop: 28, display: "grid", gap: 14, width: "70%" }}>
          {rows.map(([label, value]) => (
            <div
              key={label}
              style={{
                display: "flex",
                justifyContent: "space-between",
                border: "1px solid #334155",
                borderRadius: 12,
                padding: "14px 20px",
                fontSize: 28,
              }}
            >
              <span style={{ color: "#94a3b8" }}>{label}</span>
              <span style={{ color: "#f8fafc", fontWeight: 700 }}>{String(value)}</span>
            </div>
          ))}
        </div>
      )}
    </AbsoluteFill>
  );
};

const OutroSlide: React.FC<{ ctaText: string; ctaUrl?: string; color: string }> = ({ ctaText, ctaUrl, color }) => {
  return (
    <AbsoluteFill style={slideStyle}>
      <div style={{ fontSize: 58, fontWeight: 700 }}>Ready to upgrade?</div>
      <div
        style={{
          marginTop: 28,
          fontSize: 34,
          fontWeight: 700,
          color: "#0f172a",
          backgroundColor: color,
          borderRadius: 14,
          padding: "14px 24px",
        }}
      >
        {ctaText}
      </div>
      {ctaUrl ? <div style={{ marginTop: 18, fontSize: 24, color: "#cbd5e1" }}>{ctaUrl}</div> : null}
    </AbsoluteFill>
  );
};

import React from "react";
import { Composition } from "remotion";
import {
  ReleaseTrailerV1,
  releaseTrailerSchema,
} from "./compositions/ReleaseTrailerV1";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ReleaseTrailerV1"
        component={ReleaseTrailerV1}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        schema={releaseTrailerSchema}
        defaultProps={{
          version_name: "v1.0.0",
          release_date: "2026-05-04",
          headline: "The next release is here",
          features: [
            {
              title: "Faster builds",
              description: "Pipelines now complete up to 40% faster.",
              impact_tag: "performance",
              priority_rank: 10,
            },
          ],
          metrics: {
            commits: 120,
            contributors: 8,
            issues_closed: 34,
            adoption_percent: 67,
          },
          cta_text: "Explore the release",
          cta_url: "https://example.com/releases/v1-0-0",
          brand_color: "#7C3AED",
          channel: "youtube",
        }}
      />
    </>
  );
};

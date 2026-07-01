import React, { useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";
import EmptyState from "../components/ui/EmptyState";
import useJobDescription from "../hooks/useJobDescription";
import { uploadJobDescription } from "../services/jobDescriptionService";

export default function JobDescriptionPage() {
  const [text, setText] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const { error } = useJobDescription();

  const [parsed, setParsed] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await uploadJobDescription({ text });
      setParsed(response.parsed_signals);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-zinc-900">
          Job Description
        </h1>

        <p className="mt-1 text-sm text-zinc-600">
          Upload or paste a Job Description to automatically extract hiring
          requirements.
        </p>
      </div>

      <form
        onSubmit={onSubmit}
        className="grid gap-4 md:grid-cols-[1fr_420px]"
      >
        {/* LEFT PANEL */}

        <Card className="p-5">
          <div className="text-sm font-semibold text-zinc-900">
            JD Input
          </div>

          <div className="mt-2 text-sm text-zinc-600">
            Paste the complete Job Description below.
          </div>

          <div className="mt-4">
            <textarea
              className="min-h-[260px] w-full resize-none rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-300 focus:outline-none"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste Job Description here..."
            />
          </div>

          <div className="mt-4 flex items-center gap-3">
            <Button type="submit" disabled={submitting || !text.trim()}>
              {submitting ? (
                <Spinner label="Parsing JD..." />
              ) : (
                "Parse JD"
              )}
            </Button>

            {text.trim() && (
              <div className="text-xs text-zinc-500">
                Characters: {text.trim().length}
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 text-sm text-red-600">
              {String(error?.message ?? error)}
            </div>
          )}
        </Card>

        {/* RIGHT PANEL */}

        <Card className="p-5">
          <div className="text-sm font-semibold text-zinc-900">
            Parsed Signals
          </div>

          {submitting ? (
            <div className="mt-4">
              <Spinner label="Parsing Job Description..." />
            </div>
          ) : parsed ? (
            <div className="mt-5 space-y-5">
              {/* Job Role */}

              <div>
                <div className="text-xs text-zinc-500">Job Role</div>

                <div className="mt-1 font-semibold text-zinc-900">
                  {parsed.job_role || "Not Specified"}
                </div>
              </div>

              {/* Skills */}

              <div>
                <div className="text-xs text-zinc-500 mb-2">
                  Required Skills
                </div>

                <div className="flex flex-wrap gap-2">
                  {parsed.required_skills?.length ? (
                    parsed.required_skills.map((skill) => (
                      <span
                        key={skill}
                        className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-sm text-zinc-500">
                      No skills detected
                    </span>
                  )}
                </div>
              </div>

              {/* Experience */}

              <div>
                <div className="text-xs text-zinc-500">Experience</div>

                <div className="mt-1 font-semibold text-zinc-900">
                  {parsed.experience || "Not Specified"}
                </div>
              </div>

              {/* Education */}

              <div>
                <div className="text-xs text-zinc-500">Education</div>

                <div className="mt-1 font-semibold text-zinc-900">
                  {parsed.education || "Not Specified"}
                </div>
              </div>

              {/* Keywords */}

              <div>
                <div className="text-xs text-zinc-500 mb-2">
                  Keywords
                </div>

                <div className="flex flex-wrap gap-2">
                  {parsed.keywords?.length ? (
                    parsed.keywords.map((keyword) => (
                      <span
                        key={keyword}
                        className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700"
                      >
                        {keyword}
                      </span>
                    ))
                  ) : (
                    <span className="text-sm text-zinc-500">
                      No keywords detected
                    </span>
                  )}
                </div>
              </div>

              {/* Info Box */}

              <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-3 text-xs text-zinc-600">
                Parsed hiring requirements will be used by the Hybrid AI
                Ranking Engine to evaluate candidate suitability.
              </div>
            </div>
          ) : (
            <EmptyState
              title="No Parsed JD Yet"
              description="Paste a Job Description and click 'Parse JD' to extract recruiter-critical signals."
            />
          )}
        </Card>
      </form>
    </div>
  );
}
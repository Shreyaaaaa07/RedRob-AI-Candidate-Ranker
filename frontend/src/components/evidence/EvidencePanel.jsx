import React from "react";

export default function EvidencePanel({
  title = "Evidence",
  evidence = {},
}) {

  if (!evidence || Object.keys(evidence).length === 0) {
    return (
      <div className="space-y-3">
        <div className="text-sm font-semibold text-zinc-900">
          {title}
        </div>

        <div className="rounded-xl border border-dashed border-zinc-300 bg-zinc-50 p-5 text-sm text-zinc-600">
          No evidence available.
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">

      <div className="text-lg font-semibold">
        {title}
      </div>

      {Object.entries(evidence).map(([section, items]) => (

        <div
          key={section}
          className="rounded-xl border p-4 bg-white"
        >

          <h3 className="font-semibold text-zinc-900 capitalize mb-3">
            {section.replaceAll("_", " ")}
          </h3>

          <ul className="list-disc pl-5 space-y-2">

            {(items || []).map((item, index) => (

              <li
                key={index}
                className="text-sm text-zinc-700"
              >
                {item}
              </li>

            ))}

          </ul>

        </div>

      ))}

    </div>
  );
}
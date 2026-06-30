# Frontend Build TODO — Redrob AI Candidate Ranker

## Plan steps
- [ ] Generate Vite+React+Tailwind+Router+Axios scaffold in `frontend/`
- [ ] Add `src/services/api.js` reading base URL from environment variables
- [ ] Implement global layout: Sidebar + Topbar + responsive main content
- [ ] Implement routes/pages:
  - [ ] Dashboard
  - [ ] Job Description upload + parsed JD display
  - [ ] Candidate Ranking (search/filter/pagination + row->details)
  - [ ] Candidate Details (profile, scores, risks)
  - [ ] Explainability panel (evidence per score)
- [ ] Create reusable components (MetricCard, DataTable, Badge, Skeleton, EmptyState, ErrorState)
- [ ] Implement loading/error/empty states for all API calls
- [ ] Add candidate details drawer/page state handling for selected candidate
- [ ] Wire up Analytics sidebar item (placeholder route if backend endpoint unknown)
- [ ] Run frontend dev server + basic sanity checks



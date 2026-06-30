import React from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './layouts/Layout'
import DashboardPage from './pages/DashboardPage'
import JobDescriptionPage from './pages/JobDescriptionPage'
import CandidateRankingPage from './pages/CandidateRankingPage'
import CandidateDetailsPage from './pages/CandidateDetailsPage'
import ExplainabilityPage from './pages/ExplainabilityPage'
import AnalyticsPage from "./pages/AnalyticsPage";


export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/job-description" element={<JobDescriptionPage />} />
        <Route path="/candidate-rankings" element={<CandidateRankingPage />} />
        <Route path="/candidate/:candidateId" element={<CandidateDetailsPage />} />
        <Route path="/explainability/:candidateId" element={<ExplainabilityPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />



        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  )
}


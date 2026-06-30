import React, { useEffect, useState } from "react";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import { getDashboardSummary } from "../services/dashboardService";

export default function DashboardPage() {

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function loadDashboard() {

            try {

                const data = await getDashboardSummary();

                setDashboard(data);

            } catch (err) {

                console.error(err);

            } finally {

                setLoading(false);

            }

        }

        loadDashboard();

    }, []);

    if (loading) {
        return <div className="text-lg">Loading Dashboard...</div>;
    }

    return (

        <div className="space-y-6">

            <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">

                <div>

                    <h1 className="text-2xl font-bold">
                        Recruiter Dashboard
                    </h1>

                    <p className="text-gray-500">
                        AI Powered Candidate Ranking System
                    </p>

                </div>

                <div className="flex gap-2">

                    <Badge variant="primary">
                        AI Powered
                    </Badge>

                    <Badge variant="neutral">
                        Explainable
                    </Badge>

                </div>

            </div>

            <div className="grid md:grid-cols-3 gap-5">

                <Card className="p-5">

                    <h3>Total Candidates</h3>

                    <p className="text-4xl font-bold mt-3">
                        {dashboard.total_candidates}
                    </p>

                </Card>

                <Card className="p-5">

                    <h3>Risk Flagged</h3>

                    <p className="text-4xl font-bold mt-3">
                        {dashboard.risk_flagged_candidates}
                    </p>

                </Card>

                <Card className="p-5">

                    <h3>Top Score</h3>

                    <p className="text-4xl font-bold mt-3">
                        {dashboard.top_candidate_score ?? "-"}
                    </p>

                </Card>

            </div>

        </div>

    );

}
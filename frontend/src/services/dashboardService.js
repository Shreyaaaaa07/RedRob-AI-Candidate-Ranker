import { apiGet } from "./api";

export async function getDashboardSummary() {
    return apiGet("/dashboard/");
}
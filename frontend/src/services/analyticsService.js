import { apiGet } from "./api";

export async function getAnalytics() {
  return apiGet("/analytics");
}
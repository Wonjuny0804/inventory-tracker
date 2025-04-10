import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import OrganizationSetup from "@/components/organization/OrganizationSetup";
import Dashboard from "@/components/dashboard/Dashboard";

export default async function PrivatePage() {
  const supabase = await createClient();

  // Check if user is authenticated
  const { data, error } = await supabase.auth.getUser();
  if (error || !data?.user) {
    redirect("/login");
  }

  // Get the access token for API requests
  const { data: sessionData } = await supabase.auth.getSession();
  const token = sessionData?.session?.access_token;

  if (!token) {
    // Handle missing token (should not happen if user is authenticated)
    throw new Error("Authentication token not found");
  }

  try {
    // Check if user has an organization via the API
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/v1/orgs/me`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        cache: "no-store", // Don't cache this request
      }
    );

    if (response.ok) {
      // User has an organization, show dashboard
      const org = await response.json();
      return <Dashboard user={data.user} organization={org} />;
    } else if (response.status === 404) {
      // User doesn't have an organization, show setup
      return <OrganizationSetup user={data.user} />;
    } else {
      // Handle other errors
      throw new Error(`API error: ${response.statusText}`);
    }
  } catch (error) {
    console.error("Error checking organization:", error);
    // Show organization setup as fallback
    return <OrganizationSetup user={data.user} />;
  }
}

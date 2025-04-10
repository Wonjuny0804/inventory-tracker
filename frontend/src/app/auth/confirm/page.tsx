import { type EmailOtpType } from "@supabase/supabase-js";
import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";

// This is now a server component
export default async function ConfirmPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const token_hash = searchParams.token_hash as string;
  const type = searchParams.type as EmailOtpType;
  // Get the next parameter or default to dashboard if not provided
  const next = (searchParams.next as string) ?? "/dashboard";

  if (token_hash && type) {
    const supabase = await createClient();

    const { error } = await supabase.auth.verifyOtp({
      type,
      token_hash,
    });

    if (!error) {
      // You can use data from verifyOtp to determine where to redirect
      // For example, you can redirect to different pages based on user role
      // const { data } = await supabase.auth.getUser();
      // const redirectUrl = data.user?.user_metadata.isAdmin ? '/admin-dashboard' : next;

      // For now, we'll just use the next parameter or fall back to /dashboard
      redirect(next);
    }
  }

  // If verification fails or parameters are missing, redirect to error page
  redirect("/error");
}

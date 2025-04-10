import { redirect } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import RegisterForm from "@/components/auth/RegisterForm";

export default async function SignUpPage({
  searchParams,
}: {
  searchParams: { error?: string; message?: string };
}) {
  const { error, message } = await searchParams;
  const supabase = await createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (session) {
    redirect("/dashboard");
  }

  return (
    <div className="flex min-h-screen flex-col bg-background md:flex-row">
      {/* Form Section - Takes full width on mobile, half width on desktop */}
      <div className="flex w-full items-center justify-center px-4 py-10 md:w-1/2 md:px-10">
        <div className="w-full max-w-md">
          <div className="mb-8">
            <h1 className="text-2xl font-bold tracking-tight">
              Create an account
            </h1>
            <p className="mt-2 text-muted-foreground">
              Fill in your details to get started
            </p>

            {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
            {message && (
              <p className="mt-2 text-sm text-green-500">{message}</p>
            )}
          </div>

          <RegisterForm />

          <div className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account?{" "}
            <a
              href="/login"
              className="font-medium text-primary hover:text-primary/90"
            >
              Sign in
            </a>
          </div>
        </div>
      </div>

      {/* Brand/Hero Section - Hidden on mobile, shown on desktop */}
      <div className="hidden bg-primary/10 md:flex md:w-1/2 md:flex-col md:items-center md:justify-center md:bg-gradient-to-b md:from-primary/5 md:to-primary/30">
        <div className="relative mx-auto w-full max-w-md text-center">
          <div className="mb-4 inline-flex items-center justify-center rounded-full bg-primary/10 p-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-10 w-10 text-primary"
            >
              <path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z" />
              <path d="M3 9V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4" />
              <path d="M3 9h18" />
            </svg>
          </div>
          <h2 className="mt-6 text-3xl font-bold tracking-tight">
            Inventory Tracker Pro
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Streamline your inventory management with our powerful and intuitive
            platform.
          </p>

          <div className="mt-10">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-5 w-5 text-primary"
                  >
                    <path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z" />
                    <path d="m9 12 2 2 4-4" />
                  </svg>
                </div>
                <p className="text-left font-medium">
                  Real-time stock tracking
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-5 w-5 text-primary"
                  >
                    <path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z" />
                    <path d="m9 12 2 2 4-4" />
                  </svg>
                </div>
                <p className="text-left font-medium">
                  Automated reorder alerts
                </p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-5 w-5 text-primary"
                  >
                    <path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z" />
                    <path d="m9 12 2 2 4-4" />
                  </svg>
                </div>
                <p className="text-left font-medium">Comprehensive analytics</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

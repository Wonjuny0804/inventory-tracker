"use server";

import { createClient } from "@/utils/supabase/server";
import { z } from "zod";

// Define validation schema for registration
const registerSchema = z
  .object({
    name: z.string().min(1, "Full name is required"),
    email: z.string().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

export async function registerUser(formData: FormData) {
  // Extract form data
  const validationData = {
    name: formData.get("name") as string,
    email: formData.get("email") as string,
    password: formData.get("password") as string,
    confirmPassword: formData.get("confirmPassword") as string,
  };

  // Validate data
  const validatedFields = registerSchema.safeParse(validationData);

  if (!validatedFields.success) {
    const errors = validatedFields.error.flatten().fieldErrors;
    // Format error message for URL
    const errorMessage = Object.values(errors).flat().join(", ");

    // Return error for client to handle
    return {
      success: false,
      redirect: `/auth/register?error=${encodeURIComponent(errorMessage)}`,
    };
  }

  const { name, email, password } = validatedFields.data;

  try {
    const supabase = await createClient();

    // Register with Supabase
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          name,
        },
        emailRedirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/confirm?next=/dashboard`,
      },
    });

    if (error) {
      // Return error for client to handle
      return {
        success: false,
        redirect: `/auth/register?error=${encodeURIComponent(error.message)}`,
      };
    }

    // Return success for client to handle
    const successMessage =
      "Registration successful. Please check your email to confirm your account.";

    return {
      success: true,
      redirect: `/login?message=${encodeURIComponent(successMessage)}`,
    };
  } catch (error) {
    console.error("Registration error:", error);

    // Return error for client to handle
    return {
      success: false,
      redirect: `/auth/register?error=${encodeURIComponent(
        "An unexpected error occurred. Please try again."
      )}`,
    };
  }
}

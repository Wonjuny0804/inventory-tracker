import { User } from "@supabase/supabase-js";
import { Organization } from "@/types/database";

interface DashboardProps {
  user: User;
  organization: Organization;
}

const Dashboard = ({ user, organization }: DashboardProps) => {
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back, {user.user_metadata?.name || user.email}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Dashboard content will go here */}
        <div className="p-4 border rounded-lg bg-card">
          <h2 className="font-medium mb-2">Organization</h2>
          <p>{organization.name}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

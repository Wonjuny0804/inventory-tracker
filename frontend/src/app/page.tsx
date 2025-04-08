import { getBackendStatus } from "@/utils/api";

export default async function Home() {
  const data = await getBackendStatus().catch(console.error);
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Inventory Tracker</h1>
      <pre className="mt-4">
        {data ? JSON.stringify(data, null, 2) : "Loading..."}
      </pre>
    </main>
  );
}

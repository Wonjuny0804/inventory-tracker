export const getBackendStatus = async () => {
  const res = await fetch("http://localhost:8000", { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch backend");
  return res.json();
};

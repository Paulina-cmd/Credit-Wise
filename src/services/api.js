const API_BASE_URL = "http://localhost:8000";

export const getMisiones = async () => {
  const response = await fetch(`${API_BASE_URL}/misiones`);
  if (!response.ok) throw new Error("Error al obtener misiones");
  return response.json();
};

export const getMisionById = async (id) => {
  const response = await fetch(`${API_BASE_URL}/mision/${id}`);
  if (!response.ok) throw new Error("Error al obtener la misión");
  return response.json();
};

export const crearMision = async (mision) => {
  const response = await fetch(`${API_BASE_URL}/mision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(mision),
  });
  if (!response.ok) throw new Error("Error al crear misión");
  return response.json();
};

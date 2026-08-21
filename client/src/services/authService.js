import api, { setAccessToken } from "./api";

export const register = async ({ email, password, fullName }) => {
  const { data } = await api.post("/auth/register", {
    email,
    password,
    full_name: fullName || null,
  });
  setAccessToken(data.access_token);
  return data.user;
};

export const login = async ({ email, password }) => {
  const { data } = await api.post("/auth/login", { email, password });
  setAccessToken(data.access_token);
  return data.user;
};

export const logout = async () => {
  try {
    await api.post("/auth/logout");
  } finally {
    setAccessToken(null);
  }
};

export const fetchCurrentUser = async () => {
  const { data } = await api.get("/auth/me");
  return data;
};

// Called on app load: exchanges the httpOnly refresh cookie for a fresh
// access token so the user stays logged in across page reloads.
export const silentRefresh = async () => {
  const { data } = await api.post("/auth/refresh");
  setAccessToken(data.access_token);
  return data.user;
};

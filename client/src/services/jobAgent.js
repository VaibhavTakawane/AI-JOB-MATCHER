import api from "./api";

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/resumes/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};

export const getResumeAnalysis = async (resumeId) => {
  const response = await api.post(`/analysis/${resumeId}`);
  return response.data;
};

export const searchJobs = async (resumeId) => {
  const response = await api.post(`/jobsRouter/search/${resumeId}`);
  return response.data;
};

export const getRecommendedJobs = async (resumeId) => {
  const response = await api.post(`/recommendation/${resumeId}`);
  return response.data;
};

export type ApiEnvelope<T> = {
  success: boolean;
  message: string;
  data: T;
};

export type ListEnvelope<T> = {
  success: boolean;
  message: string;
  items: T[];
  total: number;
};

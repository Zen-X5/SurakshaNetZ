import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

// Define the request payload interface
export interface RegisterRequest {
  displayName: string
  email: string
  phoneNumber: string
  password: string
}

// Define the API response interface
export interface RegisterResponse {
  message: string
  user?: {
    id: string
    email: string
    displayName: string
    role: string
  }
}

export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000',
  }),
  endpoints: (builder) => ({
    register: builder.mutation<RegisterResponse, RegisterRequest>({
      query: (credentials) => ({
        url: '/auth/register',
        method: 'POST',
        body: credentials,
      }),
    }),
  }),
})

// Auto-generated hook for the register mutation
export const { useRegisterMutation } = authApi

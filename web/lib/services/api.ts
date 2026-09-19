import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export interface RegisterRequest {
  displayName: string
  email: string
  phoneNumber: string
  password: string
}

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
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000',
  }),
  endpoints: (builder) => ({
    register: builder.mutation<RegisterResponse, RegisterRequest>({
      query: (payload) => ({
        url: '/auth/register',
        method: 'POST',
        body: payload,
      }),
    }),
  }),
})

export const { useRegisterMutation } = authApi

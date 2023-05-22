import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  // reducerPath: "real_talk_API",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  // tagTypes: ['Post'],
  endpoints: (builder) => ({
    register: builder.mutation({
      query: ({ username, email, password }) => ({
        url: `user/register/`,
        method: "POST",
        body: { username, email, password },
      }),

      // // Pick out data and prevent nested properties in a hook or selector
      // transformResponse: (response, meta, arg) => response.data,
      // // Pick out errors and prevent nested properties in a hook or selector
      // transformErrorResponse: (response, meta, arg) => response.status,
      // invalidatesTags: ["Post"],
      // // onQueryStarted is useful for optimistic updates
      // // The 2nd parameter is the destructured `MutationLifecycleApi`
      // async onQueryStarted(
      //   arg,
      //   { dispatch, getState, queryFulfilled, requestId, extra, getCacheEntry }
      // ) {},
      // // The 2nd parameter is the destructured `MutationCacheLifecycleApi`
      // async onCacheEntryAdded(
      //   arg,
      //   {
      //     dispatch,
      //     getState,
      //     extra,
      //     requestId,
      //     cacheEntryRemoved,
      //     cacheDataLoaded,
      //     getCacheEntry,
      //   }
      // ) {},
    }),
    login: builder.mutation({
      query: ({ email, password }) => ({
        url: "user/login/",
        method: "POST",
        body: { email, password },
      }),
    }),
    user: builder.query({
      query: (id) => ({
        url: `user/${id}`,
      }),
    }),
  }),
});

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useRegisterMutation, useLoginMutation, useUserQuery } = api;

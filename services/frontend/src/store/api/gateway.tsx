/*
    This API slices are belongs to Gateway
 */


import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

// types
import {DataResponse, ListResponse} from "@/types/response.d";
import {Person} from "@/types/models/person.d";
import {Session} from "@/types/models/session.d";
import {PaginationArgs} from "@/types/args.d";


const baseQuery = fetchBaseQuery(
    {
        baseUrl: `${process.env.NEXT_PUBLIC_GW_URL}`,
        credentials: 'include'
    }
)

export const gatewayApi = createApi({
    reducerPath:  'gatewayAPI',
    baseQuery,
    refetchOnReconnect: true,
    endpoints:builder => ({

        // create new person
        createPerson: builder.mutation({
            query: ({data}) => ({
                url: `/api/v1/persons`,
                method: 'POST',
                body: data
            })
        }),

        // get person
        getPerson: builder.mutation({
            query: ({prime})=>({
                url: `/api/v1/persons/person/${prime}`,
                method: 'GET'
            })
        }),

        // upload person face
        uploadPersonFace: builder.mutation({
            query: ({data,prime})=>({
                url: `/api/v1/persons/person/${prime}/upload`,
                method: 'POST',
                body: data
            })
        }),

        // create new session
        createNewSession: builder.mutation({
            query: ({data})=>({
                url: `/api/v1/queries`,
                method: 'POST',
                body: data
            })
        }),

        // get Session by prime
        getSession: builder.query<DataResponse<Session>,{prime:string}>({
            keepUnusedDataFor: 1,
            query:({prime})=>{
                return {url: `/api/v1/queries/query/${prime}`}
            }
        }),

        // Get session list
        getSessions: builder.query<ListResponse<Session>, PaginationArgs>({
            keepUnusedDataFor: 1,
            query: ({page, pageSize}) => {
                // Make Search queries
                const query = new URLSearchParams();

                if(typeof page === 'string'){
                    query.append('page', page);
                }

                if(typeof pageSize === 'string'){
                    query.append('page_size', pageSize);
                }

                // Get query in string
                const queryString = query.toString();

                return {url: `/api/v1/queries?${queryString}`}
            }
        }),

        // Get Person List
        getPersons: builder.query<ListResponse<Person>, PaginationArgs>({
            keepUnusedDataFor: 1,
            query: ({page, pageSize})=>{

                // Make Search queries
                const query = new URLSearchParams();

                if(typeof page === 'string'){
                    query.append('page', page);
                }

                if(typeof pageSize === 'string'){
                    query.append('page_size', pageSize);
                }

                // Get query in string
                const queryString = query.toString();

                return {url: `/api/v1/persons?${queryString}`}
            }
        }),
    })
})

export const {
    // Mutation
    useCreatePersonMutation,
    useGetPersonMutation,
    useUploadPersonFaceMutation,
    useCreateNewSessionMutation,

    // Query
    useGetPersonsQuery,
    useGetSessionsQuery,
    useGetSessionQuery

} = gatewayApi;
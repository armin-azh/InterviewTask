/*
    This API slices are belongs to Gateway
 */


import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

// types
import {ListResponse} from "@/types/response.d";
import {Person} from "@/types/models/person.d";
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

    // Query
    useGetPersonsQuery

} = gatewayApi;
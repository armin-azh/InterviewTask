import {useState} from "react";
import Head from "next/head";
import {useRouter} from "next/router";

// Components
import Item from "@/components/Sessions/Item";

// Hooks
import {useGetResultsQuery} from "@/store/api/gateway";

// Types
import {PaginationArgs} from "@/types/args.d";
import {nanoid} from "nanoid";
import moment from "moment";
import Link from "next/link";

export default function Session() {
    const [page,setPage] = useState<PaginationArgs>({page:1, pageSize:10});
    const router = useRouter();
    const params = router.query;
    const prime = params.prime as string;

    const {data, isLoading} = useGetResultsQuery({prime,...page})
    
    return <div className='h-screen bg-gray-100'>
        <Head><title>Face Recognition Portal | Session</title></Head>

        <div className='flex flex-col justify-center w-full py-10 gap-6'>

            <div className='flex justify-center'>
                <div className='flex flex-col justify-center pt-3 tracking-widest'>
                    <h1 className='font-medium text-xl capitalize text-blue-600'>Session</h1>
                    <p className='text-sm text-gray-600'>
                        {prime}
                    </p>
                </div>
            </div>

            <div className='flex justify-center'>
                <div className='flex flex-col justify-center pt-3 tracking-widest'>
                    <div className="relative overflow-x-auto rounded-lg">
                        <table className="w-full text-sm text-left rtl:text-right text-gray-500">
                            <thead className="text-xs text-white uppercase bg-blue-500">
                            <tr>
                                <th scope="col" className="px-6 py-3">
                                    Image
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    Similarity
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    Status
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    Person
                                </th>
                                <th scope="col" className="px-6 py-3">

                                </th>
                            </tr>
                            </thead>
                            <tbody>

                            {
                                data?.data.results!==null?data?.data.results.map((item) => {
                                    return <Item data={item} key={nanoid()}/>
                                }):null
                            }
                            </tbody>
                        </table>
                    </div>

                </div>
            </div>
        </div>

    </div>

}
import {useState} from "react";
import Head from "next/head";
import {nanoid} from "nanoid";
import moment from "moment/moment";
import Link from "next/link";

// Components
import Loading from "@/components/Loading";

// Hooks
import {useGetSessionsQuery} from "@/store/api/gateway";
import {PaginationArgs} from "@/types/args.d";


export default function Sessions() {
    const [page,setPage] = useState<PaginationArgs>({page: 1, pageSize: 10});
    const {data, isLoading} = useGetSessionsQuery(page);

    return <div className='h-screen bg-gray-100'>
        <Head><title>Face Recognition Portal | Sessions</title></Head>
        <Loading isLoading={isLoading}/>

        <div className='flex flex-col justify-center w-full py-10 gap-6'>

            <div className='flex justify-center'>
                <div className='flex flex-col justify-center pt-3 tracking-widest'>
                    <h1 className='font-medium text-xl capitalize text-blue-600'>Sessions</h1>
                    <p className='text-sm text-gray-600'>
                        Here is all the sessions you`ve been created
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
                                    #
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    ID
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    status
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    Created
                                </th>
                                <th scope="col" className="px-6 py-3">
                                    Ended
                                </th>
                                <th scope="col" className="px-6 py-3">

                                </th>
                            </tr>
                            </thead>
                            <tbody>

                            {
                                data?.results.map((item, index) => {
                                    return <tr className="text-gray-700 border-b-2" key={nanoid()}>
                                        <th scope="row"
                                            className="px-6 py-4 font-medium">
                                            {index + 1}
                                        </th>
                                        <th scope="row"
                                            className="px-6 py-4 font-medium">
                                            {item.prime}
                                        </th>
                                        <td className="px-6 py-4 capitalize">
                                            {item.ended_at.Valid ? <span
                                                    className="bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded">Complete</span> :
                                                <span
                                                    className="bg-red-100 text-red-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded">Processing</span>}

                                        </td>
                                        <td className="px-6 py-4 capitalize">
                                            {moment(item.created_at.Time).format('YYYY-MM-DD HH:mm:ss A')}
                                        </td>
                                        <td className="px-6 py-4">
                                            {item.ended_at.Valid ? moment(item.ended_at.Time).format('YYYY-MM-DD HH:mm:ss A') : "N/A"}
                                        </td>
                                        <td className="duration-200font-medium px-6 py-4 text-blue-600 hover:text-blue-800 hover:underline">
                                            <Link href={`/sessions/${item.prime}`}>Open</Link>
                                        </td>
                                    </tr>
                                })
                            }
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>

}
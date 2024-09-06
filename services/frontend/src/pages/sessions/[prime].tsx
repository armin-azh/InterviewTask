import {useState} from "react";
import Head from "next/head";
import {useRouter} from "next/router";

// Hooks
import {useGetSessionQuery, useGetResultsQuery} from "@/store/api/gateway";

// Types
import {PaginationArgs} from "@/types/args.d";
import {nanoid} from "nanoid";

export default function Session() {
    const [page,setPage] = useState<PaginationArgs>({page:1, pageSize:10});
    const router = useRouter();
    const params = router.query;
    const prime = params.prime as string;

    const {data, isLoading} = useGetResultsQuery({prime,...page});
    console.log(data)
    
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
                    <div className="h-48 overflow-y-auto">
                        <ul className="w-full divide-y divide-gray-200">
                            {
                                data?.data.results.map((item) => {
                                    // const objectUrl = URL.createObjectURL(image);
                                    const url = new URL(item.thumbnail_path.replace("thumbnails", "media"), process.env.NEXT_PUBLIC_GW_URL || "http://localhost:8080").toString();
                                    return <li className="pb-3 sm:pb-4" key={nanoid()}>
                                        <div className="flex items-center space-x-4 rtl:space-x-reverse">
                                            <div className="flex-shrink-0">
                                                <img className="w-8 h-8 rounded-full" src={url} alt="Neil image"/>
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <p className="text-sm font-medium text-gray-900 truncate">
                                                    {item.similarity}
                                                </p>
                                            </div>

                                        </div>
                                    </li>
                                })
                            }
                        </ul>
                    </div>
                </div>
            </div>
        </div>

    </div>

}
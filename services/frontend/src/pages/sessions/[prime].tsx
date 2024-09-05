import {useState} from "react";
import Head from "next/head";
import {useRouter} from "next/router";

// Hooks
import {useGetSessionQuery} from "@/store/api/gateway";
import {string} from "prop-types";


export default function Session() {
    const router = useRouter();
    const params = router.query;
    const prime = params.prime as string;

    const {data, isLoading} = useGetSessionQuery({prime});
    
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
                    {/*<Table/>*/}
                </div>
            </div>
        </div>

    </div>

}
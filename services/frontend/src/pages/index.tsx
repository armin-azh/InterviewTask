import {useState} from "react";
import Head from "next/head";

// Components

// context
import {HomeContext} from "@/components/Home/Context";
import TabSelector from "@/components/Home/TabSelector";

export default function Home() {
  const [tabId, setTabId] = useState<number>(0);
  return <HomeContext.Provider value={{tabId}}>
    <div className='h-screen bg-gray-100'>
      <Head><title>Face Recognition Portal</title></Head>
        <TabSelector/>
        <div className='fixed bottom-4 left-1/2 transform -translate-x-1/2'>
            <div className='flex gap-4'>
                <button className="duration-200 bg-blue-500 hover:ring-2 hover:ring-blue-400 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-40" onClick={()=>setTabId(0)}>
                    Upload Video
                </button>
                <button className="duration-200 bg-blue-500 hover:ring-2 hover:ring-blue-400 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-40" onClick={()=>setTabId(1)}>
                    Enrollment
                </button>
            </div>
        </div>
    </div>
  </HomeContext.Provider>
}

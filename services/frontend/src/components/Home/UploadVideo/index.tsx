
// Component
import FaceScan from "@/components/Home/UploadVideo/FaceScan";
import Uploader from "@/components/Home/UploadVideo/Uploader";

export default function  UploadVideo(){

    return <div className='flex flex-col justify-center w-full py-10 gap-6'>

        <div className='flex w-full justify-center'>
            <div className='flex flex-col justify-center w-32'>
                <FaceScan/>
            </div>
        </div>

        <div className='flex justify-center'>
            <div className='flex flex-col justify-center pt-3 tracking-widest'>
                <h1 className='font-medium text-xl capitalize text-blue-600'>Upload video</h1>
                <p className='text-sm text-gray-600'>
                    Upload a query video to search across enrolled faces
                </p>
            </div>
        </div>

        <div className='flex justify-center'>
            <div className='flex flex-col justify-center w-1/3'>
                <Uploader/>
            </div>
        </div>
    </div>
}
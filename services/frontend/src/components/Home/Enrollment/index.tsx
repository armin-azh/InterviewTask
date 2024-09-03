

//  components
import Uploading from "@/components/Home/Enrollment/Uploading";

export default function  Enrollment() {

    return <div className='flex flex-col justify-center w-full py-10 gap-6'>

        <div className='flex w-full justify-center'>
            <div className='flex flex-col justify-center w-40'>
                <Uploading/>
            </div>
        </div>

        <div className='flex justify-center'>
            <div className='flex flex-col justify-center pt-3 tracking-widest'>
                <h1 className='font-medium text-xl capitalize text-blue-600'>Upload Images</h1>
                <p className='text-sm text-gray-600'>
                    Upload Images persons who you want to enroll their faces
                </p>
            </div>
        </div>

    </div>
}
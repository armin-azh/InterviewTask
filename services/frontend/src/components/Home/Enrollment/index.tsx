import {useState} from 'react';


// contexts
import {StepContext} from "@/components/Home/Enrollment/StepContext";

//  components
import Uploading from "@/components/Home/Enrollment/Uploading";
import StepSelector from "@/components/Home/Enrollment/StepSelector";

export default function  Enrollment() {
    const [stepId, setStepId] = useState<number>(0);
    const [personId, setPersonId] = useState<number>(0);

    return <StepContext.Provider value={{stepId, nextStep: (step)=>setStepId(step), personId, setPersonId: (id)=>{setPersonId(id)}}}>
        <div className='flex flex-col justify-center w-full py-10 gap-6'>

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

            <div className='flex justify-center gap-3'>
                <div className='flex flex-col justify-center'>
                    <StepSelector/>
                </div>
            </div>

        </div>
    </StepContext.Provider>
}
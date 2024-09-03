import {useContext} from "react";

// Context
import {StepContext} from "@/components/Home/Enrollment/StepContext";

export default function User(){
    const {nextStep} = useContext(StepContext);


    return <div className='flex gap-4'>
        <button
            className="duration-200 bg-green-500 hover:ring-2 hover:ring-green-400 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-40" onClick={()=>nextStep(1)}>
            New Person
        </button>
        <button
            className="duration-200 bg-green-500 hover:ring-2 hover:ring-green-400 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-40" onClick={()=>nextStep(2)}>
            Existing Person
        </button>
    </div>
}
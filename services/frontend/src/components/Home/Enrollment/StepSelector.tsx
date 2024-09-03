import {useContext} from "react";

// Context
import {StepContext} from "@/components/Home/Enrollment/StepContext";

// Components
import User from '@/components/Home/Enrollment/User'
import ExistingPerson from "@/components/Home/Enrollment/ExistingPerson";
import NewPerson from "@/components/Home/Enrollment/NewPerson";
import Uploader from "@/components/Home/Enrollment/Uploader";


export default function StepSelector() {

    const {stepId} = useContext(StepContext);

    switch (stepId){
        case 0:
            return <User/>

        case 1:
            return <NewPerson/>

        case 2:
            return <ExistingPerson/>

        case 3:
            return <Uploader/>

        default:
            return null;
    }
}
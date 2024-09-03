import {createContext} from "react";

// type
import {StepProp} from "@/types/pages/home.d";


export const StepContext = createContext<StepProp>({stepId:0, nextStep: (step)=>{}, personId:"", setPersonId:(id)=>{}})
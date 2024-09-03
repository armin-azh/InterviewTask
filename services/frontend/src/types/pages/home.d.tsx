

export interface TabProp{
    tabId: number;
}

export interface StepProp{
    stepId: number;
    nextStep: (step:number)=> void;
    personId: string;
    setPersonId: (id:string)=> void;
}
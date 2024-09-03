

export interface TabProp{
    tabId: number;
}

export interface StepProp{
    stepId: number;
    nextStep: (step:number)=> void;
    personId: number;
    setPersonId: (id:number)=> void;
}
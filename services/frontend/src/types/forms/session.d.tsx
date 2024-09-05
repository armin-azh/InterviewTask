

export interface SessionForm{
    video: File | undefined;
}



export const initSessionForm = ()=>({video: undefined});
import {useState} from "react";
import {toast} from "react-toastify";
import {useRouter} from"next/router";

// components
import {topCenterToastOption} from "@/components/ToastOptions";

// Hooks
import {useCreateNewSessionMutation} from "@/store/api/gateway";

// Types
import {SessionForm, initSessionForm} from "@/types/forms/session.d";
import {HookArgs} from "@/types/args.d";
import {DataResponse} from "@/types/response.d";
import {Session} from "@/types/models/session.d";

export default function useCreateSession(){
    const router = useRouter();
    const [form, setForm] = useState<SessionForm>( initSessionForm());

    const [submit, {isLoading}] = useCreateNewSessionMutation();

    function create(args: HookArgs){

        if (form.video!==undefined){
            const data = new FormData();
            data.append("video", form.video);
            submit({data})
                .unwrap()
                .then((response:DataResponse<Session>)=>{
                    router.push(`/sessions/${response.data.prime}`);
                    if(args.onUpdate){
                        args.onUpdate();
                    }
                })
                .catch(reason=>{
                    toast.error("Cannot create new session", topCenterToastOption);
                    console.log(reason)
                    if(args.onError){
                        args.onError();
                    }

                })
                .finally(()=>{
                    setForm({video: undefined});
                    if(args.onFinally){
                        args.onFinally();
                    }
                })

        }else{
            toast.warning("Select a video file", topCenterToastOption);
        }
    }


    return {form, setForm, create, isLoading}
}
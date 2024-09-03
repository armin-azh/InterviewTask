import {useState} from "react";
import {toast} from "react-toastify";

// Components
import {topCenterToastOption} from "@/components/ToastOptions";

// Types
import type {HookArgs} from "@/types/args.d";
import {PersonForm, initPersonForm} from "@/types/forms/person.d";
import {Person} from "@/types/models/person.d";
import {DataResponse} from "@/types/response.d";

// Hooks
import {useCreatePersonMutation} from "@/store/api/gateway";


interface Args extends HookArgs{
    setPersonId: (id:number) => void;
}

export default function useCreatePerson() {
    const [form, setForm] = useState<PersonForm>(initPersonForm());

    const [submit, {isLoading}] = useCreatePersonMutation();


    function create(args: Args){
        if(form.first_name!=="" && form.last_name!==""){
            console.log(form)
            submit({data:form})
                .unwrap()
                .then((response: DataResponse<Person>)=>{
                    toast.success('New person has been created', topCenterToastOption);
                    args.setPersonId(response.data.id);
                    if(args.onUpdate){
                        args.onUpdate();
                    }
                })
                .catch(reason=>{
                    toast.error('Cannot create new person', topCenterToastOption);
                    console.log(reason)
                    if(args.onError){
                        args.onError();
                    }
                })
                .finally(()=>{
                    setForm(initPersonForm());
                    if(args.onFinally){
                        args.onFinally();
                    }
                })
        }else{
            toast.warning('Firstname and lastname cannot be empty', topCenterToastOption);
        }
    }

    return {create, isLoading, form, setForm};
}
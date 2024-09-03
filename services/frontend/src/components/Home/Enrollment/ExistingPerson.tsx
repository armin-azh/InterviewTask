import {useContext, useState} from "react";
import classNames from "classnames";
import {toast} from "react-toastify";

// Components
import Spinning from "@/components/Spinning";
import {topCenterToastOption} from "@/components/ToastOptions";

// Context
import {StepContext} from "@/components/Home/Enrollment/StepContext";

// Hooks
import {useGetPersonMutation} from "@/store/api/gateway";

// Types
import {DataResponse} from "@/types/response.d";
import {Person} from "@/types/models/person.d";

export default function NewPerson() {
    const [prime, setPrime]= useState<string>("");

    const [submit, {isLoading}] = useGetPersonMutation();

    const {nextStep, setPersonId} = useContext(StepContext);

    return <div className='flex flex-col gap-4'>
        <div className='flex flex-col'>
            <label className='font-semibold text-gray-400 text-sm leading-[27px] mb-[8px]'
                   htmlFor='id-input-first-name'>
                Person ID
            </label>
            <input
                name={'first_name'}
                className={`text-gray-400 rounded-[4px] focus:outline-none font-medium text-5 leading-[30px] px-[24px] w-[474px] py-[13px] h-[56px] border-gray-400 border-[1.75px] focus:ring-2 focus:ring-gray-400 focus:border-0`}
                id={'id-input-first-name'}
                type={'text'}
                required={true}
                autoComplete={'on'}
                value={prime}
                onChange={(e) => {
                    const {value} = e.target;
                    setPrime(value)
                }}
            />
        </div>

        <div className='flex justify-center'>
            <button
                className={classNames("duration-200 bg-green-500 hover:ring-2 hover:ring-green-400 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-40",{'bg-green-600': isLoading})}
                onClick={() => {
                    if(prime !== ""){
                        submit({prime})
                            .unwrap()
                            .then((response:DataResponse<Person>)=>{
                                nextStep(3);
                                setPersonId(response.data.id);
                            })
                            .catch(reason=>{
                                toast.error(`Cannot file the person with id ${prime}`, topCenterToastOption);
                            })
                            .finally(()=>{
                                setPrime("");
                            })

                        }
                    }
                }
                disabled={isLoading}
            >
                <Spinning condition={isLoading} onLoadingText={""} onCompleteText={'Send'}/>
            </button>
        </div>
    </div>
}
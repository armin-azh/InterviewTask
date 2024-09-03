import {useContext, useState} from "react";
import {nanoid} from "nanoid";
import {toast} from "react-toastify";

// Hooks
import {useUploadPersonFaceMutation} from "@/store/api/gateway";

// Context
import {StepContext} from "@/components/Home/Enrollment/StepContext";

// Component
import Spinning from "@/components/Spinning";
import {topCenterToastOption} from "@/components/ToastOptions";


import Dropzone, {DropzoneOptions} from "react-dropzone";

const dropOptions: DropzoneOptions = {
    accept: {
        'image/jpeg': ['.jpg', '.jpeg'],
        'image/png': ['.png'],
        'image/gif': ['.gif'],
        'image/webp': ['.webp']
    },
    multiple: true
}

export default function Uploader() {
    const [images, setImages] = useState<File[]>([])
    const [isUploading, setIsUploading] = useState<boolean>(false);

    const {personId} = useContext(StepContext);

    const [submit, {isLoading}] = useUploadPersonFaceMutation();

    return <div className='flex flex-col gap-4'>

        <div className="h-48 overflow-y-auto">
            <ul className="w-full divide-y divide-gray-200">
                {
                    images.map((image) => {
                        const objectUrl = URL.createObjectURL(image);
                        return <li className="pb-3 sm:pb-4" key={nanoid()}>
                            <div className="flex items-center space-x-4 rtl:space-x-reverse">
                                <div className="flex-shrink-0">
                                    <img className="w-8 h-8 rounded-full" src={objectUrl} alt="Neil image"/>
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-medium text-gray-900 truncate">
                                        {image.name}
                                    </p>
                                </div>

                            </div>
                        </li>
                    })
                }
            </ul>
        </div>

        <div className='flex justify-center w-full hover:cursor-pointer'>
            <Dropzone onDrop={acceptedFiles => {
                setImages(prevState => [...prevState, ...acceptedFiles])
            }} {...dropOptions}>
                {({getRootProps, getInputProps}) => (
                    <div className='border-2 rounded-md p-10'>
                        <div {...getRootProps()}>
                            <input {...getInputProps()} />
                            <p className='text-blue-600 text-center tracking-widest'>Drag and Drop Images</p>
                        </div>
                    </div>
                )}
            </Dropzone>
        </div>

        <div className='flex justify-center'>
            <button
                className="duration-200 bg-green-500 hover:ring-2 hover:ring-green-400 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-32"
                onClick={() => {
                    setIsUploading(true);

                    images.forEach((image) => {
                        const data = new FormData();
                        data.append("image", image);

                        submit({data,prime: personId})
                            .unwrap()
                            .then(response=>{

                            })
                            .catch(reason=>{
                                toast.error(`cannot upload ${image.name}`, topCenterToastOption);
                            })
                    })

                    setIsUploading(false);
                    setImages([]);
                }}

                disabled={isLoading || isUploading}
            >
                <Spinning condition={isLoading || isUploading} onLoadingText={""} onCompleteText={"Upload"}/>
            </button>
        </div>
    </div>
}
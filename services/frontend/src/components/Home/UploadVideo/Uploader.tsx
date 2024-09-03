import {useState} from "react";

import Dropzone ,{DropzoneOptions} from 'react-dropzone'

const dropOptions: DropzoneOptions = {
    accept: {
        'video/*': ['.mp4', '.avi', '.mov', '.mkv']
    },
    multiple: false
}

export default function Uploader(){
    const [video,setVideo] = useState<string | undefined>(undefined);

    if (video === undefined){

        return <div className='w-full hover:cursor-pointer'>
            <Dropzone onDrop={acceptedFiles => {
                const file = acceptedFiles[0];
                if(file){
                    const objectUrl = URL.createObjectURL(file);
                    setVideo(objectUrl);
                }
            }} {...dropOptions}>
                {({getRootProps, getInputProps}) => (
                    <div className='border-2 rounded-md p-10'>
                        <div {...getRootProps()}>
                            <input {...getInputProps()} />
                            <p className='text-blue-600 text-center tracking-widest'>Drag and Drop a video file</p>
                        </div>
                    </div>
                )}
            </Dropzone>
        </div>
    }

    return <div className='flex flex-col gap-3'>
        <div className='border-2 border-blue-600 rounded-md overflow-hidden'>
            <video controls={false} autoPlay={true} loop={true}>
                <source src={video} type="video/mp4"/>
            </video>
        </div>
        <div className='flex gap-2 justify-center'>
            <button
                className="duration-200 bg-transparent text-red-600 border border-red-600 hover:ring-2 hover:ring-red-400 hover:bg-red-600 hover:text-white font-medium py-2 px-4 rounded-md shadow-lg w-32"
                onClick={()=>setVideo(undefined)}
            >
                reset
            </button>
            <button
                className="duration-200 bg-green-500 hover:ring-2 hover:ring-green-400 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-md shadow-lg w-32">
                Upload
            </button>
        </div>
    </div>
}
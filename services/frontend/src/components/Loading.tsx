
interface Props{
    isLoading:boolean;
}

export default function Loading(props: Props){

    if(props.isLoading){
        return <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-50 backdrop-blur-sm transition-opacity duration-300">
            <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white"></div>
                <p className="mt-2 text-white">Loading...</p>
            </div>
        </div>

    }
    return null;
}
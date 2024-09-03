
// Components
import Table from "@/components/Home/Persons/Table";

export default function Persons() {

    return <div className='flex flex-col justify-center w-full py-10 gap-6'>

        <div className='flex justify-center'>
            <div className='flex flex-col justify-center pt-3 tracking-widest'>
                <h1 className='font-medium text-xl capitalize text-blue-600'>Persons</h1>
                <p className='text-sm text-gray-600'>
                    All registered persons are placed in this table
                </p>
            </div>
        </div>

        <div className='flex justify-center'>
            <div className='flex flex-col justify-center pt-3 tracking-widest'>
                <Table/>
            </div>
        </div>
    </div>
}